from blocks.cli.execeptions import ValidationError
from .dummy import DummyGenerator
from blocks.core.generator import BlockGenerator
from blocks.cli.questioner import IOCLIMixin

class DummyCliGenerator(IOCLIMixin):
    def __init__(self, **opts) -> None:
        self.opts = opts

    def start(self):
        try:
            opts = self.question("enter maximum number of options available for each student (4)", int, default=4)

            gen = DummyGenerator(
                number_of_options=opts,
                **self.opts
            )
            if self.question("Generate counts by manually assigning? Otherwise use automated inital data (Y)", bool, default=True):
                ranges = self.manual_assign_ranges()
            else:
                ranges = self.opts.get("random_ranges", None)
                if ranges is None:
                    raise ValidationError("Default 'random_ranges' were not provided")
                self.output("by default using 'random_ranges' from init manager arguments with a maximum of '%s' classes per subject" % len(ranges), "i")
            gen.generate_random_counts(
                ranges,
                self.opts.get("class_length",30)
            )
            iters = self.question("how many clash iters must be generated (200)", int, default=200)
            maximum = self.question("maximum clash count each clash can reach (1)", int, default=1)
            gen.generate_random_clashes(iters, maximum)

            self.output("generating students", "i")
            gen.generate()

            if self.question("Display (N)?", bool, default=False):
                gen.display_dummy()

            if self.question("Save (N)?", bool, default=True):
                self.output("this will save to the static directory specified in the core module", "!")
                file_name = self.question("File name to save as", str)
                gen.save(file_name)


            if self.question("Generate and evaluate ?", bool):
                blocks = self.question("Number of blocks", int)
                gen = BlockGenerator(
                    data=self.opts.get("data"),
                    options=self.opts.get("options"),
                    blocks=blocks
                    )
                gen.generate()
                gen.evaluate(display=True)
            


        except KeyboardInterrupt as reason:
            if not str(reason):
                reason = "user"
            default = "cancelling student generation due to '%s'" % reason
            self.newline()
            self.output(default, "i")
        except ValidationError as error:
            self.newline()
            self.output("cancelling due to error : '%s'" % error, "error")

    def manual_assign_ranges(self):
        self.output("Manually assigning ranges", "i")
        max_classes = self.question("How many classes will there be (4)", int, default=4)
        ranges = []
        self.output("Use a dash to enter range e.g. x-y", "i")
        for klass in range(1,max_classes+1):
            res = self.question("Enter range for classes that occur '%s' " % klass, str)
            if len(res) != 2:
                raise ValidationError("Invalid range given")
            min, max = res.split("-")
            ranges.append((int(min),int(max)))
        return ranges