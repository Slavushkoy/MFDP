from pydantic import BaseModel


class AnimalInput(BaseModel):
    name: bool
    intake_type: str
    intake_condition: str
    animal_type: str
    sex_upon_intake: str
    age_upon_intake: int
    mixed_color: bool
    first_color: str
    second_color: str
    mixed_breed: bool
    first_breed: str
    second_breed: str

    class Config:
        from_attributes = True

