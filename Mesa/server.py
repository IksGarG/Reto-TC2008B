# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2023git 

from flask import Flask, request, jsonify
from carSimulation.agent import *
from carSimulation.model import CityModel
import requests
import json

url = "http://52.1.3.19:8585/"
endpoint = "api/attempts"


# Size of the board:
module = 6
cityModel = None
currentStep = 0

app = Flask("City Model Iks x Tena")

@app.route('/init', methods=['POST'])
def initModel():
    global currentStep, cityModel, module

    if request.method == 'POST':
        module = int(request.form.get('module'))
        currentStep = 0
        print(request.form)
        print(module)
        cityModel = CityModel(module)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global cityModel

    if request.method == 'GET':
        agentPositions = []
        for cell_content, (x, z) in cityModel.grid.coord_iter():
            # Asumiendo que cell_content es una lista de agentes
            for agent in cell_content:
                if isinstance(agent, Car):
                    position = {"id": str(agent.unique_id), "x": x, "y": 1, "z": z, "desx": agent.random_destination.pos[0], "desy":1, "desz": agent.random_destination.pos[1]}
                    agentPositions.append(position)

        return jsonify({'positions': agentPositions})

@app.route('/getTrafficLights', methods=['GET'])
def getTrafficLights():
    global cityModel

    if request.method == 'GET':
        trafficLightStates = []
        for cell_content, (x, z) in cityModel.grid.coord_iter():
            # Asumiendo que cell_content es una lista de agentes
            for agent in cell_content:
                if isinstance(agent, Traffic_Light):
                    state_info = {"id": str(agent.unique_id), "x": x, "y": 1, "z": z, "state": agent.state}
                    trafficLightStates.append(state_info)

        return jsonify({'trafficLights': trafficLightStates})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, cityModel
    if request.method == 'GET':
        cityModel.step()
        currentStep += 1
        if currentStep % 10 == 0:
            data = {
                "year" : 2023,
                "classroom" : 302,
                "name" : "Hoy Queda 💀",
                "num_cars": cityModel.cars_in_destinations
            }
                        
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(url+endpoint, data=json.dumps(data), headers=headers)
            print("Request " + "successful" if response.status_code == 200 else "failed", "Status code:", response.status_code)
            print("Response:", response.json())
        return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})
if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)