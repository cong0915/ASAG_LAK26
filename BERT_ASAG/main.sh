#!/bin/bash

PYTHON_EXECUTABLE=""

DATASET=""
SAVE_STEPS=500
TRAIN_BATCH_SIZE=32 # bert:32
TRAIN_EPOCHS=5
LEARNING_RATE=5e-5
EVAL_STEPS=500
DATASET_SIZES=(1) # 0.03 0.06 0.12 0.25 0.5 0.75 1
MODELS=("")

for MODE in "${MODELS[@]}"; do
    for DATASET_SIZE in "${DATASET_SIZES[@]}"; do
        echo ""
        echo "Starting finetuning with DATASET_SIZE=${DATASET_SIZE}"
        echo "Model: $MODE"
        echo "Dataset: $DATASET"
        echo "------------------------------------"

        $PYTHON_EXECUTABLE ./src/train.py \
            --model "$MODE" \
            --dataset "$DATASET" \
            --dataset_size "$DATASET_SIZE" \
            --save_steps "$SAVE_STEPS" \
            --per_device_train_batch_size "$TRAIN_BATCH_SIZE" \
            --num_train_epochs "$TRAIN_EPOCHS" \
            --learning_rate "$LEARNING_RATE" \
            --eval_steps "$EVAL_STEPS"

        echo "Finished training with dataset size ${DATASET_SIZE}"
        echo "====================================="
    done
done