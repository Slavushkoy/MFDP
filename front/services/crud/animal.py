from database.database import SessionLocal
from models.animal import IntakeType, AnimalType, IntakeCondition, SexUponIntake, Color, Breed


def get_сolors():
    session = SessionLocal()
    values = session.query(Color.color) \
        .distinct() \
        .all()
    colors_list = [value[0] for value in values]
    return colors_list


def get_breeds():
    session = SessionLocal()
    values = session.query(Breed.breed) \
        .distinct() \
        .all()
    breeds_list = [value[0] for value in values]
    return breeds_list


def get_intake_type():
    session = SessionLocal()
    values = session.query(IntakeType.intake_type) \
        .distinct() \
        .all()
    intake_type_list = [value[0] for value in values]
    return intake_type_list


def get_animal_type():
    session = SessionLocal()
    values = session.query(AnimalType.animal_type) \
        .distinct() \
        .all()
    animal_type_list = [value[0] for value in values]
    return animal_type_list


def get_intake_condition_type():
    session = SessionLocal()
    values = session.query(IntakeCondition.intake_condition) \
        .distinct() \
        .all()
    intake_condition_list = [value[0] for value in values]
    return intake_condition_list


def get_sex_upon_intake():
    session = SessionLocal()
    values = session.query(SexUponIntake.sex_upon_intake) \
        .distinct() \
        .all()
    sex_upon_intake_list = [value[0] for value in values]
    return sex_upon_intake_list

