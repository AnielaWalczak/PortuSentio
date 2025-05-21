#!/bin/bash

# 1. Tworzenie środowiska
python3 -m venv venv
source venv/bin/activate

# 2. Instalacja zależności
pip install -r requirements.txt
python -m spacy download pt_core_news_lg

# 3. Opcjonalny trening modelu
read -p "Czy chcesz uruchomic trening modelu (sentiment.py)? (t/n): " TRAIN_MODEL
if [[ "$TRAIN_MODEL" == "t" ]]; then
    echo "Uruchamianie treningu modelu..."
    python sentiment.py
fi

# 4. Uruchomienie Flask
python run.py
