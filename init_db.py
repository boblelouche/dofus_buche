from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import directories, db
from os import listdir
from models.Map import add_xml
from models.Base import Base

db_url = f"mariadb+mariadbconnector://{db["user"]}:{db["password"]}@{db["host"]}:{db["port"]}/{db["database"]}"

engine = create_engine(db_url)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    for file in listdir(directories["MAP_DIR"]):
        add_xml(file, session)
