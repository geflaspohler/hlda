import numpy as np
import os

filepath = '/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images'
VOCAB_SIZE = 5000;

# Need to output [vocab_word]
fwrite = open(os.path.join(filepath, 'vocab.dat'), 'w+')
for i in xrange(VOCAB_SIZE):
    fwrite.write(str(i) + '\n')
