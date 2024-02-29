# pylint: disable=wrong-import-order
from cluedin.rules.evaluator import default_get_property_name
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

    def test_custom_get_property_name(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/adult-movies.json')
        entity = {
            'name': 'The Godfather',
            'entityType': '/IMDb/Title',
            'imdb_title_isAdult': True,
            'imdb_title_genres': ['Crime', 'Drama'],
            'imdb_title_titleType': 'movie'
        }

        # Act
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'],
            get_property_name=lambda x: default_get_property_name(x.replace('.', '_')))

        result = evaluator.object_matches_rules(entity)

        # Assert

        assert result is True

    def test_custom_get_value(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/adult-movies.json')
        entity = {
            'name': 'The Godfather',
            'entityType': '/IMDb/Title',
            'imdb': {
                'title': {
                    'isAdult': True,
                    'genres': ['Crime', 'Drama'],
                    'titleType': 'movie'
                }
            }
        }

        def custom_get_value(field, obj):
            parts = field.split('.')
            for part in parts:
                obj = obj.get(part)
                if obj is None:
                    return None
            return obj

        # Act
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'],
            get_value=custom_get_value)

        result = evaluator.object_matches_rules(entity)

        # Assert

        assert result is True

    def test_explain(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/adult-movies.json')

        # Act
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        result = evaluator.explain()

        # Assert

        # pylint: disable=line-too-long
        assert result == \
            'df.query(\'`entityType` == "/IMDb/Title" & `imdb.title.titleType` == "movie" | `imdb.title.titleType` == "video" & `imdb.title.isAdult` == True\')'
