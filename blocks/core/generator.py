from .blocks import get_subject_count
from .clash import *
from .evaluation import *
from .exceptions import BlockDataLengthMismatch, SubjectAlreadyExists

class BlockGenerator:
    '''Object which generates option blocks'''
    def __init__(self, data:Iterable[Iterable], options:Iterable, blocks:int, **opts) -> None:
        self.data = data
        self.options = options
        self.ignore = opts.get("ignore", [])
        self.blocks = [[] for _ in range(blocks)]
        self.class_size = opts.get("class_size", 30)
        self.min_clash = opts.get("min_clash", 3)

        self.strict = opts.get("strict", True)
    
        if self.strict and len(data[0]) != len(self.blocks):
            raise BlockDataLengthMismatch(
                "number of blocks does not match given length of options")
        # mapping to determine which subjects have been used and the number
        # of times they have been used. 
        self._used = {}

    def populate(self, blocks:Iterable[int], subjects:Iterable):
        '''add subject/s to the given blocks provided'''
        for subject in subjects:
            for pos in blocks:
                block = self.blocks[pos-1]
                if subject in block:
                    raise SubjectAlreadyExists(
                        "subject '%s' already exists in block '%s'" % (subject, pos)
                        )
                block.append(subject)
                
    def update_ignore(self, *subjects):
        '''ignores provided subjects during generation'''
        for subject in subjects:
            self.ignore.append(subject)

    def subject_block_clashes(self, subject:str):
        '''return a dictionary containing the blocks and their clash count with a given subject'''
        counts = {}
        for num, block in enumerate(self.blocks):
            blocks = [opt for opt in block if opt not in self.ignore]
            clashes = block_clashes(subject, blocks, self.data, err_msgs=False)
            counts.update({num:clashes})
        
        return {k:v for k,v in sorted(counts.items(), key=lambda x:x[1])}

    def populate_lowest(self, subject:str, max_use:int):
        '''populate the max number of blocks with a certain subject that have the smallest clash priority'''
        # checks each block and report which block clashes least with a given subject
        # it will then proceed to populate it and mark the subject as dealt with
        for _ in range(max_use):
            use_count = self._used.get(subject, 0)
            if use_count >= max_use or subject in self.ignore:
                return None
            priority = 0
            while priority < 4:
                block = tuple(self.subject_block_clashes(subject).keys())[priority]
                try:
                    self.populate((block+1,), (subject,))
                    self._used.update({subject:use_count+1})
                    # print("populating :", subject, "at block :", block + 1)
                    break
                except SubjectAlreadyExists:
                    priority += 1

    def build_class(self, iterable:dict, classes:int):
        '''classes with n numbers are appened to the blocks with the lowest clash priorities'''
        data = dict(filter(lambda x:x[1]["classes"] == classes, iterable.items()))
        for subject in data.keys():
            self.populate_lowest(subject, classes)

    def generate(self):
        '''Generates option blocks from a given set of data and options'''
        # get the counts and assign number of classes
        counts = get_subject_count(self.data, self.options)
        grouped = {k:{"count":v, "classes":int(v)//self.class_size+1} for k,v in counts.items()}
        # first deal with the subjects that are 4 or greater

        negligible = dict(filter(lambda x:x[1]["classes"] >= 4, grouped.items()))
        self.populate(range(1,len(self.blocks)+1), negligible)
        self.update_ignore(*negligible)

        singles = dict(filter(lambda x:x[1]["classes"] == 1, grouped.items()))
        # generate a class matrix to deal with single classes
        matrix = generate_clash_matrix(singles,self.data,ignore_subjects=self.ignore)
        priority = dict(filter(lambda x:x[1] >= self.min_clash, matrix.items()))

        for subjects in priority:
            first, second = subjects
            self.populate_lowest(first, max_use=1)
            self.populate_lowest(second, max_use=1)

        # deal with the remaining subjects that did not fall into the 
        # priority subjects

        remaining = [s for s in singles if s not in self._used.keys()]
        # populate the remaining single subjects
        for subject in remaining:
            self.populate_lowest(subject, 1)
        
        # populate rest of subjects starting from 2
        for classes in range(2, len(self.blocks)):
            self.build_class(grouped, classes)

    def evaluate(self, display=False):
        '''evaluate the set of option blocks generated'''
        return evaluate_blocks(self.blocks, self.data, display=display)

    
