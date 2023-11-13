from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from models import Argument, ArgumentResponse


app = FastAPI(
    title="Titanic Survival Prediction",
    version="0.1",
    description="Confront with your destiny!"
)

filename = 'titanic_model.sav'
model = pickle.load(open(filename, 'rb'))

title_mapping = {"Mr": 1, "Mrs": 2, "Miss": 3, "Master": 4, "Dr": 5, "Noble": 6}
embarked_mapping = {"Southampton, England": 1, "Cherbourg, France": 2, "Queenstown, Ireland": 3}
sex_mapping = {"Male": 0, "Female": 1}


async def prediction(pclass, sex, age, sibsp, parch, embarked, title):
    new_array = np.array([pclass, sex_mapping[sex], age, sibsp, parch, embarked_mapping[embarked], title_mapping[title]]).reshape(1, -1)
    result = model.predict(new_array)
    proba = model.predict_proba(new_array)
    print(proba)
    if result == 0:
         return ("Not Survived", proba[0][0]*100)
    else:
        return ("Survived", proba[0][1]*100)


@app.post('/predict', summary="Would you survive from Titanic?")
async def predict_survive(arg: Argument):
    """
    This endpoint predicts the likelihood of survival on the Titanic based on the provided attributes. 

    - **pclass**: The passenger's class (1 = First, 2 = Second, 3 = Third)
    - **sex**: The passenger's gender ('Male' or 'Female')
    - **title**: The passenger's title ('Mr', 'Mrs', 'Miss', 'Master', 'Dr', 'Noble')
    - **age**: The passenger's age
    - **sibsp**: Number of siblings/spouses aboard the Titanic
    - **parch**: Number of parents/children aboard the Titanic
    - **embarked**: Port of embarkation ('Southampton, England', 'Cherbourg, France', 'Queenstown, Ireland')
    """

    results = await prediction(arg.pclass, arg.sex, arg.age, arg.sibsp, arg.parch, arg.embarked, arg.title)
    response = ArgumentResponse(survive=results[0], proba=results[1])
    return response