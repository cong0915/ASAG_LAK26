# put your home path
BASE_PATH=""
# excel data ID and experiment name
EXCEL_NAME=""
EXP_NAME="fintuning_0.03"


KEY_PATH="$BASE_PATH/data/openai/key.txt"
OPENAI_API_KEY=$(cat "$KEY_PATH")

# Specify target file, that should be uploaded
TARGET_FILE="$BASE_PATH/data/DS/$EXP_NAME/${EXCEL_NAME}_clean=True_conversational_train_sft.jsonl"


curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="fine-tune" \
  -F file="@${TARGET_FILE}"