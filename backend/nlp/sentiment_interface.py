from transformers import AutoTokenizer, AutoModelForSequenceClassification

sentiment_model_name = 'cardiffnlp/twitter-roberta-base-sentiment'
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)


def get_sentiment_score(text: str) -> float:
    inputs = sentiment_tokenizer(text, return_tensors="pt")
    outputs = sentiment_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[0][1].item()


def get_sentiment_scores(texts: list[str]) -> list[float]:
    inputs = sentiment_tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = sentiment_model(**inputs)
    probs = outputs.logits.softmax(dim=1).detach()
    return probs[:, 2].tolist()


if __name__ == '__main__':
    print(get_sentiment_score('putangina mo'))
