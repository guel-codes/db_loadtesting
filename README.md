# Overview

This repo will be used to perform database loadtesting on a postgres database

## How to run the test

- `pip3 install psycopg2` - https://pypi.org/project/psycopg2/

- `pip3 install locust` - https://docs.locust.io/en/stable/installation.html

- Update line 46 of the `loadtest.py` file, you can change `postgresql://postgres:postgres@localhost:5432/loadtesting_db` with the connection string for your database
- Open the terminal and run `locust -f loadtest.py` this will give you a URL tol follow. Likely `http://0.0.0.0:8089` from here, you can put in custom parameters to run your test
- For all of the custom tags that you can use in your terminal command use: `locust --help`
- To make sure the requests are actually hitting the database you can run this query `SELECT pid, query_start, state, query FROM pg_stat_activity` inside of your postgres database
