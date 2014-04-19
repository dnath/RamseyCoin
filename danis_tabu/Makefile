CC = gcc
CFLAGS = -g -DDEBUG
#CFLAGS = -g
LIBS = -lm

OBJ = tabu_search.o jval.o jrb.o dllist.o fifo.o
TARGET = tabu_search

all: $(TARGET)

$(TARGET): $(TARGET).o $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

tabu_search.o: tabu_search.c
	$(CC) $(CFLAGS) -c tabu_search.c

fifo.o: fifo.c fifo.h jrb.h jval.h dllist.h
	$(CC) $(CFLAGS) -c fifo.c

jrb.o: jrb.c jrb.h jval.h
	$(CC) $(CFLAGS) -c jrb.c

jval.o: jval.c jval.h
	$(CC) $(CFLAGS) -c jval.c

dllist.o: dllist.c dllist.h jval.h
	$(CC) $(CFLAGS) -c dllist.c

clean:
	rm -f *.o $(TARGET)
