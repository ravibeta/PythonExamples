import textmining
import os

def bigrams(text):
    # bigrams
    bigrams = textmining.bigram_collocations(words)
    for bigram in bigrams[:10]:
        print ' '.join(bigram)


def tdm_example(text):
    tdm = textmining.TermDocumentMatrix()
    # Create some very short sample 
    tdm.add_doc(text)
    for row in tdm.rows(cutoff=1):
        print row
