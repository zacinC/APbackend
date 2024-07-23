import json
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def configure_database():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(
            f"WARNING: {file} file not found, you cannot continue, please see settings_template.json")
        raise Exception(
            "settings.json file not found, you cannot continue, please see settings_template.json")

    with open(file=file) as fin:
        settings = json.load(fin)
        password = settings.get('password')
        return password


username: str = 'root'
password: str = configure_database()
host: str = 'localhost'
port: int = 3306
database: str = 'autobuska'


MYSQL_DATABASE_URL = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
