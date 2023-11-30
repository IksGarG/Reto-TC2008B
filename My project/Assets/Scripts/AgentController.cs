// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2023

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    /*
    The AgentData class is used to store the data of each agent.
    
    Attributes:
        id (string): The id of the agent.
        x (float): The x coordinate of the agent.
        y (float): The y coordinate of the agent.
        z (float): The z coordinate of the agent.
    */
    public string id;
    public float x, y, z;
    public float desx, desy, desz;

    public AgentData(string id, float x, float y, float z, float desx, float desy, float desz)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.desx = desx;
        this.desy = desy;
        this.desz = desz;
    }
}
[Serializable]

public class TrafficLightData
{
    /*
    The TrafficLightData class is used to store the data of each traffic light.
    
    Attributes:
        id (string): The id of the traffic light.
        x (float): The x coordinate of the traffic light.
        y (float): The y coordinate of the traffic light.
        z (float): The z coordinate of the traffic light.
    */
    public string id;
    public float x, y, z;
    public bool state;

    public TrafficLightData(string id, bool state, float x, float y, float z)
    {
        this.id = id;
        this.state = state;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]

public class AgentsData
{
    /*
    The AgentsData class is used to store the data of all the agents.

    Attributes:
        positions (list): A list of AgentData objects.
    */
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

public class TrafficLightsData
{
    /*
    The TrafficLightsData class is used to store the data of all the traffic lights.

    Attributes:
        positions (list): A list of TrafficLightData objects.
    */
    public List<TrafficLightData> trafficLights;

    public TrafficLightsData() => this.trafficLights = new List<TrafficLightData>();
}

public class AgentController : MonoBehaviour
{
    /*
    The AgentController class is used to control the agents in the simulation.

    Attributes:
        serverUrl (string): The url of the server.
        getAgentsEndpoint (string): The endpoint to get the agents data.
        getTrafficLightEnd (string): The endpoint to get the obstacles data.
        sendConfigEndpoint (string): The endpoint to send the configuration.
        updateEndpoint (string): The endpoint to update the simulation.
        agentsData (AgentsData): The data of the agents.
        trafficLightData (AgentsData): The data of the obstacles.
        agents (Dictionary<string, GameObject>): A dictionary of the agents.
        prevPositions (Dictionary<string, Vector3>): A dictionary of the previous positions of the agents.
        currPositions (Dictionary<string, Vector3>): A dictionary of the current positions of the agents.
        updated (bool): A boolean to know if the simulation has been updated.
        started (bool): A boolean to know if the simulation has started.
        agentPrefab (GameObject): The prefab of the agents.
        obstaclePrefab (GameObject): The prefab of the obstacles.
        floor (GameObject): The floor of the simulation.
        NAgents (int): The number of agents.
        width (int): The width of the simulation.
        height (int): The height of the simulation.
        timeToUpdate (float): The time to update the simulation.
        timer (float): The timer to update the simulation.
        dt (float): The delta time.
    */
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getTrafficLightEnd = "/getTrafficLights";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;
    TrafficLightsData trafficLightData;
    Dictionary<string, GameObject> agents;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;

    public GameObject[] agentPrefab;
    public GameObject trafficLPrefab, floor;
    public int NAgents, width, height;
    public int Module = 10;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        trafficLightData = new TrafficLightsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width/100, 1, (float)height/100);
        floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        // Launches a couroutine to send the configuration to the server.
        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            // Iterates over the agents to update their positions.
            // The positions are interpolated between the previous and current positions.

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetLightsData());
        }
    }

    IEnumerator SendConfiguration()
    {
        /*
        The SendConfiguration method is used to send the configuration to the server.

        It uses a WWWForm to send the data to the server, and then it uses a UnityWebRequest to send the form.
        */
        WWWForm form = new WWWForm();

        form.AddField("module", Module.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");

            // Once the configuration has been sent, it launches a coroutine and updates the simulation.
            StartCoroutine(UpdateSimulation());
        }
    }

    IEnumerator GetAgentsData() 
    {
        // The GetAgentsData method is used to get the agents data from the server.

        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            // Once the data has been received, it is stored in the agentsData variable.
            // Then, it iterates over the agentsData.positions list to update the agents positions.
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach(AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                Vector3 destinationPosition = new Vector3(agent.desx, agent.desy, agent.desz);

                if(!agents.ContainsKey(agent.id))
                {
                    int rand = UnityEngine.Random.Range(0, agentPrefab.Length);
                    prevPositions[agent.id] = newAgentPosition;
                    agents[agent.id] = Instantiate(agentPrefab[rand], Vector3.zero, Quaternion.identity);
                    agents[agent.id].GetComponent<ApplyTransforms>().SetDestination(newAgentPosition, true);
                }
                else
                {
                    agents[agent.id].GetComponent<ApplyTransforms>().SetDestination(newAgentPosition, false);

                    // Si el agente ha llegado a su destino final, inicia la corrutina para destruirlo
                    if (Vector3.Distance(newAgentPosition, destinationPosition) <= 0.01f) 
                    {
                        StartCoroutine(DestroyAgentAfterDelay(agent.id, 1.0f));
                    }
                }
            }
            updated = true;
            if(!started) started = true;
        }
    }

    IEnumerator GetLightsData() 
        {
            // The GetLightsData method is used to get the agents data from the server.

            UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLightEnd);
            yield return www.SendWebRequest();
    
            if (www.result != UnityWebRequest.Result.Success)
                Debug.Log(www.error);
            else 
            {
                // Once the data has been received, it is stored in the agentsData variable.
                // Then, it iterates over the agentsData.positions list to update the agents positions.
                trafficLightData = JsonUtility.FromJson<TrafficLightsData>(www.downloadHandler.text);

                foreach(TrafficLightData agent in trafficLightData.trafficLights)
                {
                    Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                    bool state = agent.state;

                        if(!agents.ContainsKey(agent.id))//buscar si no existe el agente
                        {
                            if (state == true)
                            {
                                agents[agent.id] = Instantiate(trafficLPrefab, newAgentPosition, Quaternion.identity);
                                Light light = agents[agent.id].GetComponent<Light>();
                                light.color = Color.green;
                            }
                            else
                            {
                                agents[agent.id] = Instantiate(trafficLPrefab, newAgentPosition, Quaternion.identity);
                                Light light = agents[agent.id].GetComponent<Light>();
                                light.color = Color.red;
                            }           
                        }
                        else if (state == true)
                        {
                           Light light = agents[agent.id].GetComponent<Light>();
                           light.color = Color.green;
                        }
                        else
                        {
                            Light light = agents[agent.id].GetComponent<Light>();
                            light.color = Color.red;
                        }
                }

                updated = true;
                if(!started) started = true;
            }
        }

        
    IEnumerator DestroyAgentAfterDelay(string agentId, float delay)
    {
        // Esperar el tiempo especificado
        yield return new WaitForSeconds(delay);

        // Después de la espera, destruir el agente si todavía existe
        if (agents.ContainsKey(agentId))
        {
            Debug.Log("Agent " + agentId + " has been destroyed after reaching its destination");
            Destroy(agents[agentId]);
            agents.Remove(agentId);
        }
    }

    // IEnumerator GetStateInfo() 
    // {
    //     UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTrafficLightEnd);
    //     yield return www.SendWebRequest();
 
    //     if (www.result != UnityWebRequest.Result.Success)
    //         Debug.Log(www.error);
    //     else 
    //     {
    //         trafficLightData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

    //         Debug.Log(trafficLightData.trafficLights.positions);

    //         foreach(AgentData trafficLights in trafficLightData.positions)
    //         {
    //             Instantiate(obstaclePrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
    //         }
    //     }
    // }
}
