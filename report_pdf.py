from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import PCMYKColor
from datetime import datetime
import spacy
from collections import Counter
import string
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

# Ładowanie Spacy
nlp = spacy.load("pt_core_news_lg")


# Funkcja zliczająca najczęstsze słowa oraz n-gramy
def extract_keywords_and_ngrams(comments):
    all_text = " ".join(comment.content.lower() for comment in comments)
    doc = nlp(all_text)

    # Zbiór stop words i znaków interpunkcyjnych
    stop_words = spacy.lang.pt.stop_words.STOP_WORDS
    punctuations = string.punctuation

    # Lista oczyszczonych tokenów
    tokens = [token.text for token in doc
              if token.is_alpha and token.text not in stop_words and token.text not in punctuations]

    # Najczęstsze słowa
    word_freq = Counter(tokens)
    top_words = word_freq.most_common(5)

    # N-gramy
    def get_ngrams(tokens, n):
        return zip(*[tokens[i:] for i in range(n)])

    bigrams = Counter(get_ngrams(tokens, 2)).most_common(5)
    trigrams = Counter(get_ngrams(tokens, 3)).most_common(5)

    # Formatujemy n-gramy jako stringi
    top_bigrams = [(" ".join(b), c) for b, c in bigrams]
    top_trigrams = [(" ".join(t), c) for t, c in trigrams]

    return top_words, top_bigrams, top_trigrams


# Funkcja rysująca wykresu sentymentu
def generate_sentiment_chart(result_counts):
    data = [result_counts.get(cat.lower(), 0) for cat in ["positivo", "neutro", "negativo"]]

    drawing = Drawing(200, 150)
    bar_chart = VerticalBarChart()
    bar_chart.x = 30
    bar_chart.y = 30
    bar_chart.height = 90
    bar_chart.width = 140
    bar_chart.data = [[data[0]], [data[1]], [data[2]]]
    bar_chart.barSpacing = 5
    bar_chart.strokeColor = colors.black
    bar_chart.valueAxis.valueMin = 0
    bar_chart.valueAxis.valueMax = max(data) + 1

    bar_chart.bars[0].fillColor = PCMYKColor(100, 0, 100, 0, alpha=85)
    bar_chart.bars[1].fillColor = PCMYKColor(100, 15, 0, 0, alpha=85)
    bar_chart.bars[2].fillColor = PCMYKColor(0, 100, 100, 0, alpha=85)

    drawing.add(bar_chart)
    drawing.add(String(37, 17, "Positivo", fontSize=10))
    drawing.add(String(86, 17, "Neutro", fontSize=10))
    drawing.add(String(129, 17, "Negativo", fontSize=10))
    return drawing


# Funkcja rysująca wykres wartościowania
def generate_value_chart(value_counts):
    categories = [str(i) for i in range(6)]
    data = [value_counts.get(i, 0) for i in range(6)]

    drawing = Drawing(200, 150)
    bar_chart = VerticalBarChart()
    bar_chart.x = 30
    bar_chart.y = 30
    bar_chart.height = 90
    bar_chart.width = 140
    bar_chart.data = [data]
    bar_chart.barSpacing = 5
    bar_chart.strokeColor = colors.black
    bar_chart.categoryAxis.categoryNames = categories
    bar_chart.valueAxis.valueMin = 0
    bar_chart.valueAxis.valueMax = max(data) + 1
    bar_chart.bars[0].fillColor = PCMYKColor(15, 30, 85, 2, alpha=85)

    drawing.add(bar_chart)
    return drawing


# Funkcja generująca PDF
def generate_pdf(product_name, date_from, date_to, comments):
    if not comments:
        print(f"Nenhum comentário sobre o produto: {product_name}")
        return

    if isinstance(date_from, str):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
    if isinstance(date_to, str):
        date_to = datetime.strptime(date_to, "%Y-%m-%d")

    # Zliczenie sentymentu, wartościowania oraz n-gramów
    result_counts = Counter(comment.result.lower() for comment in comments)
    grouped_values = [int(comment.value) for comment in comments]
    value_counts = Counter(grouped_values)
    top_words, top_bigrams, top_trigrams = extract_keywords_and_ngrams(comments)

    # Najlepsze komentarze dla każdego typu
    best_comments = {}
    for sentiment in ["positivo", "neutro", "negativo"]:
        filtered = [c for c in comments if c.result.lower() == sentiment]
        if filtered:
            sorted_comments = sorted(filtered, key=lambda c: c.value, reverse=True)
            # Ilość wyświetlanych komentarzy
            best_comments[sentiment] = sorted_comments[:3]

    # Dane do nazwy pliku wyjściowego
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 50

    # Logo
    c.drawImage(ImageReader("static/Logo.png"), margin - 6, height - 60, width=150, height=30)

    # Data
    c.setFont("Helvetica", 10)
    c.drawRightString(width - margin, height - 50, f"{datetime.now().strftime('%d-%m-%Y %H:%M')}")

    # Tytuł
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 60, f"Relatório: {product_name}")

    # Podtytuł
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 75,
                        f"Período: {date_from.strftime('%d-%m-%Y')} até {date_to.strftime('%d-%m-%Y')}")

    # Rysowanie statystyk sentymentu i wykresu obok
    y = height - 120
    c.setFont("Helvetica-Bold", 12)

    # Rysowanie tytułu sekcji
    c.drawString(margin, y, f"Número total de comentários: {len(comments)}")
    y -= 20
    sentiments_y = y

    # Rysowanie poszczególnych zdań i ilości sentymentu
    c.setFont("Helvetica", 10)
    for sentiment in ["positivo", "neutro", "negativo"]:
        c.drawString(margin + 20, y, f"Número de comentários {sentiment}s: {result_counts.get(sentiment, 0)} "
                                     f"({result_counts.get(sentiment, 0) / len(comments) * 100:.2f}%)")
        y -= 20

    # Rysowanie wykresu obok statystyk
    chart1 = generate_sentiment_chart(result_counts)
    chart1.drawOn(c, width / 2 + 50, sentiments_y - 82)

    # Odstęp przed kolejną sekcją
    y -= 20

    # Rozkład wartości i wykres obok
    c.setFont("Helvetica-Bold", 12)

    # Rysowanie tytułu sekcji
    c.drawString(margin, y, "Distribuição do número de comentários por valor:")
    y -= 20
    values_y = y
    c.setFont("Helvetica", 10)

    # Rysowanie poszczególnych wartości
    for val in range(6):
        c.drawString(margin + 20, y, f"Valor {val}: {value_counts.get(val, 0)} "
                                     f"({value_counts.get(val, 0) / len(comments) * 100:.2f}%)")
        y -= 17

    # Rysowanie wykresu
    chart2 = generate_value_chart(value_counts)
    chart2.drawOn(c, width / 2 + 50, values_y - 114)

    # Tabela z n-gramami
    # Dane do tabeli
    table_data = [
        ["Expressões mais frequentes", ""],
        ["Palavras", "Ocorrências"]
    ]
    table_data += [(word, str(count)) for word, count in top_words]
    table_data.append(["Bigramas", "Ocorrências"])
    table_data += [(bigram, str(count)) for bigram, count in top_bigrams]
    table_data.append(["Trigramas", "Ocorrências"])
    table_data += [(trigram, str(count)) for trigram, count in top_trigrams]

    # Ustawienie parametrów tabeli
    table = Table(table_data, colWidths=[150, 60])
    table.setStyle(TableStyle([
        # Nagłówek główny (tytuł)
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),

        # Nagłówki sekcji: Palavras, Bigramas, Trigramas
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
        ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 7), (-1, 7), colors.lightgrey),
        ('FONT', (0, 7), (-1, 7), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 13), (-1, 13), colors.lightgrey),
        ('FONT', (0, 13), (-1, 13), 'Helvetica-Bold'),

        # Styl ogólny
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    # Ustawienie miejsca do narysowania oby tabeli
    y_start = height - 350
    x_left = margin + 5
    x_right = (width / 2) + 25
    ngram_width, ngram_height = table.wrap(width, height)

    # Rysowanie tabeli
    table.drawOn(c, x_right, y_start - ngram_height)

    # Tabela z najlepszymi komentarzami
    # Ustalenie stylu komentarza
    styles = getSampleStyleSheet()
    comment_style = styles["Normal"]
    comment_style.fontName = "Helvetica"
    comment_style.fontSize = 10
    comment_style.leading = 12

    # Dane do tabeli
    comment_table_data = [
        ["Melhores comentários", ""]
    ]

    # Pomocnicza funkcja do ograniczenia długości opinii
    def truncate_text(text, max_words=20):
        words = text.split()
        if len(words) > max_words:
            return " ".join(words[:max_words]) + "..."
        return text

    # Pomocnicza funkcja do dodania sekcji do tabeli
    def add_comment_section(title, comments):
        comment_table_data.append([title, ""])

        for comment in comments:
            truncated = truncate_text(comment.content, max_words=20)
            text_with_id = f"<b>ID {comment.id}:</b> {truncated}"
            para = Paragraph(text_with_id, comment_style)
            comment_table_data.append([para, ""])

    # Dodanie trzech sekcji sentymentu
    add_comment_section("Positivo", best_comments.get("positivo", []))
    add_comment_section("Neutro", best_comments.get("neutro", []))
    add_comment_section("Negativo", best_comments.get("negativo", []))

    # Ustawienie parametrów tabeli
    comment_table = Table(comment_table_data, colWidths=[(width / 2) - 60, 0])
    comment_table.setStyle(TableStyle([
        # Nagłówek główny (tytuł)
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),

        # Sekcje: Positivo, Neutro, Negativo
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
        ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey),
        ('FONT', (0, 5), (-1, 5), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 9), (-1, 9), colors.lightgrey),
        ('FONT', (0, 9), (-1, 9), 'Helvetica-Bold'),

        # Ogólny styl
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))

    y -= 252

    # Rysowanie tabeli
    comment_width, comment_height = comment_table.wrap(width, height)
    comment_table.drawOn(c, x_left, y_start - comment_height)

    # Zapisywanie raportu
    c.save()
    buffer.seek(0)

    return buffer
