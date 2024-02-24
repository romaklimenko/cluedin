from enum import Enum

from .context import Context
from .gql import org_gql


class RuleScope(Enum):
    """
    Enum representing the scope of a rule (DataPart, Entity (Golden Record), Survivorship).
    """

    DATA_PART = 'DataPart'
    ENTITY = 'Entity'
    SURVIVORSHIP = 'Survivorship'


def get_rules(context: Context, scope=RuleScope.DATA_PART) -> dict:
    """
    Retrieves rules based on the specified parameters.

    Args:
            context (Context): The context object.
            scope (RuleScope, optional): The scope of the rules. Defaults to RuleScope.DATA_PART.

    Returns:
            dict: The rules data.

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
        "scope": scope.value
    }

    return org_gql(context, query, variables)
