import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import csv

# Open files
VOCAB_SIZE = 1000
NUM_LEVELS = 3

datapath = '/home/genevieve/mit-whoi/hlda/documents-panama-0302-images'
savepath = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images'

def get_key(filename):
    return int(filename[3:-4])

doc_files = [f for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath, f))];
doc_files.sort(key = get_key)

# For each image
scales = [];
word_ids = [];
doc_lengths = []

for fdoc in doc_files:
    print "File:", fdoc 
    with open(os.path.join(datapath, fdoc), 'rb') as csvfile:
        reader = csv.reader(csvfile)
        doc = []
        for row in reader:
            id = row[1]
            s = row[2]
            if s == 'empty':
                break;
            doc.append(float(s))
            word_ids.append(int(id))

        doc_lengths.append(len(doc))
        scales = scales + doc;

scales = np.float32(scales)
                               
# Preform k-means
flags = cv2.KMEANS_RANDOM_CENTERS
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
NUM_RESTARTS = 10
compactness, labels, centers = cv2.kmeans(scales, NUM_LEVELS, criteria, NUM_RESTARTS, flags)
print 'Kmeans finished with compactness:', compactness

# Ensure that the labels are in order of size
center_fixed = [x[0] for x in centers];
print "centers", center_fixed 
order = list(np.argsort(center_fixed))
print order

# Write results to file: <index> <cluster id> <keypoint size>
fwrite = open(os.path.join(savepath, 'levels' + str(VOCAB_SIZE) + '.dat'), 'w+')
word_index = 0;
for index, doc_len in enumerate(doc_lengths):
    print "Writing to document", index, "with length", doc_len
    
    if doc_len == 0:
        fwrite.write('1 0:1\n') # Dummy word for the images with no words, so that the document indexing remains correct 

    else:
        fwrite.write(str(doc_len) + ' ')
        for i in xrange(doc_len):
            if i == doc_len-1:
                fwrite.write(str(word_ids[word_index+i]) + ":" + str(order.index(labels[word_index+i, 0])) + '\n')
            else:
                fwrite.write(str(word_ids[word_index+i]) + ":" + str(order.index(labels[word_index+i, 0])) + ' ')

    word_index += doc_len;

# Close file
fwrite.close()

