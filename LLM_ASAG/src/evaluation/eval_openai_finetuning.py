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
    ]

    for true_word, false_word in options:
        matches = re.findall(rf'\b({true_word}|{false_word})\b', s)
        if matches:
            return matches[-1] == true_word

    return False


def evaluate_openai(eval_dataset: Dataset,
             prompt_type,
             report_path,
             eval_dataset_path: str="",
             excel_path: str="./data/MK8A.xlsx",
             openai_model: str = "",
             size: float=1):
    
    ds = DSUtils.load_ds_from_excel_for_eval_openai_finetuning(prompt_type=prompt_type, excel_path=excel_path, size=size)

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
    cm_str = np.array2string(cm) 
    with open(os.path.splitext(report_path)[0] + "_cm.csv", "w") as f:
        f.write(cm_str) 


if __name__ == "__main__":

    size = 0.5
    openai_model = "ft:gpt-4o-mini-2024-07-18:dipf:050:CBJZj2J1"
    excel_path = "/home/longwei2/text_classification/llm-text-classification/data/MK8A.xlsx"

    evaluate_openai(
        eval_dataset=None,
        prompt_type="egal",
        report_path="/home/longwei2/text_classification/llm-text-classification/results/gpt-4o-mini-2024-07-18/finetuning/{size}/report.txt".format(size=size),
        openai_model=openai_model,
        eval_dataset_path=None,
        excel_path=excel_path,
        size=size,
    )
