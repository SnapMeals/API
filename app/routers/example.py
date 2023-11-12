from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
def read_example():
    return {"example": "response"}