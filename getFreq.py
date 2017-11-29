#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:39:07 2017

@author: enyaning
"""


import pandas as pd
import re
from nltk.corpus import stopwords

import nltk
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize
from nltk import load


data = pd.read_csv('chinese.csv')

wordcount = {}
stop_words =  set(stopwords.words('english'))
costumer_stop_words = ['chinese', 'italian', 'good', 'great', 'food', 'place']
for word in costumer_stop_words: stop_words.add(word)
costumer_not_stop_words = []
for word in costumer_not_stop_words: stop_words.discard(word)

#make a new tagger
_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = load(_POS_TAGGER)

n = 2

none_words = {}

review_number = 0
for review in data.get('review_text'):
    ss = re.sub("[^A-Za-z]", " ", str(review))
    words=ss.lower().strip().split()
    newwords = []
    for word in words:
        if word not in stop_words:
            newwords.append(word)
    words = newwords
    for i in range(n - 1, len(words)):
        key = ' '.join(words[i - n + 1:i + 1])
        wordcount[key] = wordcount.get(key, 0) + 1

    #tokenize the sentence
#    review = 'It rains outside. Everyone went inside when the rain began to fall.'
    terms = nltk.word_tokenize(review.lower())
    tagged_terms=tagger.tag(terms)
#    print(tagged_terms)
    
    for tg in ngrams(tagged_terms,2):
        if tg[0][1].startswith('NN') and tg[1][1].startswith('NN'):
            key = tg[0][0] + " " + tg[1][0]
            none_words[key] = none_words.get(key, 0) + 1            
    
    for word in tagged_terms:
        if word[1].startswith('NN'):
            key = word[0]
#            none_words[key] = none_words.get(key, 0) + 1
    
    if review_number%20 == 0:
        print(review_number)
    if review_number >= 1000:
        break
    review_number += 1

import operator

sorted_x = sorted(wordcount.items(), key=operator.itemgetter(1))
print(sorted_x[-100:])

sorted_y = sorted(none_words.items(), key=operator.itemgetter(1))
print(sorted_y[-100:])
