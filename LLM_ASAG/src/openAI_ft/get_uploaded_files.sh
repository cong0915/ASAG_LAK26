# put your home path
BASE_PATH=""


KEY_PATH="$BASE_PATH/data/openai/key.txt"
OPENAI_API_KEY=$(cat "$KEY_PATH")


curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY"
