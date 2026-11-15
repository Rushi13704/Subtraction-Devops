"""
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

subtraction = num1 - num2
print(subtraction)
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    num1: float
    num2: float

def subtract(num1, num2):
    return num1 - num2

@app.post("/subtract")
def subtraction(numbers: Numbers):
    result = subtract(numbers.num1, numbers.num2)

    return {
        "num1": numbers.num1,
        "num2": numbers.num2,
        "result": result
    }