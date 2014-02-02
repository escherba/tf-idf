#!/usr/bin/env python
# encoding: utf-8
#
# tf-idf for paragraphs of text
# by Eugene Scherba
#
# The MIT License
#
# Copyright (c) 2009 Tim Trueman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# http://www.opensource.org/licenses/mit-license.php

import re
import math
import fileinput
from collections import Counter
from operator import itemgetter


def sort_by_val(d, **kwargs):
    return sorted(d.iteritems(), key=itemgetter(1), **kwargs)


class TF_IDF:
    def __init__(self, first_n):
        self.first_n = first_n
        self.original_docs = []
        self.doc_word_sets = []
        self.frequencies = []
        self.doc_lengths = []
        self.word_idfs = dict()
        self.tokenizer = Tokenizer()

    def add_doc(self, doc):
        self.original_docs.append(doc)
        tokens = self.tokenizer.tokenize(doc)
        self.doc_lengths.append(len(tokens))
        self.frequencies.append(Counter(tokens))
        self.doc_word_sets.append(set(tokens))

    def show_summary(self):
        for i, doc in enumerate(self.original_docs):
            doc_len = self.doc_lengths[i]
            tf_idf = dict()
            for word, freq in self.frequencies[i].iteritems():
                tf = float(freq) / float(doc_len)
                if word in self.word_idfs:
                    idf = self.word_idfs[word]
                else:
                    sets = self.doc_word_sets
                    idf = math.log(float(len(sets)) /
                                   float(sum(1 for s in sets if word in s)))
                    self.word_idfs[word] = idf
                tf_idf[word] = tf * idf
            show_items = sort_by_val(tf_idf, reverse=True)[:self.first_n]
            print doc
            print '{' + ', '.join("{:s}:{:.3f}".format(*item) for item in show_items) + '}'
            print


class Tokenizer:
    def __init__(self):
        self.r = re.compile(ur'(?u)[\w\']+', re.UNICODE)

    def tokenize(self, doc):
        """
        :rtype: list
        """
        return self.r.findall(doc.lower())


def main():
    tfidf = TF_IDF(5)
    paragraph = []
    for line in fileinput.input():
        if line.isspace():
            if len(paragraph) > 0:
                tfidf.add_doc("\n".join(paragraph))
                paragraph = []
        else:
            paragraph.append(line.rstrip())

    tfidf.show_summary()


if __name__ == '__main__':
    main()
