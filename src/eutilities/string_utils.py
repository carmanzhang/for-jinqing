import json
import re

import jaro
from Levenshtein.StringMatcher import StringMatcher
from nltk.corpus import stopwords
# import these modules
from nltk import PorterStemmer, WordNetLemmatizer, SnowballStemmer, LancasterStemmer


def extract_inner_words(string):
    replaced = re.sub('[^a-z]', " ", string)
    splts = replaced.split(' ')
    return [s for s in splts if len(s) > 2]


def extract_key_wods_list(key_words_str):
    key_words = []
    key_words_dict = json.loads(key_words_str)
    if key_words_dict == None:
        return []
    for item in key_words_dict:
        if 'keyword' in item:
            keyword_ = item['keyword']
            keyword_ = extract_inner_words(keyword_)
            key_words += keyword_
    return key_words


def edit_distinct_diff_chars(str1, str2):
    str_matcher = StringMatcher()
    if len(str1) < len(str2):
        str1, str2 = str2, str1
    str_matcher.set_seqs(str1, str2)
    editops = str_matcher.get_editops()
    # print(editops)
    diff_chars = []
    for model, pos1, pos2 in editops:
        if model == 'delete':
            # print('delete: ', str1[pos1])
            diff_chars.append(str1[pos1])
        elif model == 'replace':
            # print('replace: ', str1[pos1])
            diff_chars.append(str1[pos1])
        elif model == 'insert':
            # print('insert: ', str2[pos2])
            diff_chars.append(str2[pos2])
    return diff_chars


def jaro_winkler_similarity(s1, s2):
    if s1 is None or s2 is None:
        return 0.0
    return jaro.jaro_winkler_metric(s1, s2)


en_stopwords_set = set(stopwords.words('english'))


def intersection(a, b, remove_stop_word=False):
    if a is None or b is None:
        return 0
    if remove_stop_word:
        a = [n for n in a if n not in en_stopwords_set]
        b = [n for n in b if n not in en_stopwords_set]
    intersections = len(set(a).intersection(set(b)))
    return intersections


def jaccard_similarity(a, b, remove_stop_word=False):
    if a is None or b is None:
        return 0.0
    if remove_stop_word:
        a = [n for n in a if n not in en_stopwords_set]
        b = [n for n in b if n not in en_stopwords_set]
    unions = len(set(a).union(set(b)))
    if unions == 0:
        return 0.0
    intersections = len(set(a).intersection(set(b)))
    return 1. * intersections / unions


# ps = WordNetLemmatizer()
ps = SnowballStemmer('english')
# ps = LancasterStemmer()

def stem_phrase(phrase):
    arr = [stem_word(w) for w in phrase.lower().split(' ')]
    return ' '.join(arr)


def stem_word(word):
    return ps.stem(word)


if __name__ == '__main__':
    print(stem_phrase('laboratory result delivery'))
