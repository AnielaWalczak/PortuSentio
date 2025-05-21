import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import classification_report

class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        item = self.tokenizer(self.texts[idx], truncation=True, padding='max_length', max_length=self.max_length, return_tensors="pt")
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return {key: val.squeeze(0) for key, val in item.items()}

def preprocess_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    df = df.dropna(subset=['review_text', 'overall_rating'])

    df['label'] = df['overall_rating'].apply(lambda x: 2 if x >= 4 else 0 if x <= 2 else 1)  # 2 = pozytywne, 1 = neutralne, 0 = negatywne

    df['label'] = df['label'].astype(int)
    return df

def load_model_and_tokenizer():
    tokenizer = RobertaTokenizer.from_pretrained("roberta-base")  
    model = RobertaForSequenceClassification.from_pretrained("roberta-base", num_labels=3)
    return tokenizer, model


def train_model(df, tokenizer, model, device):
    train_texts, val_texts, train_labels, val_labels = train_test_split(df['review_text'].tolist(), df['label'].tolist(), test_size=0.2, random_state=42, stratify=df['label'])

    train_dataset = SentimentDataset(train_texts, train_labels, tokenizer)
    val_dataset = SentimentDataset(val_texts, val_labels, tokenizer)

    training_args = TrainingArguments(
        output_dir="../results",
        evaluation_strategy="epoch",
        learning_rate=5e-6,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_dir='../logs',
        logging_steps=10,
        gradient_accumulation_steps=4,
        save_total_limit=2,
        save_steps=500,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    model.to(device)
    trainer.train()

    model.save_pretrained('./sentiment_model_RoBERTa')
    tokenizer.save_pretrained('./sentiment_model_RoBERTa')

    return trainer, val_dataset

def predict_comment(model, tokenizer, device, comment):
    model.eval()
    encoded_comment = tokenizer(comment, truncation=True, padding=True, max_length=128, return_tensors="pt")
    encoded_comment = {key: val.to(device) for key, val in encoded_comment.items()}

    with torch.no_grad():
        outputs = model(input_ids=encoded_comment['input_ids'], attention_mask=encoded_comment['attention_mask'])
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=1).item()

    return "Positivo" if prediction == 2 else "Neutro" if prediction == 1 else "Negativo"

def load_saved_model():
    tokenizer = RobertaTokenizer.from_pretrained('./sentiment_model_xlm-r')
    model = RobertaForSequenceClassification.from_pretrained('./sentiment_model_xlm-r', num_labels=3)
    return tokenizer, model

def save_model(model, tokenizer, model_path="sentiment_model_xlm-r", tokenizer_path="sentiment_tokenizer_xlm-r"):
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(tokenizer_path)

if __name__ == "__main__":
    file_path = '../B2W-Reviews01.csv'
    df = preprocess_data(file_path)
    tokenizer, model = load_model_and_tokenizer()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    trainer, val_dataset = train_model(df, tokenizer, model, device)
    save_model(model, tokenizer)
    
    predictions = trainer.predict(val_dataset)
    preds = torch.argmax(torch.tensor(predictions.predictions), dim=1).tolist()

    true_labels = [val_dataset[i]['labels'].item() for i in range(len(val_dataset))]
    print(classification_report(true_labels, preds))
