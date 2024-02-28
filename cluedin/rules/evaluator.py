import json

from .operators import get_operator as default_get_operator
from .rule import Rule
from .rule_group import RuleGroup


class Evaluator:
    """
    A class that evaluates rules against objects.

    Args:
        rule_set (str or dict): The rule set to be evaluated. It can be either a JSON string or a dictionary.
        get_operator (function, optional): A function that returns the operator based on the operator ID. 
            Defaults to default_get_operator.

    Attributes:
        get_operator (function): A function that returns the operator based on the operator ID.
        rule_group (RuleGroup): The rule group to be evaluated.

    Methods:
        get_matching_objects(objects): Returns a list of objects that match the rules.
        object_matches_rules(obj): Checks if an object matches the rules.
        evaluate_rule_group(rule_group, obj): Evaluates a rule group against an object.
        evaluate_rule(rule, obj): Evaluates a rule against an object.
        evaluate_rule_object(rule_object, obj): Evaluates a rule object against an object.
    """

    def __init__(self, rule_set, get_operator=default_get_operator):
        self.get_operator = get_operator
        if isinstance(rule_set, str):
            self.rule_group = RuleGroup(json.loads(rule_set))
        else:
            self.rule_group = RuleGroup(rule_set)

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
        Checks if the given object matches the rules defined in the rule group.

        Args:
            obj: The object to be evaluated against the rules.

        Returns:
            bool: True if the object matches the rules, False otherwise.
        """
        return self.evaluate_rule_group(self.rule_group, obj)

    def evaluate_rule_group(self, rule_group, obj):
        """
        Evaluates a rule group based on the given condition and rules.

        Args:
            rule_group (RuleGroup): The rule group to evaluate.
            obj (object): The object to evaluate against the rules.

        Returns:
            bool: True if the rule group evaluates to True, False otherwise.

        Raises:
            ValueError: If the condition of the rule group is invalid.
        """
        if rule_group.condition == 'AND':
            return all(map(lambda x: self.evaluate_rule_object(x, obj), rule_group.rules))
        if rule_group.condition == 'OR':
            return any(map(lambda x: self.evaluate_rule_object(x, obj), rule_group.rules))
        raise ValueError(f"Invalid condition: {rule_group.condition}")

    def evaluate_rule(self, rule: dict, obj: dict) -> bool:
        """
        Evaluates a rule against an object.

        Args:
            rule (Rule): The rule to evaluate.
            obj (Object): The object to evaluate the rule against.

        Returns:
            bool: True if the rule is satisfied, False otherwise.
        """
        return self.get_operator(rule.operator_id)(
            # left - value from the evaluated object
            rule.typecast_value(obj.get(rule.field)),
            # right - value from the rule
            rule.get_value(),
            obj)

    def evaluate_rule_object(self, rule_object: dict, obj) -> bool:
        """
        Evaluates a rule object against the given object.

        Args:
            rule_object (dict): The rule object to evaluate.
            obj: The object to evaluate the rule against.

        Returns:
            The result of the evaluation.
        """
        if 'rules' in rule_object and len(rule_object['rules']) > 0:
            return self.evaluate_rule_group(RuleGroup(rule_object), obj)
        return self.evaluate_rule(Rule(rule_object), obj)
