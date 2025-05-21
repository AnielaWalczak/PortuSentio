@echo off

:: 1. Tworzenie środowiska
python -m venv venv
call venv\Scripts\activate

:: 2. Instalacja zależności
 pip install -r requirements.txt
 python -m spacy download pt_core_news_lg

:: 3. Opcjonalny trening modelu
set /p TRAIN_MODEL=Czy chcesz uruchomic trening modelu (sentiment.py)? (t/n): 
if /i "%TRAIN_MODEL%"=="t" (
    echo Uruchamianie treningu modelu...
    python sentiment.py
)

:: 4. Uruchomienie Flask
python run.py
