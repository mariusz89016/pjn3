#!/usr/bin/env python
# -*- coding: utf8 -*-

from helpers import *
import operator
import sys


def initialize():
    errors_statistics = process_errors_statistics()
    words_frequency = process_corpuses()
    return errors_statistics, words_frequency

def spellcheck(word, errors_statistics, words_frequency):
    output = []
    for c in words_frequency:
        output.append((c, errors_statistics[levenshtein_distance(word, c)] * words_frequency[c]))

    return max(output, key=operator.itemgetter(1))


if __name__=="__main__":
    errors_statistics, words_frequency = initialize()
    while True:
        word = raw_input(">").decode(sys.stdin.encoding)
        print spellcheck(word, errors_statistics, words_frequency)
