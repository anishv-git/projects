from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .model import predict_title
from .io import duckdb_connection

app = FastAPI(title="HN Pulse API", version="0.1.0")


class PredictRequest(BaseModel):
    title: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    try:
        prob = predict_title(req.title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"title": req.title, "prob_top_quartile": prob}


@app.get("/stats/top", summary="Top stories by score")
def top(limit: int = 25):
    with duckdb_connection() as con:
        df = con.execute(
            """
            SELECT title, score, ts
            FROM stories
            WHERE title IS NOT NULL AND score IS NOT NULL
            ORDER BY score DESC
            LIMIT ?
            """,
            [limit],
        ).df()
    return df.to_dict(orient="records")
