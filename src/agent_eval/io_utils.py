from pathlib import Path
from typing import Iterable, Union

import pandas as pd


PathLike = Union[str, Path]


REQUIRED_COLUMNS = [
    "id",
    "question_category",
    "question",
    "person_id",
    "human_answers",
    "ai_answers",
]


def ensure_dir(path: PathLike) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def check_required_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def load_input_data(input_path: PathLike) -> pd.DataFrame:
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_excel(input_path)
    check_required_columns(df, REQUIRED_COLUMNS)

    text_columns = [
        "question_category",
        "question",
        "person_id",
        "human_answers",
        "ai_answers",
    ]

    for col in text_columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

    return df


def save_excel(df: pd.DataFrame, output_path: PathLike) -> Path:
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    df.to_excel(output_path, index=False)
    return output_path


def save_csv(df: pd.DataFrame, output_path: PathLike) -> Path:
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    df.to_csv(output_path, index=False)
    return output_path
