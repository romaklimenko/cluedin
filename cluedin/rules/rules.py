from enum import Enum

from ..context import Context
from ..gql import org_gql


class RuleScope(Enum):
    """
    Enum representing the scope of a rule (DataPart, Entity (Golden Record), Survivorship).
    """

    DATA_PART = 'DataPart'
    ENTITY = 'Entity'
    SURVIVORSHIP = 'Survivorship'


def get_rules(context: Context, scope=RuleScope.DATA_PART, page_number=1) -> dict:
    """
    Retrieves rules based on the specified parameters.

    Args:
            context (Context): The context object.
            scope (RuleScope, optional): The scope of the rules. Defaults to RuleScope.DATA_PART.
            page_number (int, optional): The page number to retrieve. Defaults to 1.

    Returns:
            dict: The rules' data.

    """
    query = """
        query getRules($searchName: String, $isActive: Boolean, $pageNumber: Int, $sortBy: String, $sortDirection: String, $scope: String) {
            management {
                id
                rules(
                    searchName: $searchName
                    isActive: $isActive
                    pageNumber: $pageNumber
                    sortBy: $sortBy
                    sortDirection: $sortDirection
                    scope: $scope
                ) {
                    total
                    data {
                        id
                        name
                        order
                        description
                        isActive
                        createdBy
                        modifiedBy
                        ownedBy
                        createdAt
                        modifiedAt
                        author {
                            id
                            username
                            __typename
                        }
                        scope
                        isReprocessing
                        __typename
                    }
                    __typename
                }
                __typename
            }
        }
        """

    variables = {
        "scope": scope.value,
        "pageNumber": page_number
    }

    return org_gql(context, query, variables)


def get_rule(context: Context, rule_id: str) -> dict:
    """
    Retrieves the properties of a rule based on the provided rule ID.

    Args:
            context (Context): The context object.
            rule_id (str): The ID of the rule to retrieve properties for.

    Returns:
            dict: A dictionary containing the properties of the rule.
    """
    query = """
        query getRule($id: ID!) {
            management {
                id
                rule(id: $id) {
                    id
                    name
                    description
                    isActive
                    createdBy
                    modifiedBy
                    ownedBy
                    createdAt
                    modifiedAt
                    condition
                    actions
                    rules
                    sourceDetail {
                        id
                        name
                        type
                        __typename
                    }
                    author {
                        id
                        username
                        __typename
                    }
                    scope
                    isReprocessing
                    requiresAttention
                    __typename
                }
                __typename
            }
        }
        """
    variables = {
        "id": rule_id
    }

    return org_gql(context, query, variables)
