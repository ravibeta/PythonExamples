import textmining
import os

def bigrams(text):
    # bigrams
    bigrams = textmining.bigram_collocations(words)
    for bigram in bigrams[:10]:
        print ' '.join(bigram)


