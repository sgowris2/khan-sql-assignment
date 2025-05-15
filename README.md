# Calculating Retention Metrics for Khan Academy Users
### Answer by Sudeep Gowrishankar (May 15, 2025)

---

## Answer

Below the query that is used to calculate the monthly engage retention metric. 
This is also available in `monthly_engaged_retention.sql` file in the repository linked below with the [full solution code](https://github.com/sgowris2/khan-sql-assignment).


```SQL
SELECT
    registration_month,
    COUNT(time_spent_metrics.user_id) as total_users,
    ROUND(100.0 * SUM(CASE WHEN m1_time_spent >= 30 THEN 1 ELSE 0 END) / COUNT(time_spent_metrics.user_id), 0)::text || '%' AS m1_retention,
    ROUND(100.0 * SUM(CASE WHEN m2_time_spent >= 30 THEN 1 ELSE 0 END) / COUNT(time_spent_metrics.user_id), 0)::text || '%' AS m2_retention,
    ROUND(100.0 * SUM(CASE WHEN m3_time_spent >= 30 THEN 1 ELSE 0 END) / COUNT(time_spent_metrics.user_id), 0)::text || '%' AS m3_retention
FROM
(
    SELECT
        users.user_id,
        TO_CHAR(users.registration_date, 'Mon, YYYY') AS registration_month,
        SUM(CASE WHEN usage_date >= users.registration_date 
                 AND usage_date < users.registration_date + INTERVAL '1 month' THEN time_spent ELSE 0 END) AS m1_time_spent,
        SUM(CASE WHEN usage_date >= users.registration_date + INTERVAL '1 month' 
                 AND usage_date < users.registration_date + INTERVAL '2 month' THEN time_spent ELSE 0 END) AS m2_time_spent,
        SUM(CASE WHEN usage_date >= users.registration_date + INTERVAL '2 month' 
                 AND usage_date < users.registration_date + INTERVAL '3 month' THEN time_spent ELSE 0 END) AS m3_time_spent
    FROM usage
    FULL OUTER JOIN users ON usage.user_id = users.user_id
    GROUP BY users.user_id, users.registration_date
) AS time_spent_metrics
GROUP BY registration_month
ORDER BY TO_DATE(registration_month, 'Mon, YYYY');

```

---

The full code to test the solution is available at:
https://github.com/sgowris2/khan-sql-assignment

This repository contains the code used to create the SQL query for calculating the __Monthly "engaged" retention__
metric. In this repo, you can find the following:
- Docker compose to bring up a database called `khan_db`.
- Code to initialize tables and test data in the database using random number generation (in `db.py`)
- The SQL query that is the answer to the question in `monthy_engaged_retention.sql`
- Test code (in `test.py`) that checks whether the answer from the query in `monthly_engaged_retention.sql` matches with
a programmatic calculation of the same metric using step-=by-step Python code (in `calc_methods.py --> get_python_result()`)

Steps to run code in this repo:

1. Create a virtual environment with Python 3.10 or later using `virtualenv` or any other tool.
2. Install dependencies in the virtual environment using `pip install -r requirements.txt`
3. Bring up the Postgres database using `docker compose up -d`
4. Run `test.py`
    - Options when running are available as fields in the test.py file.
      - `OVERWRITE_DATA` - If True, any test data in the database will be overwritten and fresh test data will be generated and used.
      - `USE_EXAMPLE_DATA` - If True, the test data used will be the one from the example given in the [question sheet](https://docs.google.com/document/d/1oMpSDWHy723paex3WpOpkRYRLfnPypzYJ6CLgF0MxvY/edit?tab=t.0#heading=h.28qw45d9y7qu).
      - `NO_OF_USERS` - Number > 0 that determines the number of users to be used in the test dataset.
      - `MAX_NO_OF_USAGES` - Number >= 0 that determines the max number of usages per user that will be randomly selected while creating the test dataset.
5. The generation of test data assumes that data is within first 3 months of 2019, but this is only for test purposes.
6. If the run is successful, then the console will print the result of the query and the result of the calculation using programmatic Python code.

#### Note: Sometimes, the database may not respond and the run may get stuck while printing "Database tables created". Simply end the run, and re-run `test.py` a couple of times - it should resolve.

---