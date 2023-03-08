from dbsql_labeling_app_example.engine import Label, engine
from dbsql_labeling_app_example.source_loader import load_source

if __name__ == "__main__":
    Label.metadata.create_all(bind=engine)
    data = load_source()
    with engine.connect() as connection:
        print("writing labels data into DBSQL. Table will be truncated before writes.")
        connection.execute(f"TRUNCATE TABLE {Label.__tablename__}")
        data.to_sql(
            "labels",
            if_exists="append",
            con=connection,
            index=False,
            chunksize=10_000,
            method="multi",
        )
        print(f"Write finished, total written records: {len(data)}")
