#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

#include "fifo.h"	/* for taboo list */


#define MAXSIZE (512)

#define TABOOSIZE (500)
#define BIGCOUNT (9999999)

/***
 *** example of very simple search for R(6,6) counter examples
 ***
 *** starts with a small randomized graph and works its way up to successively
 *** larger graphs one at a time
 ***
 *** uses a taboo list of size #TABOOSIZE# to hold and encoding of and edge
 *** (i,j)+clique_count
 ***/

/*
 * PrintGraph
 *
 * prints in the right format for the read routine
 */

int maximumGraphSize = 101;

int edgeWeight [101];

void initialize_edge_weight()
{
	int i =0;
	for (i;i<maximumGraphSize;i++)
	{
		edgeWeight[i] = 0;
	}
}

int get_max_edge_index ()
{
	int maximum_index = 0;
	int maximum_weight = edgeWeight[maximum_index];
	int i =1;
	for (i;i<maximumGraphSize;i++)
	{
		if(edgeWeight[i]>maximum_weight)
		{
			maximum_index = i;
			maximum_weight = edgeWeight[i];
		}
	}
	return maximum_index;
}



void PrintGraph(int *g, int gsize)
{
	int i;
	int j;

	FILE * pFile = fopen ("myfileAll.txt","a");
	for(i=0; i < gsize; i++)
	{
		for(j=0; j < gsize; j++)
		{
			fprintf(pFile,"%d",g[i*gsize+j]);
		}
	}
	fprintf(pFile, "\n");
	fclose(pFile);
	return;
}

/*
 * CopyGraph 
 *
 * copys the contents of old_g to corresponding locations in new_g
 * leaving other locations in new_g alone
 * that is
 * 	new_g[i,j] = old_g[i,j]
 */
void CopyGraph(int *old_g, int o_gsize, int *new_g, int n_gsize)
{
	int i;
	int j;

	/*
	 * new g must be bigger
	 */
	if(n_gsize < o_gsize)
		return;

	for(i=0; i < o_gsize; i++)
	{
		for(j=0; j < o_gsize; j++)
		{
			new_g[i*n_gsize+j] = old_g[i*o_gsize+j];
		}
	}

	return;
}


/*
 ***
 *** returns the number of monochromatic cliques in the graph presented to
 *** it
 ***
 *** graph is stored in row-major order
 *** only checks values above diagonal
 */

int CliqueCount(int *g,
	     int gsize)
{
    int i;
    int j;
    int k;
    int l;
    int m;
    int n;
    int count=0;
    int sgsize = 6;
    initialize_edge_weight();
    for(i=0;i < gsize-sgsize+1; i++)
    {
	for(j=i+1;j < gsize-sgsize+2; j++)
        {
	    for(k=j+1;k < gsize-sgsize+3; k++) 
            { 
		if((g[i*gsize+j] == g[i*gsize+k]) && 
		   (g[i*gsize+j] == g[j*gsize+k]))
		{
		    for(l=k+1;l < gsize-sgsize+4; l++) 
		    { 
			if((g[i*gsize+j] == g[i*gsize+l]) && 
			   (g[i*gsize+j] == g[j*gsize+l]) && 
			   (g[i*gsize+j] == g[k*gsize+l]))
			{
			    //for(m=l+1;m < gsize-sgsize+5; m++) 
			    m = gsize-1;
			    {
				if((g[i*gsize+j] == g[i*gsize+m]) && 
				   (g[i*gsize+j] == g[j*gsize+m]) &&
				   (g[i*gsize+j] == g[k*gsize+m]) && 
				   (g[i*gsize+j] == g[l*gsize+m])) {
					for(n=m+1; n < gsize-sgsize+6; n++)
					{
						if((g[i*
							++j]
							== g[i*gsize+n]) &&
						   (g[i*gsize+j] 
							== g[j*gsize+n]) &&
						   (g[i*gsize+j] 
							== g[k*gsize+n]) &&
						   (g[i*gsize+j] 
							== g[l*gsize+n]) &&
						   (g[i*gsize+j] 
							== g[m*gsize+n])) {
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
    return(count);
}


int
main(int argc,char *argv[])
{
	int *g;
	int *new_g;
	int gsize;
	int count;
	int i;
	int j;
	int best_count;
	int best_i;
	int best_j;
	void *taboo_list;

	// read counter example from file
   FILE * pFile;
   char graph_size [10];
   char mystring [10202];
   pFile = fopen ("example.txt" , "r");
   if (pFile == NULL) perror ("Error opening file");
   else {
     if(fgets(graph_size,10,pFile)!=NULL)
     {
     		gsize = atoi(graph_size);
     		printf("%d\n", gsize);
     		g = (int *)malloc(gsize*gsize*sizeof(int));
			if(g == NULL) {
				exit(1);
			}
     }
     if ( fgets (mystring , gsize*gsize , pFile) != NULL )
     {
     	int element_count = 0;
     	for (element_count;element_count<gsize*gsize;element_count++)
		{
				if(mystring[element_count]=='0')
				{
					g[element_count] = 0;
				}
				else
				{
					g[element_count] = 1;
				}

		}
     }
     
     fclose (pFile);
   }
	
   generate_counter_example(g,gsize);
   return(0);

}


// generate counter examples of size n-1
void generate_counter_example(int * g, int gsize)
{
	if(gsize<=79)
	{
		return;
	}
	else
	{

		int count = CliqueCount(g,gsize);

		if(count == 0)
		{
		   PrintGraph(g,gsize);
		   //get all counter examples of size n-1
		   // current_node to be deleted from the original graph
		   int current_node = 0;
		   for(current_node = 0; current_node<gsize;current_node ++)
		   {
		   		int *  new_graph = (int *)malloc((gsize-1)*(gsize-1)*sizeof(int));
				if(new_graph == NULL) {
					exit(1);
				}
				int edge_counter = 0;
				int row = 0;
				int column = 0;
				for(row;row<gsize;row++)
				{
					for(column=0;column<gsize;column++)
					{
						if(row==current_node||column==current_node)
						{
							continue;
						}
						new_graph[edge_counter++] = g[row*gsize+column];
					}
				}
				count = CliqueCount(new_graph,gsize-1);
				if(count == 0)
				{
				   PrintGraph(new_graph,gsize-1);
				}
				generate_counter_example(new_graph,gsize-1);
				if(new_graph!=NULL)free(new_graph);
		   }	
		}
	}

}