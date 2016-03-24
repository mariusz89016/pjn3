#!/usr/bin/env python
# -*- coding: utf8 -*-

from helpers import *
import operator


if __name__=="__main__":
    words_frequency = process_corpuses()
    # for word, frequency in words_frequency.items():
        # print word, frequency, type(word)

    sorted_x = sorted(words_frequency.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    for x, y in sorted_x:
        print x, y
        raw_input()
