from datetime import datetime

from .operators import get_operator as default_get_operator


class Rule:
    """
    Represents a rule used for evaluation.

    Attributes:
        id (str): The ID of the rule.
        field (str): The field to be evaluated.
        operator (function): The operator used for evaluation.
        type (str): The type of the value to be evaluated.
        value (str or int or float or list): The value to be evaluated.

    Methods:
        __init__(self, rule, get_operator=default_get_operator): Initializes a Rule object.
        normalize_field(self, field): Normalizes the field name.
        evaluate(self, obj): Evaluates the rule against an object.
        get_value(self): Returns the value to be evaluated.
        typecast_value(self, value_to_cast): Typecasts the value to the specified type.
    """

    def __init__(self, rule, get_operator=default_get_operator) -> None:
        self.id = rule['id']
        self.field = self.normalize_field(rule['field'])
        self.operator = get_operator(rule['operator'])
        self.type = rule['type']
        self.value = rule['value']

    def normalize_field(self, field):
        """
        Normalize a field by converting it to a standardized format.

        Args:
            field (str): The field to be normalized.

        Returns:
            str: The normalized field.

        """
        if field is None:
            return None
        if field == 'EntityType':
            return 'entityType'
        return field.replace('Properties[', '').replace(']', '')

    def evaluate(self, obj):
        """
        Evaluates the rule against the given object.

        Args:
            obj (dict): The object to evaluate the rule against.

        Returns:
            bool: The result of the evaluation.
        """
        return self.operator(
            self.typecast_value(obj.get(self.field)),
            self.get_value())

    def get_value(self):
        """
        Returns the value of the rule.

        If the value is a list, it will be typecasted individually.
        If the value is a single element, it will be typecasted and returned.
        If the value is not a list, it will be typecasted and returned.

        Returns:
            The typecasted value of the rule.
        """
        if isinstance(self.value, list):
            if len(self.value) == 1:
                return self.typecast_value(self.value[0])
            return [self.typecast_value(x) for x in self.value]
        return self.typecast_value(self.value)

    def typecast_value(self, value_to_cast):
        """
        Typecasts the given value based on the rule's type.

        Args:
            value_to_cast: The value to be typecasted.

        Returns:
            The typecasted value.

        """
        # TODO: check the full list of types
        if value_to_cast is None:
            return None

        if self.type == 'string':
            return str(value_to_cast)
        if self.type == 'integer':
            return int(value_to_cast)
        if self.type == 'double':
            return float(value_to_cast)
        if self.type == 'date' or self.type == 'datetime':
            if isinstance(value_to_cast, str):
                return datetime.strptime(value_to_cast, "%Y-%m-%dT%H:%M:%S.%fZ")
            return value_to_cast
        if self.type == 'boolean' and isinstance(value_to_cast, str):
            return value_to_cast.lower() in ['true', '1']
        return value_to_cast
