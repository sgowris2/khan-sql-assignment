import os
import random
import uuid
from datetime import datetime, timedelta

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

import models
from models import User, Usage


def get_database_url():
    user = os.getenv('DB_USER', 'user')
    password = os.getenv('DB_PASSWORD', 'password')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    db = os.getenv('DB_NAME', 'khan_db')
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def init_db(overwrite_data=False, use_example_data=False, no_of_users=10, max_no_of_usages=10):
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if len(table_names) > 0:
        print("Database tables already exist:\n{}".format(table_names))
        if overwrite_data:
            session.query(models.Usage).delete()
            session.query(models.User).delete()
            session.commit()
    else:
        print("No tables found, creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created!")
    populate_new_db(session, use_example_data, no_of_users, max_no_of_usages)

    return session


def populate_new_db(session, use_example_data=False, no_of_users=10, max_no_of_usages=10):

    if use_example_data:
        users = [User(user_id='aaa', registration_date=datetime(year=2019, month=1, day=3)),
                 User(user_id='bbb', registration_date=datetime(year=2019, month=1, day=2)),
                 User(user_id='ccc', registration_date=datetime(year=2019, month=1, day=15)),
                 User(user_id='ddd', registration_date=datetime(year=2019, month=2, day=7))]

        usages = [
            Usage(user_id='aaa', usage_date=datetime(year=2019, month=1, day=3), usage_location='US', time_spent=38),
            Usage(user_id='aaa', usage_date=datetime(year=2019, month=2, day=1), usage_location='US', time_spent=12),
            Usage(user_id='aaa', usage_date=datetime(year=2019, month=3, day=4), usage_location='US', time_spent=30),
            Usage(user_id='bbb', usage_date=datetime(year=2019, month=1, day=3), usage_location='US', time_spent=20),
            Usage(user_id='bbb', usage_date=datetime(year=2019, month=2, day=4), usage_location='US', time_spent=31),
            Usage(user_id='ccc', usage_date=datetime(year=2019, month=1, day=16), usage_location='US', time_spent=40),
            Usage(user_id='ddd', usage_date=datetime(year=2019, month=2, day=8), usage_location='US', time_spent=45)
        ]

    else:
        users = []
        for i in range(0, no_of_users):
            user_id = str(uuid.uuid4())
            registration_date = generate_random_date_between(start_date=datetime(year=2019, month=1, day=1),
                                                             end_date=datetime(year=2019, month=3, day=31))
            users.append(User(user_id=user_id, registration_date=registration_date))
        usages = []
        for user in users:
            no_of_usages = max(0, round(max_no_of_usages * random.random()))  # Random number between 1 and 10
            usage_date_memo = set()
            usage_date = None
            for i in range(0, no_of_usages):
                while (usage_date is None) or (usage_date in usage_date_memo):
                    usage_date = generate_random_date_between(start_date=user.registration_date,
                                                              end_date=datetime(year=2019, month=3, day=31)) # Assume all usage is between registration date and March 31, 2019
                usage_time = round(60 * random.random()) # Assume that any usage time is between 0 and 60
                usages.append(
                    Usage(user_id=user.user_id, usage_date=usage_date, usage_location='US', time_spent=usage_time))
                usage_date_memo.add(usage_date)

    try:
        with session:
            session.add_all(users)
            session.commit()
            session.add_all(usages)
            session.commit()
            print("Test data inserted successfully.")
    except SQLAlchemyError as e:
        print("An error occurred while populating the database:", e)


def generate_random_date_between(start_date: datetime, end_date: datetime):
    date_range = (end_date - start_date).days
    return start_date + timedelta(days=round(date_range * random.random()))
