import boto3
import json
from .params import CONFIG, AWS_CLOUDTRAIL_HISTORY_QTD_CONSULTA

TRAIL = boto3.client('cloudtrail', config=CONFIG)

class ExtractCloudTrailEventHistory:
    def query_cloudtrail_event_history(self, max_items=50):
        events = []
        paginator = TRAIL.get_paginator('lookup_events')

        page_iterator = paginator.paginate(
            PaginationConfig={
                'PageSize': 50, # Máximo permitido por página.
                'MaxItems': AWS_CLOUDTRAIL_HISTORY_QTD_CONSULTA # Opcional: limite total de itens para não baixar o histórico inteiro
            }
        )

        for page in page_iterator:
            for event in page.get('Events', []):
                try:
                    events.append(json.loads(event['CloudTrailEvent']))
                except (KeyError, json.JSONDecodeError):
                    continue

        return events