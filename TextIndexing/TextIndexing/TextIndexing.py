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
# prepare text
    lines = text.split('.')
    clean_lines = [line.strip() for line in lines if line.strip()]
    newtext =  '\n'.join(clean_lines)
    tdm = textmining.TermDocumentMatrix()
    tdm.add_doc(newtext)
    for index,row in enumerate(tdm.rows(cutoff=1)):
        if index == 0 : words = row
        if index == 1 : count = row
    # filter stop words 
    text = open('stopwords.txt').read()
    stopwords = textmining.simple_tokenize(text)
    freq = [(w, count[index]) for index, w in enumerate(words) if w not in stopwords]
    freq.sort(reverse=True)
    # Concordance
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


def bayesClassify(text, category, trainer):
    words = textmining.simple_tokenize(text)
    wps = calcWordsProbability(words, category, trainer)
    return normalizeSignificance(calculateOverallProbability(wps))

def calcWordsProbability(words, category, trainer):
    wps = open('wordprobability.txt').read()
    return [getWordProbability(wps, w, category) for w in words if isClassifiable(w)]

def isClassifiable(word):
    text = open('stopwords.txt').read()
    stopwords = textmining.simple_tokenize(text)
    return w not in stopwords

def getWordProbability(wps, word, category):
    if (category):
        table = open('wordcategory.txt').read()
        matchingCount = 0
        nonmatchingCount = 0
        if word in table:
            return (table[word][probability], table[word][matchingCount], table[word][nonmatchingCount])
        else:
            table.append(word, category, 0.99, matchingCount, nonmatchingCount)
            open('wordcategory.txt').write(str((table[word][probability], table[word][matchingCount], table[word][nonmatchingCount])));
    else:
        if word in wps:
            return wps[word]
        else:
            return 0.99

def calculateOverallProbability(wps):
    # we calculate xy/(xy + z) where z = (1 - x)(1 - y)
    z = 0
    xy = 0
    for index,wp in enumerable(wps):
        if z == 0:
            z = 1-wp[1]
        else:
            z = z * (1-wp[1])
        if (xy == 0):
            xy = wp[1]
        else:
            xy = xy * wp[1]
    if (xy + z) != 0:
        return xy / (xy + z)
    else:
        return 0
   
def normalizeSignificance(p):
    if (0.99 < p):
        return 0.99
    if (0.01 > p):
        return 0.01
    return p

# Bayes ported from Ryan Whitaker

def teachMatch(category, words, wds):
    for word in words:
        if isClassifiable(word):
            addMatch(wds, category, word.tolower()) 

def teachNonMatch(category, words, wds):
    for word in words:
        if isClassifiable(word):
            addNonMatch(wds, category, word.tolower()) 

def addMatch(wds, category, word):
   return updateWordProbabilty(category, word, true)

def addMatch(wds, category, word):
   return updateWordProbabilty(category, word, false)

def updateWordProbabilty(category, word, isMatch):
    table = open('wordcategory.txt').read()
    if word in table:
        if (isMatch):
            table[word][matchCount] += 1
        else:
            table[word][nonmatchCount] += 1
    else:
        table.append(word, category, matchCount, nonMatchCount)

import stemmer
import operator
import nltk
def indexText(text):
    # prepare text
    lines = text.split('.')
    clean_lines = [line.strip() for line in lines if line.strip()]
    newtext =  '\n'.join(clean_lines)
    words = textmining.simple_tokenize(newtext)
    p = stemmer.PorterStemmer()
    # filter stop words 
    text = open('stopwords.txt').read()
    stopwords = textmining.simple_tokenize(text)
    # use stemming
    stemmed = []
    freq = {}
    occur = {}
    for index, w in enumerate(words):
        stem = p.stem(w, 0, len(w)-1)
        stemmed.append(stem)
        if stem not in stopwords:
            freq[stem] = stemmed.count(stem)
            occur[stem] = w
    sorted_freq = sorted(freq.iteritems(), key=operator.itemgetter(1), reverse=True)
    # Concordance
    most_freq_words = sorted_freq[:1]
    print "------Index-----"
    print occur[most_freq_words.pop()[0]]
    print "----------------"

sampleText = 'Clustering and Segmentation. Clustering is a data mining technique that is directed towards the goals of identification and classification. Clustering tries to identify a finite set of categories or clusters to which each data object (tuple) can be mapped. The categories may be disjoint or overlapping and may sometimes be organized into trees. For example, one might form categories of customers into the form of a tree and then map each customer to one or more of the categories. A closely related problem is that of estimating multivariate probability density functions of all variables that could be attributes in a relation or from different relations.'
#indexText(sampleText)

#from nltk.corpus import brown
# suffix_fdist = nltk.FreqDist()
# common_suffixes = suffix_fdist.keys()[:100]
 
# use pos to cleanup initial list 
# def pos_features(word):
#          features = {}
#               for suffix in common_suffixes:
#                            features['endswith(%s)' % suffix] = word.lower().endswith(suffix)
#                            
#                            tagged_words = brown.tagged_words(categories='news')
#                            featuresets = [(pos_features(n), g) for (n,g) in tagged_words]
#                            size = int(len(featuresets) * 0.1)
#                            train_set, test_set = featuresets[size:], featuresets[:size]
#                            classifier = nltk.DecisionTreeClassifier.train(train_set)
#                            classifier.classify(pos_features('cats'))
#                            'NNS'
#

# 

#import nltk
#import nltk.corpus
#from nltk.corpus import *
#cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
#most_freq_words = fd.keys()[:100]

class cluster:
    def __init__(self, seed, words):
        self.seed = seed
        self.words = words
    def merge(self, cluster):
       self.seed += "-" + cluster.seed
       self.words += cluster.words
    def seed(self):
        return seed
    def words(self):
        return words

# list of k clusters V

import nltk
import nltk.text
import nltk.corpus

def getTopic(text):
    index = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.brown.words( )])
    # filter stop words 
    stop = open('stopwords.txt').read()
    clusters = [cluster(seed, index.similar_words(seed)) for seed in nltk.word_tokenize(text) if seed not in stop]
    print clusters
    from collections import deque
    queue = deque(clusters)
    matches = []
    newclusters = []
    previousCount = len(clusters) + 1
    while (len(clusters) > 0 and len(clusters) < previousCount):
        for i, c in enumerate(clusters):
            for j, d in enumerate(clusters):
                if ( i != j & c.seed in d.word):
                    merged = false
                    for n in newclusters:
                        if (c.seed in n.seed):
                            n.merge(c)
                            merged = true
                            break;
                        if (d.seed in n.seed):
                            n.merge(d)
                            merged = true
                            break;
                    if not merged:
                        newclusters.append(c.merge(d))
                    matches.append(c)
                    matches.append(d)
        previousCount = len(clusters)
        r = set(matches)
        while(len(r) > 0):
            for c in r:
                clusters.remove(r)
    if (len(newclusters) > 0):
        return newclusters[0].seed
    if (len(clusters) > 0):
        return clusters[0].seed
# getTopic(sampleText)