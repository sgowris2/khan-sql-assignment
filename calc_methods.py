import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from sqlalchemy import text


def get_sql_result(session, query_filename):
    with open(query_filename, 'r') as query_file:
        query = query_file.read()
    result = session.execute(text(query))
    # Convert result to DataFrame so that it can be compared later
    result_df = pd.DataFrame(result.fetchall(), columns=result.keys())
    result_df.set_index('registration_month', drop=True, inplace=True)
    return result_df


def get_python_result(users_df, usage_df):

    # Add registration month to DF
    users_df['registration_month'] = users_df['registration_date'].dt.strftime('%b, %Y')
    users_df['m1_time_spent'] = 0
    users_df['m2_time_spent'] = 0
    users_df['m3_time_spent'] = 0

    # Calculate total time spent by each user in Month1, Month2, Month3
    for index, user in users_df.iterrows():
        reg_date = user['registration_date']
        reg_plus_1_month = reg_date + relativedelta(months=1)
        reg_plus_2_month = reg_date + relativedelta(months=2)
        reg_plus_3_month = reg_date + relativedelta(months=3)
        m1_time_spent = usage_df[
            (usage_df['user_id'] == user['user_id']) &
            (usage_df['usage_date'] >= reg_date) &
            (usage_df['usage_date'] < reg_plus_1_month)
            ]['time_spent'].sum()
        m2_time_spent = usage_df[
            (usage_df['user_id'] == user['user_id']) &
            (usage_df['usage_date'] >= reg_plus_1_month) &
            (usage_df['usage_date'] < reg_plus_2_month)
            ]['time_spent'].sum()
        m3_time_spent = usage_df[
            (usage_df['user_id'] == user['user_id']) &
            (usage_df['usage_date'] >= reg_plus_2_month) &
            (usage_df['usage_date'] < reg_plus_3_month)
            ]['time_spent'].sum()
        users_df.at[index, 'm1_time_spent'] = m1_time_spent
        users_df.at[index, 'm2_time_spent'] = m2_time_spent
        users_df.at[index, 'm3_time_spent'] = m3_time_spent

    # Calculate retention by registration_month
    result_data = []
    registration_months = users_df.registration_month.unique()
    for month in registration_months:
        reg_month_users_df = users_df[users_df.registration_month == month]
        total_users = reg_month_users_df.shape[0]
        if total_users > 0:
            m1_retention = '{}%'.format(
                round(100 * reg_month_users_df[reg_month_users_df.m1_time_spent >= 30].shape[0] / total_users))
            m2_retention = '{}%'.format(
                round(100 * reg_month_users_df[reg_month_users_df.m2_time_spent >= 30].shape[0] / total_users))
            m3_retention = '{}%'.format(
                round(100 * reg_month_users_df[reg_month_users_df.m3_time_spent >= 30].shape[0] / total_users))
            result_data.append(
                {'registration_month': month,
                 'total_users': total_users,
                 'm1_retention': m1_retention,
                 'm2_retention': m2_retention,
                 'm3_retention': m3_retention})
    result = pd.DataFrame(result_data)
    result['registration_month_dt'] = pd.to_datetime(result['registration_month'],
                                                                    format='%b, %Y')
    result = result.sort_values(by='registration_month_dt')
    result.drop(columns='registration_month_dt', inplace=True)
    result.set_index('registration_month', drop=True, inplace=True)

    return result
