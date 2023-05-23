import os
import pickle
import argparse

import numpy as np
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder, util
from tqdm import tqdm

from backend.nlp.dataset import TweetsDataSet


def get_retrieve_embeddings(
        model: SentenceTransformer,
        texts: list[str],
        show_progress_bar=True,
        dump_file=None,
        device=None
):
    if dump_file and os.path.exists(dump_file):
        tqdm.write(f"Embeddings exist in file {dump_file}, loading...")
        embeddings = pickle.load(open(dump_file, 'rb'))
        if len(embeddings) == len(texts):
            tqdm.write(f"Loaded from file {dump_file}")
            return embeddings
        else:
            tqdm.write(
                f"Loaded from file {dump_file}, but the number of embeddings is not equal to the number of texts."
            )
    tqdm.write(f"Embeddings do not exist in file {dump_file}, computing...")
    tqdm.write(f"Compute embeddings for {len(texts)} texts")
    embeddings = []
    batch_size = 1000
    # embeddings batch by batch to avoid GPU OOM
    for i in tqdm(range(0, len(texts), batch_size), disable=not show_progress_bar):
        embeddings.append(model.encode(
            texts[i:i + batch_size],
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=32,
            device=device
        ))
    embeddings = np.concatenate(embeddings, axis=0)
    if dump_file is not None:
        print(f"Save embeddings to file {dump_file}")
        pickle.dump(embeddings, open(dump_file, 'wb'))
        print(f"Saved to file {dump_file}")
    return embeddings


def get_retrieve_model(model_name_or_path='msmarco-MiniLM-L-6-v3', device=None):
    model = SentenceTransformer(model_name_or_path, device=device)
    return model


def get_cross_encoder_model(model_name_or_path='cross-encoder/ms-marco-MiniLM-L-6-v2', device=None):
    model = CrossEncoder(model_name_or_path, device=device)
    return model


cross_model = get_cross_encoder_model()
retrieve_model = get_retrieve_model()


def compute_embedding(text: str) -> np.ndarray | torch.Tensor:
    return retrieve_model.encode([text], convert_to_tensor=True, show_progress_bar=False)


def compute_cross_score(query: str, doc: str) -> float:
    model_input = [[query, doc]]
    return model.predict(model_input, convert_to_numpy=True, show_progress_bar=False)[0]


def retrieve(
        model: SentenceTransformer,
        query: str,
        doc_embedding: np.ndarray | torch.Tensor,
        score_function: str = 'cosine',
        top_k: int = 5,
        threshold: float = 0.5,
        method: str = 'top_k'
):
    query_embedding = model.encode(query, convert_to_tensor=True, show_progress_bar=False)
    top_k = doc_embedding.shape[0] if method == 'threshold' else top_k
    # get hits : dict(corpus_id, score)
    if score_function == 'cosine':
        hits = util.semantic_search(query_embedding, doc_embedding, top_k=top_k)[0]
    elif score_function == 'dot':
        hits = util.semantic_search(query_embedding, doc_embedding, top_k=top_k, score_function=util.dot_score)[0]
    else:
        raise ValueError(f"Unknown score function {score_function}, should be 'cosine' or 'dot'.")
    if method == 'threshold':
        index = len(hits)
        for i, hit in enumerate(hits):
            if hit['score'] < threshold:
                index = i
                break
        hits = hits[:index]  # filter by threshold
    elif method == 'top_k':
        hits = hits[:top_k]  # filter by top_k
    else:
        raise ValueError(f"Unknown method {method}, should be 'threshold' or 'top_k'.")
    indexes = [hit['corpus_id'] for hit in hits]
    scores = [hit['score'] for hit in hits]
    return indexes, scores


def get_cross_score(model: CrossEncoder, query: str, doc: str):
    model_input = [[query, doc]]
    pred_scores = model.predict(model_input, convert_to_numpy=True, show_progress_bar=False)
    return pred_scores[0]


def re_rank_topk(model: CrossEncoder, query: str, docs: list[str], top_k=5):
    model_input = [[query, doc] for doc in docs]
    pred_scores = model.predict(model_input, convert_to_numpy=True, show_progress_bar=False)
    # sort in decreasing order
    pred_scores_argsort = np.argsort(-pred_scores)
    pred_scores_sort = -np.sort(-pred_scores)
    scores = pred_scores_sort[0:top_k]
    indexes = pred_scores_argsort[0:top_k]
    return indexes, scores


def re_rank_thresh(model: CrossEncoder, query: str, docs: list[str], thresh: float = 0., min_num: int = 1):
    model_input = [[query, doc] for doc in docs]
    pred_scores = model.predict(model_input, convert_to_numpy=True, show_progress_bar=False)
    # filter by threshold
    scores = pred_scores[pred_scores > thresh]
    indexes = np.where(pred_scores > thresh)[0]
    if len(indexes) <= min_num:
        pred_scores_argsort = np.argsort(-pred_scores)
        pred_scores_sort = -np.sort(-pred_scores)
        scores = pred_scores_sort[0:min_num]
        indexes = pred_scores_argsort[0:min_num]
    return indexes, scores


def main(args, search_query='homeless'):
    retrieve_model = get_retrieve_model(args.retrieve_model, device=args.device)
    cross_encoder = get_cross_encoder_model(args.cross_encoder_model, device=args.device)
    dataset = TweetsDataSet(args.data_path)
    doc_texts = dataset.get_texts()
    len_doc_texts = len(doc_texts)
    print(f"Total {len_doc_texts} texts")

    m = args.retrieve_model.replace('/', '-')
    docs_embeddings = get_retrieve_embeddings(
        retrieve_model,
        doc_texts,
        show_progress_bar=True,
        dump_file=f'data/{m}_{len_doc_texts}_embeddings.pkl',
        device='mps'
    )

    retrieved_indexes, retrieved_scores = retrieve(
        retrieve_model,
        search_query,
        docs_embeddings,
        score_function='cosine',
        threshold=0.5,
        method='threshold'
    )
    retrieved_texts = dataset.get_texts(retrieved_indexes)
    retrieved_ids = dataset.get_ids(retrieved_indexes)

    # re ranked by thresh
    re_ranked_indexes, re_ranked_scores = re_rank_thresh(
        cross_encoder,
        search_query,
        retrieved_texts,
        thresh=0.5,
        min_num=1
    )
    texts = [retrieved_texts[i] for i in re_ranked_indexes]
    ids = [retrieved_ids[i] for i in re_ranked_indexes]

    for i, text in enumerate(texts):
        print(f"{i}: {text} ({re_ranked_scores[i]})")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--data_path', type=str, default='data/tweets_geo_merged.jsonl')
    arg_parser.add_argument('--retrieve_model', type=str, default='sentence-transformers/msmarco-MiniLM-L-6-v3')
    arg_parser.add_argument('--cross_encoder_model', type=str, default='cross-encoder/ms-marco-MiniLM-L-6-v2')
    arg_parser.add_argument('--device', type=str, default=None, help='cpu, cuda, mps')
    args = arg_parser.parse_args()
    main(args, )
