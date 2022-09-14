# option-block-generator-v1
 option-block-generator-v1

Data

Test data has already been provided in static/data.csv and options have also been provided in static/options.csv
These csv files are read when the blocks/core module is imported

Running

run 'main.py' should automatically run the block generator. 

Modules

The 'core' module is responsible for all the option block generation
The 'cli' module was just some code i used when finding a way to generate option blocks. I needed a way to interact with code
easily so i created an object to help me run functions from the cli.
The 'test' module was me just playing around trying to generate a set of data so that I could test it. 
The 'util' module has some code to help integrate with Django

cmd.py

Run cmd.py to run a function that has been registered in the manager. To see commands, type 'py cmd.py cmds' into the cli
