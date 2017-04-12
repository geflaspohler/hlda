import numpy as np

vocab_filename = "/home/genevieve/mit-whoi/hlda/ap/vocab.txt"
vocab = map(str.strip, file(vocab_filename, "r").readlines())

# True tree struture
#      x   
#   x     x   x
# x x x   x   x
# Total topics: 9
NUM_LEVELS = 3

tree = {}

# Hyperparmeters
ETA = [0.1] * len(vocab)
m = 0.5
pi = 100

# Parameters
NUM_TOPICS = 9
TOPICS = []
NUM_DOCUMENTS = 100;
NUM_WORDS = 250;

DOCUMENTS = []

def GEM_draw(m, pi):
    thetas = np.zeros(NUM_LEVELS)

    V1 = np.random.beta(m*pi, (1-m)*pi)
    thetas[0] = V1

    Sum = V1
    V_cur = 1 - V1
    for level in xrange(1, NUM_LEVELS):
        Vi = np.random.beta(m*pi, (1-m)*pi)

        thetas[level] = Vi * V_cur
        Sum += Vi * V_cur

        V_cur = V_cur * (1 - Vi)

    thetas[NUM_LEVELS-1] = 1 - Sum;

    print thetas
    return thetas

        
         

for i in xrange(NUM_TOPICS): 
    current_topic = np.random.dirichlet(ETA)
    TOPICS.append(current_topic)
    
for i in xrange(NUM_DOCUMENTS):
    #c_d = nCRP(gamma)
    theta_d = GEM_draw(m, pi)

    for j in xrange(NUM_WORDS):
        z_dn = 0
        w_dn = 0


#def nCRP_draw(gamma):
  
