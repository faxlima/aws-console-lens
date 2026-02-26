import argparse
import os
import json
from src import (
    ExtractGlueCatalog,
    AWS_GLUE_ALL_DATABASES,
    AWS_GLUE_ALL_TABLES_COLS
)

def save_json_files(list_of_json, json_target_folder, item_type):
    if not os.path.exists(json_target_folder):
        os.makedirs(json_target_folder)

    for index, item in enumerate(list_of_json):
        file_name = f'{item_type}-{index}.json'
        file_path = os.path.join(json_target_folder, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(
                item,
                f,
                ensure_ascii=False,
                indent=4,
                default=str
            )

def import_all_glue_databases():
    if os.path.exists(AWS_GLUE_ALL_DATABASES):
        print(f'A pasta "{AWS_GLUE_ALL_DATABASES}" já existe na pasta de dados.')
        return

    print("Iniciando a importação de Databases do GLUE.")
    aws = ExtractGlueCatalog()
    save_json_files(aws.query_all_databases(), AWS_GLUE_ALL_DATABASES, "database")

def import_all_table_cols():
    if os.path.exists(AWS_GLUE_ALL_TABLES_COLS):
        print(f'A pasta "{AWS_GLUE_ALL_TABLES_COLS}" já existe na pasta de dados.')
        return

    print("Iniciando a importação de Tabelas e Colunas do GLUE.")
    aws = ExtractGlueCatalog()
    save_json_files(aws.query_all_table_cols(), AWS_GLUE_ALL_TABLES_COLS, "table")

def main():
    parser = argparse.ArgumentParser(
        description="aws-console-lens: Uma lente sobre seus recursos AWS."
    )

    parser.add_argument(
        "--glue",
        action="store_true",
        help="Importa os dados do Catálogo Glue da sua conta AWS."
    )

    # Analisa os argumentos vindo do terminal.
    args = parser.parse_args()

    # Se o usuário não passar nenhuma flag, mostra a ajuda
    if not (args.glue):
        parser.print_help()
        return

    if args.glue:
        import_all_glue_databases()
        import_all_table_cols()
        return

# Só permite rodar este script diretamente.
if __name__ == "__main__":
    main()
    print('Operação Concluída.')