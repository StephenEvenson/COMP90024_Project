import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

device = 'cuda' if torch.cuda.is_available() else 'cpu'

abusive_model_name = 'Dabid/abusive-tagalog-profanity-detection'
abusive_model = AutoModelForSequenceClassification.from_pretrained(abusive_model_name, device=device)
abusive_tokenizer = AutoTokenizer.from_pretrained(abusive_model_name)


def get_abusive_score(text: str) -> float:
    inputs = abusive_tokenizer(text, return_tensors="pt")
    outputs = abusive_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[0][1].item()


def get_abusive_scores(texts: list[str]) -> list[float]:
    inputs = abusive_tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=256)
    outputs = abusive_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[:, 1].tolist()


def warm_up_abusive_model():
    get_abusive_score('test')


if __name__ == '__main__':
    print("Warm up abusive model")
    warm_up_abusive_model()
