from sqlalchemy import Column, Integer, String, Boolean

import sys
sys.path.append('C:/Users/slavu/PycharmProjects/mfdp/load_data/')
from database.database import Base, engine


class IntakeType(Base):
    __tablename__ = "intake_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intake_type = Column(String)


class IntakeCondition(Base):
    __tablename__ = "intake_condition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intake_condition = Column(String)


class AnimalType(Base):
    __tablename__ = "animal_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_type = Column(String)


class SexUponIntake(Base):
    __tablename__ = "sex_upon_intake"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sex_upon_intake = Column(String)


class Color(Base):
    __tablename__ = "color"

    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String)


class Breed(Base):
    __tablename__ = "breed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    breed = Column(String)


class Data_regressor(Base):
    __tablename__ = "data_regressor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Boolean)
    intake_type = Column(String)
    intake_condition = Column(String)
    animal_type = Column(String)
    sex_upon_intake = Column(String)
    age_upon_intake = Column(Integer)
    mixed_color = Column(Boolean)
    first_color = Column(String)
    second_color = Column(String)
    mixed_breed = Column(Boolean)
    first_breed = Column(String)
    second_breed = Column(String)
    days_in_shelter = Column(Integer)


# Создание таблиц
if __name__ == "__main__":
    Base.metadata.create_all(engine)