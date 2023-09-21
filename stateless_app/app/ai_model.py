import os
import time 
import random

class FakeModel():
    def __init__(self) -> None:
        print("This is a fake model, ")
        print("receive string, wait 0.5 second and return")
        print("then return random int")

    def forward(self, input):
        print("this is input: ", input)
        time.sleep(0.5)
        return random.randint(3, 9)
    
def build_fake_ai_model():
    return FakeModel()