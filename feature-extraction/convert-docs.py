import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os
import csv

# Open files
VOCAB_SIZE = 5000
filepath = './data'
savepath = './test-documents-5000'
curpath = '.'

def get_key(filename):
    return int(filename[3:-4])

docs = [f for f in os.listdir(savepath) if os.path.isfile(os.path.join(savepath, f))];
docs.sort(key = get_key);

# Need to output [# of unique terms] [term #] : [count] ...
fwrite = open(os.path.join(filepath, 'sim.dat'), 'w+')
for doc_i, document in enumerate(docs):
    with open(os.path.join(savepath, document)) as csvfile:
        reader = csv.reader(csvfile)
        document = []
        for row in reader:
            document.append(row[1])

        c = Counter(document)
        fwrite.write(str(len(c)))
        for i, key in enumerate(c):
            if i == len(c)-1:
                fwrite.write(str(key) + ":" + str(c[key]) + "\n")
            else:
                fwrite.write(str(key) + ":" + str(c[key]))
