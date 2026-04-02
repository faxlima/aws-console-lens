from botocore.config import Config
from datetime import date

REGION_NAME = 'sa-east-1'

# Configuração do cliente AWS com retries automáticos
CONFIG = Config(
    retries={
        'max_attempts':10, # Número máximo de tentativas.
        'mode':'adaptive' # Ajusta automaticamente o tempo de espera.
    }
)

# Diretórios de armazenamento de dados
AWS_GLUE_ALL_DATABASES = 'data/glue_all_databases/'
AWS_GLUE_ALL_TABLES_COLS = 'data/glue_all_tables_cols/'

AWS_IAM_ALL_USERS = 'data/iam_all_users/'
AWS_IAM_ALL_GROUPS = 'data/iam_all_groups/'
AWS_IAM_USERS_GROUPS = 'data/iam_users_groups/'
AWS_IAM_ALL_POLICIES = 'data/iam_all_policies/'
AWS_IAM_GROUPS_POLICIES = 'data/iam_groups_policies/'
AWS_IAM_GROUPS_POLICIES_INLINE = 'data/iam_groups_policies_inline/'
AWS_IAM_POLICIES_VERSION = 'data/iam_policies_version/'
AWS_IAM_USERS_POLICIES_INLINE = 'data/iam_users_policies_inline/'

AWS_EMR_CLUSTERS_CREATED_AFTER = date(2026,3,1)
AWS_EMR_CLUSTERS_QTD_DIAS_CONSULTA = 60
AWS_EMR_CLUSTERS = 'data/emr_clusters/'
AWS_EMR_STEPS = 'data/emr_steps/'

AWS_ATHENA_LOGS = 'data/athena_logs/'
AWS_ATHENA_QTD_HORAS = 48

AWS_CLOUDTRAIL_HISTORY_QTD_CONSULTA = 5000
AWS_CLOUDTRAIL_HISTORY = 'data/cloudtrail_history/'