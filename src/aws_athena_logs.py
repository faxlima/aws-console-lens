import boto3
from .params import (
    REGION_NAME,
    CONFIG
)
from datetime import datetime, timezone

ATHENA = boto3.client("athena", region_name=REGION_NAME, config=CONFIG)

class ExtractAthenaLogs:
    def query_athena_logs(self):
        logs = []
        paginator = ATHENA.get_paginator("list_query_executions")

        for page in paginator.paginate():
            query_exec_ids = page['QueryExecutionIds']
            
            if not query_exec_ids:
                print("Não foram recuperados Query Execution IDs.")
                break
            
            # Buscando os detalhes em lotes de 50 (limite da API)
            details = ATHENA.batch_get_query_execution(QueryExecutionIds=query_exec_ids)
            logs.extend(details)
            
        return logs
    
    def query_athena_all_logs(self, initial_date: datetime):
        all_logs = []
        paginator = ATHENA.get_paginator("list_query_executions")

        if initial_date.tzinfo is None:
            initial_date = initial_date.replace(tzinfo=timezone.utc)

        i=0
        qtd_reg=0
        for page in paginator.paginate():
            query_exec_ids = page.get('QueryExecutionIds', [])

            if not query_exec_ids:
                # Vai para a próxima página se houver, em vez de parar tudo
                continue

            # A API batch_get_query_execution processa até 50 IDs por vez
            response = ATHENA.batch_get_query_execution(QueryExecutionIds=query_exec_ids)            
            logs = response.get('QueryExecutions', [])

            for log in logs:
                data_log = log['Status']['SubmissionDateTime']
                
                # Verificação Incremental:
                # Se o log atual for mais antigo que a data_inicio, 
                # paramos tudo, pois os próximos serão ainda mais antigos.
                if data_log < initial_date:
                    print(f"Alcançada data de corte: {data_log}. Finalizando...")
                    return all_logs
                all_logs.append(log)

            qtd_reg += len(logs)
            i+=1
            print(f'Página {i}. Coletados {qtd_reg} registros.')
        return all_logs