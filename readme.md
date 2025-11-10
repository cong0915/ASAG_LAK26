# Automatic Short Answer Grading with LLMs: From Memorization to Reasoning

Repository for training and evaluating short-answer grading using LLM and BERT approaches.

## Layout
- LLM_ASAG/ — LLM training, evaluation, OpenAI fine-tuning helpers
  - src/train.py — LLM trainer entry
  - src/dataset/dataset_gen.py — dataset utilities & JSONL finetuning formatter
  - src/dataset/prompts.py — prompt templates
  - src/evaluation/ — evaluation harness and model loading
  - src/openAI_ft/ — upload/start/list/cancel helper scripts for OpenAI finetuning
  - main.sh, eval.sh, openai_eval.sh, requirements.txt
- BERT_ASAG/ — BERT training and evaluation
  - src/train.py — BERT trainer entry
  - src/dataset/dataset_gen.py — data preparation
  - src/dataset/templates.py — BERT input templates
  - src/eval.py — BERT evaluation utilities
  - main.sh, requirements.txt
- dataset/ — Excel sources and PDFs
  - MK8A.xlsx - student answers with human grading
  - evaluation_criteria_teacher.pdf - evaluation criteria for the human grading
  - item_text.pdf - text to the items

## Workflows

1. Create a Python virtual environment and install dependencies:
   - LLM: `LLM_ASAG/requirements.txt`
   - BERT: `BERT_ASAG/requirements.txt`

2. Place dataset Excel file(s) where scripts expect them (examples use `dataset/MK8A.xlsx`).

### LLM: train / evaluate

- Train: run `LLM_ASAG/src/train.py` (or use `LLM_ASAG/main.sh` to orchestrate). Configure checkpoint, prompt, dataset path, and PYTHON_EXECUTABLE as needed.

- Evaluate: use `LLM_ASAG/src/evaluation/eval.py` for local models or `eval_openai_finetuning.py` for OpenAI models.
  - Model loading / generation: `LLM_ASAG/src/evaluation/load.py`
  - OpenAI wrapper: `LLM_ASAG/src/evaluation/load_openAI.py`

### BERT: train / evaluate

- Train: run `BERT_ASAG/src/train.py` or use `BERT_ASAG/main.sh`.
- Prepare dataset with `BERT_ASAG/src/dataset/dataset_gen.py`.
- Evaluate with `BERT_ASAG/src/eval.py`.

### Hyperparameter for fine-tuning

random seeds for data split: 42

#### LLM 
- learning_rate: 1e-05
- lr_scheduler_type: "cosine"
- epochs = 2
-   peft_config = {
            "r": 16,
            "lora_alpha": 32,
            "lora_dropout": 0.05,
            "bias": "none",
            "task_type": "CAUSAL_LM",
            "target_modules": "all-linear",
            "modules_to_save": None,
        }
- ...
#### BERT
- learning_rate: 5e-05
- lr_scheduler_type: "linear"
- weight_decay: 0.01
- epochs = 5
- ...

you can find more in `LLM_ASAG/src/train.py` and `BERT_ASAG/src/train.py`.


### Notes & tips
- Many scripts require environment placeholders (e.g., `PYTHON_EXECUTABLE`, `BASE_PATH`, API keys). Set these before running.
- LLM training relies on trl/peft/flash-attn/bfloat16 configs — ensure compatible hardware and libraries.
- Evaluation scripts save reports and confusion matrices to configured report paths.