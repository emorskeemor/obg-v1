from csv import reader
import os

# base dir is the 
BASE_DIR = os.path.join(os.getcwd(), __package__.split(".")[0])

def read_static(name:str):
    '''read from a file in static root folder'''
    with open(os.path.join(STATIC_ROOT, name), "r") as f:
        return tuple(reader(f, delimiter=","))

# data files
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DATA_FILE_NAME = "data.csv"
OPTIONS_FILE_NAME = "options.csv"
BLOCKS_FILE_NAME = "blocks.csv"

# get data
DATA = [opts[:4] for opts in read_static(DATA_FILE_NAME)]
OPTIONS = [opts[1] for opts in read_static(OPTIONS_FILE_NAME)]
BLOCKS = [opts for opts in read_static(BLOCKS_FILE_NAME)]
