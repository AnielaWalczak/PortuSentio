import spacy
import pandas as pd
import numpy as np
from bertopic import BERTopic
from collections import Counter
import statistics
import heapq

pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)

nlp = spacy.load("pt_core_news_lg")


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


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

robot_pt = [
    "O robô aspirador mudou minha vida! Agora minha casa está sempre limpa sem esforço.",
    "Muito eficiente, mas um pouco barulhento.",
    "Gostei bastante, mas poderia ter uma bateria mais duradoura.",
    "Excelente para quem tem pets! Remove todos os pelos sem problema.",
    "Adorei a função de mapeamento! Ele sabe exatamente onde limpar.",
    "Preço um pouco alto, mas vale cada centavo.",
    "Não substitui uma faxina completa, mas ajuda muito na manutenção da limpeza.",
    "Simples de usar e muito eficiente!",
    "A bateria dura bastante e ele volta sozinho para carregar.",
    "Meu melhor investimento do ano!",
    "Faz um bom trabalho, mas pode ficar preso em tapetes grossos.",
    "Facilita muito a vida de quem tem crianças pequenas.",
    "Gostaria que ele tivesse um reservatório maior para poeira.",
    "Perfeito para apartamentos pequenos!",
    "Inteligência artificial excelente, desvia bem dos obstáculos.",
    "Meu cachorro tem medo dele, mas eu adoro!",
    "Economizei muito tempo na limpeza da casa.",
    "O controle pelo aplicativo é muito prático.",
    "Silencioso e eficiente!",
    "Precisa de manutenção frequente, mas compensa.",
    "Limpa bem, mas poderia subir melhor em tapetes altos.",
    "Excelente custo-benefício!",
    "Design bonito e moderno.",
    "Adorei que ele volta sozinho para a base quando a bateria está baixa.",
    "Senti falta de uma função para esfregar o chão.",
    "Ele se perde de vez em quando, mas na maioria das vezes funciona bem.",
    "O sensor antiqueda funciona perfeitamente.",
    "Vale a pena para quem tem uma rotina corrida.",
    "Funciona muito bem em pisos frios.",
    "Ele tem dificuldade em cantos, mas no geral é ótimo.",
    "Mapeia bem os cômodos e evita bater nos móveis.",
    "A função de agendamento é muito útil.",
    "Supera as expectativas!",
    "Tem um pouco de dificuldade com fios espalhados pelo chão.",
    "Limpeza rápida e eficiente.",
    "Não é tão eficiente em tapetes muito felpudos.",
    "Excelente opção para idosos que não conseguem limpar com frequência.",
    "O app é intuitivo e fácil de configurar.",
    "A função de mop poderia ser mais potente.",
    "Aspira muito bem poeira e pequenos detritos.",
    "Um pouco caro, mas muito útil.",
    "Nunca mais precisei varrer a casa!",
    "Ajuda muito na rotina doméstica.",
    "É ótimo, mas poderia ser mais barato.",
    "Meu gato adora subir nele enquanto ele trabalha!",
    "Um bom investimento para quem tem alergia a pó.",
    "Poderia ter um pouco mais de potência de sucção.",
    "Ele se enrosca em fios, mas depois aprende a evitá-los.",
    "É um ótimo ajudante para a limpeza diária.",
    "Recomendo a todos que querem uma casa sempre limpa sem esforço!"
]

watch_pt = [
    "Design elegante e sofisticado, combina com qualquer roupa.",
    "Muito confortável no pulso, nem parece que estou usando.",
    "A bateria dura bastante, não preciso carregar com frequência.",
    "A precisão do relógio é excelente, nunca atrasa.",
    "O visor é grande e fácil de ler, mesmo sob luz forte.",
    "Os materiais são de alta qualidade, parece bem durável.",
    "Tem muitas funções úteis, como cronômetro e alarme.",
    "Resistente à água, posso usá-lo sem medo de molhar.",
    "A pulseira é ajustável e muito confortável.",
    "A iluminação noturna ajuda muito em ambientes escuros.",
    "O preço é justo pela qualidade oferecida.",
    "O mecanismo automático funciona perfeitamente.",
    "O vidro é resistente a riscos, ótimo para o dia a dia.",
    "O design clássico nunca sai de moda.",
    "Boa relação custo-benefício.",
    "A conectividade com o smartphone é muito prática.",
    "Leve e confortável, ideal para uso diário.",
    "As funções esportivas são muito úteis para quem pratica exercícios.",
    "Adoro a opção de troca de pulseira, fica sempre com um visual novo.",
    "Marca confiável, já tive outros modelos e nunca me decepcionaram.",
    "Ótima resistência, já caiu algumas vezes e continua perfeito.",
    "A caixa do relógio é bem construída e elegante.",
    "O acabamento em aço inoxidável dá um toque premium.",
    "Muito bonito e sofisticado, recebo vários elogios.",
    "A precisão do cronômetro é incrível.",
    "O carregamento sem fio é uma grande vantagem.",
    "Gostei do peso, não é muito leve nem muito pesado.",
    "A pulseira de couro dá um toque de classe.",
    "A resistência à água permite usar na piscina sem problemas.",
    "O ajuste no pulso é perfeito, não fica apertado nem frouxo.",
    "O visor digital tem excelente contraste.",
    "O sistema de notificações no smartwatch é muito útil.",
    "A bateria poderia durar um pouco mais, mas ainda é boa.",
    "A interface do relógio é intuitiva e fácil de navegar.",
    "O vidro safira evita arranhões indesejados.",
    "A durabilidade parece muito boa, já estou usando há meses.",
    "O fecho é seguro e não abre facilmente.",
    "A personalização do mostrador é um diferencial incrível.",
    "Ideal tanto para ocasiões formais quanto casuais.",
    "O sistema de carregamento rápido economiza tempo.",
    "A conectividade Bluetooth funciona sem problemas.",
    "O sensor de batimentos cardíacos é bem preciso.",
    "O GPS embutido é útil para atividades ao ar livre.",
    "A tela touch responde muito bem ao toque.",
    "As notificações de chamadas e mensagens são muito úteis.",
    "A possibilidade de trocar as pulseiras aumenta a versatilidade.",
    "O relógio combina com qualquer ocasião.",
    "A precisão dos sensores é impressionante.",
    "A construção robusta garante longa vida útil.",
    "Excelente compra, recomendo para todos!"
]

# Wykonujemy wyszukiwanie tematów 20 razy, zliczamy tematy znalezione przy każdej pętli i wybieramy te, które
# pojawiają się najczęściej do 10 tematów.
sets = []
for _ in range(20):
    topic_model = BERTopic(language="portuguese")
    tematy, _ = topic_model.fit_transform(watch_pt)

    # Pobranie i wyświetlenie informacji o tematach
    topics = topic_model.get_topic_info()

    all_topic_words = set()

    for section in topics["Representation"]:
        for word in section:
            if word not in all_topic_words:
                all_topic_words.add(word)

    nouns = {word for word in all_topic_words if nlp(word)[0].pos_ == "NOUN"}
    print(nouns)

    sets.append(nouns)

word_counts = Counter(word for s in sets for word in s)
print(word_counts)

final_telephone_topics = {'brilho', 'tela', 'telefone', 'câmera', 'vídeos', 'fotos', 'bateria', 'interface', 'recursos',
                          'impressão'}

final_robot_topics = {'tapetes', 'bateria', 'casa', 'limpeza', 'vida', 'volta', 'investimento', 'útil', 'esforço',
                      'função'}

final_watch_topics = {'precisão', 'relógio', 'notificações', 'cronômetro', 'dia', 'vidro', 'pulseira', 'toque', 'visor',
                      'útil'}

# testowanie oceniania wypowiedzi ze względu na temat

# test_sentence = "O botão quebrou no primeiro uso."
#
# doc = nlp(test_sentence)
#
# sentence_nouns = {token.text for token in doc if token.pos_ == "NOUN"}
# print(sentence_nouns)
#
# noun_similarities = {}
#
# for noun in sentence_nouns:
#     noun_vector = nlp(noun).vector
#     similarities = {word: cosine_similarity(noun_vector, nlp(word).vector) for word in nouns}
#
#     Posortuj podobieństwa malejąco
#     sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
#
# noun_similarities[noun] = sorted_similarities
#
# print(noun_similarities.items())
#
# best_match = []
#
# for noun, similarities in noun_similarities.items():
#     for word, similarity in similarities[:1]:
#         best_match.append(similarity)
#
# if len(best_match) <= 3:
#     score = round(statistics.mean(best_match), 4)
# else:
#     top_3_values = heapq.nlargest(3, best_match)
#     score = round(statistics.mean(top_3_values), 4)
#
# print(score)
