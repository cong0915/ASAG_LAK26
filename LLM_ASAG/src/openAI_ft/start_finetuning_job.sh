# put your home path
BASE_PATH=""
# excel data ID and experiment name
EXCEL_NAME="MK8A"
EXP_NAME="fintuning_0.03"

KEY_PATH="$BASE_PATH/data/openai/key.txt"
OPENAI_API_KEY=$(cat "$KEY_PATH")

# put the ID of the trainingsfile, that should be used (use get_uploaded_files.sh for finding correct ID)
TRAINING_FILE=""
MODEL=""

curl https://api.openai.com/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "training_file": "'"$TRAINING_FILE"'",
    "model": "'"$MODEL"'",
    "suffix": "'"$EXCEL_NAME-$EXP_NAME"'",
    "hyperparameters": {
      "n_epochs": 1
    }
  }'
