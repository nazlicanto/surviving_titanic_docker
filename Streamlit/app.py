import streamlit as st
import numpy as np
import pickle
import requests

# Model 
#filename = '../Notebooks/titanic_model.sav'
#model = pickle.load(open(filename, 'rb'))

title_mapping = {"Mr": 1, "Mrs": 2, "Miss": 3, "Master": 4, "Dr": 5, "Noble": 6}
embarked_mapping = {"Southampton, England": 1, "Cherbourg, France": 2, "Queesntown, Ireland": 3}
sex_mapping = {"Male": 0, "Female": 1}
ports_range = ('Southampton, England', 'Cherbourg, France', 'Queesntown, Ireland')

def prediction(pclass, sex, age, sibsp, parch, embarked, title):
    new_array = np.array([pclass, sex_mapping[sex], age, sibsp, parch, embarked_mapping[embarked], title_mapping[title]])
    new_array = new_array.reshape(1, -1)
    result = model.predict(new_array)
    proba = model.predict_proba(new_array)
    if result == 0:
        return ("You Would Not Survive", proba[0][0])
    else:
        return ("You Would Survive", proba[0][1])

st.title('Titanic Survival Prediction Application')

# User inputs
pclass = st.selectbox('Your Class (1=Business, 2=Economy, 3=Lower Class)', [1, 2, 3])
sex = st.selectbox('Your Sex', ['Male', 'Female'])
title = st.selectbox('Your Title', ['Mr', 'Mrs', 'Miss', 'Master', 'Dr', 'Noble'])
age = st.slider('Your Age', 0, 90, 28)
sibsp = st.slider('Number of siblings/spouses on Titanic', 0, 8, 0)
parch = st.slider('Number of parents/children on Titanic', 0, 6, 0)
embarked = st.selectbox('Which port did you embark from?', ports_range)

payload = {
    "pclass": pclass,
    "sex": sex,
    "title": title,
    "age": age,
    "sibsp": sibsp,
    "parch": parch,
    "embarked": embarked
}


try:
    response = requests.post("http://fastapi:8000/predict", json=payload)
    response.raise_for_status() 
    res = response.json()

    ssurvival_chance = res['proba']

    print("Raw survival chance from model:", ssurvival_chance)

    if ssurvival_chance > 1:
        survival_chance = round(ssurvival_chance, 2)
    else:
        survival_chance = round(ssurvival_chance * 100, 2)

    if res['survive'] == 'Survived':
        message = f"You would have a {survival_chance}% chance of surviving."
        st.success(message)
    else:
        message = f"You would have a {100 - survival_chance}% chance of not surviving."
        st.error(message)
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while making the prediction: {e}")
