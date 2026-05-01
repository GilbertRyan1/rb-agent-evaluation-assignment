from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

from agent_eval.io_utils import load_input_data, save_excel


PathLike = Union[str, Path]


DEFAULT_MODEL = "Alibaba-NLP/gte-large-en-v1.5"


def get_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_similarity_model(model_name: str = DEFAULT_MODEL) -> SentenceTransformer:
    return SentenceTransformer(
        model_name,
        trust_remote_code=True,
        device=get_device(),
    )


def encode_texts(
    model: SentenceTransformer,
    texts: list[str],
    batch_size: int = 16,
) -> np.ndarray:
    return model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True,
    )


def compute_pairwise_scores(
    human_embeddings: np.ndarray,
    ai_embeddings: np.ndarray,
) -> list[float]:
    scores = np.sum(human_embeddings * ai_embeddings, axis=1)
    return [float(score) for score in scores]


def add_semantic_similarity_scores(
    df: pd.DataFrame,
    model_name: str = DEFAULT_MODEL,
    batch_size: int = 16,
) -> pd.DataFrame:
    model = load_similarity_model(model_name)

    human_texts = df["human_answers"].fillna("").astype(str).tolist()
    ai_texts = df["ai_answers"].fillna("").astype(str).tolist()

    human_embeddings = encode_texts(model, human_texts, batch_size=batch_size)
    ai_embeddings = encode_texts(model, ai_texts, batch_size=batch_size)

    df = df.copy()
    df["semantic_similarity_score"] = compute_pairwise_scores(
        human_embeddings,
        ai_embeddings,
    )
    df["semantic_similarity_model"] = model_name

    return df


def run_semantic_similarity(
    input_path: PathLike,
    output_path: PathLike,
    model_name: str = DEFAULT_MODEL,
    batch_size: int = 16,
) -> pd.DataFrame:
    df = load_input_data(input_path)

    result_df = add_semantic_similarity_scores(
        df=df,
        model_name=model_name,
        batch_size=batch_size,
    )

    save_excel(result_df, output_path)

    return result_df
