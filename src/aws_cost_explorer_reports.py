import boto3

from .params import (
    REGION_NAME,
    CONFIG,
)

EC = boto3.client("ce", region_name=REGION_NAME, config=CONFIG)

class ExtractCostReports:
    def query_cost(self, period: dict, grain: str, filter: dict, group: dict):
        try:
            result = EC.get_cost_and_usage(
                TimePeriod=period,
                Granularity=grain,
                Filter=[filter],
                Metrics=["UNBLENDED_COST"],
                GroupBy=[group]
            )
            return result
        except Exception as e:
            print(f"Erro ao consultar o CoastExplorer.get_cost_and_usage: {e}")
            return None
            
    def query_cost_resources(self, period: dict, grain: str, filter: dict, group: dict):
        try:
            result = EC.get_cost_and_usage_with_resources(
                TimePeriod=period,
                Granularity=grain,
                Filter=[filter],
                Metrics=["UNBLENDED_COST"],
                GroupBy=[group]
            )
            return result
        except Exception as e:
            print(f"Erro ao consultar o CoastExplorer.get_cost_and_usage_with_resources: {e}")
            return None
    
    def query_ec2_cost(self, period: dict):
        service_filter = {
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': [
                    'Amazon Elastic Compute Cloud - Compute',
                    'Amazon Elastic Compute Cloud - EC2-Other'
                ]
            }
        }

        group = {
            "Type": "DIMENSION",
            "Key": "SERVICE"
        }  
        
        return self.query_service_cost(period, "MONTHLY", service_filter, group)
    
    def query_ec2_cost_with_resources(self, period: dict):
        service_filter = {
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': [
                    'Amazon Elastic Compute Cloud - Compute',
                    'Amazon Elastic Compute Cloud - EC2-Other'
                ]
            }
        }

        group = {
            "Type": "DIMENSION",
            "Key": "RESOURCE_ID"
        } 
        
        return self.query_cost_resources(period, "DAILY", service_filter, group)
    
    def print_my_services(self, period):
        result = EC.get_dimension_values(
            TimePeriod=period,
            Dimension='SERVICE'
        )
        return result