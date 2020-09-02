from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from data.models import Base
from data.owid import owid
from data.oxford import oxford
from data.population import population
# from data.milken import milken
from data.config import db_path



def fillTables():
    engine = create_engine(db_path)

    Base.metadata.create_all(engine)

    if not database_exists(engine.url):
        create_database(engine.url)

    Session = sessionmaker(bind=engine)
    session = Session()

    owid(session)
    oxford(session)
    population(session)
    # milken(session)


if __name__ == '__main__':
    fillTables()
