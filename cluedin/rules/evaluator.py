import json

from .rule_group import RuleGroup


class Evaluator:
    """
    Class representing an evaluator for rule sets.

    Args:
        rule_set (str or dict): The rule set to be evaluated. If a string is provided, it will be parsed as JSON.

    Methods:
        get_matching_objects(objects): Returns a list of objects that match the rules in the rule set.
        object_matches_rules(obj): Checks if an object matches the rules in the rule set.

    """

    def __init__(self, rule_set):
        if isinstance(rule_set, str):
            self.parsed_rule_set = json.loads(rule_set)
        else:
            self.parsed_rule_set = rule_set

    def get_matching_objects(self, objects):
        """
        Returns a list of objects that match the rules.

        Args:
            objects (list): The list of objects to be evaluated.

        Returns:
            list: A list of objects that match the rules.
        """
        return list(filter(self.object_matches_rules, objects))

    def object_matches_rules(self, obj):
            """
            Checks if the given object matches the rules.

            Args:
                obj: The object to be evaluated.

            Returns:
                bool: True if the object matches the rules, False otherwise.
            """
            return RuleGroup(self.parsed_rule_set).evaluate(obj)
