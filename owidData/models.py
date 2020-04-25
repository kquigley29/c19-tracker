from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Date, Text

Base = declarative_base()

class Country_Data(Base):
    __tablename__ = 'Countries History'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    iso = Column(Text)
    name = Column(Text) 
    date = Column(Date)
    total_cases = Column(Integer)
    total_deaths = Column(Integer)
    total_cases_per_million = Column(Integer)
    total_deaths_per_million = Column(Integer)
    total_tests = Column(Integer)
    total_tests_per_thousand = Column(Integer)

    def __repr__(self):
        return f'Country {self.name}'
    
    def toJson(self):
        return dict(
            id=self.id,
            iso=self.iso, 
            name=self.name, 
            date=self.date, 
            total_cases=self.total_cases, 
            total_deaths=self.total_deaths,
            total_cases_per_million=self.total_cases_per_million,
            total_deaths_per_million= self.total_deaths_per_million,
            total_tests = self.total_tests,
            total_tests_per_thousand = self.total_tests_per_thousand)
