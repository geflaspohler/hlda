import numpy as np
from collections import Counter
import sys
import os

class Table:
    def __init__(self, new_rest):
        self.num_customers = 0
        self.next_restaurent = new_rest
    def get_customers(self):
        return self.num_customers
    def add_customer(self):
        self.num_customers += 1
    def next_restaurent(self):
        return self.next_restaurent

class Restaurant:
    def __init__(self, gamma, level, number):
        self.topic = np.random.dirichlet(ETA)
        self.total_customers = 0
        self.num_tables = 0
        self.gamma = gamma
        self.tables = []
        self.level = level;
        self.number = number
   
    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level 

    def get_number(self):
        return self.number

    def get_topic(self):
        return self.topic

    def new_customer(self, new_rest):
        self.total_customers += 1;

        # Draw seated table index, 0 based
        seated_table = self.CRP_draw()
        print "\t\t They sit at table", seated_table, "and draw card",

        if seated_table < self.num_tables:
            self.tables[seated_table].add_customer();
            print self.tables[seated_table].next_restaurent
            return self.tables[seated_table].next_restaurent, False 
        else:
            self.tables.append(Table(new_rest));
            self.tables[seated_table].add_customer();
            self.num_tables += 1
            print self.tables[seated_table].next_restaurent
            return self.tables[seated_table].next_restaurent, True 

    def CRP_draw(self):
        if self.num_tables == 0:
            return 0

        indicator = np.random.uniform()
        prob_sum = 0
        index = 0;

        """
        print "\t\t They draw the uniform variable", indicator
        old = 0
        # Print out the CRP
        for i in xrange(self.num_tables):
            new = self.tables[i].get_customers() /  \
                        (self.gamma + self.total_customers - 1)
            print "\t\t", i, "from", old, "to", old + new
            old = old + new
        """

        while prob_sum < indicator and index < self.num_tables:
            prob_sum += self.tables[index].get_customers() /  \
                        (self.gamma + self.total_customers - 1)
            index += 1

        if prob_sum > indicator:
            return index -1
        else:
            return index 

class City:
    def __init__(self, gamma, NUM_LEVELS):
        self.num_restaurants = 1;
        self.restaurants = [Restaurant(gamma, 0, 0)]
        self.gamma = gamma
        self.NUM_LEVELS = NUM_LEVELS

        # Keep a map of restaurants associated with each level
        self.levels = {}
        for level in xrange(self.NUM_LEVELS):
            self.levels[level] = []
        self.levels[0].append(self.restaurants[0])

    def new_customer(self):
        path = []
        next_res = 0
        for level in xrange(self.NUM_LEVELS):
            path.append(self.restaurants[next_res])
            print "\t On day (level)", level, "they visit restaurant", next_res
            if level >= self.num_restaurants:
                self.restaurants.append(Restaurant(gamma, level+1, self.num_restaurants))
                self.levels[level+1].append(self.restaurants[self.num_restaurants])
                self.num_restaurants += 1

            cur_rest = self.restaurants[next_res]
            next_res, growth = cur_rest.new_customer(self.num_restaurants);

            if growth and level < self.NUM_LEVELS - 1:
                self.restaurants.append(Restaurant(gamma, level+1, self.num_restaurants))
                self.levels[level+1].append(self.restaurants[self.num_restaurants])
                self.num_restaurants += 1
        

        return path


    def print_city(self, print_words):
        def tree_recurse(cur_rest, fwrite):
            for i in xrange(cur_rest.get_level()):
                fwrite.write('\t')
                print '\t',

            fwrite.write("[" + str(cur_rest.get_level()) + "/" + \
                            str(cur_rest.total_customers * 250) + "/" + \
                            str(cur_rest.total_customers) + "] ")
            print "[", cur_rest.get_level(), "/", cur_rest.total_customers * 250, "/", \
                    cur_rest.total_customers, "]",
            topic = cur_rest.get_topic()
            most_prevalent_words = np.argsort(topic)
            for word in most_prevalent_words[len(most_prevalent_words)-1:-print_words-1:-1]:
                fwrite.write(id_to_word[word].upper() + ' ')
                print id_to_word[word].upper(),
            fwrite.write('\n\n')
            print

            if cur_rest.get_level() == self.NUM_LEVELS - 1:
                return
            for cur_table in cur_rest.tables:
                tree_recurse(self.restaurants[cur_table.next_restaurent], fwrite)

        fwrite = open('run' + str(input) + '/tree_structure.txt', 'w+')
        base_rest = self.restaurants[0]
        tree_recurse(base_rest, fwrite)
        fwrite.close()
        

class GenerativeModel:
    def __init__(self, eta, gamma, m, pi, NUM_LEVELS):
        self.eta = eta
        self.gamma = gamma
        self.m = m
        self.pi = pi
        self.NUM_LEVELS = NUM_LEVELS
        self.city = City(self.gamma, self.NUM_LEVELS) 

    def nCRP_draw(self):
        print "A new customer arrives in the city"
        return self.city.new_customer()

    def GEM_draw(self, m, pi):
        thetas = np.zeros(self.NUM_LEVELS)
        V1 = np.random.beta(m*pi, (1-m)*pi)
        thetas[0] = V1
        Sum = V1
        V_cur = 1 - V1
        for level in xrange(1, self.NUM_LEVELS-1):
            Vi = np.random.beta(m*pi, (1-m)*pi)

            thetas[level] = Vi * V_cur
            Sum += Vi * V_cur

            V_cur = V_cur * (1 - Vi)
        thetas[self.NUM_LEVELS-1] = 1.000 - np.sum(thetas);
        return thetas

    def generateDocuments(self, NUM_DOCUMENTS, NUM_WORDS):
        corpus = []
        # For every document (customer)
        for document in xrange(NUM_DOCUMENTS):
            doc_d = []
            path_d = self.nCRP_draw();
            theta_d = self.GEM_draw(self.m, self.pi)
            #theta_d = np.random.dirichlet([m]*3)

            for n in xrange(NUM_WORDS):
                level_dn = np.random.choice(self.NUM_LEVELS, p = theta_d)
                word_dn = np.random.choice(VOCAB_SIZE, p = path_d[level_dn].get_topic())
                doc_d.append(id_to_word[word_dn])
            corpus.append(doc_d)
        return corpus

    def printTree(self, PRINT_WORDS_PER_TOPIC = 10):
        self.city.print_city(PRINT_WORDS_PER_TOPIC)
        
# Parameters
NUM_DOCUMENTS = 100;
VOCAB_SIZE = 100
NUM_WORDS = 500;
NUM_LEVELS = 3

# Create a vocab of VOCAB_SIZE words
vocab_filename = "/home/genevieve/mit-whoi/hlda/ap/vocab.txt"
id_to_word = map(str.strip, file(vocab_filename, "r").readlines())
id_to_word = id_to_word[0:VOCAB_SIZE]
word_to_id = {}
for i, word in enumerate(id_to_word):
    word_to_id[word] = i


input = int(sys.argv[1])
if not os.path.exists('run' + str(input)):
    os.makedirs('run' + str(input))

# Hyperparmeters
ETA = [1.5] * VOCAB_SIZE 
m = 0.5
pi = 100
gamma = 0.5

hLDA_model = GenerativeModel(ETA, gamma, m, pi, NUM_LEVELS)
corpus = hLDA_model.generateDocuments(NUM_DOCUMENTS, NUM_WORDS)
hLDA_model.printTree(10);

fwrite = open('run' + str(input) + '/sim.txt', 'w+')

for doc_i, document in enumerate(corpus):
    fwrite.write("Document <" + str(doc_i) + "> \n")
    for word in document:
        fwrite.write(word + " ") 
    fwrite.write('\n\n') 
fwrite.close()

# Need to output [# of unique terms] [term #] : [count] ...
fwrite = open('run' + str(input) + '/sim.dat', 'w+')
for doc_i, document in enumerate(corpus):
    c = Counter(document)
    fwrite.write(str(len(c)) + " ")
    for i, key in enumerate(c):
        if i == len(c)-1:
            fwrite.write(str(word_to_id[key]) + ":" + str(c[key]) + "\n")
        else:
            fwrite.write(str(word_to_id[key]) + ":" + str(c[key]) + " ")

fwrite.close()

fwrite = open('run' + str(input) + '/sim_vocab.txt', 'w+')
for word in id_to_word:
    fwrite.write(word + '\n')
fwrite.close
    


