from botocore.config import Config

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