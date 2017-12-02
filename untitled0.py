#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:48:39 2017

@author: enyaning
"""

from textblob import TextBlob

text = '''
For all my Chinese food cravings, I come here, an almost hidden and easy-to-miss joint in a typical strip mall by Colorado Boulevard in Eagle Rock. 
In general, the flavors of the food move me as they are well-balanced in spice and texture, leaving my palate satiated at first, then wanting more. 
My favorites are: Kung Pao Chicken, Sechzuan pork or beef, and the Veggie medley, eaten with pints of aromatic, soft white rice. 
One can dine in, pick-up, or use delivery (they take cards). 
Service is friendly, fast, and convenient. 
Not only will I come back, I also highly recommend it!
'''

blob = TextBlob(text)
blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                    #  ('threat', 'NN'), ('of', 'IN'), ...]

blob.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])

print(blob.noun_phrases)

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)
    print(sentence.noun_phrases)
# 0.060
# -0.341

blob.translate(to="es")  # 'La amenaza titular de The Blob...'