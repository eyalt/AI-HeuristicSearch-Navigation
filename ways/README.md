#`ways`
Library for handling road map.

Most of the work is done with one function, `load_map_from_csv`, and three classes: `Junction`, `Link` and `Roads`.

##Functions

#####[`load_map_from_csv(filename='israel.csv', start=0, count=sys.maxint)`](graph.py#L74)` -> `[`Roads`](#roads)
The workhorse of the library.

The basic usage is simple:
```python
from ways import load_map_from_csv
roads = load_map_from_csv()
# work with road
```
This function takes some time to finish. To test your code on smaller maps, use `count`:
```python
roads = load_map_from_csv(count=10000)
```

And you can add `start` argument to work in more "interesting" regions:
```python
roads = load_map_from_csv(start=100000, count=10000)
```

##Classes
###tl;dr
`Roads` is a mapping from integers (Junction index) to `Junction`, which has a list of `links` in it.

###Details
[`Link`](graph.py#L12) and [`Junction`](graph.py#L12) are [`namdetuple`](https://docs.python.org/2/library/collections.html#collections.namedtuple) - which means they are tuple-like and immutable.

####`Junction`

* `index` : `int` Junction index
* `lat` : `float` Latitude
* `lon` : `float` Longitude
* `links` : `list(Link)`

####`Link`

* `source` : `int` Junction index
* `target` : `int` Junction index
* `distance` : `float` Meters
* `highway_type` : `int` See [`info.py`](info.py#L7)

####[`Roads`](graph.py#L27)
The graph is a dictionary mapping Junction index to `Junction`, with some additional methods.

This is the return type of [`load_map_from_csv`](#functions).

#####Methods
All the methods for [`dict`](https://docs.python.org/2/library/stdtypes.html#mapping-types-dict) are available here too. For example, `roads[15]` is the Junction whose index is 15.

* [`iterlinks`](graph.py#L56)`(self) -> iterable(Link)`
   Chains all the links in the graph. ```for link in road.iterlinks(): ...```

* [`junctions`](graph.py#L32)`(self) -> list(Junction)`
   Iterate over the junctions in the road. Returns the values in the dictionary.

* [`has_traffic_lights`](graph.py#L41)`(self, junction) -> bool`
   Check if `link` has traffic lights, based on the file [`db/lights.txt`](../db/lights.txt).

* [`link_speed`](graph.py#L46)`(self, link)`
   Returns the speed for the link (in km/h), based on  `self.generation`.


#####Fields

* `generation` : `int`

   Represents the "sanpshot" of the speeds in the graph. This field is used by `link_speed` to decide the speed of a link for a specific generation.

   You can write and read freely to/from this field. 
