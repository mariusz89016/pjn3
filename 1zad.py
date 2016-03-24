#!/usr/bin/env python
# -*- coding: utf8 -*-

from helpers import *
import matplotlib.pyplot as plt
import numpy as np


if __name__=="__main__":
    out = process_errors_statistics()
    for k, v in out.items():
        print k, v

    # t = np.arange(0.0, 2.0, 0.01)
    # s = np.sin(2*np.pi*t)

    plt.plot(out.keys(), out.values(), "ro")

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.show()
