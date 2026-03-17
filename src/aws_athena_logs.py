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
        
        # Garante que initial_date tenha timezone para comparação
        if initial_date.tzinfo is None:
            initial_date = initial_date.replace(tzinfo=timezone.utc)
        
        # 1. Buscar todos os workgroups disponíveis
        try:
            workgroups_resp = ATHENA.list_work_groups()
            workgroup_names = [wg['Name'] for wg in workgroups_resp.get('WorkGroups', [])]
        except Exception as e:
            print(f"Erro ao listar workgroups: {e}")
            return []
        print(f"Workgroups encontrados: {workgroup_names}")

        # 2. Iterar sobre cada Workgroup
        for wg in workgroup_names:
            print(f"\n Iniciando coleta no Workgroup: {wg}")
            
            # O paginator precisa do WorkGroup fixo para cada iteração
            paginator = ATHENA.get_paginator("list_query_executions")

            i=0
            qtd_reg_wg=0
            
            # Pagina as queries especificamente DESTE workgroup
            for page in paginator.paginate(WorkGroup=wg):
                query_exec_ids = page.get('QueryExecutionIds', [])
            

                if not query_exec_ids:
                    # Vai para a próxima página se houver, em vez de parar tudo
                    continue

                # A API batch_get_query_execution processa até 50 IDs por vez
                response = ATHENA.batch_get_query_execution(QueryExecutionIds=query_exec_ids)            
                logs = response.get('QueryExecutions', [])

                stop_current_wg = False
                for log in logs:
                    data_log = log['Status']['SubmissionDateTime']
                
                    # Se o log atual for mais antigo que a data_inicio, 
                    # paramos tudo, pois os próximos serão ainda mais antigos.
                    if data_log < initial_date:
                        print(f"[{wg}] Alcançada data de corte: {data_log}. Finalizando...")
                        stop_current_wg = True
                        break                    
                    
                    all_logs.append(log)
                if stop_current_wg:
                    break

                qtd_reg_wg += len(logs)
                i+=1
                print(f'[{wg}] Página {i}. Coletados {qtd_reg_wg} registros.')
        print(f"\nTotal final de logs coletados em todos os grupos: {len(all_logs)}")
        return all_logs