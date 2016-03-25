#!/usr/bin/env python
# -*- coding: utf8 -*-

from helpers import *
import operator
import sys
import codecs


def initialize():
    errors_statistics = process_errors_statistics()
    words_frequency = process_corpuses()
    return errors_statistics, words_frequency

alphabet = u"aąbcćdęfghijklłmnńoópqrsśtuwxyzżź"

def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes = [a+b[1:] for a, b in splits if b]
    transposes = [a+b[1]+b[0]+b[2:] for a, b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a, b, in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]

    return set(deletes + transposes + replaces + inserts + [word.replace("rz", u'ż'), word.replace(u"ż", u'rz'), word.replace("u", u'ó'), word.replace(u'ó', 'u'), word.replace("ch", u'h'), word.replace('h', 'ch')])

def known(words, dictionary):
    return set(w for w in words if w in dictionary)

def known_edits2(word, dictionary):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in dictionary)

def spellcheck(word, errors_statistics, words_frequency):
    words_to_check = known([word], words_frequency) or known(edits1(word), words_frequency) or \
    known_edits2(word, words_frequency) or known_edits2(edits1(word), words_frequency)
    output = []
    for c in words_to_check:
        output.append((c, errors_statistics[levenshtein_distance(word, c)] * words_frequency[c]))
        # print (c, errors_statistics[levenshtein_distance(word, c)] * words_frequency[c])

    # output_word, probability = max(output, key=operator.itemgetter(1))
    return sorted(output, key=operator.itemgetter(1))[-10:]


if __name__=="__main__":
    errors_statistics, words_frequency = initialize()
    while True:
        word = raw_input(">").decode(sys.stdin.encoding)
        print word, 'correct into:'
        for word, freq in reversed(spellcheck(word, errors_statistics, words_frequency)):
            print '\t%s (%f)' % (word, freq)
