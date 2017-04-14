import numpy as np
from collections import Counter

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
    def __init__(self, gamma, eta, level, number):
        self.topic = np.random.dirichlet(eta)
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
    def __init__(self, gamma, eta, NUM_LEVELS, id_to_word, word_to_id):
        self.num_restaurants = 1;
        self.restaurants = [Restaurant(gamma, eta, 0, 0)]
        self.gamma = gamma
        self.eta = eta
        self.NUM_LEVELS = NUM_LEVELS
        self.id_to_word = id_to_word
        self.word_to_id = word_to_id

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
                self.restaurants.append(Restaurant(self.gamma, self.eta, level+1, self.num_restaurants))
                self.levels[level+1].append(self.restaurants[self.num_restaurants])
                self.num_restaurants += 1

            cur_rest = self.restaurants[next_res]
            next_res, growth = cur_rest.new_customer(self.num_restaurants);

            if growth and level < self.NUM_LEVELS - 1:
                self.restaurants.append(Restaurant(self.gamma, self.eta, level+1, self.num_restaurants))
                self.levels[level+1].append(self.restaurants[self.num_restaurants])
                self.num_restaurants += 1
        

        return path

    def print_city(self, print_words):
        def tree_recurse(cur_rest):
            for i in xrange(cur_rest.get_level()):
                print '\t',
            print "[", cur_rest.get_level(), "/", cur_rest.total_customers * 250, "/", \
                    cur_rest.total_customers, "]",
            topic = cur_rest.get_topic()
            most_prevalent_words = np.argsort(topic)
            for word in most_prevalent_words[len(most_prevalent_words)-1:-print_words-1:-1]:
                print self.id_to_word[word].upper(),
            print

            if cur_rest.get_level() == self.NUM_LEVELS - 1:
                return
            for cur_table in cur_rest.tables:
                tree_recurse(self.restaurants[cur_table.next_restaurent])

        base_rest = self.restaurants[0]
        tree_recurse(base_rest)
        

class GenerativeModel:
    def __init__(self, eta, gamma, m, pi, NUM_LEVELS, id_to_word, word_to_id):
        self.eta = eta
        self.gamma = gamma
        self.m = m
        self.pi = pi
        self.NUM_LEVELS = NUM_LEVELS
        self.city = City(self.gamma, self.eta, self.NUM_LEVELS, id_to_word, word_to_id) 
        self.id_to_word = id_to_word
        self.id_to_word = word_to_id

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

            for n in xrange(NUM_WORDS):
                level_dn = np.random.choice(self.NUM_LEVELS, p = theta_d)
                word_dn = np.random.choice(NUM_WORDS, p = path_d[level_dn].get_topic())
                doc_d.append(self.id_to_word[word_dn])
            corpus.append(doc_d)
        return corpus

    def printTree(self, PRINT_WORDS_PER_TOPIC = 10):
        self.city.print_city(PRINT_WORDS_PER_TOPIC)
