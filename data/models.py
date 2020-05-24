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
    new_cases = Column(Integer)
    total_deaths = Column(Integer)
    new_deaths = Column(Integer)
    total_cases_per_million = Column(Integer)
    total_deaths_per_million = Column(Integer)
    total_tests = Column(Integer)
    new_tests = Column(Integer)
    total_tests_per_thousand = Column(Integer)

    def __repr__(self):
        return f'Country {self.name}'

    def toJson(self):
        return dict(
            id = self.id,
            name = self.name,
            date = self.date,
            total_cases = self.total_cases,
            new_cases = self.new_cases,
            total_deaths = self.total_deaths,
            new_deaths = self.new_deaths,
            total_cases_per_million = self.total_cases_per_million,
            total_deaths_per_million = self.total_deaths_per_million,
            total_tests = self.total_tests,
            new_tests = self.new_tests,
            total_tests_per_thousand = self.total_tests_per_thousand
        )


class OxfordData(Base):
    __tablename__ = 'Oxford_data'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text)
    date = Column(Date)
    school_closing = Column(Integer)
    workplace_closing = Column(Integer)
    cancel_public_events = Column(Integer)
    gatherings_restrictions = Column(Integer)
    close_public_transport = Column(Integer)
    stay_at_home_requirements = Column(Integer)
    internal_movement_restrictions = Column(Integer)
    international_travel_controls = Column(Integer)
    income_support = Column(Integer)
    debt_relief = Column(Integer)
    fiscal_measures = Column(Integer)
    international_support = Column(Integer)
    public_information_campaigns = Column(Integer)
    testing_policy = Column(Integer)
    contact_tracing = Column(Integer)
    emergency_investment_in_healthcare = Column(Integer)
    investment_in_vaccines = Column(Integer)
    confirmed_cases = Column(Integer)
    confirmed_deaths = Column(Integer)
    stringency_index = Column(Integer)
    stringency_index_for_display = Column(Integer)
    legacy_stringency_index = Column(Integer)
    legacy_stringency_index_for_display = Column(Integer)


    def __repr__(self):
        return f'Country {self.name}'

    def toJson(self):
        return dict(
            id = self.id,
            name = self.name,
            date = self.date,
            school_closing = self.school_closing,
            workplace_closing = self.workplace_closing,
            cancel_public_events = self.cancel_public_events,
            gatherings_restrictions = self.gatherings_restrictions,
            close_public_transport = self.close_public_transport,
            stay_at_home_requirements = self.stay_at_home_requirements,
            internal_movement_restrictions = self.internal_movement_restrictions,
            international_travel_controls = self.international_travel_controls,
            income_support = self.income_support,
            debt_relief = self.debt_relief,
            fiscal_measures = self.fiscal_measures,
            international_support = self.international_support,
            public_information_campaigns = self.public_information_campaigns,
            testing_policy = self.testing_policy,
            contact_tracing = self.contact_tracing,
            emergency_investment_in_healthcare = self.emergency_investment_in_healthcare,
            investment_in_vaccines = self.investment_in_vaccines,
            confirmed_cases = self.confirmed_cases,
            confirmed_deaths = self.confirmed_deaths,
            stringency_index = self.stringency_index,
            stringency_index_for_display = self.stringency_index_for_display,
            legacy_stringency_index = self.legacy_stringency_index,
            legacy_stringency_index_for_display = self.legacy_stringency_index_for_display
        )


class PopulationData(Base):
    __tablename__ = 'Population'
    __table_args__ = {'sqlite_autoincrement':True}
    id = Column(Integer, primary_key=True, nullable=False)
    rank = Column(Integer)
    country = Column(Text)
    population = Column(Integer)
    yearly_change = Column(Float)
    net_change = Column(Integer)
    density = Column(Integer)
    land_area = Column(Integer)
    migrants = Column(Integer)
    fertility_rate = Column(Float)
    median_age = Column(Integer)
    urban_population = Column(Integer)
    world_share = Column(Float)

    def __repr__(self):
        return f'Country {self.country}'

    def toJson(self):
        return dict(
            id = self.id,
            country = self.country,
            population = self.population,
            yearly_change = self.yearly_change,
            net_change = self.net_change,
            density = self.density,
            land_area = self.land_area,
            migrants = self.migrants,
            fertility_rate = self.fertility_rate,
            median_age = self.median_age,
            urban_population = self.urban_population,
            world_share = self.world_share
        )


class MilkenData(Base):
    __tablename__ = 'Milken_data'
    __table_args__ = {'sqlite_autoincrement':True}
    id = Column(Integer, primary_key=True, nullable=False)
    treatment_or_vaccine = Column(Text)
    catagory = Column(Text)
    description = Column(Text)
    stage = Column(Text)
    next_steps = Column(Text)
    clinical_trials = Column(Text)
    developer = Column(Text)
    funder = Column(Text)
    results = Column(Text)
    other_uses = Column(Text)
    fda_approval = Column(Text)

    def __repr__(self):
        return f'Product {self.description}'

    def toJson(self):
        return dict(
            id = self.id,
            treatment_or_vaccine = self.treatment_or_vaccine,
            catagory = self.catagory,
            description = self.description,
            stage = self.stage,
            next_steps = self.next_steps,
            clinical_trials = self.clinical_trials,
            developer = self.developer,
            funder = self.funder,
            results = self.results,
            other_uses = self.other_uses,
            fda_approval = self.fda_approval 
        )