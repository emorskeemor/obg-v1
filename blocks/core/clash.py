from itertools import product, permutations
from typing import Iterable

# functions to generate clashes and find matches

def clash(subjects:Iterable, data:Iterable[Iterable]) -> int:
    '''
    Return a count of how many options contain an arbitrary set of subjects
    '''
    clash_count = 0
    for options in data:
        approved = 0
        for subject in subjects:
            if subject in options:
                approved += 1
        if approved == len(subjects):
            clash_count += 1
    return clash_count


def generate_clash_matrix(options:Iterable, data:Iterable[Iterable], value:int=2, ignore_subjects:tuple=None, reverse:bool=True) -> dict:
    '''
    Generates a sorted dict of clashes and their number of occurances.

    A value greater than three permuations make take a significant amount of time.
    '''
    if ignore_subjects is None:
        ignore_subjects = ()
    clashes={}
    # filter the options
    options = tuple(filter(lambda opt: opt not in ignore_subjects, options))
    for comparission in permutations(options, value):
        if len(set(comparission)) == int(value):
            comparission = tuple(sorted(comparission))
            clashes.update(
                {comparission: clash(comparission, data)}
                )
    
    return {k:v for k,v in sorted(clashes.items(), key=lambda x:x[1], reverse=reverse)}

def display_clashes(clashes:dict, value:int):
    '''
    Display clashes that match a specific value
    '''
    print("\nDisplaying clashes that match '%i'" % value)
    count = 0
    for k, v in clashes.items():
        if v==value:
            print(f"=>{k}")
            count += 1
    print("\nNumber of clashes :", count)

def match(data:Iterable[Iterable], *subjects):
    '''
    Display all options that match an arbitrary set of subjects
    '''
    for options in data:
        num = 0
        for subject in subjects:
            if subject in options:
                num += 1
        if num == len(subjects):
            yield options

def pprint_exact_matches(data:Iterable[Iterable], subjects:Iterable, display=False):
    count = 0
    for subs in match(data, *subjects):
        if display:
            print(subs)
        count += 1
    return count
    

def block_clashes(subject:str, block:Iterable, data:Iterable[Iterable], display_subjects=False, err_msgs=True):
    '''
    Displays internal clashes between a subject and its block
    '''
    total_clash_count = 0
    for opt in block:
        result = tuple(match(data, subject, opt))
        if result and subject != opt:
            clash_count = 0
            for fail in result:
                if display_subjects:
                    print(f"=> {fail}")
                clash_count += 1
            if err_msgs:
                print(f"> Clashes with '{opt}' of count : {clash_count}'")
            total_clash_count += clash_count
    return total_clash_count


