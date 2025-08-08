from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from .io import duckdb_connection


@dataclass
class FeatureArtifacts:
    X, y = None, None
    vectorizer: TfidfVectorizer | None = None


def prepare_training_data(min_score: int = 1) -> Tuple[pd.DataFrame, pd.Series]:
    with duckdb_connection() as con:
        df = con.execute(
            """
            SELECT title, COALESCE(score, 0) AS score
            FROM stories
            WHERE title IS NOT NULL
            AND score IS NOT NULL
            """
        ).df()
    if df.empty:
        return pd.DataFrame({"title": []}), pd.Series([], dtype=int)
    # Label: top quartile of score
    threshold = df["score"].quantile(0.75)
    y = (df["score"] >= threshold).astype(int)
    X_text = df["title"].fillna("").astype(str)
    return X_text.to_frame(), y


def build_vectorizer(texts: pd.Series) -> TfidfVectorizer:
    vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    vec.fit(texts)
    return vec
