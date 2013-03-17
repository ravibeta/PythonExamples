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

def summarize(text):
    lines = text.split('.')
    clean_lines = [line.strip() for line in lines if line.strip()]
    newtext =  '\n'.join(clean_lines)
    tdm = textmining.TermDocumentMatrix()
    tdm.add_doc(newtext)
    for index,row in enumerate(tdm.rows(cutoff=1)):
        if index == 0 : words = row
        if index == 1 : count = row
    text = open('stopwords.txt').read()
    stopwords = textmining.simple_tokenize(text)
    freq = [(w, count[index]) for index, w in enumerate(words) if w not in stopwords]
    freq.sort(reverse=True)
    most_freq_words = freq[:10]
    summary = []
    h = histogram(lines, most_freq_words)
    rowcount = threshold(h)
    summary = [(index, line) for index, line in enumerate(lines) if index < rowcount]
    summary.sort()
    ret = [line[1] for line in summary]
    print '.'.join(ret)
    return ret

def histogram(lines, most_freq_words):    
    histogram = []
    for index, line in enumerate(lines):
        count = 0
        for w in most_freq_words:
            if line.find(w[0]) != -1:
                count += 1
        histogram.append((count,index))
    histogram.sort(reverse=True)
    return histogram

def threshold(histogram):
    total = 0
    for count in histogram:
        total += count[0]
    sum = 0
    threshold = 0
    for count in histogram:
      if (sum < total /2 ):
        sum += count[0]
        threshold += 1
    return threshold


summarize('Clustering and Segmentation. Clustering is a data mining technique that is directed towards the goals of identification and classification. Clustering tries to identify a finite set of categories or clusters to which each data object (tuple) can be mapped. The categories may be disjoint or overlapping and may sometimes be organized into trees. For example, one might form categories of customers into the form of a tree and then map each customer to one or more of the categories. A closely related problem is that of estimating multivariate probability density functions of all variables that could be attributes in a relation or from different relations.')
