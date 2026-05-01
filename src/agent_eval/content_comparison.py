from pathlib import Path
from typing import Optional, Union
import json
import time

import pandas as pd
from tqdm.auto import tqdm

from agent_eval.io_utils import load_input_data, save_excel
from agent_eval.llm_client import call_llm, parse_json_response
from agent_eval.prompts import build_content_prompt
from agent_eval.schemas import CONTENT_SCHEMA


PathLike = Union[str, Path]


CONTENT_COLUMNS = [
    "content_recall",
    "content_precision",
    "content_f1",
    "unsupported_addition_rate",
    "omission_rate",
    "content_comparison_summary",
    "human_content_elements",
    "ai_content_elements",
    "content_matches",
    "missing_human_content",
    "unsupported_ai_content",
    "content_error",
]


def empty_content_result(error: str) -> dict:
    return {
        "content_recall": None,
        "content_precision": None,
        "content_f1": None,
        "unsupported_addition_rate": None,
        "omission_rate": None,
        "content_comparison_summary": None,
        "human_content_elements": None,
        "ai_content_elements": None,
        "content_matches": None,
        "missing_human_content": None,
        "unsupported_ai_content": None,
        "content_error": error,
    }


def to_json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def flatten_content_result(result: dict) -> dict:
    return {
        "content_recall": result.get("content_recall"),
        "content_precision": result.get("content_precision"),
        "content_f1": result.get("content_f1"),
        "unsupported_addition_rate": result.get("unsupported_addition_rate"),
        "omission_rate": result.get("omission_rate"),
        "content_comparison_summary": result.get("content_comparison_summary"),
        "human_content_elements": to_json_text(result.get("human_content_elements", [])),
        "ai_content_elements": to_json_text(result.get("ai_content_elements", [])),
        "content_matches": to_json_text(result.get("content_matches", [])),
        "missing_human_content": to_json_text(result.get("missing_human_content", [])),
        "unsupported_ai_content": to_json_text(result.get("unsupported_ai_content", [])),
        "content_error": "",
    }


def compare_content_single_row(
    row: pd.Series,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0,
) -> dict:
    prompt = build_content_prompt(row)

    raw_response = call_llm(
        prompt=prompt,
        model_name=model_name,
        response_schema=CONTENT_SCHEMA,
        temperature=temperature,
    )

    parsed = parse_json_response(raw_response)
    return flatten_content_result(parsed)


def run_content_comparison(
    input_path: PathLike,
    output_path: PathLike,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0,
    limit: Optional[int] = None,
    sleep_seconds: float = 15,
) -> pd.DataFrame:
    df = load_input_data(input_path)

    if limit is not None:
        df = df.head(limit).copy()

    results = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            result = compare_content_single_row(
                row=row,
                model_name=model_name,
                temperature=temperature,
            )
        except Exception as error:
            result = empty_content_result(str(error))

        results.append(result)

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    content_df = pd.DataFrame(results)

    final_df = pd.concat(
        [df.reset_index(drop=True), content_df.reset_index(drop=True)],
        axis=1,
    )

    save_excel(final_df, output_path)

    return final_df


def find_failed_content_rows(df: pd.DataFrame) -> pd.Series:
    missing_score = df["content_f1"].isna() if "content_f1" in df.columns else True

    has_error = (
        df["content_error"].fillna("").astype(str).str.strip() != ""
        if "content_error" in df.columns
        else False
    )

    return missing_score | has_error


def rerun_failed_content_rows(
    input_path: PathLike,
    output_path: PathLike,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0,
    sleep_seconds: float = 60,
) -> pd.DataFrame:
    df = pd.read_excel(input_path)

    for col in CONTENT_COLUMNS:
        if col not in df.columns:
            df[col] = None

    failed_mask = find_failed_content_rows(df)
    failed_indices = df[failed_mask].index.tolist()

    print(f"Failed content rows to rerun: {len(failed_indices)}")

    for idx in tqdm(failed_indices):
        row = df.loc[idx]

        try:
            result = compare_content_single_row(
                row=row,
                model_name=model_name,
                temperature=temperature,
            )
        except Exception as error:
            result = empty_content_result(str(error))

        for col, value in result.items():
            df.loc[idx, col] = value

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    save_excel(df, output_path)

    return df
