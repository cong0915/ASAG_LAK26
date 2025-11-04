#!/bin/bash

PYTHON_EXECUTABLE=""

PROMPTS=("evaluation_criteria")

CPP=""
DATASET=""

for PROMPT in "${PROMPTS[@]}"; do
    echo ""
    echo "Starting evaluate with prompt=${PROMPT}"
    echo "Model: $CPP"
    echo "Dataset: $DATASET"
    echo "------------------------------------"

    REPORT="./results/${CPP}/__${PROMPT}.txt"

    $PYTHON_EXECUTABLE ./src/evaluation/eval.py \
        --prompt_type "$PROMPT" \
        --model_dir "$CPP" \
        --report_path "$REPORT" \
        --size "$SIZE" \
        --openai True \
        --excel_path "$DATASET" \
done