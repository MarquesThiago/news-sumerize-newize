import nltk
from common.common import (
    simple_clear,
    weight_sentence,
    normalize_text,
    start_download_language,
    frequency
)


start_download_language()


def resume(sentence, list_):

    '''
    resume a text starting of the dictionary with grades and index of the
    sentences
    :param sentence: dict -> sentences and weight
    :param list_weight:list -> list of the index of the sent
    :return string  " ".join(sent):

    '''
    sent = [sentence[index] for index in list_]
    return " ".join(sent)


def sumarize_per_frequency(text, n=10, order=False, lemma=False):

    harmonized_words = normalize_text(text, lemma)
    harmonized_text = " ".join(harmonized_words)

    frequency_word = frequency(harmonized_words, harmonized_text)
    max_frequency = max(frequency_word.values())

    weight = {
        word: note/max_frequency 
        for word, note in frequency_word.items()
    }

    sentence_text = nltk.sent_tokenize(
        simple_clear(text), language="Portuguese")

    weight_sent = [[index, weight_sentence(sentence_text[index], weight)]
                   for index in range(len(sentence_text))]
    ordinate = sorted(weight_sent, key=lambda x: x[1], reverse=True)

    ordinate_rank = [index[0] for index in ordinate]
    if order:
        ordinate_rank = sorted(ordinate_rank[:n])

    return resume(sentence_text, ordinate_rank[:n])
