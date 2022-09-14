from blocks.util.cli import CliManager
from blocks.core import DATA, OPTIONS, BLOCKS
from blocks.core.clash import (
    generate_clash_matrix, 
    display_clashes, 
    block_clashes, 
    pprint_exact_matches,
    )
from blocks.core.evaluation import (
    evaluate,
    evaluate_blocks,
    get_subject_count,
    )


class DebugManager(CliManager):
    '''
    Debug Manager for generating option blocks
    '''
    def __init__(self) -> None:
        super().__init__()
        self.ignored_subjects = ("Hi","Ge")
    
    def build(self):
        evaluate_blocks(BLOCKS, DATA)
        # build(DATA)

    def m_matrix(self, iters=2, matching=2):
        '''displays clashes from a given number of iters matching a certain value'''
        generated = generate_clash_matrix(
            OPTIONS, DATA, 
            value=int(iters), 
            ignore_subjects=self.ignored_subjects
            )
        display_clashes(generated, value=int(matching))

    def matrix(self, iters=2, *subjects):
        '''displays ordered clashes'''
        print("displaying clash table matrix ignore subjects :", self.ignored_subjects)
        if not subjects:
            subjects = [opt for opt in OPTIONS if opt not in self.ignored_subjects]
        clashes = generate_clash_matrix(
            subjects, DATA, 
            value=int(iters),
            ignore_subjects=self.ignored_subjects)
        clashes = {k:v for k, v in sorted(clashes.items(), key=lambda x:x[1])}
        for k,v in clashes.items():
            print(f"{str(k)} => {v}")

    
    def b_matrix(self, subject):
        if not BLOCKS:
            print("no data for blocks could be found")
            return None

        print(f"\n<Displaying clashes for '{subject}' against all option blocks>")
        print(f"Ignoring subjects in blocks :", self.ignored_subjects)
        for n, options in enumerate(BLOCKS, 1):
            options = [opt for opt in options if opt not in self.ignored_subjects]
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
        evaluate(BLOCKS, *options)

    def matches(self, *subjects):
        '''display options that match a given set of subjects'''
        pprint_exact_matches(DATA, subjects, display=True)

    def count(self, class_count:int=30):
        '''display the count of options for each subject'''
        res = get_subject_count(DATA, OPTIONS)
        print("<Displaying subject count>")
        for k,v in res.items():
            print(f"{k} => '{v}' {int(v)//int(class_count)+1}")

