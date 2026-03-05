import argparse
import os
import json
from datetime import date, datetime, timedelta, time, timezone
from src import (
    ExtractGlueCatalog,
    AWS_GLUE_ALL_DATABASES,
    AWS_GLUE_ALL_TABLES_COLS,
    ExtractIamPolicies,
    AWS_IAM_ALL_USERS,
    AWS_IAM_ALL_GROUPS,
    AWS_IAM_USERS_GROUPS,
    AWS_IAM_ALL_POLICIES,
    AWS_IAM_GROUPS_POLICIES,
    AWS_IAM_POLICIES_VERSION,
    AWS_IAM_GROUPS_POLICIES_INLINE,
    AWS_IAM_USERS_POLICIES_INLINE,
    ExtractEmrClustersMetrics,
    AWS_EMR_CLUSTERS,
    AWS_EMR_STEPS,
    AWS_EMR_CLUSTERS_CREATED_AFTER,
    AWS_EMR_CLUSTERS_QTD_DIAS_CONSULTA,
    ExtractAthenaLogs,
    AWS_EMR_ATHENA_LOGS
)

def save_json_file(json_data, json_target_folder,json_file):
    if not os.path.exists(json_target_folder):
        os.makedirs(json_target_folder)

    file_path = os.path.join(json_target_folder, json_file)
    with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4, default=custom_serializer)

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
                default=custom_serializer
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

def custom_serializer(obj):
    # Converte para formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')

def print_message_with_time(message):
    # Função para imprimir mensagem com data e hora
    print(datetime.now().strftime("[%d/%m/%Y %H:%M:%S.%f]") + ' ' + message)

def read_json_keys(json_folder, keys):
    if not os.path.exists(json_folder):
        print(f'Erro: A pasta "{json_folder}" de arquivos JSON não foi encontrada.')
        return

    list = []
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_folder, json_file)

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    dados = json.load(f)

                    # Captura apenas os campos desejados usando dictionary comprehension
                    # Se o campo não existir, retorna None por segurança
                    values = {key: dados.get(key) for key in keys}

                    # Adiciona ao dicionário principal usando o nome do arquivo como chave
                    list.append(values)
            except FileNotFoundError:
                return {"error": "Arquivo não encontrado."}
            except json.JSONDecodeError:
                return {"error": "Erro ao ler o formato JSON."}
    return list

def import_all_glue_databases():
    if os.path.exists(AWS_GLUE_ALL_DATABASES):
        print(f'A pasta "{AWS_GLUE_ALL_DATABASES}" já existe na pasta de dados.')
        return

    print("Iniciando a importação dos esquemas do GLUE.")
    aws = ExtractGlueCatalog()
    save_json_files(aws.query_all_databases(), AWS_GLUE_ALL_DATABASES, "database")

def import_all_glue_table_cols():
    if os.path.exists(AWS_GLUE_ALL_TABLES_COLS):
        print(f'A pasta "{AWS_GLUE_ALL_TABLES_COLS}" já existe na pasta de dados.')
        return

    print("Iniciando a importação das tabelas e colunas do GLUE.")
    aws = ExtractGlueCatalog()
    database_names = read_json_files(AWS_GLUE_ALL_DATABASES, 'Name')
    save_json_files(aws.query_all_table_cols(database_names), AWS_GLUE_ALL_TABLES_COLS, "table")

def import_all_iam_users():
    if os.path.exists(AWS_IAM_ALL_USERS):
        print(f'A pasta "{AWS_IAM_ALL_USERS}" já existe na pasta de dados.')
        return

    print("Iniciando a importação dos usuários do IAM.")
    aws = ExtractIamPolicies()
    save_json_files(aws.query_all_iam_users(), AWS_IAM_ALL_USERS, "user")

def import_all_iam_groups():
    if os.path.exists(AWS_IAM_ALL_GROUPS):
        print(f'A pasta "{AWS_IAM_ALL_GROUPS}" já existe na pasta de dados.')
        return

    print("Iniciando a importação dos grupos usuários do IAM.")
    aws = ExtractIamPolicies()
    save_json_files(aws.query_all_iam_groups(), AWS_IAM_ALL_GROUPS, "group")

def import_iam_users_groups():
    if os.path.exists(AWS_IAM_USERS_GROUPS):
        print(f'A pasta "{AWS_IAM_USERS_GROUPS}" já existe na pasta de dados.')
        return

    print("Criando a tabela associativa entre usuários e grupos do IAM.")
    aws = ExtractIamPolicies()
    user_names = read_json_files(AWS_IAM_ALL_USERS, 'UserName')
    save_json_files(aws.query_iam_user_groups(user_names), AWS_IAM_USERS_GROUPS, "user_group")

def import_iam_all_policies():
    if os.path.exists(AWS_IAM_ALL_POLICIES):
        print(f'A pasta "{AWS_IAM_ALL_POLICIES}" já existe na pasta de dados.')
        return

    print("Iniciando a importação das políticas do IAM.")
    aws = ExtractIamPolicies()
    save_json_files(aws.query_aim_all_policies(), AWS_IAM_ALL_POLICIES, "policy")

def import_iam_groups_policies():
    if os.path.exists(AWS_IAM_GROUPS_POLICIES):
        print(f'A pasta "{AWS_IAM_GROUPS_POLICIES}" já existe na pasta de dados.')
        return

    print("Criando a tabela associativa entre grupos e políticas do IAM.")
    aws = ExtractIamPolicies()
    groups_names = read_json_files(AWS_IAM_ALL_GROUPS, 'GroupName')
    save_json_files(aws.query_iam_groups_policies(groups_names), AWS_IAM_GROUPS_POLICIES, "group_policy")

def import_iam_policies_version():
    if os.path.exists(AWS_IAM_POLICIES_VERSION):
        print(f'A pasta "{AWS_IAM_POLICIES_VERSION}" já existe na pasta de dados.')
        return

    print("Iniciando a importação dos documentos de políticas do IAM.")
    aws = ExtractIamPolicies()

    keys_values = read_json_keys(AWS_IAM_ALL_POLICIES, ['Arn', 'DefaultVersionId', 'AttachmentCount'])
    # Filtrando: Mantém apenas os dicionários onde AttachmentCount > 0
    keys_values = [item for item in keys_values if item['AttachmentCount'] > 0]

    data = aws.query_iam_policies_version(keys_values)
    save_json_files(data, AWS_IAM_POLICIES_VERSION, "policy_version")

def import_group_policies_inline():
    if os.path.exists(AWS_IAM_GROUPS_POLICIES_INLINE):
        print(f'A pasta "{AWS_IAM_GROUPS_POLICIES_INLINE}" já existe na pasta de dados.')
        return

    print("Iniciando a importação das políticas IN LINE dos grupos do IAM.")
    aws = ExtractIamPolicies()
    group_names = read_json_files(AWS_IAM_ALL_GROUPS, 'GroupName')

    data = aws.query_group_policies_inline(group_names)
    save_json_files(data, AWS_IAM_GROUPS_POLICIES_INLINE, "group_policy_inline")

def import_user_policies_inline():
    if os.path.exists(AWS_IAM_USERS_POLICIES_INLINE):
        print(f'A pasta "{AWS_IAM_USERS_POLICIES_INLINE}" já existe na pasta de dados.')
        return

    print("Iniciando a importação das políticas IN LINE dos usuários do IAM.")
    aws = ExtractIamPolicies()
    user_names = read_json_files(AWS_IAM_ALL_USERS, 'UserName')

    data = aws.query_user_policies_inline(user_names)
    save_json_files(data, AWS_IAM_USERS_POLICIES_INLINE, "user_policy_inline")

def import_emr_clusters():
    print("Iniciando a importação das métricas dos clusters do EMR.")
    # Gerando as datas a partir do dado parametrizado.
    initial_day = AWS_EMR_CLUSTERS_CREATED_AFTER
    final_day = date.today()
    delta = timedelta(days=1)

    if initial_day > final_day:
        print(f"A data inicial de consulta é inválida: {initial_day}.Precisa ser anterior ou igual a hoje.")
        return

    if (final_day - initial_day).days > AWS_EMR_CLUSTERS_QTD_DIAS_CONSULTA:
        print(f"A quantidade máxima de dias por consulta é de {AWS_EMR_CLUSTERS_QTD_DIAS_CONSULTA} dias.")
        return

    # Define o fuso horário de Brasília (UTC-3)
    fuso_brasilia = timezone(timedelta(hours=-3))
    days = []
    while (initial_day <= final_day):
        days.append(initial_day)
        initial_day += delta

    aws = ExtractEmrClustersMetrics()

    for day in days:
        initial_date = datetime.combine(day, time(0, 0, 0), fuso_brasilia)
        final_date = datetime.combine(day, time(23, 59, 59), fuso_brasilia)
        index = day.strftime("%Y%m%d")

        print(f"Importando para initial_date: {initial_date}; final_date: {final_date}.")

        data = aws.query_clusters_and_steps(initial_date, final_date)
        if len(data[0]) > 0:
            file_name = f'[{index}]cluster.json'
            save_json_file(data[0], AWS_EMR_CLUSTERS, file_name)

            step_file_name = f'[{index}]step.json'
            save_json_file(data[1], AWS_EMR_STEPS, step_file_name)

def import_athena_logs():
    print("Iniciando a importação dos logs da Athena.")
    index = date.today().strftime("%Y%m%d")
    aws = ExtractAthenaLogs()

    initial_date = datetime.now(timezone.utc) - timedelta(hours=36)
    data = aws.query_athena_all_logs(initial_date)
    save_json_file(data, AWS_EMR_ATHENA_LOGS, f"[{index}]athena_logs.json")

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
        "--emr",
        action="store_true",
        help="Importa os dados de clusters e jobs do EMR, dado uma data da criação do cluster."
    )

    parser.add_argument(
        "--athena",
        action='store_true',
        help="Importa os logs de execução de querys do Athena."
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Testando novas funcionalidades"
    )

    # Analisa os argumentos vindo do terminal.
    args, unknown = parser.parse_known_args()

    if args.glue:
        import_all_glue_databases()
        import_all_glue_table_cols()
    elif args.iam:
        import_all_iam_users()
        import_all_iam_groups()
        import_iam_users_groups()
        import_iam_all_policies()
        import_iam_groups_policies()
        import_iam_policies_version()
        import_group_policies_inline()
        import_user_policies_inline()
    elif args.emr:
        import_emr_clusters()
    elif args.athena:
        import_athena_logs()
    elif unknown:
        print(f"Argumento desconhecido {unknown}.")
        parser.print_help()
        return
    else:
        parser.print_help()
        return

    print('Operação Concluída.')

# Só permite rodar este script diretamente.
if __name__ == "__main__":
    main()