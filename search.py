from __future__ import division, print_function
from ways import load_map_from_csv
'implement your search methods here'
from collections import namedtuple
 
Problem = namedtuple('Problem',['init_state','goal_func','expand','id']) 
Node = namedtuple('node', ['state','parent','h','g','f'])

class open_set(object):
    def __init__(self):
        pass
    
    def add(self, state):
        pass
    
    def remove(self, state):
        pass
    
    def pop_best(self):
        pass
 
    def find_state(self):
        pass

    def is_empty(self):
        pass
 
class close_set(object):
    def __init__(self):
        pass
    
    def add(self, state):
        pass
    
    def remove(self, state):
        pass

    def find_state(self, state):
        pass

def get_path(node):
    '''
    returns the path that ends in this node according to the parant pointers.
    '''
    path = [node]
    while path[0].parent:
        path = [path[0].parent]+path
    return [x.state for x in path]
 
def run_astar(problem,h_func,cost_func):
    #initializing the algorithm groups
    hi = h_func(problem.init_state)
    closed = close_set()
    opened = open_set()
    opened.add(Node(problem.init_state,None,hi,0,hi))

    while not opened.is_empty():
        next_node = opened.pop_best()
        closed.add(next_node)
        if problem.goal_func(next_node):
            return get_path(next_node)
        for s in problem.expand(next_node.state):
            new_g = next_node.g + cost_func(next_node.state,s)
            old_node = opened.find_state(s)
            if old_node: # a node with state s is in opened
                if new_g < old_node.g:
                    old_node.g = new_g
                    old_node.parent = next_node
                    old_node.f = old_node.g + old_node.h
                    opened.remove(old_node)
                    opened.add(old_node)
                else: # old path is better - do nothing
                    pass
            else: # state isn't in opened - maybe in closed
                old_node = closed.find_state(s)
                if old_node:
                    if new_g < old_node.g:
                        old_node.g = new_g
                        old_node.parent = next_node
                        old_node.f = old_node.g + old_node.h
                        closed.remove(old_node)
                        closed.add(old_node)
                    else: # old path is better - do nothing
                        pass
                else:
                    state_h = h_func(s)
                    new_node = Node(s,next_node,state_h,new_g,state_h+new_g)
                    open.add(new_node)
        return None


if __name__ == '__main__':
    'self test your code' 
    'note: assigning variables here make them global! use functions instead.'