#!/bin/bash

# Assign the path to a variable
PYTHON_EXECUTABLE=""

DATASET=""

# general arguments 
PROMPT="zeroshot"

# training arguments
BATCHSIZE=4 #16
EPOCHS=2
SEQUENCELENGHT=512
SIZE=(0.03) #0.03 0.06 0.12 0.25 0.5 0.75 1
CPPs=("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

for CPP in "${CPPs[@]}"; do
    for DATASET_SIZE in "${SIZE[@]}"; do
        echo ""
        echo "Starting finetuning with DATASET_SIZE=${DATASET_SIZE}"
        echo "Model: $CPP"
        echo "Dataset: $DATASET"
        echo "------------------------------------"

        $PYTHON_EXECUTABLE ./src/train.py \
            --prompt "$PROMPT" \
            --epochs "$EPOCHS" \
            --batchsize "$BATCHSIZE" \
            --checkpoint_path "$CPP" \
            --max_sequ_length "$SEQUENCELENGHT" \
            --size "$DATASET_SIZE" \
            --dataset "$DATASET"
    done
done