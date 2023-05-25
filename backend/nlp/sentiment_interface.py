#
# Part of Assignment 2 - COMP90024
#
# Cluster and Cloud Computing - Team 72
#
# Authors:
#
#  - Juntao Lu (Student ID: 1290513)
#  - Runtian Zhang (Student ID: 1290379)
#  - Jiahao Shen (Student ID: 1381187)
#  - Yuchen Liu (Student ID: 1313394)
#  - Jie Shen (Student ID: 1378708)
#
# Location: Melbourne
#
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

sentiment_model_name = 'cardiffnlp/twitter-roberta-base-sentiment'
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
sentiment_model.to(device)
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)


def get_sentiment_score(text: str) -> float:
    inputs = sentiment_tokenizer(text, return_tensors="pt").to(device)
    outputs = sentiment_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[0][1].item()


def get_sentiment_scores(texts: list[str]) -> list[float]:
    inputs = sentiment_tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    outputs = sentiment_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[:, 2].tolist()


def warm_up_sentiment_model():
    get_sentiment_score('test')


if __name__ == '__main__':
    print("Warm up sentiment model")
    warm_up_sentiment_model()
