import pytest
import torch
import pandas as pd
from sentiment import preprocess_data, SentimentDataset, predict_comment, load_model_and_tokenizer

@pytest.fixture
def tokenizer_model():
    tokenizer, model = load_model_and_tokenizer()
    device = torch.device("cpu")
    return tokenizer, model, device

@pytest.fixture
def sample_csv(tmp_path):
    data = {
        'review_text': ["Produto ótimo", "Não gostei", "Mais ou menos"],
        'overall_rating': [5, 1, 3]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample.csv"
    df.to_csv(file_path, index=False)
    return file_path

#Czy preprocess_data tworzy poprawną kolumnę label (0, 1, 2).
def test_preprocess_data_creates_labels(sample_csv):
    df = preprocess_data(sample_csv)
    assert 'label' in df.columns
    assert set(df['label'].unique()).issubset({0, 1, 2})

#Czy SentimentDataset tokenizuje dane i zawiera klucze input_ids, attention_mask, labels.
def test_sentiment_dataset_returns_correct_keys(tokenizer_model):
    tokenizer, _, _ = tokenizer_model
    texts = ["Produto maravilhoso", "Não gostei"]
    labels = [2, 0]
    dataset = SentimentDataset(texts, labels, tokenizer)

    sample = dataset[0]
    assert isinstance(sample, dict)
    assert 'input_ids' in sample
    assert 'attention_mask' in sample
    assert 'labels' in sample
    assert sample['labels'].item() in [0, 1, 2]

#Czy predict_comment zwraca wynik z poprawnym opisem sentymentu.
def test_predict_comment_returns_valid_label(tokenizer_model):
    tokenizer, model, device = tokenizer_model
    comment = "Este produto é excelente!"
    prediction = predict_comment(model, tokenizer, device, comment)

    assert prediction in ["Positivo", "Neutro", "Negativo"]
