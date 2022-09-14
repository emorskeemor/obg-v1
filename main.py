from blocks.core import DATA, OPTIONS
from blocks.core.generator import BlockGenerator

if __name__ == "__main__":
    # init option block generator with
    generator = BlockGenerator(
        # data
        data=DATA, 
        options=OPTIONS, 
        # constraints
        blocks=4,
        class_size=30, 
        min_clash=3,
        strict=False,
    )
    # generate blocks
    generator.generate()

    # initial or base evaluation
    print("Initial evaluation :", generator.evaluate())
    
    for b in generator.blocks:
        print(b)

    # manually update the blocks by adding extra classes that are on the boundary
    # of being 2 classes
    generator.populate_lowest("Ar",2)
    generator.populate_lowest("Mu",2)
    generator.populate((2,), ("Co",))

    print("\nEvalutation by manually updating :", generator.evaluate())
    
    for b in generator.blocks:
        print(b)
    

    
    
# this was me playing around trying to generate dummy data
if __name__ == "__test__":
    from blocks.test.dummy import DummyGenerator
    from blocks.core.generator import BlockGenerator

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

