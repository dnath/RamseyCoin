CC = gcc
TOP = .
INCLUDES = -I$(TOP)
CFLAGS = -g 
COMPILE = $(CC) $(INCLUDES) $(CFLAGS)

INCL=./jrb.h ./jval.h
COMMON=.
PRED=.
BOBJ=$(COMMON)/jval.o $(COMMON)/jrb.o
LIBS= -lm 

PROGRAMS = iso_check

all: $(PROGRAMS)


iso_check: iso_check.c isomorph.o $(INCL) ${BOBJ}
	$(COMPILE) ${INCLUDES} -o iso_check iso_check.c isomorph.o $(BOBJ) $(LIBS)

isomorph.o: isomorph.c ${INCL} 
	$(COMPILE) ${INCLUDES} -c isomorph.c

jrb.o: jrb.c jrb.h jval.h
	$(COMPILE) ${INCLUDES} -c jrb.c

jval.o: jval.c jval.h
	$(COMPILE) ${INCLUDES} -c jval.c

clean:
	rm -f *.o core
