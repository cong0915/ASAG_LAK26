from typing import Optional, List, Any, Callable, Literal
import os
import pandas as pd
from datasets import Dataset, DatasetDict, ClassLabel
from transformers import AutoTokenizer
import uuid

from .prompts import TEMPLATES_fewshot, iM2641902_text, iM2641902_question, TEMPLATES_zeroshot
from .evaluation_criteria import TEMPLATES_EC, Evaluation_hinweise

# Basis-Pfad des Projekts
BP = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../.."))

def stratified_split(ds, size: float = 0.8, seed: int = 42):

    categories = ds.unique("category")
    ds = ds.map(lambda x: {"category_for_split": x["category"]})
    ds = ds.cast_column("category_for_split", ClassLabel(names=categories))
    
    split = ds.train_test_split(
        train_size=size,
        seed=seed,
        stratify_by_column="category_for_split"
    )
    
    split = split.remove_columns("category_for_split")
    
    return split


class DSUtils:
    @staticmethod
    def load_excel(excel_path: str,
                   excel_cols: Optional[List[str]] = None) -> Dataset:
        data = pd.read_excel(excel_path, usecols=excel_cols)
        return Dataset.from_pandas(data)
    
    @staticmethod
    def format_mapper_finetuning(sample: Any) -> Any:
        system_prompt = "You will receive a text (T), a question (Q) about the text, and an answer (A) to that question. Return true if the answer is correct, otherwise return false."
        template = TEMPLATES_zeroshot[sample["category"]]
        prompt = template.format(
            s_text=iM2641902_text[sample["category"]],
            s_question=iM2641902_question[sample["category"]],
            s_input=sample["value"]
        )
        sample["messages"] = [{"role": "system",
                               "content": system_prompt},
                              {"role": "user",
                               "content": prompt.strip()}]
        # sample["completion"] = assistant_prompt
        return sample
    
    
    @staticmethod
    def format_mapper_fewshot(sample: Any) -> Any:
        system_prompt = (
            "Sie sind Mathematiklehrer. "
            "Bewerten Sie die Antworten der Schüler."
            "Überlegen Sie sich Schritt für Schritt eine Begründung, aber Ihre Ausgabe darf nur aus einem Wort bestehen: "
            "'true' oder 'falsch'."
        ).format(Evaluation_hinweise)
        user_prompt = (
            "Sie erhalten einen Text (T), eine Frage (Q) zu diesem Text, ein paar Beispiels und am Ende eine Antwort eines Schülers (A): {}. "
            "Bitte beurteilen Sie, ob die Antwort richtig ist. "
            "\nPlease reason step by step, and put your final answer within \\boxed{{}}."
        )

        template = TEMPLATES_fewshot[sample["category"]]
        prompt = user_prompt.format(template.format(
            s_text=iM2641902_text[sample["category"]],
            s_question=iM2641902_question[sample["category"]],
            s_input=sample["value"]
        ))
        assistant_prompt = '{"result": true}' if float(sample["correct"]) > 0 else '{"result": false}'
        sample["messages"] = [{"role": "system",
                               "content": system_prompt},
                              {"role": "user",
                               "content": prompt.strip()}]
        sample["prompt"] = system_prompt + "\n" + prompt.strip()
        # sample["completion"] = assistant_prompt
        return sample
    

    @staticmethod
    def format_mapper_zeroshot(sample: Any) -> Any:
        system_prompt = (
            "Sie sind Mathematiklehrer. "
            "Bewerten Sie die Antworten der Schüler."
            "Überlegen Sie sich Schritt für Schritt eine Begründung, aber Ihre Ausgabe darf nur aus einem Wort bestehen: "
            "'true' oder 'falsch'."
        ).format(Evaluation_hinweise)
        user_prompt = (
            "Sie erhalten einen Text (T), eine Frage (Q) zu diesem Text und eine Antwort eines Schülers (A): {}. "
            "Bitte beurteilen Sie, ob die Antwort richtig ist. "
            "\nPlease reason step by step, and put your final answer within \\boxed{{}}."
        )
        template = TEMPLATES_zeroshot[sample["category"]]
        prompt = user_prompt.format(template.format(
            s_text=iM2641902_text[sample["category"]],
            s_question=iM2641902_question[sample["category"]],
            s_input=sample["value"]
        ))
        assistant_prompt = '{"result": true}' if float(sample["correct"]) > 0 else '{"result": false}'
        sample["messages"] = [{"role": "system",
                               "content": system_prompt},
                              {"role": "user",
                               "content": prompt.strip()},
                            ]
        sample["prompt"] = system_prompt + "\n" + prompt.strip()
        sample["completion"] = assistant_prompt
        return sample
    
    @staticmethod
    def format_mapper_evaluation_criteria(sample: Any) -> Any:
        system_prompt = (
            "Sie sind Mathematiklehrer. "
            "Bewerten Sie die Antworten der Schüler anhand der vorgegebenen Kriterien. Die Meta-Regeln für die Bewertung lauten: {}"
            "Überlegen Sie sich Schritt für Schritt eine Begründung, aber Ihre Ausgabe darf nur aus einem Wort bestehen: "
            "'true' oder 'falsch'."
        ).format(Evaluation_hinweise)
        user_prompt = (
            "Sie erhalten einen Text (T), eine Frage (Q) zu diesem Text und eine Antwort eines Schülers (A): {}. "
            "Bitte beurteilen Sie, ob die Antwort richtig ist. "
            "Die Bewertungskriterien sind: {}. "
             "\nPlease reason step by step, and put your final answer within \\boxed{{}}."
        )

        template = TEMPLATES_zeroshot[sample["category"]]
        prompt = user_prompt.format(template.format(
            s_text=iM2641902_text[sample["category"]],
            s_question=iM2641902_question[sample["category"]],
            s_input=sample["value"]
        ), TEMPLATES_EC[sample["category"]])
        assistant_prompt = '{"result": true}' if float(sample["correct"]) > 0 else '{"result": false}'
        sample["messages"] = [{"role": "system",
                               "content": system_prompt},
                              {"role": "user",
                               "content": prompt.strip()}]
        sample["prompt"] = system_prompt + "\n" + prompt.strip()
        # sample["completion"] = assistant_prompt
        return sample


    @staticmethod
    def convert_to_messages_format_instruct(ds: Dataset,
                                            map_func: Callable[[Any], Any],
                                            exp: str,
                                            experiment_id: str,
                                            clean: bool = True,
                                            excel_path: str = "MK8A.xlsx",
                                            size: float = 1.0) -> DatasetDict:
        if size < 1.0:
            ds = stratified_split(ds, size=size, seed=42)["train"]

        ds = ds.add_column("prompt", [None] * len(ds))
        ds = ds.add_column("completion", [None] * len(ds))
        ds = ds.map(map_func, num_proc=12)

        if clean:
            ds = ds.remove_columns(["category", "correct", "value"])

        ds_dict_temp = ds.train_test_split(test_size=0.3, seed=42)
        ds_dict = DatasetDict({
            "train_sft": ds_dict_temp["train"],
            "test_sft": ds_dict_temp["test"]
        })

        save_path = f"{BP}/LLM/data/DS/{os.path.splitext(os.path.basename(excel_path))[0]}_clean={clean}_{exp}_{experiment_id}"
        ds_dict.save_to_disk(save_path)

        return ds_dict
    

    @staticmethod
    def load_ds_from_excel(prompt_type,
                           experiment_id,
                           excel_path: str = "./data/MK8A.xlsx",
                           clean: bool = True,
                           size: float = 1.0) -> DatasetDict:
        ds = DSUtils.load_excel(excel_path=excel_path)

        if prompt_type == "fewshot":
            map_func = DSUtils.format_mapper_fewshot
        elif prompt_type == "zeroshot":
            map_func = DSUtils.format_mapper_zeroshot
        elif prompt_type == "evaluation_criteria":
            map_func = DSUtils.format_mapper_evaluation_criteria
        else:
            raise ValueError("unsupport prompt_type")

        return DSUtils.convert_to_messages_format_instruct(
            ds=ds,
            map_func=map_func,
            exp=prompt_type,
            experiment_id=experiment_id,
            clean=clean,
            excel_path=excel_path,
            size=size
        )
    
    @staticmethod
    def load_ds_from_excel_for_eval(prompt_type,
                           experiment_id: str=uuid.uuid4(),
                           excel_path: str = "./data/MK8A.xlsx",
                           size: float = 1.0,
                           openai: bool = None) -> DatasetDict:
        ds = DSUtils.load_excel(excel_path=excel_path)

        prompt_type_clean = str(prompt_type).strip().rstrip(',')
        if prompt_type_clean == "fewshot":
            map_func = DSUtils.format_mapper_fewshot
        elif prompt_type_clean == "zeroshot":
            map_func = DSUtils.format_mapper_zeroshot
        elif prompt_type_clean == "evaluation_criteria":
            map_func = DSUtils.format_mapper_evaluation_criteria
        else:
            raise ValueError("unsupport prompt_type: {}".format(prompt_type))
        
        if size < 1.0:
            # ds = ds.train_test_split(train_size=size, seed=42)["train"]
            ds = stratified_split(ds, size=size, seed=42)["train"]

        ds = ds.add_column("messages", [None] * len(ds))
        ds = ds.add_column("completion", [None] * len(ds))
        ds = ds.map(map_func, num_proc=12)

        save_path = f"{BP}/data/DS/{os.path.splitext(os.path.basename(excel_path))[0]}_{prompt_type}_{experiment_id}"
        ds.save_to_disk(save_path)

        return ds


    @staticmethod
    def load_ds_from_excel_for_eval_openai_finetuning(prompt_type,
                           experiment_id: str=uuid.uuid4(),
                           excel_path: str = "./data/MK8A.xlsx",
                           size: float = 1.0,
                           openai: bool = None) -> DatasetDict:
        ds = DSUtils.load_excel(excel_path=excel_path)

        map_func = DSUtils.format_mapper_finetuning
      
        if size < 1.0:
            # ds = ds.train_test_split(train_size=size, seed=42)["train"]
            ds = stratified_split(ds, size=size, seed=42)["train"]

        ds = ds.train_test_split(test_size=0.3, seed=42)["test"]

        ds = ds.add_column("messages", [None] * len(ds))
        ds = ds.add_column("completion", [None] * len(ds))
        ds = ds.map(map_func, num_proc=12)

        return ds


if __name__ == "__main__":
    pass
