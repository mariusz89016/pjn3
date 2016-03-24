#!/usr/bin/env python
# -*- coding: utf8 -*-

from helpers import *


if __name__=="__main__":
    words_frequency = process_corpuses()
    for word, frequency in words_frequency.items():
        print word, frequency
    print words_frequency['w']
    print words_frequency['z']
    print words_frequency['i']
    print words_frequency[u'piłka']
