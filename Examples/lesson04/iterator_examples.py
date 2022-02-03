"""
some examples used to demonstrate iterators
"""

# Making iterators:

class class_range:
    def __init__(self, start, stop, step=1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        else:
            current = self.current
            self.current += self.step
            return current




# Generators:


def simple_genfun():
    yield "yes"
    yield "no"
    yield "maybe"
    return "All done"

# Often, the yield will be in a loop


# here's a way to get a simple version of range():

def gen_range(start, stop, step=1):
    i = start
    while i < stop:
        print("about to yield")
        yield i
        i += step

# Combining the two:
# if you do need a class to maintain morestate,
# you can use a generator as the __iter__ method:


class genclass_range:
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        i = self.start
        while i < self.stop:
            yield i
            i += self.step


