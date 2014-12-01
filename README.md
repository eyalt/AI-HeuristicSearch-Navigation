#Homework 1 - Heuristic Search

The PDF for the assignment can found in [docs/AI_HW1.pdf](docs/AI_HW1.pdf?raw=true)

Library documentation can be found [here](ways/README.md)

##Directory Structure

###[`/`](http://github.com/TechnionAI/Win14_15_HW1)
Add your source files here, and insert calls for the functions in them inside [`main.py`](main.py). 

You can add directories for 3rd party libraries. Remember to declare `dir your_directory` in [`docs/dependencies.txt`](docs/dependencies.txt)

[`README.md`](README.md) This file

[`__init__.py`](__init__.py) A hint for the interpreter - ignore this file

[`main.py`](main.py) Minimal interface to the command line: `$ python main.py [args]`

[`stats.py`](stats.py) Gather and print statistics: `$ python stats.py`

___
###[`ways/`](ways/)
Primary library. Basic usage: 
```python
from ways import load_map_from_csv
roads = load_map_from_csv()
````
[`ways/README.md`](ways/README.md) Library documentation

[`ways/__init__.py`](ways/__init__.py) Defines the functions accessible using `import ways`

[`ways/graph.py`](ways/graph.py) Code to load the map from the database

[`ways/info.py`](ways/info.py) Constants

[`ways/tools.py`](ways/tools.py) Arbitrary, possibly useful tools

[`ways/draw.py`](ways/draw.py) Helper file for drawing paths using matplotlib

___

###[`docs/`](docs/)
Documentation

[`docs/AI_HW1.pdf`](docs/AI_HW1.pdf) Assignment file

[`docs/dependencies.txt`](docs/dependencies.txt) Declarations of dependencies in 3rd party libraries. For example:

> pip numpy
>

___
###[`db/`](db/)
Database. Do not change.

[`db/israel.csv`](db/israel.csv) Roads description. primary database file

[`db/lights.csv`](db/israel.csv) List of locations of traffic lights
___		
###[`results/`](results/)
Put your experiment results (text and images) here
