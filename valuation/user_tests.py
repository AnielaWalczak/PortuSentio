from valuation import valuate_opinion_testing
import pytest
import spacy
import pandas as pd
import math


@pytest.fixture(scope="module")
def nlp():
    return spacy.load("pt_core_news_lg")


@pytest.fixture(scope="module")
def error():
    error_value = 0.5
    return error_value


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


@pytest.fixture(scope="module")
def get_opinions():
    with open("opinions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    return lines


@pytest.fixture(scope="module")
def get_data():
    df = pd.read_excel('data.xlsx')
    return df


def get_results(predicted_value, expected_value):
    if predicted_value != int(predicted_value):
        predicted_value = [math.floor(predicted_value), predicted_value, math.ceil(predicted_value)]
    else:
        predicted_value = [predicted_value - 0.5, predicted_value, predicted_value + 0.5]

    print(predicted_value)

    if expected_value != int(expected_value):
        expected_value = [math.floor(expected_value), expected_value, math.ceil(expected_value)]
    else:
        expected_value = [expected_value - 0.5, expected_value, expected_value + 0.5]

    print(expected_value)

    return predicted_value, expected_value


def test_comment_1(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[0], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[0]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_2(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[1], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[1]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_3(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[2], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[2]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_4(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[3], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[3]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_5(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[4], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[4]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_6(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[5], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[5]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_7(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[6], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[6]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_8(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[7], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[7]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_9(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[8], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[8]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_10(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[9], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[9]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_11(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[10], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[10]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_12(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[11], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[11]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_13(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[12], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[12]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_14(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[13], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[13]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_15(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[14], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[14]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_16(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[15], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[15]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_17(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[16], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[16]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_18(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[17], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[17]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_19(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[18], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[18]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_20(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[19], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[19]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_21(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[20], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[20]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_22(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[21], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[21]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_23(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[22], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[22]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_24(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[23], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[23]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_25(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[24], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[24]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_26(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[25], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[25]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_27(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[26], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[26]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_28(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[27], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[27]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_29(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[28], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[28]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_30(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[29], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[29]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_31(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[30], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[30]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_32(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[31], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[31]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_33(nlp, nouns_telephone, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[32], nlp, nouns_telephone)
    expected_value = get_data["score"].iloc[32]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_34(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[33], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[33]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_35(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[34], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[34]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_36(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[35], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[35]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_37(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[36], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[36]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_38(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[37], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[37]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_39(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[38], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[38]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_40(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[39], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[39]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_41(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[40], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[40]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_42(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[41], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[41]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_43(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[42], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[42]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_44(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[43], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[43]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_45(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[44], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[44]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_46(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[45], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[45]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_47(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[46], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[46]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_48(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[47], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[47]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_49(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[48], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[48]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_50(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[49], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[49]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_51(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[50], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[50]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_52(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[51], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[51]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_53(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[52], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[52]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_54(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[53], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[53]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_55(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[54], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[54]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_56(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[55], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[55]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_57(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[56], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[56]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_58(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[57], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[57]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_59(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[58], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[58]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_60(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[59], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[59]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_61(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[60], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[60]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_62(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[61], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[61]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_63(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[62], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[62]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_64(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[63], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[63]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_65(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[64], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[64]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_66(nlp, nouns_robo, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[65], nlp, nouns_robo)
    expected_value = get_data["score"].iloc[65]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_67(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[66], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[66]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_68(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[67], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[67]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_69(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[68], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[68]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_70(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[69], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[69]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_71(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[70], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[70]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_72(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[71], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[71]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_73(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[72], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[72]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_74(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[73], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[73]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_75(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[74], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[74]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_76(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[75], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[75]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_77(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[76], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[76]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_78(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[77], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[77]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_79(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[78], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[78]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_80(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[79], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[79]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_81(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[80], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[80]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_82(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[81], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[81]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_83(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[82], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[82]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_84(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[83], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[83]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_85(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[84], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[84]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_86(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[85], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[85]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_87(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[86], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[86]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_88(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[87], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[87]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_89(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[88], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[88]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_90(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[89], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[89]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_91(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[90], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[90]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_92(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[91], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[91]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_93(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[92], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[92]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_94(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[93], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[93]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_95(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[94], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[94]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_96(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[95], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[95]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_97(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[96], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[96]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_98(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[97], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[97]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_99(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[98], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[98]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))


def test_comment_100(nlp, nouns_assistir, get_opinions, get_data):
    predicted_value = valuate_opinion_testing(get_opinions[99], nlp, nouns_assistir)
    expected_value = get_data["score"].iloc[99]
    predicted_values, expected_values = get_results(predicted_value, expected_value)

    assert bool(set(predicted_values) & set(expected_values))
