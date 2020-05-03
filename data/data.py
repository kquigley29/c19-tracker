from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from models import Base
from owid import owid
from oxford import oxford
from population import population


def stringToFloat(str):
    b = 0
    try:
        b = int(float(str))
    except:
        b = 0
    finally:
        return b


if __name__ == '__main__':
    engine = create_engine("sqlite:///data.db")

    Base.metadata.create_all(engine)

    if not database_exists(engine.url):
        create_database(engine.url)

    Session = sessionmaker(bind=engine)
    session = Session()

    owid(session)
    oxford(session)
    population(session)
    