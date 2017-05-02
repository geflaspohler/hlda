import numpy as np
import os

filepath = './data'
VOCAB_SIZE = 5000;

# Need to output [vocab_word]
fwrite = open(os.path.join(filepath, 'vocab.dat'), 'w+')
for i in xrange(VOCAB_SIZE):
    fwrite.write(str(i) + '\n')
