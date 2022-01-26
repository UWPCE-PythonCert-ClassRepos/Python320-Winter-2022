
from unittest import mock

from multi_input import single_input, chant

# the basic one -- input() called onece in the tested function

@mock.patch('builtins.input')
def test_get_input(new_mocked_input):
    new_mocked_input.return_value = 'blue'
    assert single_input() == 'blue'


class mocked_multi_input:
    def __init__(self):
        self.response = self.responses()

    def __call__(self, prompt):
        print("mocked_input called with:", prompt)
        return next(self.response)

    def responses(self):
        yield "A"
        yield "B"
        yield "C"
        yield "D"


@mock.patch('builtins.input', wraps=mocked_multi_input())
def test_chant(new_mocked_input):

    assert chant() == "ABCD"
