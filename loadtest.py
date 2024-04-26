import psycopg2
from locust import User, TaskSet, task, between, events
import time
import random
import os


def create_conn(conn_string):
    print("Connect and Query PostgreSQL")
    conn = psycopg2.connect(conn_string)
    return conn


def execute_query(conn_string, query):
    db_conn = create_conn(conn_string)
    db_query = db_conn.cursor().execute(query)
    return db_query


class PostgresClient:
    def __getattr__(self, name):
        def request_handler(*args, **kwargs):
            start_time = time.time()
            try:
                res = execute_query(*args, **kwargs)
                response_time = int((time.time() - start_time) * 1000)
                events.request.fire(
                    request_type="postgres",
                    name=name,
                    response_time=response_time,
                    response_length=0,
                )
            except Exception as e:
                response_time = int((time.time() - start_time) * 1000)
                events.request.fire(
                    request_type="postgres",
                    name=name,
                    response_time=response_time,
                    response_length=0,
                    exception=e,
                )
                print("error {}".format(e))

        return request_handler


class CustomTaskSet(TaskSet):
    conn_string = "postgresql://postgres:postgres@localhost:5432/loadtesting_db"

    @task
    def execute_query(self):
        self.client.execute_query(
            self.conn_string,
            f"SELECT * FROM loadtesting.user",
        )


# This class will be executed when you run locust
class PostgresLocust(User):
    min_wait = 0
    max_wait = 1
    tasks = [CustomTaskSet]
    print(tasks)
    wait_time = between(min_wait, max_wait)

    def __init__(self, *args):
        super()
        self.client = PostgresClient()