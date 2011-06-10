#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
The main module for processing urls.
"""


__author__ = 'Gennadiy Zlobin'
__email__ = 'gennad.zlobin@gmail.com'
__version__ = '0.0.1'
__status__ = 'Development'


def increment(url='zz'):
    url = str(url).lower()
    last_char = url[-1]
    if last_char == 'z':
        if len(url) == 1:
            return 'a' + url[0:-1] + 'a'
        else:
            return increment(url[0:-1]) + 'a'
    else:
        if len(url) == 1:
            to_ord = ord(last_char)
            to_ord += 1
            return url[0:-1] + chr(to_ord)
        else:
            to_ord = ord(last_char)
            to_ord += 1
            return url[0:-1] + chr(to_ord)

if __name__ == "__main__":
    a = increment()
    print a
