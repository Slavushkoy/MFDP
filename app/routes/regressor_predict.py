from fastapi import APIRouter
from models.schema import AnimalInput
from services.ml.send_message import send_message
import json
from fastapi.responses import JSONResponse

model_router = APIRouter(tags=["Model"])


@model_router.get("/healthcheck/")
async def healthcheck():
    try:
        animal_input = {"name": 1,
                    "intake_type": 'Wildlife',
                    "intake_condition": 'Injured',
                    "animal_type": 'Bird',
                    "sex_upon_intake": 'Unknown',
                    "age_upon_intake": 730,
                    "mixed_color": 1,
                    "first_color": 'Yellow',
                    "second_color": 'Yellow',
                    "mixed_breed": 0,
                    "first_breed": 'Hawk',
                    "second_breed": 'Not'}
        animal_json = json.dumps(animal_input)
        result = send_message(animal_json)
        try:
            float(result)
            return JSONResponse(content={"message": "Service is ready"}, status_code=200)
        except ValueError:
            return JSONResponse(content={"message": f"Service is not ready."}, status_code=500)
    except Exception as e2:
        return JSONResponse(content={"message": f"An error occurred: {e2})"}, status_code=500)


@model_router.post("/predict/")
def predict(data: AnimalInput):
    animal_input_dict = data.dict()
    animal_input_json = json.dumps(animal_input_dict)
    response = send_message(animal_input_json)
    try:
        response = float(response)
        days_in_shelter = int(response)
        return JSONResponse(content={"message": f"Days_in_shelter: {days_in_shelter}"}, status_code=200)
    except ValueError:
        return JSONResponse(content={f"Error: {response}"}, status_code=500)