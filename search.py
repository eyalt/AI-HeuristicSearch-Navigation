from __future__ import division, print_function
from ways import load_map_from_csv
'implement your search methods here'
from collections import namedtuple
 
Problem = namedtuple('Problem',['init_state','goal','expand','id']) 
Node = namedtuple('node', ['state','parent','h','g','f'])
 
def run_astar(problem,h_func,g_func):
    hi = h_func(problem.init_state)
    open = [Node(problem.init_state,None,hi,0,hi)]
    while open:
        next = open.pop(0)
    



if __name__ == '__main__':
    'self test your code' 
    'note: assigning variables here make them global! use functions instead.'