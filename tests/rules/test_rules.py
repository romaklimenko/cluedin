import os

import pytest

from cluedin import Context

# pylint: disable=wrong-import-order
from ..ctx import cluedin


class TestRules:
    # pylint: disable=missing-docstring

    @pytest.mark.integration
    def test_get_rules(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act
        rules = cluedin.rules.get_rules(context)

        # Assert
        assert rules is not None
        assert 'data' in rules
        assert 'management' in rules['data']
        assert 'rules' in rules['data']['management']
        assert 'total' in rules['data']['management']['rules']
        assert rules['data']['management']['rules']['total'] == 100
        assert len(rules['data']['management']['rules']['data']) == 20

    @pytest.mark.integration
    def test_get_rule(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()
        rule_id = 'e283807e-3da8-4183-9425-c91b39a611ae'  # Replace with an actual rule ID

        # Act
        rule = cluedin.rules.get_rule(context, rule_id)

        # Assert
        assert rule is not None
        assert 'data' in rule
        assert 'management' in rule['data']
        assert 'rule' in rule['data']['management']
        assert 'condition' in rule['data']['management']['rule']
