#!/usr/bin/python

#
# tabu.py
#
# Tabu search for counterexamples to R(6, 6)
#

DEBUG = True
DEBUG = False

import sys, pickle, time, OrderedSet

#
# debug
#
# Toggle debugging output
#
def debug(msg):
    if DEBUG:
        print "DEBUG: %s" % (msg)

#
# printGraph
#
# Print the graph to stdout
# Input: graph
#
def printGraph(graph):
    print "Size: %d" % (len(graph))
    for row in graph:
        print row

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
# findLocalMinRand
#
# Find a graph with a local minimum
# Input: graph
# Output: count, and flipped edge
#
def findLocalMinRand(tabuList, graph, failCount=999999):
    debug("Entering findLocalMin()")
    bestCount = failCount

    # Iterate over the new edges
    i = 0
    randEdges = range(len(graph))
    random.shuffle(randEdges)
    for j in randEdges:
        # Flip a random edge
        graph[i][j] = 1 - graph[i][j]

        # Check the result of the flip
        cliqueCount = vert0CliqueCount(graph)
        debug(">   local cliqueCount: %d" % (cliqueCount))

        # This was a good flip
        if cliqueCount < bestCount and not (i, j) in tabuList:
            debug(">   Updating bestCount")
            bestCount = cliqueCount
            bestI = i
            bestJ = j

        # Unfilp the edge
        graph[i][j] = 1 - graph[i][j]

    debug("Leaving findLocalMin()")

    if bestCount == failCount:
        return ()

    return (bestCount, bestI, bestJ)

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
        #print "count: %d, best: %d, i: %d, j: %d" % (cliqueCount, bestCount, i, j)

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
# tabu
#
# tabu search
# Input: graph, max graph size
# Output: 
#
def tabu(graph, tabuSize, failCount=999999, maxSize=101):
    size = len(graph) 

    cliqueCount = naiveCliqueCount(graph)

    # Create tabu list
    tabuList = OrderedSet.OrderedSet()

    # Start clock
    clockStart = time.clock()
    clockLastSolution = time.clock()

    while len(graph) <= maxSize:
        debug("tabu cliqueCount: %d" % (cliqueCount))

        # Found a counterexample
        if cliqueCount == 0:

            # Timestamp solution
            clockFoundSolution = time.clock()

            # Sanity check
            if naiveCliqueCount(graph) != 0:
                print "Error: Discrepancy between naive and vert0 counts. Abort"
                sys.exit(1)

            print "Found counterexample!"
            print "Time elapsed since start: %f" % (clockFoundSolution-clockStart)
            print "Time elapsed since last counterexample: %f" % (clockFoundSolution-clockLastSolution)

            clockLastSolution = clockFoundSolution

            # Print graph
            printGraph(graph)

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

            continue

        # Keep looking
        best = findLocalMinIter(tabuList, graph)

        # Could not find couterexample
        if len(best) == 0:
            print "Could not find counterexample for size %d" % (len(graph))
            return

        bestCount = best[0]
        bestI = best[1]
        bestJ = best[2]

        # Keep the best edge-flip
        debug("Flipping (%d, %d)" % (bestI, bestJ))
        graph[bestI][bestJ] = 1 - graph[bestI][bestJ]

        # Update the clique-count
        cliqueCount = naiveCliqueCount(graph)

        # Taboo this edge
        if len(tabuList) >= tabuSize:
            tabuList.pop(False)
        tabuList.add((bestI, bestJ))

        print "[%d] Flipping (%d, %d), clique count: %d, taboo size: %d" % (len(graph), bestI, bestJ, bestCount, tabuSize)

testGraph1 = \
        [[ 0, 0, 1, 0, 1, 0, 1, 0 ],
         [ 0, 0, 1, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
         [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
         [ 0, 0, 0, 0, 0, 0, 0, 0 ],
         [ 0, 0, 0, 0, 0, 0, 0, 0 ]]


testGraph2 = \
        [[ 0, 1, 0, 1, 0, 1, 0, 1 ],
         [ 0, 0, 1, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 1, 0, 1, 0, 1 ],
         [ 0, 0, 0, 0, 1, 0, 1, 0 ],
         [ 0, 0, 0, 0, 0, 1, 0, 1 ],
         [ 0, 0, 0, 0, 0, 0, 1, 0 ], 
         [ 0, 0, 0, 0, 0, 0, 0, 1 ],
         [ 0, 0, 0, 0, 0, 0, 0, 0 ]]

tabu(testGraph1, 20)
