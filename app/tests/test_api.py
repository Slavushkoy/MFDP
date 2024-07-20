from fastapi.testclient import TestClient


def test_model_predict(client: TestClient):
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
    response = client.post(f"/model/predict/", json=animal_input)
    assert response.status_code == 200