from helpers import *


if __name__=="__main__":
    out = process_errors_statistics()
    for k, v in out.items():
        print k, v
