#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


class FileWordCount:

    def __init__(self, filename):
        try:
            self._file = open(filename, 'r')
            self.total_lines = 0
        except FileNotFoundError:
            print("FileNotFoundError: File not exist or not found, exiting.")
            exit(1)

    def __iter__(self):
        return self

    def __next__(self):
        line = self._file.readline()
        if not len(line):
            raise StopIteration()

        self.total_lines += 1
        return len(line.split(' '))


if __name__ == '__main__':
    assert sys.argv[1]
    word_counter = FileWordCount(sys.argv[1])
    words_num = 0
    for words in word_counter:
        words_num += words

    print("Number of words and total lines from file \"%s\" is: (%i,%i)"
          % (sys.argv[1], words_num, word_counter.total_lines))
