from carSimulation.agent import *
from carSimulation.model import CityModel
import requests
import json
import time

url = "http://52.1.3.19:8585/"
endpoint = "api/attempts"

def run_model():
    highest_cars_des = 0  # Variable to store the highest value of cars_des

    for _ in range(20):  # Run the simulation 100 times
        model = CityModel(1)
        while model.running:
            model.step()
            cars_des = model.cars_in_destinations
            highest_cars_des = max(highest_cars_des, cars_des)  # Update highest value if necessary

            # Your existing code for sending data to the API
            # You can decide if you still want to send data every 100 steps in this loop

        # After each simulation, you can print the highest value so far
        data = {"year" : 2023,
                    "classroom" : 301,
                    "name" : " perdon 😥 ",
                    "num_cars": int(highest_cars_des)}  # Formatear los datos para enviar

        headers = {
            "Content-Type": "application/json"
        }

        # Enviar los datos a la API
        response = requests.post(url + endpoint, json=data, headers=headers)
        print("Highest cars_des after this run:", highest_cars_des)

    return highest_cars_des

highest_value = run_model()
print("Highest value of cars_des after 50 runs:", highest_value)
data = {"year" : 2023,
            "classroom" : 301,
            "name" : " perdon 😥",
            "num_cars": int(highest_value)}  # Formatear los datos para enviar

headers = {
    "Content-Type": "application/json"
}

# Enviar los datos a la API
response = requests.post(url + endpoint, json=data, headers=headers)
