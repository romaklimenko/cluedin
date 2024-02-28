from datetime import datetime


class Rule:
    """
    Represents a rule object.

    Args:
        rule (dict): The rule dictionary containing the rule information.

    Attributes:
        id (str): The ID of the rule.
        field (str): The normalized field of the rule.
        operator_id (str): The ID of the operator.
        type (str): The type of the rule.
        value (str or int or float or list): The value of the rule.

    Methods:
        normalize_field: Normalizes the field value.
        get_value: Returns the typecasted value of the rule.
        typecast_value: Typecasts the given value based on the rule type.
    """

    def __init__(self, rule) -> None:
        self.id = rule['id']
        self.field = rule['field']
        self.operator_id = rule['operator']
        self.type = rule['type']
        self.value = rule['value']

    def get_value(self):
        """
        Returns the value of the rule.

        If the value is a list, it will be typecasted and returned as a list.
        If the value is a single element, it will be typecasted and returned as is.
        If the value is neither a list nor a single element, it will be typecasted and returned.

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
            The typecasted value, or None if the value cannot be typecasted.

        """
        if value_to_cast is None:
            return None

        try:
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
        except ValueError:
            return None
