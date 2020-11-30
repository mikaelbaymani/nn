import numpy as np
from copy import copy
from pandas import DataFrame
from itertools import combinations
from sklearn.metrics.pairwise import pairwise_distances


class LSH:
    # Locality Sensitive Hashing provides for a fast,  efficient approximate
    # nearest neighbor search. The algorithm scales well with the respect to
    # the number of data points as well as dimensions.
    def __init__( self, data, model = None ):
        self.data = data
        self.model = model


    # Generate a  collection of  random vectors  from  the standard Guassian
    # distribution.
    def __generate_random_vectors( self, numVector, dim ):
        return np.random.randn( dim, numVector )


    # Train the LSH model.
    # LSH performs an efficient neighbor search  by randomly partitioning all
    # reference data points into different bins.
    def train( self, numVector=10, seed=None ):

        dim = self.data.shape[1]
        if seed is not None:
            np.random.seed( seed )
        randomVectors = self.__generate_random_vectors( numVector, dim )

        powersOfTwo = 1 << np.arange( numVector-1, -1, -1 )

        table = {}

        # Partition data points into bins
        binIndexBits = ( self.data.dot(randomVectors) >= 0 )

        # Encode bin index bits into integers
        binIndices = binIndexBits.dot( powersOfTwo )

        # Update `table` so that `table[i]` is the list of document ids with
        # bin index equal to i.
        for dataIndex, binIndex in enumerate( binIndices ):
            if binIndex not in table:
                # If no  list yet  exists for this  bin,  assign the bin  an
                # empty list.
                table[binIndex] = []
            # Fetch the list of document ids associated with the bin and add
            # the document id to the end.
            table[binIndex].append( dataIndex )

        self.model = { 'binIndexBits': binIndexBits,
                       'binIndices': binIndices,
                       'table': table,
                       'randomVectors': randomVectors,
                       'numVector': numVector }

        return self.model


    # For a given query vector  and trained LSH model,  return all candidate
    # neighbors for the query among all bins within the given search radius.
    def __search_nearby_bins( self, queryBinBits, table, searchRadius=2, initialCandidates=set() ):
        numVector = len( queryBinBits )
        powersOfTwo = 1 << np.arange( numVector-1, -1, -1 )

        # Allow the user to provide an initial set of candidates.
        candidateSet = copy( initialCandidates )

        for differentBits in combinations( range(numVector), searchRadius ):
            alternateBits = copy( queryBinBits )
            for i in differentBits:
                alternateBits[i] = 1 if alternateBits[i] == 0 else 0

            # Convert the new bit vector to an integer index
            nearbyBin = alternateBits.dot( powersOfTwo )

            # Fetch  the list of documents belonging  to the bin indexed  by
            # the new bit vector. Then add those documents to candidateSet.
            if nearbyBin in table:
                candidateSet.update( set(table[nearbyBin]) )

        return candidateSet


    def query( self, vec, k, maxSearchRadius ):
        table = self.model['table']
        randomVectors = self.model['randomVectors']
        numVector = randomVectors.shape[1]

        # Compute bin index for the query vector, in bit representation.
        binIndexBits = ( vec.dot(randomVectors) >= 0 ).flatten()

        # Search nearby bins and collect candidates
        candidateSet = set()
        for searchRadius in range( maxSearchRadius+1 ):
            candidateSet = self.__search_nearby_bins(binIndexBits, table, searchRadius, initialCandidates=candidateSet)

        # Sort candidates by their true distances from the query
        nearestNeighbors = DataFrame( {'id':list(candidateSet)} )
        candidates = self.data[np.array(list(candidateSet)),:]
        nearestNeighbors['distance'] = pairwise_distances( candidates, vec, metric='cosine' ).flatten()

        return nearestNeighbors.nsmallest(k, 'distance'), len( candidateSet )
