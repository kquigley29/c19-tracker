from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData


# Global Variables
SQLITE = 'sqlite'

# Table Names
CURRENT_DATA = 'current_data'
ALL_DATA = 'all_data'

class Database:
    
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")


    def create_db_tables(self):
        metadata = MetaData()
        current_data = Table(CURRENT_DATA, metadata,
                      Column('iso_code', String, primary_key=True),
                      Column('location', String),
                      Column('date', String),
                      Column('total_cases', String),
                      Column('new_cases', String),
                      Column('total_deaths', String),
                      Column('new_deaths', String),
                      Column('total_cases_per_million', String),
                      Column('new_cases_per_million', String),
                      Column('total_deaths_per_million', String),
                      Column('new_deaths_per_million', String),
                      Column('total_tests', String),
                      Column('new_tests', String),
                      Column('total_tests_per_thousand', String),
                      Column('new_tests_per_thousand', String),
                      Column('tests_units', String)
                      )

        # all_data = Table(ALL_DATA, metadata,
        #           Column('id', Integer, primary_key=True)
        #           Column('iso_code', String),
        #           Column('location', String),
        #           Column('date', String),
        #           Column('total_cases', String),
        #           Column('new_cases', String),
        #           Column('total_deaths', String),
        #           Column('new_deaths', String), 
        #           Column('total_cases_per_million', String),
        #           Column('new_cases_per_million', String),
        #           Column('total_deaths_per_million', String),
        #           Column('new_deaths_per_million', String),
        #           Column('total_tests', String),
        #           Column('new_tests', String),
        #           Column('total_tests_per_thousand', String),
        #           Column('new_tests_per_thousand', String),
        #           Column('tests_units', String)
        #           )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)


    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return
        # print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)


    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)
                result.close()
        print("\n")


    def insert(self, current_data=[], all_data=[]):
        self.execute_query('DELETE FROM ' + CURRENT_DATA + ';')
        # self.execute_query('DELETE FROM ' + ALL_DATA + ';')

        # insert current data into the current
        for d in current_data:
            query = 'INSERT INTO ' + CURRENT_DATA + ' VALUES (' + str([d.values()])[15:-3] + ');'
            self.execute_query(query)

        # all_data = all
        # for d in all_data:
        #     query = 'INSERT INTO ' + ALL_DATA + ' VALUES (' + str([d.values()])[15:-3] + ');'
        #     self.execute_query(query)

        print('Data inserted')