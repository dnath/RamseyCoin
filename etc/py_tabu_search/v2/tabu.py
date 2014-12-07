#!/usr/bin/python

######################################################################
#
# tabu.py
#
# Tabu search for counterexamples to R(6, 6)
#
# Authors: Daniel Kudrow, Dev Nath, Victor Zakhary
#
######################################################################
#
# Graphs are 2d Python lists. The tabu search is invoked with the
# tabu() function. It takes two arguments:
# 1. graph
# 2. number of workers (how much to divide the search space)
# The tabu list is set to the number of vertices in the graph and is
# increased as necessary.
#
######################################################################


######################################################################
#
# Modules
#
import copy
import OrderedSet
import pickle
import random
import sys
import time
import math
#
######################################################################


######################################################################
#
# debug
#
# Toggle debugging output
#
DEBUG = True
# DEBUG = False
def debug(msg):
    if DEBUG:
        sys.stdout.write(msg)
#
######################################################################


######################################################################
#
# printGraph
#
# Print the graph to stdout
# Input: graph
#
def printGraph(graph):
    print "Size: %d" % (len(graph))
    for row in graph:
        s = ""
        for ele in row:
            s += str(ele)
        print s
#
######################################################################


######################################################################
#
# readGraph
# 
# Attempt to read in a pickled graph
# Input: filename of pickled graph
# Output: un-pickled graph as array or empty array in case of error
#
def readGraph(filename):
    try:
        return pickle.load(open(filename, "r"))
    except IOError:
        return []
#
######################################################################


######################################################################
#
# naiveCliqueCount
#
# Count monochromatic 6-cliques by examining every node in the graph
# Input: graph as array
# Output: number of monochromatic 6-cliques
#
def naiveCliqueCount(graph):
    size = len(graph)
    cliqueCount = 0

    for i in range(0, size-5):
        for j in range(i+1, size-4):
            for k in range(j+1, size-3):
                if (graph[i][j] == graph[i][k] and
                        graph[i][j] == graph[j][k]):
                    for l in range(k+1, size-2):
                        if (graph[i][j] == graph[i][l] and
                                graph[i][j] == graph[j][l] and
                                graph[i][j] == graph[k][l]):
                            for m in range(l+1, size-1):
                                if (graph[i][j] == graph[i][m] and
                                        graph[i][j] == graph[j][m] and
                                        graph[i][j] == graph[k][m] and
                                        graph[i][j] == graph[l][m]):
                                    for n in range(m+1, size):
                                        if (graph[i][j] == graph[i][n] and
                                                graph[i][j] == graph[j][n] and
                                                graph[i][j] == graph[k][n] and
                                                graph[i][j] == graph[l][n] and
                                                graph[i][j] == graph[m][n]):
                                            cliqueCount += 1

    return cliqueCount
#
######################################################################


######################################################################
#
# vert0CliqueCount
#
# Count monochromatic 6-cliques containing vertex 0
# Input: graph as array
# Output: number of monochromatic 6-cliques
#
def vert0CliqueCount(graph):
    size = len(graph)
    cliqueCount = 0

    i = 0
    for j in range(i+1, size-4):
        for k in range(j+1, size-3):
            if (graph[i][j] == graph[i][k] and
                    graph[i][j] == graph[j][k]):
                for l in range(k+1, size-2):
                    if (graph[i][j] == graph[i][l] and
                            graph[i][j] == graph[j][l] and
                            graph[i][j] == graph[k][l]):
                        for m in range(l+1, size-1):
                            if (graph[i][j] == graph[i][m] and
                                    graph[i][j] == graph[j][m] and
                                    graph[i][j] == graph[k][m] and
                                    graph[i][j] == graph[l][m]):
                                for n in range(m+1, size):
                                    if (graph[i][j] == graph[i][n] and
                                            graph[i][j] == graph[j][n] and
                                            graph[i][j] == graph[k][n] and
                                            graph[i][j] == graph[l][n] and
                                            graph[i][j] == graph[m][n]):
                                        cliqueCount += 1

    return cliqueCount
#
######################################################################


######################################################################
#
# findLocalMinRand
#
# Find a graph with a local minimum
# Input: graph
# Output: count, and flipped edge
#
def findLocalMinRand(tabuList, graph, numWorkers, failCount=999999):
    bestCount = failCount

    # Prep search space
    randomEdges = range(1, len(graph))
    random.shuffle(randomEdges)
    numWorkers = min(len(graph), numWorkers)

    # Iterate over the new edges
    i = 0
    for j in randomEdges[:len(graph)/numWorkers]:
        # Flip an edge
        graph[i][j] = 1 - graph[i][j]

        # Check the result of the flip
        cliqueCount = vert0CliqueCount(graph)

        # This was a good flip
        if cliqueCount < bestCount and not (i, j) in tabuList:
            bestCount = cliqueCount
            bestI = i
            bestJ = j

        # Unfilp the edge
        graph[i][j] = 1 - graph[i][j]


    if bestCount == failCount:
        return ()

    return (bestCount, bestI, bestJ)
#
######################################################################


######################################################################
#
# findLocalMinIter
#
# Find a graph with a local minimum
# Input: graph
# Output: count, and flipped edge
#
def findLocalMinIter(tabuList, graph, failCount=999999):
    bestCount = failCount

    # Iterate over the new edges
    i = 0
    for j in range(1, len(graph)):
        # Flip an edge
        graph[i][j] = 1 - graph[i][j]

        # Check the result of the flip
        cliqueCount = vert0CliqueCount(graph)

        # This was a good flip
        if cliqueCount < bestCount and not (i, j) in tabuList:
            bestCount = cliqueCount
            bestI = i
            bestJ = j

        # Unfilp the edge
        graph[i][j] = 1 - graph[i][j]


    if bestCount == failCount:
        return ()

    return (bestCount, bestI, bestJ)
#
######################################################################

def tabu(graph, type, numWorkers=1, maxSize=101):
    if type is '2Darray':
        _tabu(seed, numWorkers, maxSize)
    elif type is 'string':
        length = len(graph)
        graph_size = int(math.sqrt(length))
        g = [ [graph[i*graph_size + j] for j in xrange(graph_size)] for i in xrange(graph_size)]
        # print g
        maxSize = 1000
        _tabu(g, numWorkers, maxSize)


######################################################################
#
# tabu
#
# tabu search
# Input: graph, number of worker nodes
# Output: 
#
def _tabu(seed, numWorkers, maxSize):
    # Initialize the search space
    graph = copy.deepcopy(seed)
    cliqueCount = naiveCliqueCount(graph)
    tabuSize = len(graph)
    tabuDecrement = False

    # Make sure the seed is valid
    if cliqueCount != 0:
        print "Seed is not a counterexample for R(6, 6). Aborting."
        return

    # Create tabu list
    tabuList = OrderedSet.OrderedSet()

    # Start clock
    clockStart = time.clock()
    clockLastSolution = time.clock()

    # Tabu search
    while len(graph) <= maxSize:

        # Found a counterexample
        if cliqueCount == 0:

            # Check whether this is a new counterexample
            if tabuDecrement == False:

                # Timestamp solution
                clockFoundSolution = time.clock()

                debug("Found counterexample!\n")
                debug("Time elapsed since start: %f\n" % (clockFoundSolution-clockStart))
                debug("Time elapsed since last counterexample: %f\n" % (clockFoundSolution-clockLastSolution))

                clockLastSolution = clockFoundSolution

                # Print graph
                printGraph(graph)



              # TODO: Dispatch graph

            # This is the new seed
            seed = copy.deepcopy(graph)

            # Sanity check
            if naiveCliqueCount(graph) != 0:
                print "Error: Discrepancy between naive and vert0 counts. Aborting."
                sys.exit(1)

            # Add new vertex to adjacency matrix
            graphDim = len(graph)
            graph.insert(0, [])
            for i in range(graphDim):
                graph[0].append(0)
            for row in graph:
                row.insert(0, 0)

            # Update the clique-count
            cliqueCount = naiveCliqueCount(graph)

            # Reset the tabu list
            tabuList.clear()
            if tabuDecrement == True:
                    tabuSize = tabuSize - 1
                    tabuDecrement = False
            else:
                tabuSize = len(graph) / numWorkers 

            continue

        # Keep looking
        #best = findLocalMinIter(tabuList, graph)
        best = findLocalMinRand(tabuList, graph, numWorkers)

        # Could not find couterexample
        if len(best) == 0:

            # Try decreasing the tabu size
            if tabuSize >= 0:
                debug("Search failed, resetting tabuSize to %d.\n" % (tabuSize - 1))
                tabuDecrement = True
                graph = copy.deepcopy(seed)
                cliqueCount = 0
                continue

            # Should never get here -- tabu size of zero should run forever...
            print "Could not find counterexample for size %d." % (len(graph))
            return

        # Results of local search
        bestCount = best[0]
        bestI = best[1]
        bestJ = best[2]

        # Keep the best edge-flip
        graph[bestI][bestJ] = 1 - graph[bestI][bestJ]

        # Update the clique count
        cliqueCount = bestCount

        # Taboo this edge
        if tabuSize != 0:
            if len(tabuList) >= tabuSize:
                tabuList.pop(False)
            tabuList.add((bestI, bestJ))

        debug("[%d] " % (len(graph)))
        debug("Flipping (%d, %d), " % (bestI, bestJ))
        debug("clique count: %d, " % (cliqueCount))
        debug("taboo size: %d\n" % (tabuSize))
#
######################################################################


######################################################################
#
# TESTING
#
testGraph1 = \
        [[ 0, 0, 1, 0, 1, 0, 1, 0 ],
         [ 0, 0, 1, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
         [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
         [ 0, 0, 0, 0, 0, 0, 0, 0 ],
         [ 0, 0, 0, 0, 0, 0, 0, 0 ]]

g = "0100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010011100100100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010011100000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010011100000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010011100000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010011000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010010000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100010000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101100000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101101000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101100000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101100000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111101000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111100000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111100000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111111000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111110000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111100000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000111000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000110000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000100000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010110000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010100000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110010000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000110000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000100000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010100000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101010000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100101000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100100000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100100000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010100000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101010000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000101000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000100000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000100000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001100000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101001000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001101000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001100000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001100000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100001000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111100000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111111000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111110000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111100000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110111000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110110000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110100000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110110000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110100000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
tabu(g, type="string")
#
######################################################################