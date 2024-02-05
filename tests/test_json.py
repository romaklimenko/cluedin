import os

from .ctx import cluedin


class TestJson:
    # pylint: disable=missing-docstring

    def test_dump_and_load(self):
        # Arrange

        a = {'a': 1, 'b': 2}

        # Act

        cluedin.json.dump('test.json', a)

        b = cluedin.json.load('test.json')

        # Assert

        assert a == b
        assert a is not b

        # cleanup

        os.remove('test.json')
