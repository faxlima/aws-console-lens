import boto3
from .params import (
    REGION_NAME,
    CONFIG,
    AWS_EMR_CLUSTERS_STATES,
    AWS_EMR_CLUSTERS_CREATED_AFTER
)

EMR = boto3.client("emr", region_name=REGION_NAME, config=CONFIG)

class ExtractEmrClustersMetrics:
    def query_steps(self, clusters):
        steps = []
        paginator = EMR.get_paginator("list_steps")

        for cluster in clusters:
            page_iterator = paginator.paginate(ClusterId = cluster["Id"])

            # Coletando os itens do cluster.
            for page in page_iterator:
                # Adicionando chaves para identificar o cluster.
                for step in page["Steps"]:
                    step["ClusterId"] = cluster["Id"]
                    step["ClusterName"] = cluster["Name"]
                steps.extend(page["Steps"])
        return steps

    def query_clusters_and_steps(self, initial_date, final_date):
        cluster_paginator = EMR.get_paginator("list_clusters")

        # A paginação do EMR é realizada via iterador.
        cluster_iterator = cluster_paginator.paginate(
            CreatedAfter = initial_date,
            CreatedBefore = final_date
        )

        clusters = []
        steps = None
        for page in cluster_iterator:
            clusters.extend(page["Clusters"])

        steps = self.query_steps(clusters)
        return clusters, steps
