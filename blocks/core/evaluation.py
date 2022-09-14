
import copy
from typing import Iterable

def get_subject_count(data, options):
    subjects = dict.fromkeys(options, 0)
    for options in data:
        for subject in options:
            if subject:
                count = subjects.get(subject, None)
                if count is not None:
                    count += 1
                subjects.update({subject:count})
    return {k:v for k, v in sorted(subjects.items(), key=lambda x:x[1], reverse=True)}

def count_options(options:list, blocks:Iterable[Iterable]):
    counts = {}
    for option in options:
        num = 0
        for block in blocks:
            if block is not None and option in block:
                num += 1
        counts[option] = num
    return {k:v for k, v in sorted(counts.items(), key=lambda x:x[1])}

def evaluate(blocks:Iterable[Iterable], *options, display=False):
    '''evaluate four subjects against the option blocks'''
    if display:
        print("\nEvaluating options : ", options)
    # copy and set some initial variables
    blocks = copy.deepcopy(blocks)
    options:list = copy.copy(list(options))
    repetitions = len(options)
    required = [None] * len(blocks)
    cleared = 0
    iters = 0
    # go through each option and see if it can fit in the option blocks
    # prioritise the lowest number of occurances of that subject if any.
    while iters < repetitions:
        counts = count_options(options, blocks)
        # get the first item in the dictionary to deal with priorities
        subject, value = tuple(counts.items())[0]
        # if there are no occurances of a subject it does not exist or can no longer
        # fit in the option blocks
        if value == 0 and display:
            print(f"WARNING : '{subject}' could not be evaluated")
        for n, block in enumerate(blocks):
            if block is not None and subject in block:
                # set the block to None to declare we've dealt it
                cleared += 1
                blocks[n] = None
                required[n] = subject
                break
        iters += 1
        options.remove(subject)
    # display some evaluation
    if display:
        print("Constructed :", required)
        if cleared == repetitions:
            print("=> Evaluation successful")
            return True
        print("=> Evaluation failed")
        return False
    else:
        return cleared == repetitions

def evaluate_blocks(blocks:Iterable[Iterable], data:Iterable[list], display=True):
    '''evaluate all options in data against option blocks. Displays success rate
    of option blocks'''
    success_count = 0
    failed = []
    # evaluate each option
    for options in data:
        if "" in options:
            options.remove("")
        eval = evaluate(blocks, *options, display=display)
        if eval is True:
            success_count += 1
        else:
            failed.append(options)
    # display overall results
    count = len(data)
    percent = round(success_count / len(data) * 100, 2)
    if display:
        print("\n<Displaying results>")
        print(r"Success counts :", success_count)
        print(r"total failed :", count - success_count)
        print(r"total number of options :", count)
        print(r"% success :", percent)
    return {"success":success_count, "total":count, "percentage": percent}
