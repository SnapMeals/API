import os
import json
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict


router = APIRouter()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

class Meal(BaseModel):
    id: str
    name: str
    ingredients: List[str]
    photo: str


class OpenAIMeal(BaseModel):
    name: str
    meal: Dict[str, Dict[str, str]]


MEAL_SCHEMA = '''{
        "name": "meal_name",
        "meal": {
            "meal_component1": {
                "ingredient1": "quantity",
                "ingredient2": "quantity",
            },
            "meal_component2": {
                "ingredient1": "quantity",
                "ingredient2": "quantity",
            }
        }
    }'''

def submit_openai_prompt(meal_name: str):
    main_prompt = f'''Make me a list of ingredients for a meal called {meal_name}. Please give me the list of ingredients in JSON.
    The schema of the JSON output should look like this:
    
    {MEAL_SCHEMA}
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a world-class chef."},
            {"role": "user", "content": main_prompt},
        ]
    )
    raw_message_content = response.choices[0].message.content
    processed_message_content = json.loads(raw_message_content)
    return processed_message_content


def vegetarianize_openai_meal(meal: OpenAIMeal):
    json_meal = meal.model_dump_json()
    main_prompt = f'''Take the following meal as JSON input:
    
    {json_meal}
    
    Following the schema below, I want you to replace all the meat ingredients with vegetarian alternatives:
    
    {MEAL_SCHEMA}
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a world-class chef."},
            {"role": "user", "content": main_prompt},
        ]
    )
    raw_message_content = response.choices[0].message.content
    processed_message_content = json.loads(raw_message_content)
    return processed_message_content


def lowcal_openai_meal(meal: OpenAIMeal):
    json_meal = meal.model_dump_json()
    main_prompt = f'''Take the following meal as JSON input:
    
    {json_meal}
    
    Following the schema below, I want you to replace all the ingredients with low calorie alternatives:
    
    {MEAL_SCHEMA}
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a world-class chef."},
            {"role": "user", "content": main_prompt},
        ]
    )
    raw_message_content = response.choices[0].message.content
    processed_message_content = json.loads(raw_message_content)
    return processed_message_content


@router.post("/suggest_meal")
async def suggest_meal(meal: Meal):
    # Process the base64 image to identify what the meal represents - for this hackathon, we will not be doing this
    # For this event, we will just use the name of the meal as the input to the OPENAI API.
    
    # Submit the following prompt to the OPENAI API:
    response = submit_openai_prompt(meal.name)

    # Check the response for errors
    if not response:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # Return the response back to the client - the client will decide what to do with the response
    return response


def load_profile():
    with open("run/profile.json", "r") as f:
        profile = json.load(f)
    return profile


def write_meal_to_profile(meal: Dict[str, Dict[str, str]]):
    with open("run/profile.json", "w") as f:
        json.dump(meal, f)


@router.post("/confirm_meal")
async def confirm_meal(meal: OpenAIMeal):

    # Add the meal to the profile
    existing_meals = load_profile()
    existing_meals[meal.name] = meal.meal
    write_meal_to_profile(existing_meals)

    # Reflect the updated meal the response back to the client
    return meal


@router.get("/profile")
async def get_profile():
    # Load the user's profile - this includes all their saved meals
    profile = load_profile()

    # Reflect the updated meal list back to the client
    return profile


##### Premium Features #######
@router.post("/vegetarianize")
async def vegetarianize_meal(meal: OpenAIMeal):
    response = vegetarianize_openai_meal(meal)

    # Check the response for errors
    if not response:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # Return the response back to the client - the client will decide what to do with the response
    return response


@router.post("/lowcal")
async def lowcal_meal(meal: OpenAIMeal):
    response = lowcal_openai_meal(meal)

    # Check the response for errors
    if not response:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # Return the response back to the client - the client will decide what to do with the response
    return response