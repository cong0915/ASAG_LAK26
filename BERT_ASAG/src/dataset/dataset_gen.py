import pandas as pd
from datasets import Dataset, DatasetDict

from dataset.templates import *

def load_excel(dataset_path) -> Dataset:
    excel_data = pd.read_excel(dataset_path)
    data = pd.DataFrame(excel_data)
    ds = Dataset.from_pandas(data)
    return ds

def prepare_template(row):
    category = row['category']
    s_input = row['value']
    s_text = iM2641902_text.get(category, "")
    s_question = iM2641902_question.get(category, "")

    template = TEMPLATES.get(category, "")
    if template:
        return template.format(s_text=s_text, s_question=s_question, s_input=s_input)
    else:
        return s_input

def prepare_dataset(dataset_path: str) -> DatasetDict:

    df = pd.read_excel(dataset_path)   
    df['model_input'] = df.apply(prepare_template, axis=1)     
    df = df.dropna(subset=['model_input', 'correct'])     
    df['correct'] = df['correct'].astype(int)

    # df_for_training = df[["model_input", "correct"]].rename(columns={"model_input": "text", "correct": "label"})
    df_for_training = df.rename(columns={"model_input": "text", "correct": "label"})
    dataset = Dataset.from_pandas(df_for_training)

    return dataset
