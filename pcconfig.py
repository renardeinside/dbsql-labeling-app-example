import pynecone as pc

config = pc.Config(
    app_name="dbsql_labeling_app_example",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
