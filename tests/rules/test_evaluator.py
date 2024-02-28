# pylint: disable=wrong-import-order
from cluedin.rules.evaluator import default_get_value
from cluedin.rules.operators import default_get_operator

from ..ctx import cluedin


class TestEvaluator:
    # pylint: disable=missing-docstring

    def test_object_matches_rules(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/adult-movies.json')
        entity = {
            'name': 'The Godfather',
            'entityType': '/IMDb/Title',
            'imdb.title.isAdult': True,
            'imdb.title.genres': ['Crime', 'Drama'],
            'imdb.title.titleType': 'movie'
        }

        # Act
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        result = evaluator.object_matches_rules(entity)

        # Assert

        assert result is True

    def test_custom_operators(self):

        def custom_get_operator(operator_id):
            if operator_id == 'compare_properties':
                return lambda l, r, o: l == o.get(r) != None
            return default_get_operator(operator_id)

        # Arrange
        rule = cluedin.json.load(
            'tests/fixtures/rules/compare-properties.json')
        entity0 = {
            'name': 'The Godfather',
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'The Godfather',
        }
        entity1 = {
            'name': 'The Godfather',
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'The Godfather II',
        }

        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'], custom_get_operator)

        # Act
        # Assert

        assert evaluator.object_matches_rules(entity0) is True
        assert evaluator.object_matches_rules(entity1) is False

    def test_custom_get_value(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/adult-movies.json')
        entity = {
            'name': 'The Godfather',
            'entityType': '/IMDb/Title',
            'imdb_title_isAdult': True,
            'imdb_title_genres': ['Crime', 'Drama'],
            'imdb_title_titleType': 'movie'
        }

        def custom_get_value(field, obj):
            return default_get_value(field.replace('.', '_'), obj)

        # Act
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'],
            get_value=custom_get_value)

        result = evaluator.object_matches_rules(entity)

        # Assert

        assert result is True
