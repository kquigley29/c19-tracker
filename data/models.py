from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Date, Text

Base = declarative_base()

class OwidData(Base):
    __tablename__ = 'Owid_data'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
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
            name=self.name, 
            date=self.date, 
            total_cases=self.total_cases, 
            total_deaths=self.total_deaths,
            total_cases_per_million=self.total_cases_per_million,
            total_deaths_per_million= self.total_deaths_per_million,
            total_tests = self.total_tests,
            total_tests_per_thousand = self.total_tests_per_thousand)


class OxfordData(Base):
    __tablename__ = 'Oxford_data'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text) 
    date = Column(Date)
    school_closing = Column(Integer)
    workplace_closing = Column(Integer)
    cancel_public_events = Column(Integer)
    close_public_transport = Column(Integer)
    public_information_campaigns = Column(Integer)
    internal_movement_restrictions = Column(Integer)
    international_travel_controls = Column(Integer)
    fiscal_measures = Column(Integer)
    monetary_measures = Column(Integer)
    emergency_investment_in_healthcare = Column(Integer)
    investment_in_vaccines = Column(Integer)
    testing_framework = Column(Integer)
    contact_tracing = Column(Integer)
    stringency_index = Column(Integer)
    stringency_index_for_display = Column(Integer)


    def __repr__(self):
        return f'Country {self.name}'
    
    def toJson(self):
        return dict(
            id=self.id, 
            name=self.name, 
            date=self.date, 
            school_closing=self.school_closing, 
            workplace_closing=self.workplace_closing,
            cancel_public_events=self.cancel_public_events,
            close_public_transport= self.close_public_transport,
            public_information_campaigns=self.public_information_campaigns,
            internal_movement_restrictions=self.internal_movement_restrictions,
            international_travel_controls=self.international_travel_controls,
            fiscal_measures=self.fiscal_measures,
            monetary_measures=self.monetary_measures,
            emergency_investment_in_healthcare=self.emergency_investment_in_healthcare,
            investment_in_vaccines=self.investment_in_vaccines,
            testing_framework=self.testing_framework,
            contact_tracing=self.contact_tracing,
            stringency_index=self.stringency_index,
            stringency_index_for_display=self.stringency_index_for_display)
