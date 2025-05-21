import spacy
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import re
import statistics
from flask import Flask
from models import db, MyComment
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)

# Ładowanie spacy dla języka portugalskiego
nlp = spacy.load("pt_core_news_lg")

# Pomocnicze dicty
ner_counts = defaultdict(int)
ner_counts_exact_2 = defaultdict(int)
total_counts = defaultdict(int)

# Komentarze z testowej bazy
comments = [
    "Produto excelente, superou minhas expectativas!",
    "Muito bom, recomendo a todos!",
    "Ótima qualidade e entrega rápida.",
    "Adorei, funciona perfeitamente!",
    "Valeu cada centavo, estou muito satisfeito!",
    "Produto incrível, superou todas as minhas expectativas!",
    "Muito satisfeito, valeu cada centavo!",
    "Entrega rápida e produto de ótima qualidade!",
    "Perfeito! Exatamente como descrito no anúncio.",
    "Adorei! Funciona perfeitamente e é muito fácil de usar.",
    "A qualidade é excelente, recomendo a todos!",
    "Ótimo custo-benefício, compraria novamente!",
    "Melhor compra que fiz nos últimos tempos!",
    "O design é lindo e o material muito resistente!",
    "Super recomendo! Muito acima do esperado!",
    "Sensacional, cumpre tudo o que promete!",
    "Muito bom, a experiência de uso foi ótima!",
    "Chegou antes do prazo e em perfeito estado!",
    "Muito bem embalado e em perfeito funcionamento!",
    "Ótima escolha! Estou muito feliz com a compra.",
    "Simplesmente perfeito, atendeu todas as minhas necessidades!",
    "Produto de altíssima qualidade, fiquei impressionado!",
    "Excelente atendimento e um produto maravilhoso!",
    "O desempenho é incrível, melhor do que eu esperava!",
    "Resistente e funcional, uso todos os dias!",
    "Super fácil de usar e muito prático!",
    "Melhor investimento que fiz, super útil!",
    "Com certeza voltarei a comprar mais produtos dessa marca!",
    "Muito bonito e confortável, adorei!",
    "Perfeito para o que eu precisava, 100% satisfeito!",
    "Chegou direitinho, bem embalado e sem nenhum defeito!",
    "Ótima experiência de compra, nota 10!",
    "Já testei várias vezes e sempre funciona perfeitamente!",
    "Produto maravilhoso, vale muito a pena!",
    "A qualidade surpreendeu, melhor do que eu imaginava!",
    "Produto razoável, nada de especial.",
    "Funciona como esperado, mas nada incrível.",
    "Entrega no prazo, mas qualidade mediana.",
    "Não é ruim, mas também não é ótimo.",
    "Atendeu às expectativas básicas.",
    "O produto é aceitável, mas não me impressionou.",
    "Não é ruim, mas também não é algo que eu compraria de novo.",
    "A qualidade é média, cumpre o que promete.",
    "Parece durável, mas ainda preciso testar mais.",
    "Chegou no prazo, embalagem estava intacta.",
    "Produto razoável, funciona como descrito.",
    "Não vi muita diferença em relação a outros similares.",
    "Entrega foi dentro do esperado, sem surpresas.",
    "O material poderia ser um pouco melhor, mas não é ruim.",
    "Bom custo-benefício, mas nada extraordinário.",
    "Não me arrependo da compra, mas esperava mais.",
    "A descrição corresponde ao produto, sem grandes destaques.",
    "Funciona bem, mas há opções melhores pelo mesmo preço.",
    "Parece ser um produto comum, nada fora do normal.",
    "Atende ao propósito, mas não supera expectativas.",
    "A cor e o tamanho são exatamente como na foto.",
    "Não notei defeitos, mas também não achei incrível.",
    "O desempenho é mediano, não se destaca.",
    "A experiência de uso é neutra, nem boa nem ruim.",
    "Aceitável pelo preço, mas há alternativas melhores.",
    "A qualidade não surpreende, mas também não decepciona.",
    "Produto correto, sem nenhum diferencial especial.",
    "Cumpre o que promete, mas esperava mais pelo valor.",
    "O acabamento poderia ser um pouco melhor.",
    "O design é simples, sem detalhes chamativos.",
    "A durabilidade parece boa, mas ainda estou testando.",
    "Para uso básico, atende bem.",
    "O manual poderia ser mais detalhado, mas dá para entender.",
    "A funcionalidade é normal, sem grandes destaques.",
    "Péssima qualidade, não recomendo.",
    "Muito decepcionado, esperava mais.",
    "Quebrou depois de poucos dias de uso.",
    "Produto veio com defeito, experiência ruim.",
    "Não vale o preço, perdi dinheiro.",
    "Produto de péssima qualidade, não recomendo.",
    "Muito frágil, quebrou em poucos dias.",
    "Não vale o preço, dinheiro jogado fora.",
    "A entrega demorou muito, fiquei decepcionado.",
    "Material muito ruim, parece que vai quebrar fácil.",
    "Não funciona como prometido, propaganda enganosa!",
    "Chegou com defeito, tive que pedir reembolso.",
    "Fiquei frustrado, esperava algo muito melhor.",
    "O produto veio incompleto, faltam peças.",
    "Não atendeu às minhas expectativas, qualidade baixa.",
    "Péssima experiência de compra, não recomendo essa loja.",
    "A descrição não condiz com o que recebi.",
    "Muito difícil de usar, manual confuso.",
    "O acabamento é horrível, cheio de falhas.",
    "O produto veio riscado e parece usado.",
    "A embalagem estava toda amassada quando chegou.",
    "O suporte ao cliente foi péssimo, ninguém resolveu meu problema.",
    "Não durou nem um mês, muito decepcionado.",
    "Comprei esperando algo de qualidade, mas é muito inferior.",
    "A bateria acaba rápido demais, péssima autonomia.",
    "A montagem foi extremamente difícil, instruções ruins.",
    "Não funciona direito, trava o tempo todo.",
    "Muito barulhento, não dá para usar direito.",
    "A cor não é como na foto, bem diferente.",
    "Chegou atrasado e veio com defeitos.",
    "Tive que devolver, não gostei nada do produto.",
    "A conexão com outros dispositivos é horrível.",
    "O botão quebrou no primeiro uso.",
    "Parece um produto barato e mal feito.",
    "Não recomendo para ninguém, totalmente insatisfeito."
]

# Komentarze o telefonie
phone_comments = [
    "O celular tem uma excelente bateria, dura o dia inteiro com uso intenso.",
    "Adorei a qualidade da câmera, as fotos ficam nítidas até em ambientes com pouca luz.",
    "O design é muito bonito, mas o desempenho deixa a desejar. O processador poderia ser mais rápido.",
    "Ótimo custo-benefício. É um celular simples, mas cumpre bem as funções básicas.",
    "Fiquei impressionado com a fluidez do sistema. Não trava nem com vários aplicativos abertos.",
    "Não gostei do armazenamento, é muito limitado para quem precisa de mais espaço.",
    "A tela AMOLED é linda! A resolução é excelente para assistir vídeos e jogar.",
    "Fiquei muito satisfeito com a velocidade de carregamento. Carrega 50% em menos de 30 minutos!",
    "O som é bem alto, mas a qualidade deixa a desejar. Falta um pouco de clareza.",
    "Um celular bem equilibrado, sem grandes surpresas, mas atende bem as expectativas.",
    "A qualidade de construção é ótima. O celular é robusto e não parece frágil.",
    "Infelizmente, a câmera frontal não é muito boa para selfies em ambientes com pouca luz.",
    "O sistema operacional é bem fluido e fácil de usar, mesmo para quem não é muito familiarizado com tecnologia.",
    "Eu usava o modelo anterior e a melhoria na performance é notável. Valeu muito a pena a troca.",
    "O celular é ótimo para quem só precisa de um aparelho para chamadas e mensagens. Funciona muito bem para o básico.",
    "O preço não é tão barato, mas você recebe um celular de alta qualidade, com bons recursos.",
    "A bateria poderia durar mais, mas a carga rápida ajuda bastante no dia a dia.",
    "Comprei esse celular para jogos e estou bem satisfeito. Não esquenta nem trava durante partidas longas.",
    "É um celular excelente, mas o serviço de suporte técnico deixou a desejar. Demoraram para responder.",
    "A tela é grande, mas o celular é um pouco pesado. Não é o mais confortável para usar por longos períodos.",
    "A câmera é boa, mas a gravação de vídeo não é tão estabilizada quanto eu esperava.",
    "O sensor de impressão digital é rápido e preciso. Gosto de como o desbloqueio é ágil.",
    "Esse celular tem um design elegante e moderno, perfeito para quem se preocupa com estilo.",
    "Recomendo para quem busca um celular intermediário, com bom desempenho e preço justo.",
    "O celular é rápido, mas senti que o sistema pode melhorar em termos de personalização.",
    "A durabilidade da bateria impressiona. Mesmo com uso intensivo, dura o dia inteiro sem problemas.",
    "Não tem 5G, o que me deixou um pouco decepcionado, já que estou buscando um celular mais futurista.",
    "O atendimento da loja foi muito bom. Recebi o celular rapidamente e com muito cuidado no envio.",
    "Funciona bem para redes sociais e apps básicos, mas não é o ideal para quem precisa de um celular para tarefas mais pesadas.",
    "Comprei esse celular por recomendação de um amigo, e ele realmente não me decepcionou. Excelente para quem precisa de algo confiável."
]

telephone_pt = [
    "A câmera deste celular é incrível! As fotos ficam muito nítidas.",
    "A bateria dura o dia inteiro, estou muito satisfeito.",
    "O design é muito bonito, mas o telefone é um pouco pesado.",
    "A tela tem cores vibrantes e o brilho é ótimo ao ar livre.",
    "O sistema operacional é muito rápido e fluido.",
    "A qualidade do áudio nos alto-falantes é impressionante.",
    "O reconhecimento facial funciona muito bem, mesmo no escuro.",
    "O carregamento rápido é realmente eficiente, em menos de uma hora está completo.",
    "A interface é intuitiva e fácil de usar.",
    "O preço é um pouco alto, mas vale a pena pelo desempenho.",
    "O telefone esquenta um pouco quando jogo por muito tempo.",
    "A câmera frontal poderia ser melhor, especialmente em pouca luz.",
    "A conectividade 5G é muito rápida e estável.",
    "A memória interna é suficiente para todos os meus aplicativos.",
    "O sensor de impressão digital é rápido e preciso.",
    "A resistência à água me dá mais segurança no uso diário.",
    "O GPS funciona perfeitamente e é muito preciso.",
    "O telefone é muito leve e confortável na mão.",
    "O processador é muito potente, não trava nunca.",
    "O telefone vem com muitos aplicativos pré-instalados desnecessários.",
    "A bateria descarrega rápido quando uso aplicativos pesados.",
    "A qualidade das chamadas é excelente, o microfone capta muito bem.",
    "O armazenamento poderia ser maior, falta espaço para minhas fotos.",
    "A tela grande facilita a leitura e assistir vídeos.",
    "O suporte ao cliente foi muito prestativo quando precisei de ajuda.",
    "A construção do aparelho parece muito resistente.",
    "O celular tem um bom custo-benefício.",
    "A câmera tem muitos modos e funcionalidades úteis.",
    "A duração da bateria poderia ser melhor.",
    "O carregador original é muito eficiente.",
    "O som nos fones de ouvido Bluetooth é muito claro.",
    "O telefone atualiza para a versão mais recente do sistema rapidamente.",
    "O sensor de proximidade às vezes não funciona direito.",
    "O brilho automático da tela não é muito preciso.",
    "O telefone tem um ótimo desempenho em jogos pesados.",
    "O tempo de resposta do touch é imediato.",
    "O design é elegante e sofisticado.",
    "O telefone tem uma ótima relação custo-benefício.",
    "A câmera traseira tem estabilização óptica, o que ajuda muito nos vídeos.",
    "O telefone suporta carregamento sem fio, o que é muito conveniente.",
    "O vidro traseiro deixa muitas marcas de dedo.",
    "A interface do usuário tem muitos recursos interessantes.",
    "O telefone é muito rápido para abrir aplicativos.",
    "A experiência de uso no dia a dia é excelente.",
    "O modo noturno da câmera faz um ótimo trabalho.",
    "O telefone é compatível com caneta stylus, o que é útil para anotações.",
    "A qualidade da imagem da tela OLED é impressionante.",
    "O telefone desbloqueia muito rápido com reconhecimento facial.",
    "A vibração do telefone poderia ser mais forte.",
    "A conectividade Wi-Fi é estável e rápida.",
    "O telefone tem uma excelente duração de bateria para vídeos em streaming."
]

# Średnie występowanie poszczególnych części mowy w dowolnym zdaniu
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


# Funkcja gaussowska o wartości 1 dla argumentu 27 - średniej długości opinii ze zbioru uczącego
def gaussian(x, sigma):
    return np.exp(-((x - 27) ** 2) / (2 * sigma ** 2))


# Funkcja rysująca funkcję gaussowską
def plot_gaussian(x_min, x_max, sigma, num_points=400):
    x_values = np.linspace(x_min, x_max, num_points)
    y_values = gaussian(x_values, sigma)

    plt.plot(x_values, y_values, label=f'σ={sigma}')
    plt.axvline(27, color='r', linestyle='--', label='x=27')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Funkcja Gaussowska')
    plt.legend()
    plt.grid()
    plt.show()


# Funkcja logistyczna dla długości opinii (dla x = 27 mamy y = 0.5)
def logistic_function(x):
    k = 0.068
    x0 = 27
    return 1 / (1 + np.exp(-k * (x - x0)))


def plot_logistic():
    x_values = np.linspace(0, 120, 500)
    y_values = logistic_function(x_values)

    plt.plot(x_values, y_values)
    plt.axvline(27, color='gray', linestyle='--', label='x=27')
    plt.axhline(0.5, color='gray', linestyle='--', label='y=0.5')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Funkcja logistyczna dla długości opinii')
    plt.legend()
    plt.show()


# Funkcja wyznaczająca funkcję regresji wielomianowej dla jednostek nazwanych
def poly_regression(data, degree=5):
    X = np.array(list(data.keys())).reshape(-1, 1)
    y = np.array(list(data.values()))

    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    X_pred = np.linspace(min(X), max(X), 500).reshape(-1, 1)
    X_pred_poly = poly.transform(X_pred)
    y_pred = model.predict(X_pred_poly)

    plt.scatter(X, y, color='blue', label='Dane rzeczywiste')
    plt.plot(X_pred, y_pred, color='red', label=f'Regresja wielomianowa (stopień {degree})')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    coefs = model.coef_
    intercept = model.intercept_

    equation = "y = "
    terms = [f"{coefs[i]:} * x^{i}" for i in range(1, len(coefs))]
    equation += " + ".join(terms) + f" + {intercept:}"

    # print("Funkcja regresji:")
    # print(equation)


# Funkcja do testowania jednostek nazwanych
# def test_named_entities(doc, tokens_total, ner_counts, total_counts, ner_counts_exact_2):
#     ent_sum = sum(1 for _ in doc.ents)
#
#     if ent_sum == 0:
#         score = 0
#
#     elif ent_sum == 1:
#         if tokens_total <= 8:
#             score = 1
#         else:
#             score = 1 - (0.003313970734004532 * pow(tokens_total, 1) + 0.00015696512739263817 * pow(tokens_total, 2) +
#                          -2.3679075854889744e-06 * pow(tokens_total, 3) + 1.2517163773718845e-08 * pow(tokens_total,
#                                                                                                        4) +
#                          -2.3216250970292673e-11 * pow(tokens_total, 5) + 0.2667574445970023)
#     elif ent_sum == 2:
#         if tokens_total <= 24:
#             score = 1
#         else:
#             score = 1 - (0.0057932865451986795 * pow(tokens_total, 1) + -5.0627363501186835e-05 *
#             pow(tokens_total, 2) + 1.3397708095719274e-07 * pow(tokens_total, 3) + -0.017595490918165896)
#     else:
#         score = 1
#
#     #print(tokens_total)
#     #print(ent_sum)
#     #print(score)
#
#     total_counts[tokens_total] += 1
#
#     if ent_sum > 0:
#         ner_counts[tokens_total] += 1
#
#     if ent_sum == 2:
#         ner_counts_exact_2[tokens_total] += 1


# Funkcja wyliczająca podobieństwo kosinusowe
def cosine_similarity2(vec1, vec2):
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return np.dot(vec1, vec2) / (norm1 * norm2)


# Ładowanie zbioru uczącego analizy sentymentalnej
def preprocess_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)
    df = df.dropna(subset=['review_text', 'overall_rating'])

    df['label'] = df['overall_rating'].apply(lambda x: 2 if x >= 4 else 0 if x <= 2 else 1)

    df['label'] = df['label'].astype(int)
    return df


# Funkcja analizująca strukturę tekstu
def structure(text, nlp):
    pos_total = defaultdict(int)
    tokens_total = 0
    punctuation = 0
    if bool(re.search(r"[!?:]", text)):
        punctuation = 1

    doc = nlp(text)

    oov_tokens = sum(1 for token in doc if token.is_oov)

    if len(doc) > 0 and oov_tokens / len(doc) > 0.8:
        return 0.0, len(doc), doc, {}, punctuation

    for token in doc:
        tokens_total += 1
        pos_total[token.pos_] += 1

    pos_percentage_opinion = {}

    for pos, count in pos_total.items():
        percentage = round(count / tokens_total, 4)
        pos_percentage_opinion[pos] = percentage

    differences = {key: round(pos_percentage_opinion[key] - pos_percentage[key], 4)
                   for key in pos_percentage_opinion if key in pos_percentage}

    total_difference = sum(differences.values())

    score = round(1 - total_difference, 4)

    if len(doc) == 0:
        score = 0.0

    return score, tokens_total, doc, pos_total, punctuation


# Funkcja analizująca występowanie istotnych części mowy
def important_pos(pos_total, punctuation):
    categories_20 = ["ADJ", "ADV"]
    categories_10 = ["VERB", "NUM"]
    categories_7_5 = ["CCONJ", "SCONJ"]
    categories_5 = ["AUX", "PROPN"]
    score = 0
    for category in categories_20:
        count = pos_total.get(category, 0)
        if count > 0:
            score += 0.2

    if punctuation == 1:
        score += 0.15

    for category in categories_10:
        count = pos_total.get(category, 0)
        if count > 0:
            score += 0.1

    for category in categories_7_5:
        count = pos_total.get(category, 0)
        if count > 0:
            score += 0.075

    for category in categories_5:
        count = pos_total.get(category, 0)
        if count > 0:
            score += 0.05

    score = score * 5 / 4

    if score >= 1:
        return 1.0
    else:
        return round(score, 4)


# Funkcja analizująca jednostki nazwane
# def named_entities(doc, tokens_total):
#     ent_sum = sum(1 for _ in doc.ents)
#
#     if ent_sum == 0:
#         score = 0
#
#     elif ent_sum == 1:
#         if tokens_total <= 8:
#             score = 1
#         else:
#             score = 1 - (0.003313970734004532 * pow(tokens_total, 1) + 0.00015696512739263817 * pow(tokens_total, 2) +
#                          -2.3679075854889744e-06 * pow(tokens_total, 3) + 1.2517163773718845e-08 * pow(tokens_total,
#                                                                                                        4) +
#                          -2.3216250970292673e-11 * pow(tokens_total, 5) + 0.2667574445970023)
#     elif ent_sum == 2:
#         if tokens_total <= 24:
#             score = 1
#         else:
#             score = 1 - (0.0057932865451986795 * pow(tokens_total, 1) + -5.0627363501186835e-05 *
#             pow(tokens_total, 2) + 1.3397708095719274e-07 * pow(tokens_total, 3) + -0.017595490918165896)
#     else:
#         score = 1
#
#     return round(score, 4)


def full_opinion_comparison(doc):
    with app.app_context():
        comments = MyComment.query.all()
        embeddings = [np.array(comment.embedding) for comment in comments]

        opinion_vector = nlp(doc).vector

        similarities = cosine_similarity([opinion_vector], embeddings)[0]

        score = float(np.mean(similarities)) * 6 / 4

        if score >= 1:
            return 1.0
        else:
            return round(score, 4)


# Funkcja analizująca temat tekstu
def topic(doc, nouns):
    sentence_nouns = {token.text for token in doc if token.pos_ == "NOUN"}

    if not sentence_nouns:
        return 0

    noun_similarities = {}

    for noun in sentence_nouns:
        noun_vector = nlp(noun).vector
        similarities = {word: cosine_similarity2(noun_vector, nlp(word).vector) for word in nouns}

        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

        noun_similarities[noun] = sorted_similarities

    data_dict = dict(noun_similarities.items())
    max_values = {key: max(sublist, key=lambda x: x[1])[1] for key, sublist in data_dict.items()}

    if len(max_values) <= 3:
        score = round(statistics.mean(max_values.values()), 4)
    else:
        top_3_values = sorted(max_values.values(), reverse=True)[:3]
        score = round(statistics.mean(top_3_values), 4)

    if np.isnan(score):
        return 0.0

    return round(score, 4)


# Funkcja analizująca długość tekstu
def opinion_length(tokens_total, score_3):
    if tokens_total <= 8:
        score = 0.0
    elif tokens_total >= 100:
        score = 1.0
    else:
        score = round(logistic_function(tokens_total), 4)

    if score == 0 and score_3 > 0.7:
        return 0.7

    return round(score, 4)


# Funkcja dostosowująca wynik dla specyficznych przypadków. Parametry zostały dopasowane poprzez testy manualne.
def total_score_adjustment(score_1, score_2, score_3, score_4, score_5):
    total_score = round(score_1 + score_2 + score_3 + score_4 + score_5, 4)

    # sprawdzenie stosunku tematyki do struktury
    if score_4 < score_1:
        ratio = score_4 / score_1

        # opinia nie na temat i nie jest opinią
        if ratio < 0.45 and score_3 <= 0.6:
            return 0.0

        elif ratio < 0.45 and score_3 <= 0.6:
            return 0.5

        # opinia kompletnie nie na temat, ale jest bardzo krótką opinią
        elif ratio == 0 and score_3 > 0.6 and score_5 < 0.20:
            return 1.0

        # opinia kompletnie nie na temat, ale jest opinią
        elif ratio == 0 and score_3 > 0.6:
            return 1.5

        # opinia, która zdecydowanie jest opinią
        elif score_3 > 0.8:
            total_score = round(total_score - 0.5, 4)

        # opinia jest mniej więcej na temat i jest dłuższą opinią
        elif 0.45 <= ratio <= 0.6 and score_3 > 0.6 and score_5 > 0.4:
            total_score = round(total_score * (ratio * 1.5), 4)

        # opinia jest mniej więcej na temat i jest krótszą opinią
        elif 0.45 <= ratio <= 0.6 and score_3 <= 0.6:
            total_score = round(total_score * (ratio * 1.35), 4)

        # pozostałe przypadki
        else:
            total_score = round(total_score * ratio - 0.002, 4)

    # ogólne warunki
    # opinia jest za krótka przy dobrych pozostałych parametrach
    if score_4 > score_1 and score_5 <= 0.4:
        total_score = round(total_score / 2, 4)

    if score_1 < 0.4 and score_5 <= 0.4:
        total_score = round(total_score / 2, 4)

    elif score_2 <= 0.1:
        return 0.0

    return total_score


# Funkcja wartościująca opinię
def valuate_opinion(text, nlp, nouns):
    score_1, tokens_total, doc, pos_total, punctuation = structure(text, nlp)
    score_2 = important_pos(pos_total, punctuation)
    score_3 = full_opinion_comparison(doc)
    score_4 = topic(doc, nouns)
    score_5 = opinion_length(tokens_total, score_3)
    total_score = total_score_adjustment(score_1, score_2, score_3, score_4, score_5)

    return round(total_score)


def valuate_opinion_for_custom_product(text, nlp):
    score_1, tokens_total, doc, pos_total, punctuation = structure(text, nlp)
    score_2 = important_pos(pos_total, punctuation)
    score_3 = full_opinion_comparison(doc)
    score_4 = opinion_length(tokens_total, score_3)

    total_score = round((score_1 + score_2 + score_3 + score_4), 4)
    # Liniowa transformacja z zakresu 0-5 do 0-4
    total_score = total_score * 5 / 4

    return round(total_score)


# Funkcja wartościująca opinię dla testów
def valuate_opinion_testing(text, nlp, nouns):
    score_1, tokens_total, doc, pos_total, punctuation = structure(text, nlp)
    score_2 = important_pos(pos_total, punctuation)
    score_3 = full_opinion_comparison(doc)
    score_4 = topic(doc, nouns)
    score_5 = opinion_length(tokens_total, score_3)
    total_score = total_score_adjustment(score_1, score_2, score_3, score_4, score_5)

    if total_score <= 0.25:
        return 0
    elif total_score >= 4.75:
        return 5
    else:
        value = round(total_score * 2) / 2
        return value
