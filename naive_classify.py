# -*- coding: utf-8 -*-
import os
import sys
import socket
import json
import pickle
import nltk

def word_feats(words):
    return dict([(word, True) for word in words])

def load_classifier(path):
   f = open(path, 'rb')
   classifier = pickle.load(f)
   f.close()
   return classifier

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

print 'Loading classifier...'
classifier = load_classifier('Naive.pickle')

print 'Start classifier service...'
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    try:
        data = json.loads(c.recv(4096))
        print '    got {0} tokens'.format(len(data))
    except:
        c.send(json.dumps({'pos':-1,'neg':-1}))
        c.close()
        continue
    result = classifier.prob_classify(word_feats(data))
    pos = result.prob('pos')
    neg = result.prob('neg')
    c.send(json.dumps({'pos':pos,'neg':neg}))
    c.close()

s.close()
