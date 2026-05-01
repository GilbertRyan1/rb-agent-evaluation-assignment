from pathlib import Path
from typing import Dict, Union

import pandas as pd

from agent_eval.io_utils import ensure_dir, save_csv, save_excel


PathLike = Union[str, Path]


SCORE_COLUMNS = [
    "semantic_similarity_score",
    "behavior_match_score",
    "preference_match_score",
    "reasoning_match_score",
    "detail_preservation_score",
    "unsupported_additions_control_score",
    "response_style_match_score",
    "overall_simulation_match_score",
    "content_recall",
    "content_precision",
    "content_f1",
    "unsupported_addition_rate",
    "omission_rate",
]


DISPLAY_NAMES = {
    "semantic_similarity_score": "Semantic Similarity",
    "behavior_match_score": "Behavior Match",
    "preference_match_score": "Preference Match",
    "reasoning_match_score": "Reasoning Match",
    "detail_preservation_score": "Detail Preservation",
    "unsupported_additions_control_score": "Unsupported Additions Control",
    "response_style_match_score": "Response Style Match",
    "overall_simulation_match_score": "Overall Simulation Match",
    "content_recall": "Content Recall",
    "content_precision": "Content Precision",
    "content_f1": "Content F1",
    "unsupported_addition_rate": "Unsupported Addition Rate",
    "omission_rate": "Omission Rate",
}


def available_score_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in SCORE_COLUMNS if col in df.columns]


def make_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()

    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def create_metric_summary(df: pd.DataFrame) -> pd.DataFrame:
    score_cols = available_score_columns(df)
    temp = make_numeric(df, score_cols)

    rows = []

    for col in score_cols:
        rows.append(
            {
                "metric": DISPLAY_NAMES.get(col, col),
                "column": col,
                "mean_score": temp[col].mean(),
                "median_score": temp[col].median(),
                "min_score": temp[col].min(),
                "max_score": temp[col].max(),
                "valid_rows": temp[col].notna().sum(),
                "missing_rows": temp[col].isna().sum(),
            }
        )

    return pd.DataFrame(rows).sort_values("mean_score", ascending=False)


def create_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    score_cols = available_score_columns(df)
    temp = make_numeric(df, score_cols)

    if "question_category" not in temp.columns:
        return pd.DataFrame()

    return (
        temp.groupby("question_category")[score_cols]
        .mean()
        .reset_index()
    )


def create_person_summary(df: pd.DataFrame) -> pd.DataFrame:
    score_cols = available_score_columns(df)
    temp = make_numeric(df, score_cols)

    if "person_id" not in temp.columns:
        return pd.DataFrame()

    return (
        temp.groupby("person_id")[score_cols]
        .mean()
        .reset_index()
    )


def create_failure_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "main_failure_type" not in df.columns:
        return pd.DataFrame()

    return (
        df["main_failure_type"]
        .fillna("missing")
        .value_counts()
        .rename_axis("main_failure_type")
        .reset_index(name="count")
    )


def create_verdict_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "final_verdict" not in df.columns:
        return pd.DataFrame()

    return (
        df["final_verdict"]
        .fillna("missing")
        .value_counts()
        .rename_axis("final_verdict")
        .reset_index(name="count")
    )


def create_correlation_summary(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "semantic_similarity_score",
        "overall_simulation_match_score",
        "content_f1",
        "content_recall",
        "content_precision",
    ]

    columns = [col for col in columns if col in df.columns]
    temp = make_numeric(df, columns).dropna(subset=columns)

    if len(temp) < 2:
        return pd.DataFrame()

    corr = temp[columns].corr().reset_index()
    corr = corr.rename(columns={"index": "metric"})

    return corr


def create_high_semantic_low_alignment(df: pd.DataFrame) -> pd.DataFrame:
    required = [
        "semantic_similarity_score",
        "overall_simulation_match_score",
        "content_f1",
    ]

    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    temp = make_numeric(df, required)

    columns = [
        "id",
        "question_category",
        "person_id",
        "human_answers",
        "ai_answers",
        "semantic_similarity_score",
        "overall_simulation_match_score",
        "content_f1",
        "unsupported_addition_rate",
        "omission_rate",
        "main_failure_type",
        "content_comparison_summary",
    ]

    columns = [col for col in columns if col in temp.columns]

    return temp[
        (temp["semantic_similarity_score"] >= 0.70)
        & (
            (temp["overall_simulation_match_score"] <= 2)
            | (temp["content_f1"] <= 0.40)
        )
    ][columns].sort_values("semantic_similarity_score", ascending=False)


def create_best_and_worst_examples(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    temp = df.copy()

    if "content_f1" in temp.columns:
        temp["content_f1"] = pd.to_numeric(temp["content_f1"], errors="coerce")

    columns = [
        "id",
        "question_category",
        "person_id",
        "human_answers",
        "ai_answers",
        "semantic_similarity_score",
        "overall_simulation_match_score",
        "content_recall",
        "content_precision",
        "content_f1",
        "unsupported_addition_rate",
        "omission_rate",
        "main_failure_type",
        "content_comparison_summary",
    ]

    columns = [col for col in columns if col in temp.columns]

    return {
        "best_examples": temp.sort_values("content_f1", ascending=False)[columns].head(5),
        "worst_examples": temp.sort_values("content_f1", ascending=True)[columns].head(5),
    }


def save_analysis_outputs(
    df: pd.DataFrame,
    output_dir: PathLike,
) -> Dict[str, pd.DataFrame]:
    output_dir = ensure_dir(output_dir)

    tables = {
        "metric_summary": create_metric_summary(df),
        "category_summary": create_category_summary(df),
        "person_summary": create_person_summary(df),
        "failure_type_summary": create_failure_type_summary(df),
        "verdict_summary": create_verdict_summary(df),
        "correlation_summary": create_correlation_summary(df),
        "high_semantic_low_alignment": create_high_semantic_low_alignment(df),
    }

    example_tables = create_best_and_worst_examples(df)
    tables.update(example_tables)

    for name, table in tables.items():
        save_csv(table, output_dir / f"{name}.csv")

    final_results_path = output_dir / "final_combined_results.xlsx"
    save_excel(df, final_results_path)

    summary_path = output_dir / "analysis_summary.xlsx"

    with pd.ExcelWriter(summary_path, engine="openpyxl") as writer:
        for name, table in tables.items():
            table.to_excel(writer, sheet_name=name[:31], index=False)

    return tables
