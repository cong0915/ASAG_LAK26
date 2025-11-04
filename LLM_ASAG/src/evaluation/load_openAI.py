from typing import Optional, List, Any, Literal
import backoff
from openai import OpenAI, OpenAIError

# Create a function to communicate with the OpenAI API
@backoff.on_exception(backoff.expo, OpenAIError, max_tries=4)
def get_gpt_response(messages: List[dict], client: OpenAI, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content