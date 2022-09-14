from blocks.core import DATA, OPTIONS
from blocks.core.generator import BlockGenerator

if __name__ == "__test__":
    generator = BlockGenerator(
        data=DATA, 
        options=OPTIONS, 
        blocks=6,
        
        ignore=["Bb"], 
        class_size=30, 
        min_clash=3,
        strict=False,
    )
    generator.generate()

    generator.ignore.remove("Bb")
    generator.populate_lowest("Bb",2)
    generator.populate_lowest("Ar",2)
    generator.populate_lowest("Mu",2)
    generator.populate((2,), ("Co",))

    for b in generator.blocks:
        print(b)

    print(generator.evaluate())
    

if __name__ == "__main__":
    from blocks.test.dummy import DummyGenerator
    from blocks.core.generator import BlockGenerator
    from blocks.core.evaluation import get_subject_count
    from blocks.core import BLOCKS_FILE_NAME

    BLOCK_NO = 4
    
    test_ranges = [
        (5, 30),
        (35, 60),
        (65, 85),
        (90, 120),

    ]

    dummy_gen = DummyGenerator(
        number_of_options=4,
        data=DATA,
        options=OPTIONS,
        min_opts=3
        )
    dummy_gen.generate_random_counts(
        [(5,30), (35,60), (65,90), (90,120)],
        class_length=30,
        )
    dummy_gen.generate_random_clashes(15,5)

    dummy_gen.generate()
    dummy_gen.display_dummy()
    
    opt_gen = BlockGenerator(
        data=dummy_gen.data,
        options=dummy_gen._init["subjects"],
        blocks=BLOCK_NO,
    )
    dummy_gen.save(file_name="testing")

    opt_gen.generate()

    for block in opt_gen.blocks:
        print(block)

    eval = opt_gen.evaluate()
    print(eval)

