from __future__ import division, print_function
from ways import load_map_from_csv, tools
'implement your search methods here'
from time import clock
from ways.tools import compute_distance
from random import randint

class Problem(object):
    def __init__(self, init_state, goal_func, expand, id_func):
        self.init_state = init_state
        self.goal_func = goal_func
        self.expand = expand
        self.id_func = id_func

class Node(object):
    def __init__(self, state, parent, h, g, f):
        self.state = state
        self.parent = parent
        self.h = h
        self.g = g
        self.f = f

class open_set(object):    
    def __init__(self):
        self.nodes_dict = {}
        self.nodes_f_val = {}
    
    def add(self, node):
        self.nodes_dict[node.state] = node
        self.nodes_f_val[node.state] = node.f
    
    def remove(self, node):
        self.nodes_dict.pop(node.state)
        self.nodes_f_val.pop(node.state)
    
    
    def pop_best(self):
        state = min(self.nodes_f_val, key=self.nodes_f_val.get)
        node = self.nodes_dict[state]
        self.remove(node)
        return node
 
    def find_state(self, state):
        return self.nodes_dict.get(state, None)

    def is_empty(self):
        return self.nodes_dict == {}
 
class close_set(object):
    def __init__(self):
        self.nodes = {}
    
    def add(self, node):
        self.nodes[node.state] = node
    
    def remove(self, node):
        self.nodes.pop(node.state)

    def find_state(self, state):
        return self.nodes.get(state, None)

def get_path(node):
    '''
    returns the path that ends in this node according to the parent pointers.
    '''
    path = [node]
    while path[0].parent:
        path = [path[0].parent] + path
    return [x.state for x in path]
 
def run_astar(problem, h_func, cost_func, time_limit = 2**100):
    start_time = clock()
    
    # initializing the algorithm groups
    hi = h_func(problem.init_state)
    closed = close_set()
    opened = open_set()
    opened.add(Node(problem.init_state, None, hi, 0, hi))

    while not opened.is_empty() and (clock() - start_time < time_limit):
        next_node = opened.pop_best()
        
        closed.add(next_node)
        if problem.goal_func(next_node.state):
            return get_path(next_node)
        for s in problem.expand(next_node.state):
            new_g = next_node.g + cost_func(next_node.state, s)
            old_node = opened.find_state(s)
            if old_node:  # a node with state s is in opened
                if new_g < old_node.g:
                    old_node.g = new_g
                    old_node.parent = next_node
                    old_node.f = old_node.g + old_node.h
                    opened.remove(old_node)
                    opened.add(old_node)
                else:  # old path is better - do nothing
                    pass
            else:  # state isn't in opened - maybe in closed
                old_node = closed.find_state(s)
                if old_node:
                    if new_g < old_node.g:
                        old_node.g = new_g
                        old_node.parent = next_node
                        old_node.f = old_node.g + old_node.h
                        closed.remove(old_node)
                        opened.add(old_node)
                    else:  # old path is better - do nothing
                        pass
                else:
                    state_h = h_func(s)
                    new_node = Node(s, next_node, state_h, new_g, state_h + new_g)
                    opened.add(new_node)
    return None


def calc_link_time(roads,link):
    return link.distance / (roads.link_speed(link) / 3.6)

def cost_func_gen(roads):
#     junctions = roads.junctions()
    def cost_func(id1, id2):
        j = roads[id1]
        for link in j.links:
            if link.target == id2:
                return calc_link_time(roads, link)
    return cost_func

def h_func_gen(roads, dest_id):
#     junctions = roads.junctions()
    dest = roads[dest_id]
    def h_func(j_id):
        j = roads[j_id]
        return (compute_distance(j.lat,j.lon,dest.lat,dest.lon) / 110) * 3600
        
    return h_func

def expand_gen(roads):
#     junctions = roads.junctions()
    def expand(j_id):
        j = roads[j_id]
        return [link.target for link in j.links]
    return expand

def calc_path_time(roads, path):
    tot = 0
#     junctions = roads.junctions()
    for i in range(len(path) - 1):
        j = roads[path[i]]
        for link in j.links:
            if link.target == path[i+1]:
                tot += calc_link_time(roads, link)
                break
    return tot

def simple(source, target):
    roads = load_map_from_csv('israel.csv')
    problem = Problem(init_state=source, goal_func=(lambda x: (x == target)), expand=expand_gen(roads), id_func=1)
    
    start_time = clock()
    path = run_astar(problem, h_func_gen(roads, target), cost_func_gen(roads))
    end_time = clock()
    
    print ("# of nodes:", len(path))
    print ("Run time:", end_time - start_time)
    print ("Path time:", calc_path_time(roads, path))
    print ("Huristic time:", h_func_gen(roads, target)(source))
    print ("Path:", path)
    return path

def run_astar_random(roads, time_limit = 300):
#     junctions = roads.junctions()
    source = randint(0, len(roads))
    target = randint(0, len(roads))
    
    problem = Problem(init_state=source, goal_func=(lambda x: (x == target)), expand=expand_gen(roads), id_func=1)
    
    start_time = clock()
    path = run_astar(problem, h_func_gen(roads, target), cost_func_gen(roads),time_limit)
    end_time = clock()
    if path:
        print ("----- From",source,"to",target,"-----")
        print ("# of nodes:", len(path))
        print ("Run time:", end_time - start_time)
        print ("Path time:", calc_path_time(roads, path))
        print ("Huristic time:", h_func_gen(roads, target)(source))
        print ("Path:", path)
    else:
        print (source,"and",target,"aren't connected!")
    return path
    
def run_twenty_paths():
    roads = load_map_from_csv('israel.csv')
    roads.generation = 0
    
    i=0
    while i<20:
        path = run_astar_random(roads)
        if path:
            i+=1
        

if __name__ == '__main__':
    'self test your code' 
    'note: assigning variables here make them global! use functions instead.'
#     run_twenty_paths()
    simple(171154,123198)
    
    
