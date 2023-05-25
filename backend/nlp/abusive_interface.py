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

abusive_model_name = 'Dabid/abusive-tagalog-profanity-detection'
abusive_model = AutoModelForSequenceClassification.from_pretrained(abusive_model_name)
abusive_model.to(device)
abusive_tokenizer = AutoTokenizer.from_pretrained(abusive_model_name)


def get_abusive_score(text: str) -> float:
    inputs = abusive_tokenizer(text, return_tensors="pt").to(device)
    outputs = abusive_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[0][1].item()


def get_abusive_scores(texts: list[str]) -> list[float]:
    inputs = abusive_tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    outputs = abusive_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[:, 1].tolist()


def warm_up_abusive_model():
    get_abusive_score('test')


if __name__ == '__main__':
    print("Warm up abusive model")
    warm_up_abusive_model()
