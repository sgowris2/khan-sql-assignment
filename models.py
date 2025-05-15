from sqlalchemy import (
    Column, Integer, String, ForeignKey, DATE, UniqueConstraint, PrimaryKeyConstraint
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# -----------------
# ORGANIZATIONS
# -----------------
class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    registration_date = Column(DATE, nullable=False)


class Usage(Base):
    __tablename__ = 'usage'
    user_id = Column(String, ForeignKey('users.user_id'))
    usage_date = Column(DATE, nullable=False)
    usage_location = Column(String, nullable=False)
    time_spent = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'usage_date'),
    )

