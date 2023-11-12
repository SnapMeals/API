import os
import openai
from fastapi import APIRouter
from openai import OpenAI

router = APIRouter()

client = OpenAI(
    # organization=os.getenv("OPENAI_ORGANIZATION"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

@router.get("/example")
def read_example():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    return {"example": response}