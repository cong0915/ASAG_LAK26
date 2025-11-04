from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, AutoModelForSequenceClassification
from argparse import ArgumentParser

from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score
import numpy as np
import wandb

from dataset.dataset_gen import prepare_dataset
from eval import evaluate
from datasets import ClassLabel

import uuid

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*encoder_attention_mask.*")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds)
    kappa = cohen_kappa_score(labels, preds)
    return {
        "accuracy": acc,
        "f1": f1,
        "kappa": kappa,
    }

def stratified_split(ds, size: float = 0.8, seed: int = 42):

    categories = ds.unique("category")
    ds = ds.map(lambda x: {"category_for_split": x["category"]})
    ds = ds.cast_column("category_for_split", ClassLabel(names=categories))
    
    split = ds.train_test_split(
        train_size=size,
        seed=seed,
        stratify_by_column="category_for_split"
    )["train"]
    
    split = split.remove_columns("category_for_split")
    
    return split

def train(model_checkpoint, 
          csv_path: str= "data/ED/MK8A.xlsx",
          dataset_size: float=1, 
          save_steps: int=500, 
          per_device_train_batch_size: int=32,
          num_train_epochs:int=5, 
          learning_rate:float=5e-5,
          eval_steps:int=500):
    num_labels = 2

    experiment_id = str(uuid.uuid4())

    wandb.init(project="bert-classification", name="{}_{}".format(model_checkpoint.split("/")[-1], experiment_id))

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    if "bert" in model_checkpoint.lower():
        model = BertForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)
    else:
        model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)

    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

    dataset = prepare_dataset(csv_path)
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    if dataset_size < 1.0:
        _split = stratified_split(tokenized_datasets, size=dataset_size)
    else:
        _split = tokenized_datasets 
    split = _split.train_test_split(test_size=0.3, seed=42)

    train_ds = split["train"]
    eval_ds = split["test"]

    training_args = TrainingArguments(
        output_dir="./results/{}/{}".format(model_checkpoint.split("/")[-1], experiment_id),
        do_train=True,
        do_eval=True,
        save_strategy="steps", 
        save_steps=save_steps,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=16,
        num_train_epochs=num_train_epochs,
        weight_decay=0.01,
        learning_rate=learning_rate,
        warmup_steps=100,
        lr_scheduler_type="linear",
        logging_dir="./logs",
        logging_steps=10,
        metric_for_best_model="kappa",
        eval_strategy="steps",  
        eval_steps=eval_steps, 
        load_best_model_at_end=True,

        report_to="wandb",
        run_name=model_checkpoint,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    evaluate(trainer, eval_ds, report_path="./results/{}/{}/report.txt".format(model_checkpoint.split("/")[-1], experiment_id),
             wrong_pred_path = "./results/{}/{}/wrong_pred.txt".format(model_checkpoint.split("/")[-1], experiment_id),
             correct_pred_path = "./results/{}/{}/correct_pred.txt".format(model_checkpoint.split("/")[-1], experiment_id),)

    with open("./results/{}/{}/training_parameters.txt".format(model_checkpoint.split("/")[-1], experiment_id), "w") as f:
        f.write(f"model: {model_checkpoint}\n")
        f.write(f"dataset size: {dataset_size}\n")
        for key, value in training_args.to_dict().items():
            f.write(f"{key}: {value}\n")

    wandb.finish()

if __name__ == "__main__":
    parser = ArgumentParser(description="Script to train the model")

    parser.add_argument(
        "--model",
        type=str,
        default="tbs17/MathBERT",
    )
    
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/ED/MK8A.xlsx",
    )

    parser.add_argument(
        "--dataset_size",
        type=float,
        default=1,
    )

    parser.add_argument(
        "--save_steps",
        type=int,
        default=500,
    )

    parser.add_argument(
        "--per_device_train_batch_size",
        type=int,
        default=32,
    )

    parser.add_argument(
        "--num_train_epochs",
        type=int,
        default=5,
    )

    parser.add_argument(
        "--learning_rate",
        type=float,
        default=5e-5,
    )

    parser.add_argument(
        "--eval_steps",
        type=int,
        default=500,
    )

    args = parser.parse_args()

    train(model_checkpoint=args.model, 
          csv_path= args.dataset,
          dataset_size=args.dataset_size, 
          save_steps=args.save_steps, 
          per_device_train_batch_size=args.per_device_train_batch_size,
          num_train_epochs=args.num_train_epochs, 
          learning_rate=args.learning_rate,
          eval_steps=args.eval_steps)
