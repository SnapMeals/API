import os
import json
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from typing import List


router = APIRouter()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

class Meal(BaseModel):
    id: str
    name: str
    ingredients: List[str]
    photo: str


def submit_openai_prompt(meal_name: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a world-class chef."},
            {"role": "user", "content": f"Make me a list of ingredients for a meal called {meal_name}. Please give me the list of ingredients in JSON."},
        ]
    )
    raw_message_content = response.choices[0].message.content
    processed_message_content = json.loads(raw_message_content)
    return processed_message_content


@router.post("/meal")
async def create_meal(meal: Meal):
    # Process the base64 image to identify what the meal represents - for this hackathon, we will not be doing this
    # For this event, we will just use the name of the meal as the input to the OPENAI API.
    
    # Submit the following prompt to the OPENAI API:
    response = submit_openai_prompt(meal.name)

    # Check the response for errors
    if not response:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # Return the response back to the client - the client will decide what to do with the response
    return {"meal": response}