import streamlit as st
import requests
from services.crud.animal import get_сolors, get_breeds, get_animal_type, get_intake_type, get_sex_upon_intake, get_intake_condition_type


FASTAPI_URL = "http://api:8000"


def main():
    st.title('Welcome to the portal!')
    st.text("Our service will help you optimize your shelter's resources,\n"
            'due to information about the duration of the animal’s stay in the shelter.\n'
            'Enter the parameters of the animal upon admission to the shelter \n'
            'and click the predict button.\n'
            '\n'
            'The service is provided free of charge\n'
            'and has a purpose'
            'help animals find a new home sooner.\n')

    opt = ['Yes', 'Not']
    name = st.selectbox('name', opt)
    if name == 'Yes':
        name = 1
    else:
        name = 0

    intake_type_opt = get_intake_type()
    intake_type = st.selectbox('intake_type', intake_type_opt)

    intake_condition_opt = get_intake_condition_type()
    intake_condition = st.selectbox('intake_condition', intake_condition_opt)

    animal_type_opt = get_animal_type()
    animal_type = st.selectbox('animal_type', animal_type_opt)

    sex_upon_intake_opt = get_sex_upon_intake()
    sex_upon_intake = st.selectbox('sex_upon_intake', sex_upon_intake_opt)

    age_upon_intake = st.number_input('age_upon_intake in days', min_value=0, step=1, value=0)

    color = st.selectbox('mixed_color', opt)

    color_opt = get_сolors()

    if color == 'Yes':
        mixed_color = 1

        search_color = st.text_input('Search by first_color:')
        filtered_options = [option for option in color_opt if search_color.lower() in option.lower()]
        first_color = st.selectbox('first_color', filtered_options)

        search_color_2 = st.text_input('Search by second_color:')
        filtered_options = [option for option in color_opt if search_color_2.lower() in option.lower()]
        second_color = st.selectbox('second_color', filtered_options)
    else:
        mixed_color = 0

        search_color = st.text_input('Search by first_color:')
        filtered_options = [option for option in color_opt if search_color.lower() in option.lower()]
        first_color = st.selectbox('first_color', filtered_options)

        second_color = 'Not'

    breed = st.selectbox('mixed_breed', opt)

    breed_opt = get_breeds()

    if breed == 'Yes':
        mixed_breed = 1
        search_breed = st.text_input('Search by first_breed:')
        filtered_options = [option for option in breed_opt if search_breed.lower() in option.lower()]
        first_breed = st.selectbox('first_breed', filtered_options)

        search_breed = st.text_input('Search by second_breed:')
        filtered_options = [option for option in breed_opt if search_breed.lower() in option.lower()]
        second_breed = st.selectbox('second_breed', filtered_options)

    else:
        mixed_breed = 1
        search_breed = st.text_input('Search by first_breed:')
        filtered_options = [option for option in breed_opt if search_breed.lower() in option.lower()]
        first_breed = st.selectbox('first_breed', filtered_options)
        second_breed = 'Not'


    # Button to make prediction
    if st.button('Predict days in shelter'):
        # Form the request payload
        payload = {
            'name': name,
            'intake_type': intake_type,
            'intake_condition': intake_condition,
            'animal_type': animal_type,
            'sex_upon_intake': sex_upon_intake,
            'age_upon_intake': age_upon_intake,
            'mixed_color': mixed_color,
            'first_color': first_color,
            'second_color': second_color,
            'mixed_breed': mixed_breed,
            'first_breed': first_breed,
            'second_breed': second_breed
        }

        try:
            response = requests.post(f"{FASTAPI_URL}/model/predict/", json=payload)
            if response.status_code == 200:
                st.success(response.json()['message'])
            elif response.status_code == 400:
                st.error(response.json()['message'])
            else:
                st.error(response)
        except requests.exceptions.ConnectionError:
            st.error("Service is not alive")


if __name__ == '__main__':
    main()
