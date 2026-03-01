from .aws_glue_datacatalog import ExtractGlueCatalog
from .aws_iam_policies import ExtractIamPolicies
from .params import (
    CONFIG,
    REGION_NAME,
    AWS_GLUE_ALL_DATABASES,
    AWS_GLUE_ALL_TABLES_COLS,
    AWS_IAM_ALL_USERS,
    AWS_IAM_ALL_GROUPS,
    AWS_IAM_USERS_GROUPS,
    AWS_IAM_ALL_POLICIES,
    AWS_IAM_GROUPS_POLICIES
)

"""
aws-console-lens: Ferramenta de auditoria e visibilidade AWS.
"""

__version__ = "0.1.1"
__author__ = "Francisco Alex Xavier de Lima"
__email__ = "alex.xavier.lima@gmail.com"