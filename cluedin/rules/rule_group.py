class RuleGroup:
    """
    Represents a group of rules.

    Attributes:
        condition (str): The condition for the rule group. Can be 'AND' or 'OR'.
        rules (list): The list of rules in the group.
    """

    def __init__(self, rule_group):
        self.condition = rule_group['condition']
        self.rules = rule_group['rules']
