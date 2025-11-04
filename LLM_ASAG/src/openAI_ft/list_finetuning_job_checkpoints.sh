# put your home path
BASE_PATH=""

KEY_PATH="$BASE_PATH/data/openai/key.txt"
OPENAI_API_KEY=$(cat "$KEY_PATH")

# specify the finetune-job ID
FT_JOB="unk"


curl https://api.openai.com/v1/fine_tuning/jobs/${FT_JOB}/checkpoints \
  -H "Authorization: Bearer $OPENAI_API_KEY"
