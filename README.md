# Data labeling app example with Python, Dash and Databricks SQL

## Prerequisites

- Databricks SQL endpoint
- Locally: Docker, Makefile

## Quick demo

#TODO 

## How to 

1. Create or start an existing SQL endpoint of any size in your Databricks workspace
2. On the local machine, clone the repository and create `.env` file in the repository directory. Follow the `.env.sample` for instructions. 
3. Build the demo container:

```bash
docker build -t dbsql-labeling-app-example-demo -f dockerfiles/Dockerfile.demo .
```

4. Prepare the data (please note that this script will run `TRUNCATE TABLE` command on the table called `labels` stored in a given catalog and database. Please make sure that such table doesn't exist!)

```
docker run \
    -it \
    --env-file=.env \
    dbsql-labeling-app-example-demo \
    python dbsql_labeling_app_example/loader.py
```

5. Start the UI:

```
docker run \
    -it \
    --env-file=.env \
    -p 8050:8050 \
    dbsql-labeling-app-example-demo \
    python dbsql_labeling_app_example/app.py
```

5. Open [http://localhost:8050](http://localhost:8050) and enjoy the new application 🔥


## Developer instructions

- Use the VSCode + DevContainers extension
- After the start of the DevContainer run this command to open the poetry shell:

```
> poetry shell
``` 

- For UI development with hot reloading run:

```
> DEBUG=True python dbsql_labeling_app_example/app.py
```

- For ETL part, check the `dbsql_labeling_app_example/loader.py` source code

## Technologies used

- [Databricks SQL](https://www.databricks.com/product/databricks-sql)
- [Databricks SQL Connector](https://docs.databricks.com/dev-tools/python-sql-connector.html)
- [Dash by Plotly](https://plotly.com/dash/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)