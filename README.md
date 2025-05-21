
1. Tworzenie środowiska

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate

2. Instalacja zależności

pip install -r requirements.txt
python -m spacy download pt_core_news_lg

3. (Opcjonalnie) Trenowanie modelu

python sentiment.py

4. Uruchomienie aplikacji

python run.py

Aplikacja uruchomi się na http://127.0.0.1:5000

5. (Opcjonalnie) Automatyczne uruchomienie całego projektu

Możesz uruchomić skrypt komendą:

./start_project.sh      # dla Linux/macOS

.\start_project.bat       # dla Windows

Skrypt:

- aktywuje środowisko,

- instaluje zależności,

- pyta, czy trenować model,

- uruchamia aplikację Flask.

6. Testowanie
Testy znajdują się w folderze testy/. Użyj:

pytest -v
