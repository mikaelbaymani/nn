import sys
from importlib import import_module


class Dimport:

    def __init__( self, moduleName, methodName, pathTo = None):
        if pathTo:
            # the pathTo contains module
            sys.path.append( pathTo )
        # import_module method used to fetch module
        mod = import_module( moduleName )
        # getting attribute by getattr() method
        self.method = getattr( mod, methodName )


    def __call__( self, *args, **kwargs ):
        return self.method(*args, **kwargs)
