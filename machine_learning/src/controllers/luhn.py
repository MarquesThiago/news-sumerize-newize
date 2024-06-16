import nltk
from common import normalize_text


def check_index(phrase, word):
    '''
    check index in phrase and return or index of words in a list
    :param list phrase:
    :param str  word
    return: int phrase.index(word)| None
    '''

    try:
        return phrase.index(word)
    except Exception as err:
        err
        pass


def sepeared_words_sent(sentences):

    '''
    separeds in list of words on list of sentences and
    return list of words in sentences per sentences
    :param sentences: list
    return list [nltk.word_tokenize(sentence.lower()) for sentence in
    sentences ];'''

    return [nltk.word_tokenize(sentence.lower())
            for sentence in sentences]


def define_index(sentences, import_words):

    '''
    Check in list if exists important words and
    return list of index per sentences
    :param sentences: list
    :param import_words: list
    :return list index:
    '''
    index = []

    sentences_sep_words = sepeared_words_sent(sentences)
    for sentence in sentences_sep_words:
        check = [check_index(sentence, word) for word in import_words]
        index_ = [index for index in check if index is not None]
        index.append(sorted(index_))

    return index


def define_group(index, distance):

    '''
    create subgroups in the matrix of indexes, considering the
    distance between index.
    :param index : list -> matrix of the index
    :param distance: int -> parameter distance between index
    :return list listed:
    '''

    listed = []

    for group in index:
        if len(group) == 0:
            listed.append([])
            continue

        list_group = []
        sub_group = [group[0]]
        num = 1

        while num < len(group):
            if group[num] - group[num-1] < distance:
                sub_group.append(group[num])

            else:
                list_group.append(sub_group[:])
                sub_group = [group[num]]
            num += 1

        list_group.append(sub_group)
        listed.append(list_group)

    return listed


def calc(listed):

    '''
    applied calculation grade for matrix of the index and return a
    list of the grades
    :param listed:list matrix with subgroup of the index
    :return list grades:
    '''

    grades = []

    for index in range(0, len(listed)):
        if len(listed[index]) == 0:
            grades.append((index, 0))
            continue

        minimum = 0
        for n_group in listed[index]:

            import_word = len(n_group)
            total_words = n_group[-1] - n_group[0] + 1
            grade = 1.0 * import_word**2 / total_words

            if minimum < grade:
                minimum = grade

        grades.append((index, minimum))
    return grades


def calc_note(sentences, import_words, distance):

    '''
    calculate grade per sentences, from the algorithm of the lunh
    :param sentences list
    :param import_words: list -> important words in text
    :param distance: int -> distance to created groups used in
    calculate of grade
    :return calc(currency) list '''

    index = define_index(sentences, import_words)
    currency = define_group(index, distance)
    return calc(currency)


def variables(text, rank, lemma=False):

    '''
    create variables for use in calculate of the lunh, starting by text and
    number of ranking
    created variables in function
    tokens: separed text in sentences, sentence_clear: applied cleaning in
    sentences (remove break line,stop words and others),
    all_words list of the all words in text (aren't stop words) and rank:  n
    words, most used in text
    :param text: str
    :param rank: int -> number to return of words most commons in text
    :return dict {"tokens": tokens, "sentence_clear": clear_sentence,
    "all_words": words, "rank": rank_words}'''

    tokens = nltk.sent_tokenize(text.lower(), language="Portuguese")
    clear_sentence = [" ".join(normalize_text(sentence, lemma))
                      for sentence in tokens]
    words = nltk.word_tokenize(" ".join(clear_sentence), language="Portuguese")
    frequency = nltk.FreqDist(words)
    rank_words = [target[0] for target in frequency.most_common(rank)]

    return {"tokens": tokens, "sentence_clear": clear_sentence,
            "all_words": words, "rank": rank_words}


def sumarize(tokens, notes, limit, order=False):

    '''
    applied notes to the sentences and return more high notes
    :param tokens: list -> list of the sentences
    :param notes: list -> list of the grede per sentences
    :param limit: number -> limit of the sentences returned
    :param order: bool -> important order of the text
    :return str text:
    '''
    rankeament = sorted(notes, key=lambda x: x[1], reverse=True)

    if order:
        rankeament = sorted(rankeament[:limit],
                            key=lambda x: x[0],
                            reverse=False)

    text = [tokens[target[0]] for target in rankeament[:limit]]
    return text


def sumarize_by_luhn(text, n=5, distance=3, order=False, lemma=False):

    var = variables(text, n, lemma)
    note = calc_note(var["sentence_clear"], var["rank"], distance)
    return "".join(sumarize(var["tokens"], note, n, order))
