'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''
from __future__ import division, print_function
from collections import namedtuple
from ways import load_map_from_csv, info
import collections


# Q7:
def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    junctions = roads.junctions()
    
    linksNum = [len(j.links) for j in junctions]
    
    typeHist = collections.Counter()
    for lnk in roads.iterlinks():
        typeHist[info.ROAD_TYPES[lnk.highway_type]] += 1
    
    return {
        'Number of junctions' : len(junctions),
        'Number of links' : sum(linksNum),
        'Outgoing branching factor' : Stat(max=max(linksNum),
                                            min=min(linksNum), 
                                            avg=sum(linksNum)/float(len(linksNum))),
        'Link distance' : Stat(max=max(l.distance for l in roads.iterlinks()), min=min(l.distance for l in roads.iterlinks()), avg=sum(l.distance for l in roads.iterlinks())/float(len(list(roads.iterlinks())))),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : dict(typeHist),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
