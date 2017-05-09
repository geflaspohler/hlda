'''
Reads in the modefile generated from hLDA and saves images into tired
folders for visualization according to their path assignments there
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import re

# Open files
VOCAB_SIZE = 1000
filepath = '/home/genevieve/mit-whoi/hlda/inference-panama-0302-images/run005'
savepath1 = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images/run005-topic-clusters-1'
savepath2 = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images/run005-topic-clusters-2'
imagepath = '/home/genevieve/mit-whoi/hlda/dataset-panama-0302-images'
docupath = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images/sim-vocab1000.dat'

image_files = [f for f in os.listdir(imagepath) if os.path.isfile(os.path.join(imagepath, f))];
image_files = sorted(image_files);

# Read in and disgard the header file; return a fileptr to just after header
def read_header(fileptr):
    NUM_HEADERS = 9;
    for i in xrange(NUM_HEADERS):
        header_line = f.readline();
        print header_line
    return fileptr;

def key_sort(topic_row):
    return topic_row.ndocs;

class Topic_row:
    def __init__(self, val_list):
        self.id = int(val_list[0])
        self.parent = int(val_list[1])
        self.ndocs = int(val_list[2])
        self.nwords = int(val_list[3])
        self.word_cnt = np.array(val_list[5:])

    def generate_top_words(self, N):
        self.word_cnt_arg = np.flip(np.argsort(self.word_cnt), axis = 0)
        return self.word_cnt_arg[0:N]

class Document:
    def __init__(self, val_list):
        self.word_to_count = {}
        self.nwords = 0;

        self.unique_terms = val_list[0];
        for entry in val_list[1:]:
            items = re.split(r':+', entry)
            self.word_to_count[int(items[0])] = int(items[1])
            self.nwords += int(items[1])

    def calc_purity(self, top_words):
        purity = 0;
        for word in top_words:
            if word in self.word_to_count:
                purity += float(self.word_to_count[word]) / float(self.nwords);
        return purity
        

class Corpus:
    def __init__(self):
        self.corpus = [];
    def add_document(self, doc):
        self.corpus.append(doc)
    def calc_purity(self, top_words, N):
        purity = [];
        for i, document in enumerate(self.corpus):
            doc_purity = document.calc_purity(top_words)
            purity.append(doc_purity)

        #print "Purity:", purity
        top_docs = np.flip(np.argsort(purity), axis = 0)
        #print "top documents:", top_docs
        return top_docs[0:N]


class Topics:
    def __init__(self):
        self.topics = []
        self.level_one = []
        self.level_two = []

    def add_row(self, topic_row):
        if topic_row.parent == -1:
            return;

        elif topic_row.parent == 0:
            self.level_one.append(topic_row)
        else:
            self.level_two.append(topic_row)
    
        self.topics.append(topic_row);

    def generate_top_topics(self, N):

        print "Total topics:", len(self.topics)
        print "Level 1 topics:", len(self.level_one)
        print "Level 2 topics:", len(self.level_two)


        self.level_one.sort(key = key_sort, reverse = True)
        self.level_two.sort(key = key_sort, reverse = True)

        return (self.level_one[0:N], self.level_two[0:N])

    def generate_pure_topics(self, N):
        print "Total topics:", len(self.topics)
        print "Level 1 topics:", len(self.level_one)
        print "Level 2 topics:", len(self.level_two)


        self.level_one.sort(key = key_sort, reverse = True)
        self.level_two.sort(key = key_sort, reverse = True)

        return (self.level_one[0:N], self.level_two[0:N])

if __name__ == "__main__":
    # Read in corpus
    corpus = Corpus();
    f = open(docupath)
    for line in f:
        vals = re.split(r' +', line.rstrip('\n'))
        cur_doc = Document(vals)
        corpus.add_document(cur_doc)

    f.close()

    # Open 'mode' file
    f = open(os.path.join(filepath, 'mode'));
    f = read_header(f)

    next_line = f.readline()
    num_topics = 1;
    # Check if we have reached the end of the file
    topic_table = Topics();

    while(next_line != '\n' and next_line):
        num_topics += 1
        vals = re.split(r' +', next_line.rstrip('\n'))
        cur_row = Topic_row(vals);
        topic_table.add_row(cur_row);
        next_line = f.readline()

    f.close()

    top_one, top_two = topic_table.generate_top_topics(N = 20);

    print "top one",  len(top_one)

    for index, topic_group in enumerate([top_one, top_two]):
        for topic in topic_group:
            print "Group:", index, " Topic:", topic
            top_words = topic.generate_top_words(N = 10);
            print "Top words at topic (", topic.id, "): ", 
            print top_words
            top_docs = corpus.calc_purity(top_words, N = 50);
            print "Top docs at topic (", topic.id, "): ", 
            print top_docs

            if index == 0:
                topic_dir = os.path.join(savepath1, 'topic' + str(topic.id) + '/')
            else:
                topic_dir = os.path.join(savepath2, 'topic' + str(topic.id) + '/')

            if not os.path.exists(topic_dir):
                os.makedirs(topic_dir)

            for i, doc in enumerate(top_docs):
                img = str(i) + '_' + image_files[doc]
                img_read = image_files[doc]
                cv2.imwrite(os.path.join(topic_dir, img), cv2.imread(os.path.join(imagepath, img_read)))
        


