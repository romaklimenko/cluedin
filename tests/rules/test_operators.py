# pylint: disable=wrong-import-order
from ..ctx import cluedin


class TestOperators:
    # pylint: disable=missing-docstring

    def test_begins_with(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/begins-with.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is False

    def test_not_begins_with(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/not-begins-with.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is True

    def test_contains(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/contains.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is False

    def test_not_contains(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/not-contains.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is True

    def test_ends_with(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/ends-with.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Far From Home',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'far from home',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is False

    def test_not_ends_with(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/not-ends-with.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Far From Home',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'far from home',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is True

    def test_equals(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/equals.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is False

    def test_not_equals(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/not-equals.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is True

    def test_exists(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/exists.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Mad Max: Fury Road',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is False

    def test_does_not_exist(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/does-not-exist.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Mad Max: Fury Road',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is True

    def test_is_not_null(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/is-not-null.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Mad Max: Fury Road',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is False

    def test_is_null(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/is-null.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Mad Max: Fury Road',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is True

    def test_matches_pattern(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/matches-pattern.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is False

    def test_does_not_match_pattern(self):
        # Arrange
        rule = cluedin.json.load(
            'tests/fixtures/rules/does-not-match-pattern.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'home alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Sweet Home Alabama',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': None,
        }) is True

    def test_in(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/in.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is False

    def test_not_in(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/not-in.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home Alone',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Home',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.primaryTitle': 'Alone',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title'
        }) is True

    def test_greater(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/greater.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 11,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 10,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 9,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 'cactus',
        }) is False

    def test_less(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/less.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 11,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 10,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 9,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 'cactus',
        }) is False

    def test_greater_or_equal(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/greater-or-equal.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 11,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 10,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 9,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 'cactus',
        }) is False

    def test_less_or_equal(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/less-or-equal.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 11,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 10,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 9,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 'cactus',
        }) is False

    def test_between(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/between.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 9,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 10,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 15,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 30,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 31,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 'cactus',
        }) is False

    def test_not_between(self):
        # Arrange
        rule = cluedin.json.load('tests/fixtures/rules/not-between.json')
        evaluator = cluedin.rules.Evaluator(
            rule['data']['management']['rule']['condition'])

        # Act
        # Assert

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 9,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 10,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 15,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 30,
        }) is False

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 31,
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
        }) is True

        assert evaluator.object_matches_rules({
            'entityType': '/IMDb/Title',
            'imdb.title.runtimeMinutes': 'cactus',
        }) is True
