from data_pipelines.sport_monks.dag_builder import SportMonksDownloadDagBuilder
from data_pipelines.sport_monks.sport_monks_client import SportMonksGetEndpoints

globals()["sport_monks_dags"] = SportMonksDownloadDagBuilder(
    SportMonksGetEndpoints.PLAYERS, None
).build()
