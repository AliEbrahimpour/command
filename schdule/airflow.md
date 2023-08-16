# Run Apache AirFlow with Docker

## Fetching docker-compose.yaml
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/docker-compose.yaml'
```


## Setting the right Airflow user
```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## Initialize the database
```
docker compose up airflow-init
```

## Running Airflow
```
docker compose up -d 
```

## Running the CLI commands
```
docker compose run airflow-worker airflow info
```

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.3/airflow.sh'
chmod +x airflow.sh
```


```
./airflow.sh bash
```

```
./airflow.sh python

```




source:
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
