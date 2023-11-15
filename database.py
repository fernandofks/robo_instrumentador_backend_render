from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://roboinstrumentadorpostgresql_user:3CC4JHHevUFA5mUuAwI0SF4JLvmBtS46@dpg-cl60fgcn7k7c73capqn0-a.oregon-postgres.render.com/roboinstrumentadorpostgresql'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()