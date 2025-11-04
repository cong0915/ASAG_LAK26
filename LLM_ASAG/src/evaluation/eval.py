from typing import Optional, List, Any, Literal
import os
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, cohen_kappa_score
from tqdm import tqdm
import re
from datasets import Dataset
from openai import OpenAI
from datasets import load_from_disk, load_dataset
from argparse import ArgumentParser
import numpy as np
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataset.dataset_gen import DSUtils
from evaluation.load import load_model, generate
from evaluation.load_openAI import get_gpt_response

BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../../.."))


import re

def find_answer(s: str) -> bool:
    s = s.lower()
    options = [
        ("true", "false"),
        ("correct", "incorrect"),
        ("richtig", "falsch"),
        ("ja", "nein"),
        ("yes", "no"),
        ("1", "0")
    ]

    for true_word, false_word in options:
        matches = re.findall(rf'\b({true_word}|{false_word})\b', s)
        if matches:
            return matches[-1] == true_word

    return None

def evaluate(eval_dataset: Dataset,
             prompt_type,
             report_path,
             model_dir: Optional[str],
             eval_dataset_path: str="",
             excel_path: str="./data/MK8A.xlsx",
             size: float=1,
             device: Literal["cuda:0", "cuda:1", "cuda:2", "cuda:3"] = "cuda:0",
             max_new_token: int = 32,
             openai: bool = False):

    if eval_dataset:
        ds = eval_dataset
    elif eval_dataset_path:
        ds = load_from_disk(eval_dataset_path)
    else:
        ds = DSUtils.load_ds_from_excel_for_eval(prompt_type=prompt_type, excel_path=excel_path, size=size, openai=openai)

    model, tokenizer = load_model(model_dir=model_dir, device=device)

    y_pred, y_true = [], []

    categories = list(set(ds["category"]))
    label_dict = {item: index for index, item in
                  enumerate([f"{cat}-{val}" for cat in categories for val in ["Correct", "Incorrect"]])}

    with tqdm(desc=f"Evaluation", total=len(ds)) as pbar:
        jump = 0
        for idx, sample in enumerate(ds):
            try:
                result, _ = generate(prompt=sample["messages"],
                                model=model,
                                tokenizer=tokenizer,
                                device=device,
                                max_new_tokens=800)
                # print(result)
                # break
                if result is None:
                    pbar.update(1)
                    jump += 1
                    continue
                res = find_answer(result)

                val_pred = "Correct" if res else "Incorrect"
                y_pred.append(label_dict[f'{sample["category"]}-{val_pred}'])

                val_true = "Correct" if sample["correct"] > 0 else "Incorrect"
                y_true.append(label_dict[f'{sample["category"]}-{val_true}'])


                acc = accuracy_score(y_true, y_pred)
                pbar.set_postfix({"acc": f"{acc:.3f}", "jump": f"{jump}"})
            except Exception as e:
                print(f"Error at idx {idx}: {e}")
                continue
            
            pbar.update(1)

    label_id_to_name = {v: k for k, v in label_dict.items()}
    y_true_pred = set(y_true+y_pred)
    labels = [i for i in label_dict.values() if i in y_true_pred]
    target_names = [label_id_to_name[i] for i in labels]

    report = classification_report(y_true, y_pred, labels=labels, target_names=target_names,zero_division=0.0)
    print(report)
    with open(os.path.splitext(report_path)[0] + ".txt", "w") as f:
        f.write(report)


def evaluate_openai(eval_dataset: Dataset,
             prompt_type,
             report_path,
             eval_dataset_path: str="",
             excel_path: str="./data/MK8A.xlsx",
             openai_model: str = "",
             size: float=1):
    
    if eval_dataset:
        ds = eval_dataset
    elif eval_dataset_path:
        ds = load_from_disk(eval_dataset_path)
    else:
        ds = DSUtils.load_ds_from_excel_for_eval(prompt_type=prompt_type, excel_path=excel_path, size=size)

    with open(f"{BP}/data/openai/key.txt", "r") as f:
        api_key = f.read().strip()

    y_pred, y_true = [], []
    categories = list(set(ds["category"]))
    label_dict = {item: index for index, item in
                  enumerate([f"{cat}-{val}" for cat in categories for val in ["Correct", "Incorrect"]])}

    with tqdm(desc=f"Evaluation", total=len(ds)) as pbar:
        for idx, sample in enumerate(ds):
            try:
                result = get_gpt_response(
                    messages=sample["messages"],
                    client=OpenAI(api_key=api_key),
                    model=openai_model)
                # print(sample["messages"])
                print("response from openai: ", result)
                # break
                res = find_answer(result)

                
                val_pred = "Correct" if res else "Incorrect"
                y_pred.append(label_dict[f'{sample["category"]}-{val_pred}'])

                val_true = "Correct" if sample["correct"] > 0 else "Incorrect"
                y_true.append(label_dict[f'{sample["category"]}-{val_true}'])
            except Exception as e:
                print(e)
            
            acc = accuracy_score(y_true, y_pred)
            pbar.set_postfix({"acc": f"{acc:.3f}"})

            pbar.update(1)

    label_id_to_name = {v: k for k, v in label_dict.items()}
    y_true_pred = set(y_true+y_pred)
    labels = [i for i in label_dict.values() if i in y_true_pred]
    target_names = [label_id_to_name[i] for i in labels]

    report = classification_report(y_true, y_pred, labels=labels, target_names=target_names,zero_division=0.0)
    print(report)
    with open(report_path, "w") as f:
        f.write(report)
    
    cm = confusion_matrix(y_true, y_pred)
    with open(os.path.splitext(report_path)[0] + "_cm.csv", "w") as f:
        f.write(cm) 

    kappa = cohen_kappa_score(y_true, y_pred)
    kappa_linear = cohen_kappa_score(y_true, y_pred, weights="linear")
    kappa_quadratic = cohen_kappa_score(y_true, y_pred, weights="quadratic")
    with open(os.path.splitext(report_path)[0] + "_kappa.txt", "w") as f:
        f.write(f"Cohen's Kappa: {kappa}\n")
        f.write(f"Cohen's Kappa (Linear Weights): {kappa_linear}\n")
        f.write(f"Cohen's Kappa (Quadratic Weights): {kappa_quadratic}\n")
    print("Cohen's Kappa: ", kappa, "linear weighted: ", kappa_linear, "quadratic weighted: ", kappa_quadratic)

if __name__ == "__main__":
    parser = ArgumentParser(description="Evaluate a model on a dataset")
    parser.add_argument("--prompt_type", required=True, help="Prompt type for DSUtils")
    parser.add_argument("--report_path", required=True, help="Where to save evaluation report")
    parser.add_argument("--model_dir", help="Path to model directory")
    parser.add_argument("--eval_dataset_path", default="", help="Path to saved dataset (HuggingFace format)")
    parser.add_argument("--excel_path", default="./data/MK8A.xlsx", help="Path to Excel dataset")
    parser.add_argument("--size", type=float, default=1.0, help="Fraction of data to use")
    parser.add_argument("--openai", type=bool, default=False, help="use openai model or not")
    parser.add_argument("--openai_open", type=bool, default=False, help="use opened openai model or not")

    args = parser.parse_args()


    if not args.openai:
        evaluate(
            eval_dataset=None,
            prompt_type=args.prompt_type,
            report_path=args.report_path,
            model_dir=args.model_dir,
            eval_dataset_path=args.eval_dataset_path,
            excel_path=args.excel_path,
            size=args.size,
            openai=args.openai_open,
            max_new_token=32
        )
    else:
        evaluate_openai(
            eval_dataset=None,
            prompt_type=args.prompt_type,
            report_path=args.report_path,
            openai_model=args.model_dir,
            eval_dataset_path=args.eval_dataset_path,
            excel_path=args.excel_path,
            size=args.size,
        )
