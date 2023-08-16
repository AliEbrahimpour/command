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


before run it you can false example dags in docker-compose.yml file:
```
AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
```



## Add sample File
```
cp sample_airflow.py ./dags
```

## Running Airflow
```
docker compose up -d 
```

after run it you can see dags in dashboard 
```
http://127.0.0.1:8080/home
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


## Cleaning up
```
docker compose down --volumes --rmi all
```



source:
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
