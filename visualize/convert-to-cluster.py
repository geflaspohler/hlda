'''
Reads in the mode.assign file generated from hLDA and saves images into tired
folders for visulization according to their path assignments there
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
import csv

# Open files
VOCAB_SIZE = 5000
filepath = '/home/genevieve/mit-whoi/hlda/inference-panama-0302-images/run004'
savepath = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images/doc-clusters4'
imagepath = '/home/genevieve/mit-whoi/hlda/dataset-panama-0302-images'

image_files = [f for f in os.listdir(imagepath) if os.path.isfile(os.path.join(imagepath, f))];
image_files = sorted(image_files);

# Clusters at differnt levels
clusters = {};
second_clusters = {}
third_clusters = {}
clusters[2] = second_clusters;
clusters[3] = third_clusters;

tree_data = np.loadtxt(os.path.join(filepath, 'mode.assign'));
for row in tree_data:
    doc_id = int(row[0])
    topic_level_two  = int(row[3])
    topic_level_three = int(row[4])

    if topic_level_two in second_clusters:
        second_clusters[topic_level_two].append(image_files[doc_id])
    else:
        second_clusters[topic_level_two] = []
        second_clusters[topic_level_two].append(image_files[doc_id])

    if topic_level_three in third_clusters:
        third_clusters[topic_level_three].append(image_files[doc_id])
    else:
        third_clusters[topic_level_three] = []
        third_clusters[topic_level_three].append(image_files[doc_id])

if not os.path.exists(savepath):
    os.makedirs(savepath)

for i in [2,3]:
    cluster_dir = os.path.join(savepath, 'level' + str(i) + '/')
    if not os.path.exists(cluster_dir):
        os.makedirs(cluster_dir)
    for topic in clusters[i]:
        topic_dir = os.path.join(cluster_dir, 'topic' + str(topic) + '/')
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)
        for img in clusters[i][topic]:
            cv2.imwrite(os.path.join(topic_dir, img), cv2.imread(os.path.join(imagepath, img)))
        
