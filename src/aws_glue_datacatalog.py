import boto3
import botocore
from botocore.exceptions import ClientError
from .params import CONFIG

GLUE = boto3.client('glue', config=CONFIG)

class ExtractGlueCatalog:
    def query_all_databases(self):
        paginator = GLUE.get_paginator('get_databases')

        databases = []
        for page in paginator.paginate():
            databases.extend(page['DatabaseList'])
        return databases

    def query_all_table_cols(self, database_names):
        tables = []

        for database_name in database_names:
            try:
                paginator = GLUE.get_paginator('get_tables')
                for page in paginator.paginate(DatabaseName=database_name):
                    tables.extend(page['TableList'])
            except GLUE.exceptions.EntityNotFoundException:
                print(f'⚠️ Aviso: O banco de dados "{database_name}" não foi encontrado no Glue.')
                continue # Pula para o próximo database da lista.
            except botocore.exceptions.ClientError as e:
                # Trata outros erros como a falta de permissão ao Throttling.
                erro_code = e.response['Error']['Code']
                print(f'❌ Erro de cliente no banco "{database_name}": {erro_code}!')
                continue
        return tables