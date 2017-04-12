import numpy as np

VOCAB_SIZE = 250

# Create a vocab of 250 words
vocab_filename = "/home/genevieve/mit-whoi/hlda/ap/vocab.txt"
vocab = map(str.strip, file(vocab_filename, "r").readlines())
vocab = vocab[0:VOCAB_SIZE]

# True tree struture
#      x   
#   x     x   x
# x x x   x   x
# Total topics: 9
NUM_LEVELS = 3

# Hyperparmeters
ETA = [0.005] * len(vocab) 
m = 0.5
pi = 100

# Parameters
NUM_TOPICS = 9
TOPICS = []
NUM_DOCUMENTS = 100;
NUM_WORDS = 250;
gamma = 1.0

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

    return thetas

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
    def __init__(self, gamma):
        self.num_restaurants = 1;
        self.restaurants = [Restaurant(gamma, 0, 0)]
        self.gamma = gamma

        # Keep a map of restaurants associated with each level
        self.levels = {}
        for level in xrange(NUM_LEVELS):
            self.levels[level] = []
        print "Adding to self.levels[0]"
        self.levels[0].append(self.restaurants[0])

    def new_customer(self):
        path = []
        next_res = 0
        for level in xrange(NUM_LEVELS):
            path.append(self.restaurants[next_res])
            print "\t On day (level)", level, "they visit restaurant", next_res
            if level >= self.num_restaurants:
                self.restaurants.append(Restaurant(gamma, level+1, self.num_restaurants))
                print "Adding to self.levels[", level+1, "]"
                self.levels[level+1].append(self.restaurants[self.num_restaurants])
                self.num_restaurants += 1

            cur_rest = self.restaurants[next_res]
            next_res, growth = cur_rest.new_customer(self.num_restaurants);

            if growth and level < NUM_LEVELS - 1:
                self.restaurants.append(Restaurant(gamma, level+1, self.num_restaurants))
                self.levels[level+1].append(self.restaurants[self.num_restaurants])
                print "Adding to self.levels[", level+1, "]"
                self.num_restaurants += 1
        

        return path

    def print_city(self):
        print "Tree structure:"
        for i in xrange(NUM_LEVELS):
            for j in xrange(NUM_LEVELS - i):
                print '\t',
            for rest in self.levels[i]:
                print rest.get_number(), '\t' , 
            print 



def nCRP_draw(gamma):
    print "A new customer arrives in the city"
    return nCRP_draw.City.new_customer()

# Create a city for the nCRP prior 
nCRP_draw.City = City(gamma)
corpus = []

# For every document (customer)
for document in xrange(NUM_DOCUMENTS):
    doc_d = []
    path_d = nCRP_draw(gamma);
    theta_d = GEM_draw(m, pi) 

    for n in xrange(NUM_WORDS):
        print theta_d
        print NUM_LEVELS
        level_dn = np.random.choice(NUM_LEVELS, p = [theta_d])
        word_dn = np.random.choice(NUM_WORDS, p = [path_d[z_dn].get_topic()])
        doc.append(word_dn)
    corpus.append(doc_d)

nCRP_draw.City.print_city()
    


