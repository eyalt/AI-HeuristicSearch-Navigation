'''
 A set of utilities for using israel.csv 
 The map is extracted from the openstreetmap project
'''
from __future__ import print_function
from collections import namedtuple
import tools
import info
import sys

# define class Link
Link = namedtuple('Link',
       ['source', 'target',  #  int (junction indices)
        'distance',          #  float
        'highway_type',      #  int < len(road_info.ROAD_TYPES)
       ])


# define class Junction
Junction = namedtuple('Junction',
           ['index',       #  int
            'lat', 'lon',  #  floats: latitude/longitude
            'links',       #  list of Link
           ])


class Roads(dict):
    '''The graph is a dictionary Junction_id->Junction, with some methods to help.
    To change the generation, simply assign to it:
    g.generation = 5
    '''
    def junctions(self):
        return self.values()
    
    def __init__(self, junction_list, lights):
        super(Roads, self).__init__(junction_list)
        self._LIGHTS = lights
        'to change the generation, simply assign to it'
        self.generation = 0
        
    def has_traffic_lights(self, junction):
        'self.generation is an implicit argument'
        ilat, ilon = (int(junction.lat * info.L_FACTOR), int(junction.lon * info.L_FACTOR))
        return (ilat, ilon) in self._LIGHTS
    
    def link_speed(self, link):
        '''`decides` (deterministically) a reasonable speed for the link.'''
        def has_traffic_jam():
            return not bool(tools.dhash(link, self.generation) % info.TRAFFIC_JAM_PARAM)
        
        if not has_traffic_jam():
            bot, top = info.SPEED_RANGES[link.highway_type]
            return tools.dhash(link) % (top - bot) + bot
        return 5

    def iterlinks(self):
        '''chain all the links in the graph. 
        use: for link in roads.iterlinks(): ... '''
        return (link for j in self.values() for link in j.links)


def _make_junction(i_str, lat_str, lon_str, *link_row):
    'This function is for local use only'
    i, lat, lon = int(i_str), float(lat_str), float(lon_str)
    try:
        links = tuple(Link(i, *[int(x) for x in lnk.split("@")])
                 for lnk in link_row)
    except ValueError:
        links = []
    return Junction(i, lat, lon, links)


@tools.timed
def load_map_from_csv(filename='israel.csv', start=0, count=sys.maxint):
    '''returns graph, encoded as an adjacency list
    @param slice_params can be used to cut part of the file
    example: load_map_from_csv(start=50000, count=50000))
    '''

    import csv
    from itertools import islice
    with tools.dbopen(filename, 'rb') as f:
        it = islice(f, start, min(start+count, sys.maxint))
        lst = {int(row[0]):_make_junction(*row) for row in csv.reader(it)}
        if count < sys.maxint:
            lst = {i:Junction(i, j.lat, j.lon, tuple(lnk for lnk in j.links if lnk.target in lst))
                              for i, j in lst.items()}
    return Roads(lst, load_lights())
    

def load_lights():
    with tools.dbopen('lights.csv') as f:
        'factor since equality makes no sense for floats'
        return frozenset(tuple(int(float(i) * info.L_FACTOR) 
                                for i in line.strip().split(','))
                            for line in f)
