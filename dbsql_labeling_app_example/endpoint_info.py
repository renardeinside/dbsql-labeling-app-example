import os
from dataclasses import dataclass


@dataclass
class EndpointInfo:
    """Represents information required to connect to the DBSQL endpoint"""

    # endpoint coordinates
    server_hostname: str
    token: str
    http_path: str
    # data catalog coordinates
    catalog: str
    database: str


def provide_endpoint_info() -> EndpointInfo:
    required_env_variables = [
        "DATABRICKS_HOST",
        "DATABRICKS_TOKEN",
        "DATABRICKS_HTTP_PATH",
    ]

    for _env in required_env_variables:
        if not os.environ.get(_env):
            raise EnvironmentError(f"Required env variable {_env} is not provided")

    return EndpointInfo(
        server_hostname=os.environ["DATABRICKS_HOST"],
        token=os.environ["DATABRICKS_TOKEN"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        catalog=os.environ.get("DATABRICKS_CATALOG", "hive_metastore"),
        database=os.environ.get("DATABRICKS_DATABASE", "default"),
    )
