from valuation import structure, important_pos, full_opinion_comparison, topic, opinion_length
import pytest
import spacy


@pytest.fixture(scope="module")
def nlp():
    return spacy.load("pt_core_news_lg")


@pytest.fixture(scope="module")
def nouns_telephone():
    with open("topics.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    dicts = [eval(line.strip()) for line in lines]
    return dicts[0]


@pytest.fixture(scope="module")
def nouns_robo():
    with open("topics.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    dicts = [eval(line.strip()) for line in lines]
    return dicts[1]


@pytest.fixture(scope="module")
def nouns_assistir():
    with open("topics.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    dicts = [eval(line.strip()) for line in lines]
    return dicts[2]



@pytest.fixture(autouse=True)
def setup_global_pos_percentage():
    global pos_percentage
    pos_percentage = {
        "NOUN": 0.1883,
        "PUNCT": 0.1378,
        "VERB": 0.1366,
        "ADP": 0.0964,
        "DET": 0.0890,
        "ADV": 0.0827,
        "ADJ": 0.0717,
        "CCONJ": 0.0388,
        "PRON": 0.0377,
        "PROPN": 0.0354,
        "AUX": 0.0344,
        "SCONJ": 0.0266,
        "NUM": 0.0118,
        "SPACE": 0.0096,
        "INTJ": 0.0007,
        "SYM": 0.0004,
        "X": 0.0003,
        "PART": 0.000005
    }


# Test sprawdzający równość ilości tokenów z długością dokumentu przetworzonego przez spacy.
def test_structure_token_and_pos_count(nlp):
    text = "Este é um teste."
    score, tokens_total, doc, pos_total, punctuation = structure(text, nlp)

    assert tokens_total == len(doc)
    assert isinstance(pos_total, dict)
    assert "PUNCT" in pos_total


# Test sprawdzający pozytywne wykrycie interpunkcji.
def test_structure_detects_punctuation(nlp):
    text = "O que é isso?"
    _, _, _, _, punctuation = structure(text, nlp)
    assert punctuation == 1


# Test sprawdzający brak interpunkcji.
def test_structure_no_punctuation(nlp):
    text = "Isso é bom"
    _, _, _, _, punctuation = structure(text, nlp)
    assert punctuation == 0


# Test sprawdzający poprawność wyniku.
def test_structure_score_range(nlp):
    text = "Olá mundo!"
    score, _, _, _, _ = structure(text, nlp)
    assert 0.0 <= score <= 1.0


# Test sprawdzający wykrywanie wszystkich części mowy w zdaniu.
def test_structure_pos_percentage_calculation(nlp):
    text = "Estou muito feliz!"
    score, tokens_total, doc, pos_total, punctuation = structure(text, nlp)

    assert all(pos in pos_total for pos in ["AUX", "ADV", "ADJ", "PUNCT"])


# Test dla pustego tekstu.
def test_structure_score_0(nlp):
    text = ""
    score, _, _, _, _ = structure(text, nlp)
    assert score == 0.0


# Test dla losowych znaków.
def test_structure_random_characters(nlp):
    text = "iadsvnuiaerbuio vargaerg ggesrg reresrersgres dbxbdfhesrhfdb fdbsrtger gfserger"
    score, _, _, _, _ = structure(text, nlp)
    assert score == 0.0


# Test dla losowych liczb.
def test_structure_random_numbers(nlp):
    text = "46546861 98498465 8949845 16589 77474 88"
    score, _, _, _, _ = structure(text, nlp)
    assert score == 0.0


# Test poprawnego przypisywania wartości dla poszczególnych części mowy.
def test_important_pos_values():
    pos_total = {"ADJ": 1, "ADV": 1, "VERB": 1, "NUM": 1, "CCONJ": 1, "SCONJ": 1, "AUX": 1, "PROPN": 1}
    punctuation = 1

    score = important_pos(pos_total, punctuation)
    assert score == 1.0


# Test poprawnego przypisywania wartości dla poszczególnych części mowy bez interpunkcji.
def test_important_pos_values_no_punctuation():
    pos_total = {"ADJ": 1, "ADV": 1, "VERB": 1, "NUM": 1, "CCONJ": 1, "SCONJ": 1, "AUX": 1, "PROPN": 1}
    punctuation = 0

    score = important_pos(pos_total, punctuation)
    assert score == 1.0


# Test poprawnego przypisywania wartości dla wybranych części mowy.
def test_important_pos_selected_correct_pos():
    pos_total = {"ADJ": 5, "VERB": 4, "NUM": 3, "CCONJ": 2, "SCONJ": 1, "AUX": 1}
    punctuation = 1

    score = important_pos(pos_total, punctuation)
    assert score == 0.9375


# Test dla nieistotnych części mowy.
def test_important_pos_not_important_pos():
    pos_total = {"PRON": 1, "PART": 1, "INTJ": 1}
    punctuation = 0

    score = important_pos(pos_total, punctuation)
    assert score == 0.0


# Test wychwytywania rzeczowników.
def test_important_pos_noun():
    pos_total = {"NOUN": 10}
    punctuation = 0

    score = important_pos(pos_total, punctuation)
    assert score == 0.0


# Test pustego słownika, ale ze znakami interpunkcyjnymi.
def test_important_pos_punctuation():
    pos_total = {}
    punctuation = 1

    score = important_pos(pos_total, punctuation)
    assert score == 0.1875


# Test wykrywania poprawnej opinii.
def test_full_opinion_comparison_correct_opinion():
    text = "Gosto muito do celular. A bateria dura muito tempo. A tela é brilhante e fácil de ler."

    score = full_opinion_comparison(text)
    assert score >= 0.5


# Test wykrywania niepoprawnej opinii.
def test_full_opinion_comparison_incorrect_opinion():
    text = "q w e r t y u i o p a s d f g h j k l z x c v b n m"

    score = full_opinion_comparison(text)
    assert score < 0.5


# Test dla poprawnie napisanego tekstu niebędącego opinią.
def test_full_opinion_comparison_correct_text_but_not_opinion():
    text = "Pelicanos, pelicanos (Pelecanidae) - uma família monotípica de aves da ordem Pelicanos (Pelecaniformes). " \
           "A família dos pelicanos inclui espécies aquáticas que habitam o mundo inteiro fora da região " \
           "circumpolar, norte, oeste e centro da Europa, Sibéria, Saara e noroeste da África, Nova Zelândia " \
           "e Oceania, e estão ausentes do interior da América do Sul e de suas costas orientais. As espécies do " \
           "Velho Mundo preferem águas interiores, enquanto as que habitam o Novo Mundo são aves marinhas " \
           "(exceto o pelicano-de-bico)."

    score = full_opinion_comparison(text)
    assert score < 0.6


# Test liter alfabetu.
def test_topic_alphabet(nlp, nouns_telephone):
    text = "q w e r t y u i o p a s d f h j k l z x c v b n m"

    _, _, doc, _, _ = structure(text, nlp)

    score = topic(doc, nouns_telephone)
    assert score == 0


# Test zawierania słów ze słownika,
def test_topic_words_in_dictionary(nlp, nouns_telephone):
    text = "tela vídeos bateria"

    _, _, doc, _, _ = structure(text, nlp)

    score = topic(doc, nouns_telephone)
    assert score == 1.0


# Test niezawierania słów ze słownika, ale związanych z tematem.
def test_topic_words_not_in_dictionary(nlp, nouns_telephone):
    text = "dispositivo botões aplicação"

    _, _, doc, _, _ = structure(text, nlp)

    score = topic(doc, nouns_telephone)
    assert score > 0.5


# Test losowych słów niezwiązanych z tematem.
def test_topic_random_irrelevant_words(nlp, nouns_telephone):
    text = "flor espaço skate"

    _, _, doc, _, _ = structure(text, nlp)

    score = topic(doc, nouns_telephone)
    assert score < 0.5


# Test długości opinii dla równo średniej liczby tokenów.
def test_opinion_length_middle_point():
    total_tokens = 27

    score = opinion_length(total_tokens, 0)
    assert score == 0.5


# Test długości opinii dla mniejszej niż 8 liczby tokenów.
def test_opinion_length_less_than_8():
    total_tokens = 5

    score = opinion_length(total_tokens, 0)
    assert score == 0.0


# Test długości opinii dla równo 100 tokenów.
def test_opinion_length_100():
    total_tokens = 100

    score = opinion_length(total_tokens, 0)
    assert score == 1.0


# Test krótkiego tekstu zdecydowanie będącego opinią
def test_opinion_length_short_opinion():
    total_tokens = 4

    score = opinion_length(total_tokens, 0.75)
    assert score == 0.7
