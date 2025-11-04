from typing import Optional, Literal, Tuple, Any
import re

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Mxfp4Config, BitsAndBytesConfig

import os

BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../../.."))

def extract_final_answer(full_text: str) -> str:

    match = re.search(
        r"<\|start\|>assistant<\|channel\|>final<\|message\|>(.*?)<\|return\|>",
        full_text,
        re.DOTALL
    )

    match_analysis = re.search(
        r"<\|start\|>assistant<\|channel\|>analysis<\|message\|>(.*)",
        full_text,
        re.DOTALL
    )
    if match:
        return match.group(1).strip()
    else:
        return None
        # return match_analysis.group(1).strip()


def load_model(model_dir: Optional[str] = None,
               device: Literal["cuda:0", "cuda:1", "cuda:2", "cuda:3"] = "cuda:0") -> Any:

    model_kwargs = dict(
        use_cache=False,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16, 
        device_map=None,

        # only for openai-oss
        # torch_dtype="auto", # only for openai-oss
        # device_map="auto", 
        attn_implementation="flash_attention_2", # do not use it for openai-oss
    )
    model = AutoModelForCausalLM.from_pretrained(model_dir, **model_kwargs).to(device)

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=False)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)
    tokenizer.padding_side = 'right'


    return model, tokenizer


def generate(prompt: str,
             model: Any,
             tokenizer: Any,
             device: Literal["cuda:0", "cuda:1", "cuda:2", "cuda:3"] = "cuda:0",
             max_new_tokens: int = 64) -> str:

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs.to(model.device)

    # only for openai-oss
    # inputs = tokenizer.apply_chat_template(
    #     prompt,
    #     add_generation_prompt=True,
    #     return_tensors="pt",
    #     return_dict=True,
    # ).to(model.device)

    # deepseekmath
    # inputs = tokenizer.apply_chat_template(prompt, add_generation_prompt=True, return_tensors="pt")


    with torch.no_grad():
        outputs = model.generate(
                                **inputs,
                                max_new_tokens=max_new_tokens,                
                                temperature=0.7,         
                                pad_token_id=tokenizer.eos_token_id
                            )

        # only for openai-oss
        # outputs = model.generate(
        #                         **inputs,
        #                         max_new_tokens=800, # 200
        #                         temperature=0.7, # 0.7
        #                         )


    # only for openai-oss
    # full_text = tokenizer.decode(outputs[0])
    # generated_text = extract_final_answer(full_text)

    generated_text = tokenizer.decode(outputs[:, inputs["input_ids"].shape[1]:][0], skip_special_tokens=True)
    tokens = tokenizer.tokenize(generated_text)
    return generated_text, len(tokens)


if __name__ == "__main__":
    pass