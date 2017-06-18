#! /usr/bin/python
#
# the following finds the lines with the
# most densely packed words from the given set
#

def build_counts(text):
    h = {}
    for word in text.split():
         w = word.strip().lower()
         if w:
            if w in h:
               h[w] += 1
            else:
               h[w] = 1
    return h

def find_closest(text, chosen_words, counts):
    lines = text.split('\n')
    scores = {}
    for i,line in enumerate(lines):
        bare_line = line.strip()
        matches = [x.lower() for x in bare_line.split(' ') if x.lower() in chosen_words]
        match_count = len(matches)
        scores[i] = match_count
    print(repr(scores))
    import operator
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    print('sorted_scores='+repr(sorted_scores))
    candidates = [lines[x[0]] for x in sorted_scores[0:3]]
    return candidates


def get_text():
    with open('filename', 'r') as fin:
         text = fin.readlines()
    text = '\n'.join(text)
    return text

def test_build_counts(text):
    counts = build_counts(text)
    #print(repr(counts))
    return counts


def test_find_closest(text, counts):
    import operator
    sorted_counts = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
    print(repr(sorted_counts))
    chosen_words = [x[0] for x in sorted_counts[0:3]]
    print(repr(chosen_words))
    closest = find_closest(text, chosen_words, counts)
    print(repr(closest))

text = get_text()
counts = test_build_counts(text)
closest = test_find_closest(text, counts)
