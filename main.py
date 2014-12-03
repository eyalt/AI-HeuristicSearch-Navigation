'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''
from __future__ import division, print_function
import search
# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions


def simple(source, target):
    'call function to find path, and return list of indices'
    return search.simple(source, target)

    
def lights(source, target):
    'call function to find path, and return list of indices'
    return search.lights(source, target)
    

def assured(source, target, time, confidence):
    'call function to find path, and return list of indices'
    raise NotImplementedError


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'simple':
        path = simple(source, target)
    elif argv[1] == 'lights':
        path = lights(source, target)
    elif argv[1] == 'assured':
        time, confidence = int(argv[4]), float(argv[5])
        path = assured(source, target, time, confidence)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
