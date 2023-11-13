from pydantic import BaseModel, Field

class Argument(BaseModel):
    pclass: int = Field(..., description="The passenger's class (1 = First, 2 = Second, 3 = Third)")
    sex: str = Field(..., description="The passenger's gender ('Male' or 'Female')")
    title: str = Field(..., description="The passenger's title ('Mr', 'Mrs', 'Miss', 'Master', 'Dr', 'Noble')")
    age: int = Field(..., description="The passenger's age")
    sibsp: int = Field(..., description="Number of siblings/spouses aboard the Titanic")
    parch: int = Field(..., description="Number of parents/children aboard the Titanic")
    embarked: str = Field(..., description="Port of embarkation('Southampton, England', 'Cherbourg, France', 'Queesntown, Ireland')")


    # Default
    class Config:
        schema_extra = {
            "example": {
                "pclass": 1,
                "sex": "Male",
                "title": "Dr",
                "age": 35,
                "sibsp": 0,
                "parch": 0,
                "embarked": "Cherbourg, Fransa"
            }
        }

class ArgumentResponse(BaseModel):
    survive: str
    proba: float

    class Config:
        schema_extra = {
            "example": {
                "survive": "Survived",
                "proba": 75.35
            }
        }

