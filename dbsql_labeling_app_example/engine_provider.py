from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

from dbsql_labeling_app_example.endpoint_info import provide_endpoint_info
from dbsql_labeling_app_example.mode import debug_mode


def get_prepared_engine():
    print("Loading environment variables")
    if Path(".env").exists():
        print("Found the .env file, loading it's content")
        load_dotenv()
    else:
        print(
            ".env file is non existent, please make sure that you've provided the required environment variables"
        )

    endpoint_info = provide_endpoint_info()

    print(f"Using catalog {endpoint_info.catalog}")
    print(f"Using database {endpoint_info.database}")

    # Set up SQL Alchemy engine to create a Database
    pre_engine = create_engine(
        f"databricks://token:{endpoint_info.token}@{endpoint_info.server_hostname}?http_path={endpoint_info.http_path}&catalog={endpoint_info.catalog}",
        echo=debug_mode,
    )

    with pre_engine.connect() as conn:
        conn.execute(f"CREATE DATABASE IF NOT EXISTS {endpoint_info.database}")

    # use the created database
    engine = create_engine(
        f"databricks://token:{endpoint_info.token}@{endpoint_info.server_hostname}?http_path={endpoint_info.http_path}&catalog={endpoint_info.catalog}&schema={endpoint_info.database}",
        echo=debug_mode,
    )

    return engine
