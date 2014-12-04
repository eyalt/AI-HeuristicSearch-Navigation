from __future__ import division, print_function
from ways import load_map_from_csv, tools
'implement your search methods here'
from time import clock
from ways.tools import compute_distance
from random import randint
from ways.graph import Roads
import random

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
 
def run_astar(problem, h_func, cost_func, time_limit=2 ** 100):
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


def calc_link_time(roads, link):
    return link.distance / (roads.link_speed(link) / 3.6)

def simple_cost_func_gen(roads):
#     junctions = roads.junctions()
    def cost_func(id1, id2):
        j = roads[id1]
        for link in j.links:
            if link.target == id2:
                return calc_link_time(roads, link)
    return cost_func

def lights_cost_func_gen(roads, w):
    simple_g = simple_cost_func_gen(roads)
    def cost_func(id1, id2):
        j = roads[id1]
        for link in j.links:
            if link.target == id2:
                return simple_g(id1, id2) + w * roads.has_traffic_lights(j)
    return cost_func

def simple_h_func_gen(roads, dest_id):
#     junctions = roads.junctions()
    dest = roads[dest_id]
    def h_func(j_id):
        j = roads[j_id]
        return (compute_distance(j.lat, j.lon, dest.lat, dest.lon) / 110) * 3600
    return h_func

def lights_h_func_gen(roads, dest_id, w):
    return simple_h_func_gen(roads, dest_id)

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
            if link.target == path[i + 1]:
                tot += calc_link_time(roads, link)
                break
    return tot

def lights(source, target):
    source = int(source)
    target = int(target)
    w = 30
    roads = load_map_from_csv('israel.csv')
    problem = Problem(init_state=source, goal_func=(lambda x: (x == target)), expand=expand_gen(roads), id_func=1)
    
    start_time = clock()
    path = run_astar(problem, lights_h_func_gen(roads, target, w), lights_cost_func_gen(roads, w))
    end_time = clock()
    
    print ("# of nodes:", len(path))
    print ("Run time:", end_time - start_time)
    print ("Path time:", calc_path_time(roads, path))
    print ("Huristic time:", lights_h_func_gen(roads, target, w)(source))
    print ("Path:", path)
    return path

def simple(source, target):
    source = int(source)
    target = int(target)
    roads = load_map_from_csv('israel.csv')
    problem = Problem(init_state=source, goal_func=(lambda x: (x == target)), expand=expand_gen(roads), id_func=1)
    
    start_time = clock()
    path = run_astar(problem, simple_h_func_gen(roads, target), simple_cost_func_gen(roads))
    end_time = clock()
    
    print ("# of nodes:", len(path))
    print ("Run time:", end_time - start_time)
    print ("Path time:", calc_path_time(roads, path))
    print ("Huristic time:", simple_h_func_gen(roads, target)(source))
    print ("Path:", path)
    return path

def run_astar_random(roads, time_limit=300):
#     junctions = roads.junctions()
    source = randint(0, len(roads))
    target = randint(0, len(roads))
    
    problem = Problem(init_state=source, goal_func=(lambda x: (x == target)), expand=expand_gen(roads), id_func=1)
    
    start_time = clock()
    path = run_astar(problem, simple_h_func_gen(roads, target), simple_cost_func_gen(roads), time_limit)
    end_time = clock()
    if path:
        print ("----- From", source, "to", target, "-----")
        print ("# of nodes:", len(path))
        print ("Run time:", end_time - start_time)
        print ("Path time:", calc_path_time(roads, path))
        print ("Huristic time:", simple_h_func_gen(roads, target)(source))
        print ("Path:", path)
    else:
        print (source, "and", target, "aren't connected!")
    return path
    
def run_twenty_paths():
    roads = load_map_from_csv('israel.csv')
    roads.generation = 0
    
    i = 0
    while i < 20:
        path = run_astar_random(roads)
        if path:
            i += 1
        

def assured(source, target, time, confidence, time_limit=2 ** 100, roads=None):
    k = randint(1, 100)
    return assured_k(source, target, time, confidence, k, time_limit, roads)

def assured_k(source, target, time, confidence, k, time_limit=2**100, roads=None):
    generations = random.sample(range(100), k)
    return assured_gens(source, target, time, confidence, generations, time_limit, roads)

def assured_gens(source, target, time, confidence, generations, time_limit=2**100, roads=None):
    source = int(source)
    target = int(target)
    time = int(time)
    confidence = float(confidence)
    print ("Have %d generations. confidence set to %f" % (len(generations), confidence))
    print ("Generations:", ",".join([str(gen) for gen in sorted(generations)]))
    
    if roads is None:
        roads = load_map_from_csv('israel.csv')
    
    # calculate best path for each given generation
    paths = []
    for gen in sorted(generations):
        roads.generation = gen
        problem = Problem(init_state=source, goal_func=(lambda x: (x == target)), expand=expand_gen(roads), id_func=1)
        
        start_time = clock()
        path = run_astar(problem, simple_h_func_gen(roads, target), simple_cost_func_gen(roads), time_limit)
        print ("gen %d: %f seconds" % (gen, clock() - start_time))
        
        if path:
            paths.append(path)
    print ("")
    
    # for each path calculate all the N times
    paths_times = {}
    for i, path in enumerate(paths):
        for j in range(100):
            roads.generation = j
            paths_times[i] = paths_times.setdefault(i, []) + [calc_path_time(roads, path)]
        print ("paths_times[%d] = %s" % (i, paths_times[i]))
    
    # leave only the ones who are assuring        
    good_gens_number_for_path = {i:len([t for t in paths_times[i] if t < time * 60]) for i in paths_times}  # i : number of generations path is safe
    print ("good_gens_number_for_path:")
    print ("\n".join(("%d: %d" % (i, good_gens_number_for_path[i]) for i in good_gens_number_for_path)))
    confident_ids = [i for i in good_gens_number_for_path if good_gens_number_for_path[i] >= confidence]
    print ("Confident ids:", ",".join([str(i) for i in confident_ids]))
    print ("Found %d confident ids" % (len(confident_ids,)))
    print("")
    
    if not confident_ids:
        return None
    
    # return the assured path with the best average
    return paths[min(confident_ids, key=lambda x: sum(paths_times[x]))]



if __name__ == '__main__':
    'self test your code' 
    'note: assigning variables here make them global! use functions instead.'
#     run_twenty_paths()
    roads = load_map_from_csv('israel.csv')

# this is for question 10. show path with and w/o lights
#     simple_path = simple(171154, 123198)
#     lights_path = lights(171154, 123198)
#     draw.plot_path(roads, simple_path, color='g')
#     draw.plot_path(roads, lights_path, color='r')
#     draw.plot_lights()
#     draw.plt.show()
    
    # 20 assured problems
    problems = [('171154', '123198', '2559.85192632'),
               ('495228', '89206', '5142.67398152'),
               ('341367', '238100', '6752.41353903'),
               ('833329', '224195', '14132.4098235'),
               ('795682', '891696', '1929.33995947'),
               ('617408', '796958', '11590.1877365'),
               ('358948', '581591', '5386.10853204'),
               ('925582', '587144', '8481.35736499'),
               ('938317', '795849', '4642.23155003'),
               ('452775', '546678', '4464.65691943'),
               ('111972', '360880', '5758.15112434'),
               ('532801', '190496', '3914.73694707'),
               ('671054', '449796', '5548.53555159'),
               ('863989', '733531', '3819.64041675'),
               ('764425', '565724', '6193.99339083'),
               ('812157', '914568', '6880.36468259'),
               ('366137', '877341', '2094.81115949'),
               ('781267', '505105', '8751.7385419'),
               ('625831', '502267', '11163.1873778'),
               ('437053', '470689', '5947.59750186')]
    
    for source,target,sec_time in problems:
        k, p, T = 5, 50.0, (float(sec_time)/60)*1.11
        print ("----- From", source, "to", target, "-----")
        print ("k = %d, p = %f, T = %f minutes" % (k, p, T))
        path = assured_k(source=source,target=target,time=T, confidence=p, k=k, roads=roads)
        if path:
            print ("# of nodes:", len(path))
            print ("Path time:", calc_path_time(roads, path))
            print ("Path:", path)
        else:
            print ("No assured path")
        print("")
            
        p = 73.0
        print ("----- From", source, "to", target, "-----")
        print ("k = %d, p = %f, T = %f minutes" % (k, p, T))
        path = assured_k(source=source,target=target,time=T, confidence=p, k=k, roads=roads)
        if path:
            print ("# of nodes:", len(path))
            print ("Path time:", calc_path_time(roads, path))
            print ("Path:", path)
        else:
            print ("No assured path")
        print("")
        print("---------------------------------------------------------------")
        print("")
