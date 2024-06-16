import re
import string
import nltk
import spacy
from typing import List

from store.extra_files import read_column_csv


def start_download_language(language: str = "punkt") -> None:

    """
    Make downloaf to languague, defire to using in processement of the
    natural language

    Args:
        language: set language from make download
    """

    nltk.download(language)


def get_list_stop_words() -> List[str]:
    data = read_column_csv(
        ".\\..\\Assets\\stop_words.csv", ["words"]
    )

    return data["words"]


STOP_WORDS = get_list_stop_words()


def simple_clear(text):

    '''
    simples clear, delete space and break lines
    :param text: str text
    return: str re.sub(r'\\s+'," ", text.lower())
    '''

    return re.sub(r'\s+', " ", text.lower())


def normalize_text(text, lemma=False):

    '''
    harmonization of text,sepaled text in words,
    remove space, simbol and stop word (words not contribuinls to meaning)
    :param text: str text
    return: list text_harmonization: list fo words harmonized
    '''

    if lemma:
        pln = spacy.load("pt_core_news_sm")
        tokens = [token.lemma_ for token in pln(text)
                  if str(token) not in STOP_WORDS
                  and str(token) not in string.punctuation
                  and not str(token).isdigit()]
    else:
        tokens = nltk.word_tokenize(text.lower(), language="Portuguese")

    text_harmonization = [word for word in tokens
                          if word not in STOP_WORDS and word
                          not in string.punctuation and not word.isdigit()]
    return text_harmonization


def frequency_in_text(word, text):

    '''
    search word in text and return number of times it appears in the text
    :param word: string -> word search in text
    :param text: string -> text
    :return int len(re.findall(word, text)):
    '''
    try:
        return len(re.findall(word, text))
    except Exception as err:
        err
        return 1


def frequency(list_words, text):

    '''
    search list if the words in text and return dictionary of word and
    frequency on the text
    :param list_word: string -> list of the words search in text
    :param text: string -> text
    :return dict { word : frequency_in_text(word, text) for word in
    list_words}):
    '''

    return {word: frequency_in_text(word, text) for word in list_words}


def weight_sentence(sentence, weights):

    '''
    calculate a sumarize of the grades per words in sentence and return a value
    :param sentence: str
    :param weights: dict -> dictionary of the words with weights
    :return float sum([weights[word] for word in tokens if word in weights.
    keys()])?
    '''

    tokens = nltk.word_tokenize(sentence, language="Portuguese")
    return sum([weights[word] for word in tokens if word in weights.keys()])
