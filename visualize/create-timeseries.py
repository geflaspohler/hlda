'''
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import re

# Open files
VOCAB_SIZE = 1000
NUM_DOCS = 1000
filepath = '/home/genevieve/mit-whoi/hlda/inference-panama-0302-images/run010'
savepath = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images'

if __name__ == "__main__":
    # Read in corpus
    NUM_TOPICS = 0;
    doc = [None] * NUM_DOCS
    f = open(os.path.join(filepath, 'mode.words'))
    for line in f:
        vals = re.split(r' +', line.rstrip('\n'))
        cur_doc = int(vals[0])
        word_list = [int(x) for x in vals[1:]]
        highest_topic = max(word_list)
        if highest_topic > NUM_TOPICS:
            NUM_TOPICS = highest_topic
        
        c = Counter(word_list)
        doc[cur_doc] = c

    f.close()

    print "number of topics:", NUM_TOPICS
    f = open(os.path.join(savepath, 'run010-topics.hist.csv'), 'w+')
    for time, counter in enumerate(doc):
        if counter == None:
            print 'ERROR at', time
            f.write(str(time) + ',')
            f.write(str(1))
            f.write(',')
            for i in xrange(1, NUM_TOPICS):
                f.write(str(0))
                if i != NUM_TOPICS - 1:
                    f.write(',')
            f.write('\n')
            continue;

        f.write(str(time) + ',')
        for i in xrange(NUM_TOPICS):
            if i in counter:
                f.write(str(counter[i]))
            else:
                f.write(str(0))

            if i != NUM_TOPICS - 1:
                f.write(',')
        f.write('\n')
