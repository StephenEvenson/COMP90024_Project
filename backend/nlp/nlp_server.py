import numpy as np
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from search_interface import get_cross_score, get_cross_encoder_model, get_retrieve_model, compute_embedding

app = FastAPI()

retrieve_model_name = 'msmarco-MiniLM-L-6-v3'
cross_model_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2'

retrieve_model = get_retrieve_model(retrieve_model_name, device='cpu')
cross_model = get_cross_encoder_model(cross_model_name, device='cpu')

all_texts = []
all_embeddings = []


class CrossScoreReq(BaseModel):
    query: str
    doc: str


class CrossScoreRes(BaseModel):
    query: str
    doc: str
    model: str
    score: float


class UpdateEmbeddingReq(BaseModel):
    query: str


class UpdateEmbeddingRes(BaseModel):
    query: str
    total: int


@app.post("/get_score")
async def get_score(req: CrossScoreReq):
    score = get_cross_score(cross_model, req.query, req.doc)
    return CrossScoreRes(query=req.query, doc=req.doc, model=cross_model, score=score)


@app.post("/update_embedding")
async def update_embedding(req: UpdateEmbeddingReq):
    new_embedding = compute_embedding(req.query)
    all_texts.append(req.query)
    all_embeddings.append(new_embedding)
    return UpdateEmbeddingRes(query=req.query, total=len(all_texts))

# async def update_embedding(req: UpdateEmbeddingReq):


# usage:
# cd backend/nlp/
# uvicorn nlp_server:app --reload
