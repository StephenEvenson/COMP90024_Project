import time
from typing import Union

import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def get_retrieve_model(model_name_or_path='msmarco-MiniLM-L-6-v3', device=None):
    model = SentenceTransformer(model_name_or_path, device=device)
    return model


retrieve_model = get_retrieve_model(device=device)


def compute_embedding(text: Union[str, list[str]]) -> Union[np.ndarray, torch.Tensor]:
    if isinstance(text, list):
        return retrieve_model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    else:
        return retrieve_model.encode([text], convert_to_numpy=True, show_progress_bar=False)[0]


def cosine_similarity(a, b):
    return util.pytorch_cos_sim(a, b).item()

labels = [
    'homeless, lost job, unemployed',
    'homeless, poverty, Income Inequality, poor, struggle',
    'homeless, mental Health, Substance Abuse',
    'homeless, Homeless prevention, Organizations, charities',
    'homeless, Education Opportunities, lack of education, education'
]
matching_emb = [compute_embedding(label) for label in labels]

def get_label_sim(text):

    keys = ['job', 'eco', 'men', 'soc', 'edu']
    
    scores = []
    for emb in matching_emb:
        scores.append(cosine_similarity(compute_embedding(text), emb))
    return [{'label': label, 'score': score} for label, score in zip(keys, scores)]


if __name__ == '__main__':
    start = time.time()
    for i in range(100):
        text = 'I lost all my money and now I am homeless'
        get_label_sim(compute_embedding(text))

    print(f"Time: {(time.time() - start) / 100}")
