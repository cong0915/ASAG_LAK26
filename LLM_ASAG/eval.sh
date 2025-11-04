#!/bin/bash

PYTHON_EXECUTABLE=""

PROMPTS=("evaluation_criteria" 'fewshot' 'zeroshot')

SIZE=0.1
DATASET=""
OPENAI=False

CPPS=("deepseek-ai/deepseek-math-7b-instruct")

for CPP in "${CPPS[@]}"; do
    for PROMPT in "${PROMPTS[@]}"; do
        echo ""
        echo "Starting evaluate with prompt=${PROMPT}"
        echo "Model: $CPP"
        echo "Dataset: $DATASET"
        echo "------------------------------------"

        # Create report path dynamically
        REPORT="./results/${CPP##*/}/${PROMPT}/tem_tokens_report.txt"

        $PYTHON_EXECUTABLE ./src/evaluation/eval.py \
            --prompt_type "$PROMPT" \
            --model_dir "$CPP" \
            --report_path "$REPORT" \
            --size "$SIZE" \
            --openai_open "$OPENAI" \
            --excel_path "$DATASET" \
    # --eval_dataset_path "$DATASET" \
    done
done

