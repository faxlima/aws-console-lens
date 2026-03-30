from .aws_glue_datacatalog import ExtractGlueCatalog
from .aws_iam_policies import ExtractIamPolicies
from .aws_emr_clusters import ExtractEmrClustersMetrics
from .aws_athena_logs import ExtractAthenaLogs
from .aws_cloudtrail_event_history import ExtractCloudTrailEventHistory
from .params import (
    CONFIG,
    REGION_NAME,
    AWS_GLUE_ALL_DATABASES,
    AWS_GLUE_ALL_TABLES_COLS,
    AWS_IAM_ALL_USERS,
    AWS_IAM_ALL_GROUPS,
    AWS_IAM_USERS_GROUPS,
    AWS_IAM_ALL_POLICIES,
    AWS_IAM_GROUPS_POLICIES,
    AWS_IAM_POLICIES_VERSION,
    AWS_IAM_GROUPS_POLICIES_INLINE,
    AWS_IAM_USERS_POLICIES_INLINE,
    AWS_EMR_CLUSTERS,
    AWS_EMR_STEPS,
    AWS_EMR_CLUSTERS_CREATED_AFTER,
    AWS_EMR_CLUSTERS_QTD_DIAS_CONSULTA,
    AWS_EMR_ATHENA_LOGS,
    AWS_CLOUDTRAIL_HISTORY,
    AWS_CLOUDTRAIL_HISTORY_QTD_CONSULTA
)

"""
aws-console-lens: Ferramenta de auditoria e visibilidade AWS.
"""

__version__ = "0.1.13"
__author__ = "Francisco Alex Xavier de Lima"
__email__ = "alex.xavier.lima@gmail.com"