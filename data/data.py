from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from models import Base
from owid import owid
from oxford import oxford
from population import population
#from milken import milken


def fillTables():
    engine = create_engine("sqlite:///data.db")

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