from typing import Iterable, Tuple
import random
import copy
import csv
import random
import os
from blocks.core.evaluation import get_subject_count
from blocks.core.exceptions import LengthMismatch, SubjectNonExistent
from blocks.core import STATIC_ROOT

class DummyGenerator:
    '''
    Generate dummy data
    '''
    def __init__(self, number_of_options:int, **opts) -> None:
        self.subject_counts = opts.get("subject_counts", None)
        self.clashes = opts.get("clashes", None)
        self.number_of_options = number_of_options
        self.opts = opts
        # set initials
        self.data = []
        self._init = {}



    def _decrement(self, subject):
        count = self.subject_counts.get(subject, None)
        if count is None:
            raise SubjectNonExistent(subject)
        elif count <= 0:
            return self.subject_counts.pop(subject)

        self.subject_counts[subject] = count - 1
        return True

    def _generate_clash(self, clash:Tuple[str,str], count:int):
        try:
            for _ in range(count):
                populated = [*clash]
                for sub in populated:
                    self._decrement(sub)
                subjects = [s for s in self.subject_counts.keys() if s not in populated]
                remaining = self.number_of_options - len(populated)

                while remaining > 0:
                    if not subjects:
                        break
                    # pick a random subject and populate our student and decrement it
                    # from overall
                    choice = random.choice(subjects)
                    if self._decrement(choice):
                        populated.append(choice)
                        remaining -= 1
                    subjects.remove(choice)
                # assert len(set(populated)) >= self.opts.get("min_opts")
                if len(populated) >= self.opts.get("min_opts"):

                    self.data.append(populated)
        except SubjectNonExistent as e:
            # print("stoped iteration due to :", e)
            pass

    def _validate_clash(self, subject, count):
        sub_count = self.subject_counts.get(subject)
        if count > sub_count:
            raise LengthMismatch(
                "'%s' occurs only '%s' times which cannot clash '%s' times" 
                % (subject, sub_count, count)
                ) 
                    
    def generate(self):
        assert self.subject_counts is not None, "set 'subject_counts'"
        assert self.clashes is not None, "set 'clashes'"
        ordered_clashes = {k:v for k,v in sorted(
            self.clashes.items(), key=lambda x:x[1])}
        # validate the clashes
        for clash, count in ordered_clashes.items():
            one, two = clash
            self._validate_clash(one, count)
            self._validate_clash(two, count)

        # start to populate with the smallest clashes being priority
        for clash, count in ordered_clashes.items():
            self._generate_clash(clash, count)

        # remaining = copy.copy(self.subject_counts)
        # for subj, count in remaining.items():
        #     self._generate_clash((subj,), count)

        return self.data

    def generate_random_clashes(self, iters:int, minimum:int):
        assert self.subject_counts is not None, "set 'subject_counts'"
        counts = self.subject_counts
        generated = {}
        for _ in range(iters):
            copied_counts = copy.copy(counts)
            # first get two random options
            one = random.choice(tuple(copied_counts.keys()))
            choice_one = one
            choice_one_counts = copied_counts.pop(choice_one)
            choice_two = random.choice(tuple(copied_counts.keys()))
            
            maximum = sorted([choice_one_counts,counts.get(choice_two)])[0]
            assert minimum < maximum, "minimum 'clash_counts' is greater than a generated maximum '%s'" % maximum
            generated.update({(choice_one,choice_two):random.randint(minimum, maximum)})

        self.clashes = generated
        self._init["clashes"] = generated
        return generated

    def generate_random_counts(self, ranges:list, class_length:int):
        '''
        generate a dict from an already existing data set. Provide 'data'
        and 'options' variables on init.
        '''
        data = self.opts.get("data")
        options = self.opts.get("options")
        data_set = get_subject_count(data, options)
        generated = {}
        for subject, count in data_set.items():
            classes = count // class_length 
            if classes > 3:
                classes = 3
            minimum, maximum = ranges[classes]
            generated.update(random_bias_count(subject,minimum,maximum))
        self.subject_counts = generated
        self._init["subjects"] = tuple(generated.keys())
        self._init["subject_counts"] = copy.copy(generated)
        return generated

    def save(self,file_name:str, path=None):
        if path is None:
            # if there is no path given, default to static root
            path = STATIC_ROOT
        writer = csv.writer(
            open(os.path.join(path, "%s.csv" % file_name), "w", newline=""))
        writer.writerows(self.data)

        

    def display_dummy(self):
        '''display data about generated students'''
        print("\nDisplaying dummy data:")
        print("Number of students generated :", len(self.data))
        print("Remaining subjects :", self.subject_counts)
        print("Default clashes generated :", self._init["clashes"])
        print("Default subject counts :", self._init["subject_counts"], "\n")

def random_bias_count(subject:str, minimum:int, maximum:int):
    return {subject:random.randint(minimum, maximum)}


