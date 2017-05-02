import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import csv

# Open files
VOCAB_SIZE = 5000
#filepath = './test-images'
filepath = './panama-0302-images'
#savepath = './test-documents'
savepath = './panama-0302-documents'
datapath = './panama-0302-data'
curpath = '.'

def get_key(filename):
    return int(filename[3:-4])

image_files = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))];
image_files = sorted(image_files);

# Create with an origional, dummy entry
all_descriptors = np.zeros((1, 128));
all_keypoints = np.array([]);
image_lengths = [];

# For each image
for fimg in image_files[0:1000]:  # Only use a subset of the total images
    print "File:", fimg, 
    img = cv2.imread(os.path.join(filepath, fimg))

    surf = cv2.SURF(200);
    kp, des = surf.detectAndCompute(img, None);
    if des == None:
        image_lengths.append(0)
        print "No keypoints:", all_descriptors.shape
        continue;

    image_lengths.append(des.shape[0])

    all_descriptors = np.concatenate((all_descriptors, des), axis = 0)
    all_keypoints = np.concatenate((all_keypoints, kp), axis = 0)

    print "Number of keypoints:", all_descriptors.shape

# Remove the first dummy entry
all_descriptors = all_descriptors[1:]
all_descriptors = np.float32(all_descriptors)

# Preform k-means
flags = cv2.KMEANS_RANDOM_CENTERS
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
NUM_RESTARTS = 3
compactness, labels, centers = cv2.kmeans(all_descriptors, VOCAB_SIZE, criteria, NUM_RESTARTS, flags)
print 'Kmeans finished with compactness:', compactness

np.savetxt(os.path.join(datapath, 'cluster-centers-'+ str(VOCAB_SIZE) + '.txt'), centers, delimiter = ",")

# Write results to file: <index> <cluster id> <keypoint size>
word_index = 0;
for index, doc_length in enumerate(image_lengths):
    doc = open(os.path.join(savepath, 'doc' + str(index+1) + '.txt'), 'w+')
    print "Writing to document", index, "with length", doc_length
    for i in xrange(doc_length):
        doc.write(str(i) + ", " + str(labels[word_index+i, 0]) + ", " + str(all_keypoints[word_index+i].size) + '\n')
    if doc_length == 0:
        doc.write('empty, empty, empty\n')

    # Close file
    doc.close()
    word_index += doc_length;

# Write output in format expected by Blei's code
docs = [f for f in os.listdir(savepath) if os.path.isfile(os.path.join(savepath, f))];
docs.sort(key = get_key);

# Need to output [# of unique terms] [term #] : [count] ...
fwrite = open(os.path.join(datapath, 'sim.dat'), 'w+')
for doc_i, document in enumerate(docs):
    with open(os.path.join(savepath, document)) as csvfile:
        reader = csv.reader(csvfile)
        document = []
        for row in reader:
            document.append(row[1])

        c = Counter(document)
        if len(c) == 1 and document[0] == 'empty':
            fwrite.write('0')
        else:
            fwrite.write(str(len(c)))
            for i, key in enumerate(c):
                if i == len(c)-1:
                    fwrite.write(str(key) + ":" + str(c[key]) + "\n")
                else:
                    fwrite.write(str(key) + ":" + str(c[key]))
fwrite.close() 


    
