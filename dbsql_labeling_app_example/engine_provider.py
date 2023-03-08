from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

from dbsql_labeling_app_example.endpoint_info import provide_endpoint_info
from dbsql_labeling_app_example.mode import debug_mode


def get_prepared_engine():
    if Path(".env").exists():
        print("Found the .env file, loading it's content")
        load_dotenv()
    else:
        print(
            ".env file is non existent, please make sure that you've provided the required environment variables"
        )

    endpoint_info = provide_endpoint_info()

    ## Set up SQL Alchemy engine
    engine = create_engine(
        f"databricks://token:{endpoint_info.token}@{endpoint_info.server_hostname}?http_path={endpoint_info.http_path}&catalog={endpoint_info.catalog}&schema={endpoint_info.database}",
        echo=debug_mode,
    )

    return engine
