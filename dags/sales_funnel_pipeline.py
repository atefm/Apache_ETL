import datetime
import logging
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from sql.init import create_and_populate_transactional_tables
from sql.init import create_and_populate_warehouse_tables

import os

transactional_db_hook = PostgresHook("transactional_db")
warehouse_db_hook = PostgresHook("data_warehouse_db")


def sales_funnel_transformation():
    sql_stmt = create_and_populate_warehouse_tables.CREATE_SALES_FUNNEL
    warehouse_db_hook.run(sql_stmt)
    logging.info("successfully created sales funnel transformation table")


def create_table(table, hook):
    if table == "deals":
        sql_stmt = create_and_populate_transactional_tables.CREATE_DEALS_TABLE_SQL
    elif table == "invites":
        sql_stmt = create_and_populate_transactional_tables.CREATE_INVITES_TABLE_SQL
    elif table == "offers":
        sql_stmt = create_and_populate_transactional_tables.CREATE_OFFERS_TABLE_SQL
    else:
        sql_stmt = create_and_populate_transactional_tables.CREATE_ORDERS_TABLE_SQL

    hook.run(sql_stmt)
    logging.info('{}:{}'.format(table, "successfully created"))


def truncate_table(table, hook):
    sql_stmt = create_and_populate_transactional_tables.TRUNCATE_TABLE.format(table)
    hook.run(sql_stmt)
    logging.info('{}:{}'.format(table, "successfully truncated"))


def load_data(table):
    conn = PostgresHook("transactional_db").get_conn()
    cur = conn.cursor()
    sql_stmt = create_and_populate_transactional_tables.COPY_CSV_DATA_TO_DB.format(table)
    cwd = os.getcwd()
    with open(os.environ['PYTHONPATH'] + '/data/' + table + '.csv', 'r') as f:
        cur.copy_expert(sql_stmt, file=f)
        logging.info('{}:{}'.format(table, "loading data"))
        conn.commit()
        cur.close()


def copy_transactional_to_warehouse(**kwargs):
    dest_table = kwargs.get('dest_table')
    source_table = kwargs.get('source_table')
    data_to_copy = transactional_db_hook.get_records(sql=create_and_populate_warehouse_tables.GET_ALL_TABLE_DATA_SQL.
                                                     format(source_table))

    warehouse_db_hook.insert_rows(dest_table, data_to_copy, commit_every=1000)
    logging.info('{}:{}'.format(source_table, "successfully copied"))


dag = DAG(
    dag_id='sales_pipeline',
    start_date=datetime.datetime.now(),
    schedule_interval=None,
    tags=['sales', 'etl', 'dashboard']
)

# Create tables in transactional_db
creating_offers_table_task = PythonOperator(
    task_id='create_offers_table',
    dag=dag,
    op_kwargs={'table': 'offers', 'hook': transactional_db_hook},
    python_callable=create_table,
)

creating_invites_table_task = PythonOperator(
    task_id='create_invites_table',
    dag=dag,
    op_kwargs={'table': 'invites', 'hook': transactional_db_hook},
    python_callable=create_table,
)

creating_deals_table_task = PythonOperator(
    task_id='create_deals_table',
    dag=dag,
    op_kwargs={'table': 'deals', 'hook': transactional_db_hook},
    python_callable=create_table,
)

creating_orders_table_task = PythonOperator(
    task_id='create_orders_table',
    dag=dag,
    op_kwargs={'table': 'orders', 'hook': transactional_db_hook},
    python_callable=create_table,
)

# truncate tables
truncating_orders_table_task = PythonOperator(
    task_id='truncate_orders_table',
    dag=dag,
    op_kwargs={'table': 'orders', 'hook': transactional_db_hook},
    python_callable=truncate_table,
)

truncating_deals_table_task = PythonOperator(
    task_id='truncate_deals_table',
    dag=dag,
    op_kwargs={'table': 'deals', 'hook': transactional_db_hook},
    python_callable=truncate_table,
)

truncating_invites_table_task = PythonOperator(
    task_id='truncate_invites_table',
    dag=dag,
    op_kwargs={'table': 'invites', 'hook': transactional_db_hook},
    python_callable=truncate_table,
)

truncating_offers_table_task = PythonOperator(
    task_id='truncate_offers_table',
    dag=dag,
    op_kwargs={'table': 'offers', 'hook': transactional_db_hook},
    python_callable=truncate_table,
)

# load transactional tables
loading_offers_table_task = PythonOperator(
    task_id='load_offers_table',
    dag=dag,
    op_kwargs={'table': 'offers', 'hook': transactional_db_hook},
    python_callable=load_data,
)

loading_invites_table_task = PythonOperator(
    task_id='load_invites_table',
    dag=dag,
    op_kwargs={'table': 'invites', 'hook': transactional_db_hook},
    python_callable=load_data,
)

loading_deals_table_task = PythonOperator(
    task_id='load_deals_table',
    dag=dag,
    op_kwargs={'table': 'deals', 'hook': transactional_db_hook},
    python_callable=load_data,
)

loading_orders_table_task = PythonOperator(
    task_id='load_orders_table',
    dag=dag,
    op_kwargs={'table': 'orders', 'hook': transactional_db_hook},
    python_callable=load_data,
)

transactional_db_truncated_task = DummyOperator(
    task_id='transactional_db_truncated_task'
)

transactional_db_tables_ready_task = DummyOperator(
    task_id='transactional_db_tables_ready'
)

transactional_db_tables_loaded_ready_task = DummyOperator(
    task_id='transactional_db_tables_loaded_ready'
)

# create warehouse table
creating_warehouse_offers_table_task = PythonOperator(
    task_id='create_warehouse_offers_table',
    dag=dag,
    op_kwargs={'table': 'offers', 'hook': warehouse_db_hook},
    python_callable=create_table,
)

creating_warehouse_invites_table_task = PythonOperator(
    task_id='create_warehouse_invites_table',
    dag=dag,
    op_kwargs={'table': 'invites', 'hook': warehouse_db_hook},
    python_callable=create_table,
)

creating_warehouse_deals_table_task = PythonOperator(
    task_id='create_warehouse_deals_table',
    dag=dag,
    op_kwargs={'table': 'deals', 'hook': warehouse_db_hook},
    python_callable=create_table,
)

creating_warehouse_orders_table_task = PythonOperator(
    task_id='create_warehouse_orders_table',
    dag=dag,
    op_kwargs={'table': 'orders', 'hook': warehouse_db_hook},
    python_callable=create_table,
)

warehouse_db_tables_ready_task = DummyOperator(
    task_id='warehouse_db_tables_ready'
)

# load warehouse data
load_full_offers_data = PythonOperator(
    task_id='load_full_offers',
    python_callable=copy_transactional_to_warehouse,
    op_kwargs={
        'dest_table': 'offers',
        'source_table': 'offers',
    })

load_full_invites_data = PythonOperator(
    task_id='load_full_invites',
    python_callable=copy_transactional_to_warehouse,
    op_kwargs={
        'dest_table': 'invites',
        'source_table': 'invites',
    })

load_full_deals_data = PythonOperator(
    task_id='load_full_deals',
    python_callable=copy_transactional_to_warehouse,
    op_kwargs={
        'dest_table': 'deals',
        'source_table': 'deals',
    })

load_full_orders_data = PythonOperator(
    task_id='load_full_orders',
    python_callable=copy_transactional_to_warehouse,
    op_kwargs={
        'dest_table': 'orders',
        'source_table': 'orders',
    })

warehouse_db_tables_loaded_ready_task = DummyOperator(
    task_id='warehouse_db_tables_loaded_ready'
)

sales_funnel_transformation_task = PythonOperator(
    task_id = "sales_funnel_transformation_task",
    python_callable = sales_funnel_transformation
)


[creating_offers_table_task,
 creating_invites_table_task,
 creating_deals_table_task,
 creating_orders_table_task] >> transactional_db_tables_ready_task

transactional_db_tables_ready_task >> [truncating_orders_table_task,
                                       truncating_deals_table_task,
                                       truncating_invites_table_task,
                                       truncating_offers_table_task]

[truncating_orders_table_task,
 truncating_deals_table_task,
 truncating_invites_table_task,
 truncating_offers_table_task] >> transactional_db_truncated_task

transactional_db_truncated_task >> [loading_offers_table_task,
                                    loading_invites_table_task,
                                    loading_deals_table_task,
                                    loading_orders_table_task]

[loading_offers_table_task,
 loading_invites_table_task,
 loading_deals_table_task,
 loading_orders_table_task] >> transactional_db_tables_loaded_ready_task

transactional_db_tables_loaded_ready_task >> [creating_warehouse_offers_table_task,
                                              creating_warehouse_invites_table_task,
                                              creating_warehouse_deals_table_task,
                                              creating_warehouse_orders_table_task]

[creating_warehouse_offers_table_task,
creating_warehouse_invites_table_task,
creating_warehouse_deals_table_task,
creating_warehouse_orders_table_task] >> warehouse_db_tables_ready_task

warehouse_db_tables_ready_task >> [load_full_offers_data,
                                   load_full_invites_data,
                                    load_full_deals_data,
                                    load_full_orders_data]

[load_full_offers_data,
 load_full_invites_data,
 load_full_deals_data,
 load_full_orders_data] >> warehouse_db_tables_loaded_ready_task

warehouse_db_tables_loaded_ready_task >> sales_funnel_transformation_task

# Traffic analysis
# location_traffic_task = PostgresOperator(
#     task_id="calculate_location_traffic",
#     dag=dag,
#     postgres_conn_id="redshift",
#     sql=sql_statements.STATION_TRAFFIC_SQL
# )
