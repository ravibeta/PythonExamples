from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import logging
import base64
import json
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
#import httplib2
import os
import uuid
from django.core import serializers
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
#from models import Metric
#from serializers import MetricSerializer
import logging
import datetime
logging.basicConfig()
logger = logging.getLogger(__name__)

user=''
password=''
#http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
#http.add_credentials(user, password)
#auth = base64.encodestring(user + ':' + password)
from gensim.summarization import summarize
def add(request):
    logger.info('add metric='+str(request.POST))
    #logger.info('text='+str(request.data.get('text','')))
    text = request.POST.get('text','')
    #msgType = None
    #msgType = request.META.get('HTTP_x_amz_sns_message_type')
    #if msgType == 'Notification':
    #   #add metric
    #   pass
    #from textselector import test_build_counts, test_find_closest
    #text = get_text()
    #counts = test_build_counts(text)
    #closest = test_find_closest(text, counts)
    #closest = text.splitlines()[0:1]
    #summary = '\n'.join(closest)
    text = text.split('.')
    text = '\n'.join(text)
    try:
       logger.info('text='+repr(text))
       summary = summarize(text)
       if summary:
          pass
       else:
          summary = ''.join(text.splitlines()[0:1])
    except Exception as e:
       summary = str(e)
       if type(e).__name__ == "TypeError":
          summary = ''.join(text.splitlines()[0:1])
    logger.info('summary='+repr(summary))
    return HttpResponse(json.dumps({'status':'success',
              'msg':'added',
              'summary':summary
              }))

import textract
def upload(request):
    name = request.POST.get('name','')
    import urllib.parse
    name = urllib.parse.unquote(name)
    text = [""]
    path = os.path.dirname(os.path.abspath(__file__))+"/"+"../../../../ui/summarizer/public/uploads/"
    try:
       h = ''
       if name:
          print('opening file='+path+name)
          h = textract.process(path+name)
       if h:
          text = [x.strip() for x in h.decode('utf-8').splitlines()]
          text = '\n'.join(text)
          #print(text)
       else:
          with open(path+"/"+name, 'r') as fin:
               text = fin.readlines()
               text = '\n'.join(text)
       summary = ""
       if text:
          #logger.info('text='+repr(text))
          summary = summarize(text)
       if summary:
          print("summarized:"+name)
          pass
       else:
          summary = ''.join(text.splitlines()[0:1])
    except Exception as e:
       summary = str(e)
       if type(e).__name__ == "TypeError":
          summary = ''.join(text.splitlines()[0:1])
    #logger.info('summary='+repr(summary))
    return HttpResponse(json.dumps({'status':'success',
              'msg':'added',
              'summary':summary
              }))




def test(request):
    return HttpResponse('', status=200)
    pass

def word_similarity_graph(words):
            import networkx as nx
            G = nx.Graph() #undirected
            G.add_nodes_from(words)
            for i in range(len(words)):
                for j in range(len(words)):
                    if i == j:
                        continue
                    word_1 = words[i]
                    word_2 = words[j]
                    weight_i_j = word2vec.similarity(word_1, word_2)
                    if weight_i_j < WEIGHT_THRESHOLD:
                       continue
                    G.add_edge(word_1, word_2, weight_i_j)
            return G

def pagerank_summarize(self, text):
        from gensim.models import word2vec
        # load the test sample
        sentences = text.split('\n')
        model = word2vec.Word2Vec(sentences, size=200)
        model.save_word2vec_format('/tmp/vectors.bin', binary=True)
        model = word2vec.Word2Vec.load_word2vec_format('/tmp/vectors.bin', binary=True)
        G = self.word_similarity_graph(model)
        pr = nx.pagerank(G,tol=1e-10)
        #get selection from text based on pagerank of words
        import operator
        sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
        important = [int(i[0]) for i in sorted_x][:10]
        scored_sentences = {}
        for sentence in sentences:
              matches = set(sentence.split()).intersection(important)
              score = 0
              for match in matches:
                  score+= pr[match]
              scored_sentences[sentence]=score
        reordered_sentences = [ i[0] for i in sorted(scored_sentences.items(), key=operator.itemgetter(1), reverse=True)[:10] ]
        ordered_sentences = [ x for x in sentences if x in reordered_sentences ]
        summary = '\n'.join(ordered_sentences)
        #print(summary)
        return summary
