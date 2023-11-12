from fastapi import FastAPI
from .routers import example, meal

app = FastAPI()

app.include_router(example.router)
app.include_router(meal.router)