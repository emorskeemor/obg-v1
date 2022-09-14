from blocks.util.cli import CliManager
from blocks.core import DATA, OPTIONS, BLOCKS
from blocks.core.clash import *
from blocks.core.evaluation import *
from blocks.test.dummy_cli import DummyCliGenerator

from sys import argv

class Manager(CliManager):
    def __init__(self, **opts) -> None:
        super().__init__(**opts)

    def build(self):
        evaluate_blocks(BLOCKS, DATA)
        # build(DATA)

    def m_matrix(self, iters=2, matching=2):
        '''displays clashes from a given number of iters matching a certain value'''
        generated = generate_clash_matrix(
            OPTIONS, DATA, 
            value=int(iters), 
            ignore_subjects=self.opts.get("ignore_subjects", ())
            )
        display_clashes(generated, value=int(matching))

    def matrix(self, iters=2, *subjects):
        '''displays ordered clashes'''
        ignore_subjects = self.opts.get("ignore_subjects", ())

        print("displaying clash table matrix ignore subjects :", ignore_subjects)
        if not subjects:
            subjects = [opt for opt in OPTIONS if opt not in ignore_subjects]
        clashes = generate_clash_matrix(
            subjects, DATA, 
            value=int(iters),
            ignore_subjects=ignore_subjects)
        clashes = {k:v for k, v in sorted(clashes.items(), key=lambda x:x[1])}
        for k,v in clashes.items():
            print(f"{str(k)} => {v}")

    
    def block_clashes(self, subject):
        '''display clashes against all blocks for a given subject'''
        if not BLOCKS:
            print("no data for blocks could be found")
            return None
        ignore_subjects = self.opts.get("ignore_subjects", ())

        print(f"\n<Displaying clashes for '{subject}' against all option blocks>")
        print(f"Ignoring subjects in blocks :", )
        for n, options in enumerate(BLOCKS, 1):
            options = [opt for opt in options if opt not in ignore_subjects]
            print(f"\n[{n}] Showing '{subject}' Clashes with option blocks")
            print(f"<{','.join(options)}>")
            count = block_clashes(
                subject, 
                options, 
                data=DATA, 
                err_msgs=True,
                )
            print("CLASH COUNT => ", count)

    def eval(self, *options):
        '''evaluate given amount of options against blocks'''
        evaluate(BLOCKS, *options, display=True)

    def matches(self, *subjects):
        '''display options that match a given set of subjects'''
        pprint_exact_matches(DATA, subjects, display=True)

    def count(self, class_count:int=30):
        '''display the count of options for each subject'''
        res = get_subject_count(DATA, OPTIONS)
        print("<Displaying subject count>")
        for k,v in res.items():
            print(f"{k} => '{v}' {int(v)//int(class_count)+1}")

    def generate_dummy(self):
        
        gen = DummyCliGenerator(**self.opts)
        print("\nEntering Generation Options")
        gen.start()

if __name__ == "__main__":
    manager = Manager(
        ignore_subjects=("Hi","Ge"),

        # global use of data and options
        data=DATA,
        options=OPTIONS,
        strict=False,
        # for dummy generation
        random_ranges=[(5,30), (35,60), (65,90), (90,120)],
        min_opts=3
    )
    
    manager.exec(argv)