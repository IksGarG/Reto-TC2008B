from carSimulation.agent import *
from carSimulation.model import CityModel
import requests
import json
import time  # Agrega esto al inicio de tu archivo

url = "http://52.1.3.19:8585/"
endpoint = "api/attempts"

def run_model():
    model = CityModel(3)
    currentStep = 0  # Mover esta línea dentro de la función para evitar un error de variable no definida

    while model.running:
        model.step()
        cars_des = model.cars_in_destinations
        if currentStep % 100 == 0:
            data = {"year" : 2023,
                    "classroom" : 301,
                    "name" : "La Ultima",
                    "num_cars": int(cars_des)}  # Formatear los datos para enviar

            headers = {
                "Content-Type": "application/json"
            }

            # Enviar los datos a la API
            response = requests.post(url + endpoint, json=data, headers=headers)
            time.sleep(8)
            if response.status_code == 200:
                print("Datos enviados correctamente en el paso", currentStep)
            else:
                print("Error al enviar datos:", response.text)

        currentStep += 1

run_model()
