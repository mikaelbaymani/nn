#!/usr/bin/env python3
import os
import sys
sys.dont_write_bytecode = True
import pickle
import base64
import pandas as pd


from lsh import LSH
from dimport import Dimport
from base64 import b64decode
from sklearn.feature_extraction.text import TfidfVectorizer


class _Const( object ):
    from constant import constant
    @constant
    def DATASET():    return 'dataset.csv'
    @constant
    def MODEL():      return 'model.p'
CONST = _Const()
PATHNAME = lambda : os.path.dirname( sys.argv[0] )


def query( fname, key='key', topk=10, truncate=80 ):

    model = pickle.load( open(CONST.MODEL, 'rb') )

    dataframe = pd.read_csv( CONST.DATASET )
    corpus    = TfidfVectorizer().fit_transform( dataframe['content'] )

    lsh = LSH( corpus, model )
    index = dataframe[dataframe[key].apply( str ) == str( fname )].index[0]

    dataframe['content'] = dataframe['content'].str[:int( truncate )]
    return lsh.query( corpus[index,:], int( topk ), 10 )[0].join(dataframe, on='id').sort_values('distance').iloc[:,1:]




if __name__ == "__main__" :

    if "-h" in sys.argv or "--help" in sys.argv :
        print( "Usage: ./nn.py [OPTION]                                    \n\n"
               "   -h | --help        Show this help message and exit        \n"
               "   --fetch <plugin>   Fetch new data with proprietary plugin \n"
               "   --train            Train LSH model                        \n"
               "   --query <ID>       Nearest Neighbor query                 \n" )
        exit(0)


    if "--fetch" in sys.argv :
        pluginName = sys.argv[2].replace('.py', '')
        Dimport( "plugins.%s"%pluginName, pluginName )( CONST.DATASET )


    if "--train" in sys.argv :

        dataframe = pd.read_csv( PATHNAME() + "/" + CONST.DATASET )
        corpus    = TfidfVectorizer().fit_transform( dataframe['content'] )

        lsh = LSH( corpus )
        model = lsh.train()

        pickle.dump( model, open( CONST.MODEL, 'wb' ) )


    if "--query" in sys.argv :
        print( query( sys.argv[2] ) )
