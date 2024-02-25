def get_operator(operator_id):
    """
    Retrieves the operator based on the provided operator ID.

    Args:
            operator_id (str): The ID of the operator to retrieve.

    Returns:
            dict: A dictionary containing the properties of the operator.
    """
    rule_operator_by_id = {
        # 'Is Not True'
        '7cd9d1e6-25d8-4fbf-977a-1d2c3832289d': eval_is_false,
        # 'Is True'
        'bd804d86-f2bc-4bc1-9598-58cb6c490311': eval_is_true,
        # 'Begins With'
        'daf3a318-569f-4baf-a17f-35b4426ae603': eval_not_implemented,
        # 'Between'
        '566bc291-df6a-427c-b7f4-00f8766d37a2': eval_not_implemented,
        # 'Contains'
        '4988d076-3ec1-4414-9f56-5b9b30e25f72': eval_not_implemented,
        # 'Ends With'
        'ff9a47ac-8e3c-4123-80ee-e0b660aa5f9f': eval_not_implemented,
        # 'Equals'
        '0bafc522-8011-43ba-978a-babe222ba466': eval_equals,
        # 'Exists'
        '306e5d29-832f-41e7-a6db-1c02eb5ebf74': eval_not_implemented,
        # 'Greater'
        '85ecec6b-9c45-4365-9614-ef090137098d': eval_not_implemented,
        # 'Greater or Equal'
        '5a2d1185-7fd8-4dda-9d33-7f69e42e9147': eval_not_implemented,
        # 'In'
        '31feed84-ce0e-435f-ba94-ce01b9c7bd15': eval_not_implemented,
        # 'Is False'
        'dfbfc760-69ea-4241-b33e-0425c2a51688': eval_is_false,
        # 'Is Not Null'
        'a42a9f87-7944-4d07-b1f3-d2f404bc4fd7': eval_not_implemented,
        # 'Is Null'
        '9ad76320-021e-4211-9e9a-8b148c9c600d': eval_not_implemented,
        # 'Is True'
        '04f2d73a-c908-4bc3-a7d5-1774b7db44dd': eval_is_true,
        # 'Less'
        '0de353ce-bbe4-4a27-8e20-0dc21947e987': eval_not_implemented,
        # 'Less or Equal'
        '42d4d22d-e37a-4c5f-96eb-7ae59513f80f': eval_not_implemented,
        # 'Matches pattern'
        '4e4782d7-8c17-47c1-9797-37434fce0c77': eval_not_implemented,
        # 'Not Begins With'
        'bbd02195-213e-40e2-9597-65ec05100dfc': eval_not_implemented,
        # 'Not Between'
        '5642150e-fa0a-462c-a230-619d97cb3f8b': eval_not_implemented,
        # 'Not Contains'
        '4af53db0-acdb-44a6-89a1-40fa8ef05cde': eval_not_implemented,
        # 'Not Ends With'
        '3527ff72-bdd4-4bb4-b964-f18898d5a82d': eval_not_implemented,
        # 'Not Equal'
        '4f7f2b0f-155a-4208-b849-3e972f5d89d2': eval_not_equals,
        # 'Does Not Exist'
        '16b2dc07-94e3-4c29-bc60-a7a1d25de53b': eval_not_implemented,
        # 'Not In'
        '25c16d50-d170-4295-ad85-c2571431794a': eval_not_implemented,
        # 'Does not match pattern'
        '9253eea0-5975-460a-8373-dd6ff57d4e65': eval_not_implemented,
    }

    if operator_id in rule_operator_by_id:
        return rule_operator_by_id[operator_id]

    raise ValueError(f"Operator ID '{id}' not found.")


def eval_not_implemented(left, right):
    """
    Raises a NotImplementedError with a message indicating that the operator is not implemented.

    Args:
        left: The left operand of the operator.
        right: The right operand of the operator.

    Raises:
        NotImplementedError: If the operator is not implemented.
    """
    raise NotImplementedError("Operator not implemented")


def eval_equals(left, right):
    """
    Evaluates if the left operand is equal to the right operand.

    Args:
        left: The left operand.
        right: The right operand.

    Returns:
        True if the left operand is equal to the right operand, False otherwise.
    """
    return left == right


def eval_not_equals(left, right):
    """
    Evaluates if the left value is not equal to the right value.

    Args:
        left: The left value to compare.
        right: The right value to compare.

    Returns:
        True if the left value is not equal to the right value, False otherwise.
    """
    return not eval_equals(left, right)


def eval_is_true(left, _):
    """
    Evaluates if the left operand is true.

    Parameters:
    - left: The left operand to be evaluated.
    - _: Ignored parameter.

    Returns:
    - True if the left operand is true, False otherwise.
    """
    return left


def eval_is_false(left, _):
    """
    Evaluates if the given value is False.

    Args:
        left: The value to be evaluated.

    Returns:
        bool: True if the value is False, False otherwise.
    """
    return not left
