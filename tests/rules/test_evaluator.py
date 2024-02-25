# pylint: disable=wrong-import-order
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
