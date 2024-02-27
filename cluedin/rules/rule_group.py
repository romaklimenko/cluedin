from .rule import Rule


class RuleGroup:
    """
    Represents a group of rules that can be evaluated based on a condition.

    Args:
        rule_group (dict): A dictionary containing the rule group data.

    Attributes:
        condition (str): The condition for evaluating the rules ('AND' or 'OR').
        rules (list): A list of rules to be evaluated.

    Methods:
        evaluate(obj): Evaluates the rule group based on the condition and returns a boolean result.
        get_rule_object(rule): Returns the rule object based on the given rule data.

    Raises:
        ValueError: If an invalid condition is provided.

    """

    def __init__(self, rule_group):
        self.condition = rule_group['condition']
        self.rules = rule_group['rules']

    def evaluate(self, obj):
        """
        Evaluates the rule group based on the condition.

        Args:
            obj: The object to be evaluated against the rules.

        Returns:
            bool: True if the rule group evaluates to True, False otherwise.

        Raises:
            ValueError: If the condition is invalid.
        """
        if self.condition == 'AND':
            return all(map(lambda x: RuleGroup.get_rule_object(x).evaluate(obj), self.rules))
        if self.condition == 'OR':
            return any(map(lambda x: RuleGroup.get_rule_object(x).evaluate(obj), self.rules))
        raise ValueError(f"Invalid condition: {self.condition}")

    @staticmethod
    def get_rule_object(rule):
        """
        Returns a RuleGroup object
        if the 'rule' dictionary contains a 'rules' key with non-empty value,
        otherwise returns a Rule object.

        Args:
            rule (dict): The rule dictionary.

        Returns:
            RuleGroup or Rule: The corresponding rule object.
        """
        if 'rules' in rule and len(rule['rules']) > 0:
            return RuleGroup(rule)
        return Rule(rule)
