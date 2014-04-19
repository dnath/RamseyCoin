/*
 * tabu_search.c
 *
 * Authors: Dani Kudrow, Dev Nath, Victor Zakhary
 *
 * This tabu search is somewhat different from Rich's version. It must be
 * seeded with a valid counter example and only the edges originating at
 * the new vertex are mutated in the tabu search. This makes the search
 * much less expensive. Also the clique counter need only search for
 * monochromatic 6-cliques that contain the new node - we are guaranteed
 * that the remainder of the graph is valid.
 *
 * Notes:
 * - There are two clique counters
 *   -> the naive clique counter searches the full graph for 6-cliques
 *   -> the vert0 clique counter searches only the 6-cliques that contain
 *   	vertex 0
 * - The vert0_clique_counter is capable of storing edges weights in an
 *   array. How to make use of this?
 * - This approach is very sensitive to taboo list size. We need a good way
 *   of choosing this dynamically.
 * - Input graphs have the format:
 *   <# vertices>
 *   <graph as 1-d array of 1's and 0's>
 *   <everything after the second line is ignored>
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "fifo.h"

#define ELEM_TYPE int
#define FAIL_COUNT 999999
#define MAX_SIZE 101

#ifdef DEBUG
#define debug_print(...) printf(__VA_ARGS__);
#else
#define debug_print(...)
#endif

/*
 * dump_graph
 *
 * save a graph in a text file
 * parameters:
 * 	graph -- array of ints
 * 	size -- # vertices in graph
 */
void dump_graph(const ELEM_TYPE *graph, const int size)
{
	char *filename;
}

/*
 * print_graph
 *
 * print a graph to stdout
 * parameters:
 * 	graph -- array of ints
 * 	size -- # vertices in graph
 */
void print_graph(const ELEM_TYPE *graph, const int size)
{
	int i, j;

	printf("size: %d\n", size);
	for (i=0; i<size; i++) {
		for (j=0; j<size; j++) {
			printf("%d ", graph[i*size+j]);
		}
		printf("\n");
	}
}

/*
 * read_graph
 *
 * read a graph from a file into an array
 * paramters:
 * 	filename -- name of input file
 * 	size -- integer in which to store size of graph
 * returns the graph as an array of size**2 integers
 */
ELEM_TYPE *read_graph(const char *filename, int *vertices)
{
	FILE *input_file;
	ELEM_TYPE *graph;
	int i, edges;
	char *buf;

	if ((input_file = fopen(filename, "r")) == NULL)
		return NULL;

	fscanf(input_file, "%d\n", vertices);
	edges = *vertices * *vertices;

	if ((buf = malloc(edges * sizeof(char) + 1)) == NULL) {
		return NULL;
	} else if ((graph = malloc(edges * sizeof(ELEM_TYPE))) == NULL) {
		free(buf);
		return NULL;
	}

	fgets(buf, edges+1, input_file);

	for (i=0; i<edges; i++) {
		graph[i] = buf[i]-48 ? 1 : 0;
	}

	free(buf);

	return graph;
}

/*
 * naive_clique_count6
 *
 * count the number of monochromatic 6-cliques in the graph, examining
 * every group of 6 nodes
 * parameters:
 * 	graph -- array of ints
 * 	size -- # vertices in graph
 * returns the number monochromatic cliques 
 */
int naive_clique_count6(const ELEM_TYPE *graph, const int size)
{
	int i, j, k, l, m, n;
	int count = 0;

	for (i=0; i<size-5; i++) {
		for (j=i+1; j<size-4; j++) {
			for (k=j+1; k<size-3; k++) { 
				if (
					(graph[i*size+j] == graph[i*size+k]) &&
					(graph[i*size+j] == graph[j*size+k])) {
					for (l=k+1; l<size-2; l++) { 
						if (
							(graph[i*size+j] == graph[i*size+l]) &&
							(graph[i*size+j] == graph[j*size+l]) &&
							(graph[i*size+j] == graph[k*size+l])) {
							for (m=l+1; m<size-1; m++) {
								if (
									(graph[i*size+j] == graph[i*size+m]) &&
									(graph[i*size+j] == graph[j*size+m]) &&
									(graph[i*size+j] == graph[k*size+m]) &&
									(graph[i*size+j] == graph[l*size+m])) {
									for (n=m+1; n<size;n++) {
										if (
											(graph[i*size+j] == graph[i*size+n]) &&
											(graph[i*size+j] == graph[j*size+n]) &&
											(graph[i*size+j] == graph[k*size+n]) &&
											(graph[i*size+j] == graph[l*size+n]) &&
											(graph[i*size+j] == graph[m*size+n])) {
											count++;
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return count;
}

/*
 * vert0_clique_count6
 *
 * count the number of monochromatic 6-cliques in the graph, examining
 * only groups of 6 nodes containing vertex 0
 * also, keeps track of how many cliques each (new) edge is a part of
 * parameters:
 * 	graph -- array of ints
 * 	size -- # vertices in graph
 * 	weights -- store # cliques to which edge belongs (set NULL to ignore)
 * returns the number monochromatic cliques 
 */
int vert0_clique_count6(const int *graph, const int size, int *weights)
{
	int i, j, k, l, m, n;
	int count = 0;

	i = 0;
	for (j=i+1; j<size-4; j++) {
		for (k=j+1; k<size-3; k++) { 
			if (
					(graph[i*size+j] == graph[i*size+k]) &&
					(graph[i*size+j] == graph[j*size+k])) {
				for (l=k+1; l<size-2; l++) { 
					if (
							(graph[i*size+j] == graph[i*size+l]) &&
							(graph[i*size+j] == graph[j*size+l]) &&
							(graph[i*size+j] == graph[k*size+l])) {
						for (m=l+1; m<size-1; m++) {
							if (
									(graph[i*size+j] == graph[i*size+m]) &&
									(graph[i*size+j] == graph[j*size+m]) &&
									(graph[i*size+j] == graph[k*size+m]) &&
									(graph[i*size+j] == graph[l*size+m])) {
								for (n=m+1; n<size;n++) {
									if (
											(graph[i*size+j] == graph[i*size+n]) &&
											(graph[i*size+j] == graph[j*size+n]) &&
											(graph[i*size+j] == graph[k*size+n]) &&
											(graph[i*size+j] == graph[l*size+n]) &&
											(graph[i*size+j] == graph[m*size+n])) {
										count++;
										if (weights != NULL) {
											++weights[j];
											++weights[k];
											++weights[l];
											++weights[m];
											++weights[n];
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return count;
}

/*
 * main
 *
 * this is the main logic of the tabu search
 * notes:
 * - the size of the taboo list affects performance a lot. The code below
 *   allows us to resize the taboo list each time a counter example is
 *   found.
 */
main(int argc, char *argv[])
{
	ELEM_TYPE *graph;	/* the current candidate solution */
	ELEM_TYPE *new_graph; /* current graph plus another vertex */
	int size;			/* number of vertices in current graph */
	int new_size;		/* number of vertices in next graph (size + 1) */
	int taboo_size;		/* size of taboo_list */
	int count;			/* number of monochromatic 6-cliques in candidate */
	int best_count;		/* lowest clique count found */
	int i, j;			/* index of flipped edge */
	int best_i, best_j;	/* index of most effective edge flipped */
	char *seed_file;	/* file containing seed graph */
	void *taboo_list;	/* taboo list */
	clock_t clock_start, clock_found_ce, clock_last_ce;


	if (argc != 3) {
		fprintf(stderr, "Usage: ./tabu <seed_file> <taboo_size>.\n");
		exit(1);
	}

	seed_file = argv[1];
	taboo_size = atoi(argv[2]);

	/* read in the seed graph */
	graph = read_graph(seed_file, &size);
	if (graph == NULL) {
		fprintf(stderr, "Error loading graph. Aborting.\n");
		exit(1);
	}
	count = naive_clique_count6(graph, size);

	/* create a taboo list */
	taboo_list = FIFOInitEdge(taboo_size);
	if (taboo_list == NULL) {
		fprintf(stderr, "Error initializing taboo graph. Aborting.\n");
		exit(1);
	}

	/* start the clock */
	clock_start = clock();
	clock_last_ce = clock_start;

	/* loop until we have a solution of size 101 */
	while (size <= MAX_SIZE) {

		/* get the current clique count */

		/* we have found a counter example */
		if (count == 0) {
			/* timestamp */
			clock_found_ce = clock();

			/* sanity check! */
			if (naive_clique_count6(graph, size)) {
				fprintf(stderr, "Discrepency between naive and vert0 clique counts!\n");
				exit(1);
			}

			fprintf(stdout, "Found counter example!\n");
			fprintf(stdout, "Time elapsed since start: %f, since last CE: %f\n",
					(double)(clock_found_ce-clock_start)/CLOCKS_PER_SEC,
					(double)(clock_found_ce-clock_last_ce)/CLOCKS_PER_SEC);;

			clock_last_ce = clock_found_ce;

			print_graph(graph, size);

			/* the new graph will be one node larger */
			new_size = size + 1;
			new_graph = (int *)malloc(new_size * new_size * sizeof(ELEM_TYPE));
			if (new_graph == NULL) {
				fprintf(stderr, "Error allocating new graph.\n");
				exit(1);
			}

			/* place the new node at position 0 */
			/* TODO randomize edges */
			for (i=0; i<new_size; i++)
				new_graph[i] = 0;

			/* copy in the previous graph */
			for (i=1; i<new_size; i++) {
				new_graph[i*new_size] = 0;
				memcpy(&new_graph[i*new_size+1],
						&graph[(i-1)*size],
						size*sizeof(ELEM_TYPE));
			}

			free(graph);
			graph = new_graph;
			size = new_size;

			/* update the clique_count */
			count = naive_clique_count6(graph, size);

			/* reset the taboo list and increase it's size */
			FIFODelete(taboo_list);
			taboo_list = FIFOInitEdge(taboo_size);

			continue;
		} /* END found counterexample */ 

		/* try flipping all of the new edges */
		best_count = FAIL_COUNT;
		i = 0;
		for (j=1; j<size; j++) {
			/* flip the edge */
			graph[i*size+j] = 1 - graph[i*size+j];

			/* check the result of the flip */
			count = vert0_clique_count6(graph, size, NULL);

			/* update the taboo list if this is locally optimal */
			if ((count < best_count) && !FIFOFindEdge(taboo_list, i, j)) {
				best_count = count;
				best_i = i;
				best_j = j;
			}

			/* unflip the edge */
			graph[i*size+j] = 1 - graph[i*size+j];

		} /* END iterate over new edges */

		/* check results */
		if (best_count == FAIL_COUNT) {
			fprintf(stderr, "Unable to reduce clique_count. Game over.\n");
			exit(1);
		}

		/* keep the best flip */
		graph[best_i*size+best_j] = 1 - graph[best_i*size+best_j];
		count = best_count;

		/* taboo this graph */
		FIFOInsertEdge(taboo_list, best_i, best_j);

		//debug_print("Flipped edge (%d, %d), clique count: %d.\n", best_i, best_j, best_count);
		debug_print("[%d] Flipping (%d, %d), clique count: %d, taboo size: %d\n", size, best_i, best_j, best_count, taboo_size);

	} /* END size == 101 */

	return 0;
}

