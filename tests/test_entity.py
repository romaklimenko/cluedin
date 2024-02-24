import os

# pylint: disable=wrong-import-order
from .ctx import cluedin
from cluedin import Context


class TestEntity:
    # pylint: disable=missing-docstring

    def test_get_entity_blob(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        entity_id = cluedin.account.get_users(context)[0]['Entity']['entity']['attribute-id']

        # Act
        blob = cluedin.entity.get_entity_blob(context, entity_id)

        # Assert
        assert '<?xml version="1.0" encoding="utf-8"?>' in blob.partition('\n')[
            0]

    def test_get_entity_as_clue(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        entity_id = cluedin.account.get_users(context)[0]['Entity']['entity']['attribute-id']

        # Act
        blob = cluedin.entity.get_entity_as_clue(context, entity_id)

        # Assert
        assert '<?xml version="1.0" encoding="utf-8"?>' in blob.partition('\n')[0]
