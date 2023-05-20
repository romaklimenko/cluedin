import os

# pylint: disable=wrong-import-order
from .ctx import cluedin
from cluedin import Context


class TestVocab:
    # pylint: disable=missing-docstring

    def test_get_vocab_keys(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act
        keys = cluedin.vocab.get_vocab_keys(context)

        # Assert
        assert 'Key' in keys[0]
        assert 'VocabularyName' in keys[0]
