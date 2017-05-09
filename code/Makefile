.SUFFIXES: .c .u
CC = gcc
CFLAGS_MAC = -g -Wall -O3 -DHAVE_INLINE -DGSL_RANGE_CHECK_OFF -Winline -I/opt/local/include/gsl -I/home/genevieve/gsl/include
CFLAGS_PTON = -g -Wall -O3 -DHAVE_INLINE=1 -DGSL_RANGE_CHECK_OFF=1
CFLAGS_DEBUG = -g -O0 -Wall --enable-checking -v -da -Q
CFLAGS = -g -Wall -I/opt/local/include/gsl/ -I/usr/include/sys/ -I/usr/include/ -I/home/genevieve/gsl/include/

MAC_LDFLAGS = -lm -L/home/genevieve/gsl/lib -lgsl -lgslcblas -L/opt/local/lib 
C2_LDFLAGS = -lgsl -lcblas -latlas
CYCLES_LDFLAGS = -lgsl -lgslcblas
LSOURCE = utils.c topic.c doc.c hyperparameter.c main.c gibbs.c
LOBJECTS = utils.o topic.o doc.o hyperparameter.o main.o gibbs.o

main:	$(LOBJECTS)
	$(CC) $(CFLAGS_MAC) $(LOBJECTS) -o main $(MAC_LDFLAGS)

debug:	$(LOBJECTS)
	$(CC) $(CFLAGS_DEBUG) $(LOBJECTS) -o main $(MAC_LDFLAGS)

clean:
	-rm -f *.o
