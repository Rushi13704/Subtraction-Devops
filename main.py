from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Numbers(BaseModel):
    num1: float
    num2: float


def subtract(num1, num2):
    return num1 - num2


# GET Method
@app.get("/")
def home():
    return {
        "message": "Welcome to Subtraction API"
    }


# POST Method
@app.post("/subtract")
def subtraction(numbers: Numbers):
    result = subtract(numbers.num1, numbers.num2)

    return {
        "num1": numbers.num1,
        "num2": numbers.num2,
        "result": result
    }