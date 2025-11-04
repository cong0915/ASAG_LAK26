from sklearn.metrics import classification_report, confusion_matrix, cohen_kappa_score
from tqdm import tqdm
import numpy as np
from datasets import Dataset
import os
import torch
import pandas as pd

def evaluate(trainer, test_ds, report_path, wrong_pred_path=None, correct_pred_path=None):

    y_pred, y_true = [], []
    results = []
    wrong_samples = []
    correct_samples = []

    # Build label dictionary: category-Correct / category-Incorrect
    categories = sorted(set(test_ds["category"]))
    label_dict = {item: index for index, item in
                  enumerate([f"{cat}-{val}" for cat in categories for val in ["Correct", "Incorrect"]])}

    print("Label dictionary:", label_dict)

    with tqdm(desc="Evaluation", total=len(test_ds)) as pbar:
        for idx, sample in enumerate(test_ds):
            single_ds = Dataset.from_dict({k: [v] for k, v in sample.items()})
            prediction = trainer.predict(single_ds)

            logits = prediction.predictions
            pred_label_id = np.argmax(logits, axis=-1)[0]

            probs = torch.softmax(torch.tensor(logits), dim=1)
            uncertainty = 1-torch.max(probs).item()

            pred_val = "Correct" if pred_label_id > 0 else "Incorrect"
            true_val = "Correct" if sample["label"] > 0 else "Incorrect"

            pred_id = label_dict[f"{sample['category']}-{pred_val}"]
            true_id = label_dict[f"{sample['category']}-{true_val}"]

            y_pred.append(pred_id)
            y_true.append(true_id)

            if pred_val != true_val:
                wrong_samples.append({"index": idx, "sample": sample, "pred": pred_val, "true": true_val})
            else:
                correct_samples.append({"index": idx, "sample": sample, "pred": pred_val, "true": true_val})

            result_record = {
                "index": idx,
                "bert score": pred_label_id,
                "human score": sample["label"],
                "bert confidence": 1.0 - uncertainty,
                "text": sample["value"]
            }
            results.append(result_record)
            pbar.update(1)
    df = pd.DataFrame(results)
    excel_path = os.path.splitext(report_path)[0] + "_confidence.xlsx"
    df.to_excel(excel_path, index=False)

    # Prepare classification report
    label_id_to_name = {v: k for k, v in label_dict.items()}
    labels_present = sorted(set(y_true + y_pred))
    target_names = [label_id_to_name[i] for i in labels_present]

    report = classification_report(
        y_true, y_pred,
        labels=labels_present,
        target_names=target_names,
        zero_division=0
    )
    print(report)
    with open(report_path, "w") as f:
        f.write(report)
    
    cm = confusion_matrix(y_true, y_pred) 
    cm_str = np.array2string(cm) 
    with open(os.path.splitext(report_path)[0] + "_cm.csv", "w") as f:
        f.write(cm_str) 

    kappa = cohen_kappa_score(y_true, y_pred)
    kappa_linear = cohen_kappa_score(y_true, y_pred, weights="linear")
    kappa_quadratic = cohen_kappa_score(y_true, y_pred, weights="quadratic")
    with open(os.path.splitext(report_path)[0] + "_kappa.txt", "w") as f:
        f.write(f"Cohen's Kappa: {kappa}\n")
        f.write(f"Cohen's Kappa (Linear Weights): {kappa_linear}\n")
        f.write(f"Cohen's Kappa (Quadratic Weights): {kappa_quadratic}\n")
    print("Cohen's Kappa: ", kappa, "linear weighted: ", kappa_linear, "quadratic weighted: ", kappa_quadratic)

    # Save wrong predictions
    if wrong_pred_path:
        with open(wrong_pred_path, "w") as f:
            for w in wrong_samples:
                f.write(f"Index: {w['index']} | Pred: {w['pred']} | True: {w['true']} | Sample: {w['sample']}\n")

    # Save correct predictions
    if correct_pred_path:
        with open(correct_pred_path, "w") as f:
            for c in correct_samples:
                f.write(f"Index: {c['index']} | Pred: {c['pred']} | True: {c['true']} | Sample: {c['sample']}\n")

    print(f"Wrong predictions saved to: {wrong_pred_path}")
    print(f"Correct predictions saved to: {correct_pred_path}")