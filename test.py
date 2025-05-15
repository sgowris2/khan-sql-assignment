import pandas as pd
from sqlalchemy import text

from calc_methods import get_sql_result, get_python_result
from db import init_db

OVERWRITE_DATA = True
USE_EXAMPLE_DATA = False # If True, it uses the data given in the example in the problem statement (https://docs.google.com/document/d/1oMpSDWHy723paex3WpOpkRYRLfnPypzYJ6CLgF0MxvY/edit?tab=t.0#heading=h.28qw45d9y7qu)
NO_OF_USERS = 10
MAX_NO_OF_USAGES = 10

if __name__ == "__main__":

    # Initialize the database session and test data
    with init_db(overwrite_data=OVERWRITE_DATA, use_example_data=USE_EXAMPLE_DATA, no_of_users=NO_OF_USERS, max_no_of_usages=MAX_NO_OF_USAGES) as session:  # Use a context manager for the session

        # Get input data from the DB for Python Calculation
        users_result = session.execute(text('SELECT * FROM users;'))
        usage_result = session.execute(text('SELECT * FROM usage;'))
        users_df = pd.DataFrame(users_result.fetchall(), columns=users_result.keys())
        users_df['registration_date'] = pd.to_datetime(users_df['registration_date'])
        usage_df = pd.DataFrame(usage_result.fetchall(), columns=usage_result.keys())
        usage_df['usage_date'] = pd.to_datetime(usage_df['usage_date'])

        # Perform Python Calculation
        python_result_df = get_python_result(users_df=users_df, usage_df=usage_df)

        # Execute SQL to get result
        sql_result_df = get_sql_result(session=session, query_filename='monthly_engaged_retention.sql')

    # Print the results
    print("\nResult from Python DataFrame:")
    print(python_result_df)
    print("\nResult from SQL Query DataFrame:")
    print(sql_result_df)

    # Compare the results just to check that the query is doing the right thing
    if python_result_df.equals(sql_result_df):
        print("\n\nThe results are identical.\n")
    else:
        print("\n\nThe results differ.\n")