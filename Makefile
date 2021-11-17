include .env

build:
	docker-compose up -d --force-recreate --remove-orphans
	sleep 120
	docker exec airflow airflow users create --username admin --password admin --role Admin --firstname atif --lastname muhammad --email atif.muhammad0001@gmail.com
	docker exec airflow airflow connections add 'airflow-metastore' --conn-uri 'postgresql://airflow:airflow@airflow-metastore:54321/airflow'
	docker exec airflow airflow connections add 'transactional_db' --conn-uri 'postgresql://${TRANSACTIONAL_DB_USER}:${TRANSACTIONAL_DB_PASSWORD}@${TRANSACTIONAL_DB_HOST}:5432/${TRANSACTIONAL_DB}'
	docker exec airflow airflow connections add 'data_warehouse_db' --conn-uri 'postgresql://${DATA_WAREHOUSE_DB_USER}:${DATA_WAREHOUSE_DB_PASSWORD}@${DATA_WAREHOUSE_DB_HOST}:5432/${DATA_WAREHOUSE_DB}'

stop:
	docker-compose down

# testing:
# 	docker exec airflow pytest -v

