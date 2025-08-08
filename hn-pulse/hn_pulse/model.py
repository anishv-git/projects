from __future__ import annotations
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from .config import MODELS_DIR
from .features import prepare_training_data, build_vectorizer


MODEL_PATH = MODELS_DIR / "model.pkl"
VEC_PATH = MODELS_DIR / "vectorizer.pkl"
META_PATH = MODELS_DIR / "meta.json"


def train(save_dir: Path = MODELS_DIR) -> dict:
    X_df, y = prepare_training_data()
    if X_df.empty or y.empty:
        raise RuntimeError("Not enough data to train. Ingest and build first.")
    texts = X_df["title"]
    vectorizer = build_vectorizer(texts)
    X = vectorizer.transform(texts)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    # Save artifacts
    save_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)
    meta = {
        "model": "LogisticRegression",
        "num_samples": int(X.shape[0]),
        "num_features": int(X.shape[1]),
    }
    META_PATH.write_text(json.dumps(meta, indent=2))
    return meta


def predict_title(title: str) -> float:
    if not MODEL_PATH.exists() or not VEC_PATH.exists():
        raise RuntimeError("Model not trained. Run training first.")
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
    X = vectorizer.transform(pd.Series([title]))
    prob = float(model.predict_proba(X)[0][1])
    return prob
