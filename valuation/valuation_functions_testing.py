import pandas as pd
import matplotlib.pyplot as plt
from valuation import structure, important_pos, full_opinion_comparison, topic, opinion_length
import spacy

nlp = spacy.load("pt_core_news_lg")


def valuate_opinion_testing(text, nlp, nouns):
    score_1, tokens_total, doc, pos_total, punctuation = structure(text, nlp)
    score_2 = important_pos(pos_total, punctuation)
    score_3 = full_opinion_comparison(doc)
    score_4 = topic(doc, nouns)
    score_5 = opinion_length(tokens_total)
    total_score = round((score_1 + score_2 + score_3 + score_4 + score_5), 4)

    return {
        "structure": score_1,
        "important_pos": score_2,
        "full_comparison": score_3,
        "topic": score_4,
        "length": score_5,
        "total": total_score
    }


def analyze_opinions(file_path, excel_path, nlp, nouns_sets):

    scores = {
        "structure": [],
        "important_pos": [],
        "full_comparison": [],
        "topic": [],
        "length": [],
        "total": []
    }

    predicted = []

    df = pd.read_excel(excel_path)
    true_scores = df["score"].tolist()

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            text = line.strip()
            if not text:
                continue

            if i < 33:
                current_nouns = nouns_sets[0]
            elif i < 66:
                current_nouns = nouns_sets[1]
            else:
                current_nouns = nouns_sets[2]

            result = valuate_opinion_testing(text, nlp, current_nouns)

            for key in scores:
                scores[key].append(result[key])
            predicted.append(result["total"])
            print(predicted)

    print("Średnie wartości (predykcje):")
    for key in scores:
        avg = round(sum(scores[key]) / len(scores[key]), 4)
        print(f"{key}: {avg}")

    if len(predicted) != len(true_scores):
        print("Liczba opinii nie zgadza się z liczbą ocen w pliku Excel.")
        return

    errors = [abs(p - t) for p, t in zip(predicted, true_scores)]
    print(errors)
    mae = round(sum(errors) / len(errors), 4)
    print(f"\n Średni błąd bezwzględny (MAE): {mae}")

    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    axs = axs.ravel()
    for i, key in enumerate(scores):
        axs[i].hist(scores[key], bins=10, color='skyblue', edgecolor='black')
        axs[i].set_title(f"Rozkład: {key}")
        axs[i].set_xlabel("Wartość")
        axs[i].set_ylabel("Liczba opinii")

    plt.tight_layout()
    plt.show()


nouns_1 = {'brilho', 'tela', 'telefone', 'câmera', 'vídeos', 'fotos', 'bateria', 'interface', 'recursos','impressão'}
nouns_2 = {'tapetes', 'bateria', 'casa', 'limpeza', 'vida', 'volta', 'investimento', 'útil', 'esforço','função'}
nouns_3 = {'precisão', 'relógio', 'notificações', 'cronômetro', 'dia', 'vidro', 'pulseira', 'toque', 'visor','útil'}

nouns_sets = [nouns_1, nouns_2, nouns_3]
analyze_opinions("opinions.txt", "data.xlsx", nlp, nouns_sets)
