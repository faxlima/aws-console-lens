import boto3
import botocore
from botocore.exceptions import ClientError
import os
import json
from datetime import datetime
from .params import CONFIG, AWS_GLUE_ALL_DATABASES

GLUE = boto3.client('glue', config=CONFIG)

class ExtractGlueCatalog:
    def query_all_databases(self):
        paginator = GLUE.get_paginator('get_databases')

        databases = []
        for page in paginator.paginate():
            databases.extend(page['DatabaseList'])
        return databases

    def get_json_database_names(self, json_folder):
        if not os.path.exists(AWS_GLUE_ALL_DATABASES):
            print(f'Erro: A pasta {AWS_GLUE_ALL_DATABASES} não foi encontrada.')
            return

        database_name = []
        for json_file in os.listdir(json_folder):
            if json_file.endswith('.json'):
                json_path = os.path.join(json_folder, json_file)

                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        database_name.append(json.load(f).get('Name'))
                except Exception as e:
                    print(f'Erro ao ler o arquivo {json_path}: {e}')
        return database_name

    def query_all_table_cols(self):
        database_names = self.get_json_database_names(AWS_GLUE_ALL_DATABASES)
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