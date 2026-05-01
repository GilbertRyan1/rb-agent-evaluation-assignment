from pathlib import Path
from typing import Optional, Union
import time

import pandas as pd
from tqdm.auto import tqdm

from agent_eval.io_utils import load_input_data, save_excel
from agent_eval.llm_client import call_llm, parse_json_response
from agent_eval.prompts import build_judge_prompt
from agent_eval.schemas import JUDGE_SCHEMA


PathLike = Union[str, Path]


DIMENSIONS = [
    "behavior_match",
    "preference_match",
    "reasoning_match",
    "detail_preservation",
    "unsupported_additions_control",
    "response_style_match",
]


FLAT_COLUMNS = [
    "behavior_match_score",
    "behavior_match_reason",
    "preference_match_score",
    "preference_match_reason",
    "reasoning_match_score",
    "reasoning_match_reason",
    "detail_preservation_score",
    "detail_preservation_reason",
    "unsupported_additions_control_score",
    "unsupported_additions_control_reason",
    "response_style_match_score",
    "response_style_match_reason",
    "overall_simulation_match_score",
    "final_verdict",
    "main_failure_type",
    "short_summary",
    "judge_error",
]


def empty_result(error: str) -> dict:
    result = {}

    for dim in DIMENSIONS:
        result[f"{dim}_score"] = None
        result[f"{dim}_reason"] = None

    result["overall_simulation_match_score"] = None
    result["final_verdict"] = None
    result["main_failure_type"] = None
    result["short_summary"] = None
    result["judge_error"] = error

    return result


def flatten_result(result: dict) -> dict:
    flat = {}

    for dim in DIMENSIONS:
        flat[f"{dim}_score"] = result.get(dim, {}).get("score")
        flat[f"{dim}_reason"] = result.get(dim, {}).get("reason")

    flat["overall_simulation_match_score"] = result.get(
        "overall_simulation_match_score"
    )
    flat["final_verdict"] = result.get("final_verdict")
    flat["main_failure_type"] = result.get("main_failure_type")
    flat["short_summary"] = result.get("short_summary")
    flat["judge_error"] = ""

    return flat


def judge_single_row(
    row: pd.Series,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0,
) -> dict:
    prompt = build_judge_prompt(row)

    raw_response = call_llm(
        prompt=prompt,
        model_name=model_name,
        response_schema=JUDGE_SCHEMA,
        temperature=temperature,
    )

    result = parse_json_response(raw_response)
    return flatten_result(result)


def run_llm_judge(
    input_path: PathLike,
    output_path: PathLike,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0,
    limit: Optional[int] = None,
    sleep_seconds: float = 2,
) -> pd.DataFrame:
    df = load_input_data(input_path)

    if limit is not None:
        df = df.head(limit).copy()

    results = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            result = judge_single_row(
                row=row,
                model_name=model_name,
                temperature=temperature,
            )
        except Exception as error:
            result = empty_result(str(error))

        results.append(result)

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    judge_df = pd.DataFrame(results)

    final_df = pd.concat(
        [df.reset_index(drop=True), judge_df.reset_index(drop=True)],
        axis=1,
    )

    save_excel(final_df, output_path)

    return final_df


def find_failed_rows(df: pd.DataFrame) -> pd.Series:
    if "overall_simulation_match_score" in df.columns:
        missing_score = df["overall_simulation_match_score"].isna()
    else:
        missing_score = pd.Series([True] * len(df), index=df.index)

    if "judge_error" in df.columns:
        has_error = df["judge_error"].fillna("").astype(str).str.strip() != ""
    else:
        has_error = pd.Series([False] * len(df), index=df.index)

    return missing_score | has_error


def rerun_failed_judge_rows(
    input_path: PathLike,
    output_path: PathLike,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0,
    sleep_seconds: float = 15,
) -> pd.DataFrame:
    df = pd.read_excel(input_path)

    for col in FLAT_COLUMNS:
        if col not in df.columns:
            df[col] = None

    failed_mask = find_failed_rows(df)
    failed_indices = df[failed_mask].index.tolist()

    print(f"Failed rows to rerun: {len(failed_indices)}")

    for idx in tqdm(failed_indices):
        row = df.loc[idx]

        try:
            result = judge_single_row(
                row=row,
                model_name=model_name,
                temperature=temperature,
            )
        except Exception as error:
            result = empty_result(str(error))

        for col, value in result.items():
            df.loc[idx, col] = value

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    save_excel(df, output_path)

    return df
