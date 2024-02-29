import re


def default_get_operator(operator_id):
    """
    Retrieves the operator based on the provided operator ID.

    Args:
            operator_id (str): The ID of the operator to retrieve.

    Returns:
            dict: A dictionary containing the properties of the operator.
    """
    rule_operator_by_id = {
        # 'Is Not True'
        '7cd9d1e6-25d8-4fbf-977a-1d2c3832289d': lambda l, r, o: not is_true(l, r, o),
        # 'Is True'
        'bd804d86-f2bc-4bc1-9598-58cb6c490311': is_true,
        # 'Begins With'
        'daf3a318-569f-4baf-a17f-35b4426ae603': begins_with,
        # 'Between'
        '566bc291-df6a-427c-b7f4-00f8766d37a2': between,
        # 'Contains'
        '4988d076-3ec1-4414-9f56-5b9b30e25f72': contains,
        # 'Ends With'
        'ff9a47ac-8e3c-4123-80ee-e0b660aa5f9f': ends_with,
        # 'Equals'
        '0bafc522-8011-43ba-978a-babe222ba466': equals,
        # 'Exists'
        '306e5d29-832f-41e7-a6db-1c02eb5ebf74': lambda l, r, o: not is_null(l, r, o),
        # 'Greater'
        '85ecec6b-9c45-4365-9614-ef090137098d': greater,
        # 'Greater or Equal'
        '5a2d1185-7fd8-4dda-9d33-7f69e42e9147': greater_or_equal,
        # 'In'
        '31feed84-ce0e-435f-ba94-ce01b9c7bd15': in_list,
        # 'Is False'
        'dfbfc760-69ea-4241-b33e-0425c2a51688': lambda l, r, o: not is_true(l, r, o),
        # 'Is Not Null'
        'a42a9f87-7944-4d07-b1f3-d2f404bc4fd7': lambda l, r, o: not is_null(l, r, o),
        # 'Is Null'
        '9ad76320-021e-4211-9e9a-8b148c9c600d': is_null,
        # 'Is True'
        '04f2d73a-c908-4bc3-a7d5-1774b7db44dd': is_true,
        # 'Less'
        '0de353ce-bbe4-4a27-8e20-0dc21947e987': less,
        # 'Less or Equal'
        '42d4d22d-e37a-4c5f-96eb-7ae59513f80f': less_or_equal,
        # 'Matches pattern'
        '4e4782d7-8c17-47c1-9797-37434fce0c77': matches_pattern,
        # 'Not Begins With'
        'bbd02195-213e-40e2-9597-65ec05100dfc': lambda l, r, o: not begins_with(l, r, o),
        # 'Not Between'
        '5642150e-fa0a-462c-a230-619d97cb3f8b': lambda l, r, o: not between(l, r, o),
        # 'Not Contains'
        '4af53db0-acdb-44a6-89a1-40fa8ef05cde': lambda l, r, o: not contains(l, r, o),
        # 'Not Ends With'
        '3527ff72-bdd4-4bb4-b964-f18898d5a82d': lambda l, r, o: not ends_with(l, r, o),
        # 'Not Equal'
        '4f7f2b0f-155a-4208-b849-3e972f5d89d2': lambda l, r, o: not equals(l, r, o),
        # 'Does Not Exist'
        '16b2dc07-94e3-4c29-bc60-a7a1d25de53b': is_null,
        # 'Not In'
        '25c16d50-d170-4295-ad85-c2571431794a': lambda l, r, o: not in_list(l, r, o),
        # 'Does not match pattern'
        '9253eea0-5975-460a-8373-dd6ff57d4e65': lambda l, r, o: not matches_pattern(l, r, o)
    }

    if operator_id in rule_operator_by_id:
        return rule_operator_by_id[operator_id]

    raise ValueError(f"Operator ID '{id}' not found.")


def begins_with(left, right, _obj):
    """
    Evaluates if the left operand begins with the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand begins with the right operand, False otherwise.
    """
    if left is None:
        return False
    return str(left).lower().startswith(str(right).lower())


def not_begins_with(left, right, _obj):
    """
    Evaluates if the left operand does not begin with the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand does not begin with the right operand, False otherwise.
    """
    return not begins_with(left, right, _obj)


def contains(left, right, _obj):
    """
    Evaluates if the left operand contains the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand contains the right operand, False otherwise.
    """
    if left is None:
        return False
    return str(right).lower() in str(left).lower()


def ends_with(left, right, _obj):
    """
    Evaluates if the left operand ends with the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand ends with the right operand, False otherwise.
    """
    if left is None:
        return False
    return str(left).lower().endswith(str(right).lower())


def equals(left, right, _obj):
    """
    Evaluates if the left operand is equal to the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is equal to the right operand, False otherwise.
    """
    if left is None or right is None:
        return False
    return str(left.lower()) == str(right.lower())


def is_null(left, _right, _obj):
    """
    Evaluates if the given value is null.

    Args:
        left: The value to be evaluated.
        _right: Ignored parameter.
        _obj: Ignored parameter.

    Returns:
        bool: True if the value is null, False otherwise.
    """
    return left is None


def is_true(left, _right, _obj):
    """
    Check if the left operand is true.

    Args:
        left: The left operand.
        _right: The right operand (not used in this function).
        _obj: The object being evaluated (not used in this function).

    Returns:
        bool: True if the left operand is true, False otherwise.
    """
    return left


def matches_pattern(left, right, _obj):
    """
    Evaluates if the left operand matches the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand matches the right operand, False otherwise.
    """
    if left is None:
        return False
    return bool(re.match(right, left, re.IGNORECASE))


def in_list(left, right, _obj):
    """
    Evaluates if the left operand is in the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is in the right operand, False otherwise.
    """
    if left is None:
        return False
    return any(str(left).lower() == str(item).lower() for item in right)


def greater(left, right, _obj):
    """
    Evaluates if the left operand is greater than the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is greater than the right operand, False otherwise.
    """
    if left is None or right is None:
        return False
    return left > right


def greater_or_equal(left, right, _obj):
    """
    Evaluates if the left operand is greater than or equal to the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is greater than or equal to the right operand, False otherwise.
    """
    if left is None or right is None:
        return False
    return left >= right


def less(left, right, _obj):
    """
    Evaluates if the left operand is less than the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is less than the right operand, False otherwise.
    """
    if left is None or right is None:
        return False
    return left < right


def less_or_equal(left, right, _obj):
    """
    Evaluates if the left operand is less than or equal to the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is less than or equal to the right operand, False otherwise.
    """
    if left is None or right is None:
        return False
    return left <= right


def between(left, right, _obj):
    """
    Evaluates if the left operand is between the right operand.

    Args:
        left: The left operand.
        right: The right operand.
        _obj: Ignored parameter. (input object)

    Returns:
        True if the left operand is between the right operand, False otherwise.
    """
    if left is None or right is None:
        return False
    return right[0] <= left <= right[1]


def pandas_get_operator(left, operator_id, right):
    """
    Retrieves the operator based on the provided operator ID.

    Args:
        left: The left operand.
        operator_id (str): The ID of the operator to retrieve.
        right: The right operand.

    Returns:
        dict: A dictionary containing the properties of the operator.
    """
    rule_operator_by_id = {
        # 'Is Not True'
        '7cd9d1e6-25d8-4fbf-977a-1d2c3832289d': lambda l, r: f"~{l}",
        # 'Is True'
        'bd804d86-f2bc-4bc1-9598-58cb6c490311': lambda l, r: l,
        # 'Begins With'
        'daf3a318-569f-4baf-a17f-35b4426ae603': lambda l, r: f"{l}.str.startswith({r})",
        # 'Between'
        '566bc291-df6a-427c-b7f4-00f8766d37a2': lambda l, r: f"({l} >= {r[0]}) & ({l} <= {r[1]})",
        # 'Contains'
        '4988d076-3ec1-4414-9f56-5b9b30e25f72': lambda l, r: f"{l}.str.contains({r})",
        # 'Ends With'
        'ff9a47ac-8e3c-4123-80ee-e0b660aa5f9f': lambda l, r: f"{l}.str.endswith({r})",
        # 'Equals'
        '0bafc522-8011-43ba-978a-babe222ba466': lambda l, r: f"{l} == {r}",
        # 'Exists'
        '306e5d29-832f-41e7-a6db-1c02eb5ebf74': lambda l, r: f"~{l}.isnull()",
        # 'Greater'
        '85ecec6b-9c45-4365-9614-ef090137098d': lambda l, r: f"{l} > {r}",
        # 'Greater or Equal'
        '5a2d1185-7fd8-4dda-9d33-7f69e42e9147': lambda l, r: f"{l} >= {r}",
        # 'In'
        '31feed84-ce0e-435f-ba94-ce01b9c7bd15': lambda l, r: f"{l}.isin({r})",
        # 'Is False'
        'dfbfc760-69ea-4241-b33e-0425c2a51688': lambda l, r: f"{l} == False",
        # 'Is Not Null'
        'a42a9f87-7944-4d07-b1f3-d2f404bc4fd7': lambda l, r: f"~{l}.isnull()",
        # 'Is Null'
        '9ad76320-021e-4211-9e9a-8b148c9c600d': lambda l, r: f"{l}.isnull()",
        # 'Is True'
        '04f2d73a-c908-4bc3-a7d5-1774b7db44dd': lambda l, r: f"{l} == True",
        # 'Less'
        '0de353ce-bbe4-4a27-8e20-0dc21947e987': lambda l, r: f"{l} < {r}",
        # 'Less or Equal'
        '42d4d22d-e37a-4c5f-96eb-7ae59513f80f': lambda l, r: f"{l} <= {r}",
        # 'Matches pattern'
        '4e4782d7-8c17-47c1-9797-37434fce0c77': lambda l, r: f"{l}.str.match({r})",
        # 'Not Begins With'
        'bbd02195-213e-40e2-9597-65ec05100dfc': lambda l, r: f"~{l}.str.startswith({r})",
        # 'Not Between'
        '5642150e-fa0a-462c-a230-619d97cb3f8b': lambda l, r: f"({l} < {r[0]}) | ({l} > {r[1]})",
        # 'Not Contains'
        '4af53db0-acdb-44a6-89a1-40fa8ef05cde': lambda l, r: f"~{l}.str.contains({r})",
        # 'Not Ends With'
        '3527ff72-bdd4-4bb4-b964-f18898d5a82d': lambda l, r: f"~{l}.str.endswith({r})",
        # 'Not Equal'
        '4f7f2b0f-155a-4208-b849-3e972f5d89d2': lambda l, r: f"{l} != {r}",
        # 'Does Not Exist'
        '16b2dc07-94e3-4c29-bc60-a7a1d25de53b': lambda l, r: f"{l}.isnull()",
        # 'Not In'
        '25c16d50-d170-4295-ad85-c2571431794a': lambda l, r: f"~{l}.isin({r})",
        # 'Does not match pattern'
        '9253eea0-5975-460a-8373-dd6ff57d4e65': lambda l, r: f"~{l}.str.match({r})"
    }

    if operator_id in rule_operator_by_id:
        return rule_operator_by_id[operator_id](left, right)

    return f"{left} {operator_id} {right}"
