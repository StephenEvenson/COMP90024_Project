from fastapi import FastAPI
from retrieve_rerank import get_cross_score, get_cross_encoder_model
from pydantic import BaseModel

app = FastAPI()
model_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
model = get_cross_encoder_model(model_name, device='cpu')


class CrossScoreReq(BaseModel):
    query: str
    doc: str


class CrossScoreRes(BaseModel):
    query: str
    doc: str
    model: str
    score: float


@app.post("/get_score")
async def get_score(req: CrossScoreReq):
    score = get_cross_score(model, req.query, req.doc)
    return CrossScoreRes(query=req.query, doc=req.doc, model=model_name, score=score)


# usage:
# cd backend/nlp/
# uvicorn nlp_server:app --reload
