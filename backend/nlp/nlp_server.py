import numpy as np
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from backend.nlp import compute_cross_score, compute_embedding, get_abusive_score, get_sentiment_score

app = FastAPI()

# retrieve_model_name = 'msmarco-MiniLM-L-6-v3'
# cross_model_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
#
# retrieve_model = get_retrieve_model(retrieve_model_name, device='cpu')
# cross_model = get_cross_encoder_model(cross_model_name, device='cpu')

all_texts = []
all_embeddings = []


class CrossScoreReq(BaseModel):
    query: str
    doc: str


class CrossScoreRes(BaseModel):
    score: float


class ScoreReq(BaseModel):
    query: str


class ScoreRes(BaseModel):
    score: float


class UpdateEmbeddingReq(BaseModel):
    query: str


class UpdateEmbeddingRes(BaseModel):
    query: str
    total: int


@app.post("/get_score")
async def get_score(req: CrossScoreReq):
    score = compute_cross_score(req.query, req.doc)
    return CrossScoreRes(score=score)


@app.post("/get_abusive_score")
async def get_a_score(req: ScoreReq):
    score = get_abusive_score(req.query)
    return ScoreRes(score=score)


@app.post("/get_sentiment_score")
async def get_s_score(req: ScoreReq):
    score = get_sentiment_score(req.query)
    return ScoreRes(score=score)


@app.post("/update_embedding")
async def update_embedding(req: UpdateEmbeddingReq):
    new_embedding = compute_embedding(req.query)
    all_texts.append(req.query)
    all_embeddings.append(new_embedding)
    return UpdateEmbeddingRes(query=req.query, total=len(all_texts))

# async def update_embedding(req: UpdateEmbeddingReq):


# usage:
# uvicorn backend.nlp.nlp_server:app --host 0.0.0.0 --port 8000 --reload
