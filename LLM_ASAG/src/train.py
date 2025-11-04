import sys
import logging
import os
from argparse import ArgumentParser
import wandb
import datasets
from datasets import load_dataset
from peft import LoraConfig
import torch
import transformers
from trl import SFTTrainer, SFTConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig, Mxfp4Config
import gc
import uuid
from peft import AutoPeftModelForCausalLM
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

from dataset.dataset_gen import DSUtils
from evaluation.eval import evaluate

BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../.."))

def train(max_sequ_length: int = 1024,
          epochs: int = 2,
          batchsize: int = 4,
          checkpoint_path: str = "",
          prompt: str = "fewshot",
          dataset_path: str ="",
          size: float = 1.0):
    logger = logging.getLogger(__name__)
    experiment_id = str(uuid.uuid4())
    wandb.init(project="LLM-classification", name="{}_{}".format(checkpoint_path.split("/")[-1], experiment_id))
    
    # Training configuration
    training_config = {
        "packing": False,
        "bf16": True,
        # "do_eval": False,
        "learning_rate": 1e-05,
        "log_level": "info",
        "logging_steps": 20,
        "logging_strategy": "steps",
        "lr_scheduler_type": "cosine",
        "num_train_epochs": epochs,
        "max_steps": -1,
        "output_dir": "{}/results/{}/{}".format(BP, checkpoint_path.split("/")[-1], experiment_id),
        "overwrite_output_dir": True,
        "per_device_eval_batch_size": batchsize,
        "per_device_train_batch_size": batchsize,
        "remove_unused_columns": True,
        "save_steps": 500 ,
        "save_total_limit": 4,
        "seed": 0,
        "gradient_checkpointing": True,
        "gradient_accumulation_steps": 4,
        "warmup_ratio": 0.1, 
        "eval_strategy": "steps",
        "eval_steps": 1000,
        # "load_best_model_at_end": True,
        # "metric_for_best_model": "accuracy",  # or F1、loss
        "greater_is_better": True,
        # "max_seq_length": max_sequ_length,  # Important: place max_seq_length here

        "report_to": "wandb",
        "run_name": checkpoint_path,
    }

    training_config["dataset_text_field"] = "prompt"

    train_conf = SFTConfig(**training_config)

    # PEFT configuration
    peft_config = {
        "r": 16,
        "lora_alpha": 32,
        "lora_dropout": 0.05,
        "bias": "none",
        "task_type": "CAUSAL_LM",
        "target_modules": "all-linear",
        "modules_to_save": None,
    }
    peft_conf = LoraConfig(**peft_config)

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    log_level = train_conf.get_process_log_level()
    logger.setLevel(log_level)
    datasets.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()

    logger.warning(
        f"Process rank: {train_conf.local_rank}, device: {train_conf.device}, n_gpu: {train_conf.n_gpu}"
        + f" distributed training: {bool(train_conf.local_rank != -1)}, 16-bits training: {train_conf.fp16}"
    )
    logger.info(f"Training/evaluation parameters {train_conf}")
    logger.info(f"PEFT parameters {peft_conf}")

    # Load model and tokenizer
    model_kwargs = dict(
        use_cache=False,
        trust_remote_code=True,
        attn_implementation="flash_attention_2",  # loading the model with flash-attenstion support
        torch_dtype=torch.bfloat16, #torch_dtype=torch.bfloat16, # for large r1
        device_map=None,
        # quantization_config=Mxfp4Config(dequantize=True),  
        # load_in_8bit=True,  # for large r1
    )
    model = AutoModelForCausalLM.from_pretrained(checkpoint_path, **model_kwargs)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path, trust_remote_code=True)
    tokenizer.use_default_system_prompt = False
    tokenizer.model_max_length = max_sequ_length
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)
    tokenizer.padding_side = 'right'

    # Load dataset
    raw_dataset = DSUtils.load_ds_from_excel(
        experiment_id=experiment_id,
        prompt_type=prompt,
        excel_path=dataset_path,
        clean=False,
        size=size
    )
    train_dataset = raw_dataset["train_sft"]
    test_dataset = raw_dataset["test_sft"]

    print("Sample training data:", train_dataset[0])

    # Setup trainer
    trainer = SFTTrainer(
        model=model,
        # tokenizer=tokenizer,
        args=train_conf,
        peft_config=peft_conf,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )

    # Train
    train_result = trainer.train()
    metrics = train_result.metrics
    trainer.log_metrics("train", metrics)
    trainer.save_metrics("train", metrics)
    trainer.save_state()

    trainer.save_model(f"{train_conf.output_dir}/final")

    peft_model = AutoPeftModelForCausalLM.from_pretrained(f"{train_conf.output_dir}/final")
    merged_model = peft_model.merge_and_unload()
    merged_model.save_pretrained(f"{train_conf.output_dir}/merged")
    tokenizer.save_pretrained(f"{train_conf.output_dir}/merged")

    wandb.finish()

    return experiment_id, test_dataset

if __name__ == "__main__":
    parser = ArgumentParser(description="Script to train the model")

    parser.add_argument(
        "--max_sequ_length",
        type=int,
        default=2048,
        help="Maximum sequence length (default: 2048)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of epochs (default: 5)"
    )
    parser.add_argument(
        "--batchsize",
        type=int,
        default=4,
        help="Batch size (default: 4)"
    )
    parser.add_argument(
        "--checkpoint_path",
        type=str,
        default="",
        help="Checkpoint path "
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="fewshot",
        help="Experiment type (default: fewshot)"
    )
    parser.add_argument(
        '--size',
        type=float,
        help='how many samples from the original data are getting selected? in percent, default 100% i.e. 1.0',
        default=1.0
    )
    parser.add_argument(
        '--dataset',
        type=str,
        default="data/ED/MK8A.xlsx"
    )

    parser.add_argument(
        '--evaluation',
        type=bool,
        default=1
    )

    args = parser.parse_args()

    experiment_id, test_dataset = train(
        max_sequ_length=args.max_sequ_length,
        epochs=args.epochs,
        batchsize=args.batchsize,
        checkpoint_path=args.checkpoint_path,
        prompt=args.prompt,
        size=args.size,
        dataset_path=args.dataset
    )

    
    gc.collect()
    torch.cuda.empty_cache()

    if args.evaluation:
        evaluate(eval_dataset=test_dataset,
                prompt_type=args.prompt,
                model_dir="{}/results/{}/{}/merged".format(BP, args.checkpoint_path.split("/")[-1], experiment_id),
                report_path="./results/{}/{}/report.txt".format(args.checkpoint_path.split("/")[-1], experiment_id),
                max_new_token=16
                )
