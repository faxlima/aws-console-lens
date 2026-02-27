import argparse
import os
import json
from src import (
    ExtractGlueCatalog,
    AWS_GLUE_ALL_DATABASES,
    AWS_GLUE_ALL_TABLES_COLS,
    ExtractIamPolicies,
    AWS_IAM_ALL_USERS,
    AWS_IAM_ALL_GROUPS,
    AWS_IAM_USERS_GROUPS
)

def save_json_files(list_of_json, json_target_folder, item_type):
    if not os.path.exists(json_target_folder):
        os.makedirs(json_target_folder)

    for index, item in enumerate(list_of_json):
        file_name = f'{item_type}_{index}.json'
        file_path = os.path.join(json_target_folder, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(
                item,
                f,
                ensure_ascii=False,
                indent=4,
                default=str
            )

def read_json_files(json_folder, key):
    if not os.path.exists(json_folder):
        print(f'Erro: A pasta "{json_folder}" de arquivos JSON não foi encontrada.')
        return

    values = []
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_folder, json_file)

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    values.append(json.load(f).get(key))
            except FileNotFoundError:
                return {"error": "Arquivo não encontrado."}
            except json.JSONDecodeError:
                return {"error": "Erro ao ler o formato JSON."}
    return values

def import_all_glue_databases():
    print("Iniciando a importação de Databases do GLUE.")
    aws = ExtractGlueCatalog()
    save_json_files(aws.query_all_databases(), AWS_GLUE_ALL_DATABASES, "database")

def import_all_glue_table_cols():
    if os.path.exists(AWS_GLUE_ALL_TABLES_COLS):
        print(f'A pasta "{AWS_GLUE_ALL_TABLES_COLS}" já existe na pasta de dados.')
        return

    print("Iniciando a importação de Tabelas e Colunas do GLUE.")
    aws = ExtractGlueCatalog()
    database_names = read_json_files(AWS_GLUE_ALL_DATABASES, 'Name')
    save_json_files(aws.query_all_table_cols(database_names), AWS_GLUE_ALL_TABLES_COLS, "table")

def import_all_iam_users():
    if os.path.exists(AWS_IAM_ALL_USERS):
        print(f'A pasta "{AWS_IAM_ALL_USERS}" já existe na pasta de dados.')
        return

    aws = ExtractIamPolicies()
    save_json_files(aws.query_all_iam_users(), AWS_IAM_ALL_USERS, "user")

def import_all_iam_groups():
    if os.path.exists(AWS_IAM_ALL_GROUPS):
        print(f'A pasta "{AWS_IAM_ALL_GROUPS}" já existe na pasta de dados.')
        return

    aws = ExtractIamPolicies()
    save_json_files(aws.query_all_iam_groups(), AWS_IAM_ALL_GROUPS, "group")

def import_users_groups():
    if os.path.exists(AWS_IAM_USERS_GROUPS):
        print(f'A pasta "{AWS_IAM_USERS_GROUPS}" já existe na pasta de dados.')
        return

    aws = ExtractIamPolicies()
    save_json_files(aws.query_iam_user_groups(), AWS_IAM_USERS_GROUPS, "user_group")

def main():
    parser = argparse.ArgumentParser(
        description="aws-console-lens: Uma lente sobre seus recursos AWS."
    )

    parser.add_argument(
        "--glue",
        action="store_true",
        help="Importa os dados do Catálogo Glue da sua conta AWS."
    )

    parser.add_argument(
        "--iam",
        action="store_true",
        help="Importa os dados das Políticas de Gerenciamento de Acesso e Identidade da sua conta AWS."
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Testando novas funcionalidades"
    )

    # Analisa os argumentos vindo do terminal.
    args = parser.parse_args()

    if args.glue:
        import_all_glue_databases()
        import_all_glue_table_cols()

    if args.iam:
        import_all_iam_users()
        import_all_iam_groups()
        import_users_groups()

    if args.test:
        data = read_json_files(AWS_GLUE_ALL_DATABASES, 'Name')
        print(type(data))
        print(data)

# Só permite rodar este script diretamente.
if __name__ == "__main__":
    main()
    print('Operação Concluída.')