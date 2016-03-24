#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
from collections import defaultdict
import codecs
import operator
import re
from os.path import join


DIRECTORY = 'lab3_data'
FILES = ['dramat.iso.utf8',
         'popul.iso.utf8',
         'proza.iso.utf8',
         'publ.iso.utf8',
         'wp.iso.utf8']

errors_map = {
    u'u': [{'letter2': u'ó', 'cost': 0.25}],
    u'z': [{'letter2': u'ż', 'before_letter1': u'r', 'not_before_letter2': u'r', 'cost': -0.5 },
            {'letter2': u'ź', 'cost': 0.25},
            {'letter2': u'ż', 'cost': 0.25},
            {'letter2': u'ż', 'before_letter1': u's', 'cost': -0.5}],
    u'h': [{'letter2': u'h', 'before_letter1': u'c', 'not_before_letter2': u'c', 'cost': -0.5 }],
    u'a': [{'letter2': u'ą', 'cost': 0.25}],
    u'c': [{'letter2': u'ć', 'cost': 0.25}],
    u'e': [{'letter2': u'ę', 'cost': 0.25}],
    u'l': [{'letter2': u'ł', 'cost': 0.25}],
    u'n': [{'letter2': u'ń', 'cost': 0.25}],
    u's': [{'letter2': u'ś', 'cost': 0.25}],
    u'ą': [{'letter2': u'm', 'before_letter2': u'o', 'cost': -0.5},
           {'letter2': u'n', 'before_letter2': u'o', 'cost': -0.5}],
    u'ę': [{'letter2': u'n', 'before_letter2': u'e', 'cost': -0.5}]

}

def compare(letter1, letter2, before_letter1, before_letter2):
    if letter1==letter2:
        return 0
    elif letter1==before_letter2 and letter2==before_letter1:
        # schoolboy mistake
        return 0.5
    return min(compare_letter_improved(letter1, letter2, before_letter1, before_letter2), compare_letter_improved(letter2, letter1, before_letter2, before_letter1))

def compare_letter_improved(letter1, letter2, before_letter1, before_letter2, errors_map=errors_map):
    if(letter1==letter2):
        return 0
    elif letter1 not in errors_map:
        return 1
    output = [1]
    for x in errors_map[letter1]:
        map_letter2 = x['letter2']
        map_before_letter1 = x['before_letter1'] if 'before_letter1' in x else ''
        map_before_letter2 = x['before_letter2'] if 'before_letter2' in x else ''
        map_not_before_letter1 = x['not_before_letter1'] if 'not_before_letter1' in x else ''
        map_not_before_letter2 = x['not_before_letter2'] if 'not_before_letter2' in x else ''

        if(letter2==map_letter2 and \
        (map_before_letter1=='' or (map_before_letter1!='' and map_before_letter1==before_letter1)) and \
        (map_before_letter2=='' or (map_before_letter2!='' and map_before_letter2==before_letter2)) and \
        (map_not_before_letter1=='' or (map_not_before_letter1!='' and map_not_before_letter1!=before_letter1)) and \
        (map_not_before_letter2=='' or (map_not_before_letter2!='' and map_not_before_letter2!=before_letter2))):
            output.append(x['cost'])

    return min(output)

def levenshtein_distance(word1, word2, debug=False):
    len1 = len(word1)
    len2 = len(word2)
    d = [[0 for x in range(len1+1)] for y in range(len2+1)]
    for i in range(len1+1):
        d[0][i] = i
    for j in range(len2+1):
        d[j][0] = j

    for i in range(1, len2+1):
        for j in range(1, len1+1):
            before_word2 = word2[i-2] if i-2>=0 else u''
            before_word1 = word1[j-2] if j-2>=0 else u''
            subst = compare(word2[i-1], word1[j-1], before_word2, before_word1)
            d[i][j] = min(d[i][j-1] + 1,
                          d[i-1][j] + 1,
                          d[i-1][j-1] + subst)

    if debug:
        print
        print_debug(word1, word2, d)
    return d[len2][len1]


def process_errors_statistics():
    output = []
    with codecs.open('lab3_data/bledy.txt', 'r', 'utf8') as f:
        for line in f.readlines():
            output.append(line.split(';'))

    # with codecs.open('lab3_data/bledy2.txt', 'r', 'utf8') as f:
        # for line in f.readlines():
            # output.append(line.split(' -'))

    errors = defaultdict(int)

    for err, nerr in output:
        # print beautify_word(err).encode('utf8'), beautify_word(nerr).encode('utf8'), "->", levenshtein_distance(beautify_word(err), beautify_word(nerr)), "vs", levenshtein_distance_simple(beautify_word(err), beautify_word(nerr))
        errors[levenshtein_distance(beautify_word(err), beautify_word(nerr))] += 1
    sum = float(reduce(lambda x,y: x+y, errors.values()))
    for k in errors:
        errors[k]/=sum
    return errors

def beautify_word(word):
    try:
        float(word)
        return word
    except ValueError:
        p = re.compile('(.*?)(\[\d+\])+') #remove reference number 'asd[102]'
        matchObj = p.match(word)
        if matchObj:
            word = matchObj.group(1)
        return word.encode('utf8').translate(None, "(),.:;[]!").lower().strip().decode('utf8')

def process_corpuses():
    output = defaultdict(int)
    for file in FILES:
        with codecs.open(join(DIRECTORY, file), 'r', 'utf8') as f:
            for line in f.readlines():
                if line.startswith('*'):
                    continue
                for word in line.split(' '):
                    bword = beautify_word(word)
                    # if bword==u'w' or bword==u'i' or bword==u'się' or bword==u'na' or bword==u'nie' or bword==u'z':
                    #     continue
                    output[bword] += 1

    print len(output)
    sum_laplace = float(reduce(lambda x,y: x+y, output.values())) + len(output)

    for k in output:
        output[k] = (output[k] + 1) / sum_laplace
    return dict(output)

def levenshtein_distance_simple(word1, word2, debug=False):
    len1 = len(word1)
    len2 = len(word2)
    d = [[0 for x in range(len1+1)] for y in range(len2+1)]
    for i in range(len1+1):
        d[0][i] = i
    for j in range(len2+1):
        d[j][0] = j

    if debug:
        print_debug(word1, word2, d)

    for i in range(1, len2+1):
        for j in range(1, len1+1):
            if word2[i-1] == word1[j-1]:
                subst = 0
            else:
                subst = 1
            d[i][j] = min(d[i][j-1] + 1,
                          d[i-1][j] + 1,
                          d[i-1][j-1] + subst)
    return d[len2][len1]
