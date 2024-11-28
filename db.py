from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import db

db_url = f"mariadb+mariadbconnector://{db["user"]}:{db["password"]}@{db["host"]}:{db["port"]}/{db["database"]}"

engine = create_engine(db_url, echo=True)

Session = sessionmaker(bind=engine)

session = Session()
