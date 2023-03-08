from dbsql_labeling_app_example.engine import Label, engine
from dbsql_labeling_app_example.source_loader import load_source

if __name__ == "__main__":
    print("Creating database and table")
    Label.metadata.create_all(bind=engine)
    print("Metadata prepared")
    print("Loading the sample sklearn dataset")
    data = load_source()
    print("sklearn dataset prepared")
    with engine.connect() as connection:
        print("Writing labels data into DBSQL. Table will be truncated before writes.")
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
