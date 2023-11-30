/*
Use matrices to modify the vertices of amesh using the basic transforms

Santiago Tena
2023-11-02
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    Vector3 startPos;
    Vector3 finalPos;
    [SerializeField] float t;
    [SerializeField] float moveTime;
    float elapsedTime = 0.0f;
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    [SerializeField] float giro;
    [SerializeField]  GameObject wheelPrefab;
    
    GameObject wheel1;
    GameObject wheel2;
    GameObject wheel3;
    GameObject wheel4;
    [SerializeField] AXIS rotationAxis;



    Mesh mesh;
    Vector3[] baseVertices;
    Vector3[] newVertices;

    Mesh meshW1;
    Vector3[] baseVerticesW1;
    Vector3[] newVerticesW1;

    Mesh meshW2;
    Vector3[] baseVerticesW2;
    Vector3[] newVerticesW2;

    Mesh meshW3;
    Vector3[] baseVerticesW3;
    Vector3[] newVerticesW3;

    Mesh meshW4;
    Vector3[] baseVerticesW4;
    Vector3[] newVerticesW4;

    private float timer, dt;
    private float angle3;





    // Start is called before the first frame update
    void Start()
    {   
        wheel1 = Instantiate(wheelPrefab, new Vector3(0f, 0f, 0f), Quaternion.identity);
        wheel2 = Instantiate(wheelPrefab, new Vector3(0f, 0f, 0f), Quaternion.identity);
        wheel3 = Instantiate(wheelPrefab, new Vector3(0f, 0f, 0f), Quaternion.identity);
        wheel4 = Instantiate(wheelPrefab, new Vector3(0f, 0f, 0f), Quaternion.identity);

        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;

        meshW1= wheel1.GetComponentInChildren<MeshFilter>().mesh;
        baseVerticesW1 = meshW1.vertices;

        meshW2= wheel2.GetComponentInChildren<MeshFilter>().mesh;
        baseVerticesW2 = meshW2.vertices;

        meshW3= wheel3.GetComponentInChildren<MeshFilter>().mesh;
        baseVerticesW3 = meshW3.vertices;

        meshW4= wheel4.GetComponentInChildren<MeshFilter>().mesh;
        baseVerticesW4 = meshW4.vertices;

        // Create a copy of the original vertices
        newVertices = new Vector3[baseVertices.Length];
        for (int i=0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        newVerticesW1 = new Vector3[baseVerticesW1.Length];
        for (int i=0; i < baseVerticesW1.Length; i++)
        {
            newVerticesW1[i] = baseVerticesW1[i];
        }

        newVerticesW2 = new Vector3[baseVerticesW2.Length];
        for (int i=0; i < baseVerticesW2.Length; i++)
        {
            newVerticesW2[i] = baseVerticesW2[i];
        }

        newVerticesW3 = new Vector3[baseVerticesW3.Length];
        for (int i=0; i < baseVerticesW3.Length; i++)
        {
            newVerticesW3[i] = baseVerticesW3[i];
        }

        newVerticesW4 = new Vector3[baseVerticesW4.Length];
        for (int i=0; i < baseVerticesW4.Length; i++)
        {
            newVerticesW4[i] = baseVerticesW4[i];
        }
    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {

        // Coordinates for each wheel
        Vector3 targetPos1 = new Vector3(-1.88f, -0.39f, -0.3f);
        Vector3 targetPos2 = new Vector3(1.7f, -0.39f, -0.3f);
        Vector3 targetPos3 = new Vector3(1.81f, -0.39f, 6.19f);
        Vector3 targetPos4 = new Vector3(-1.52f, -0.39f, 6.19f);

        // Apply the transformation matrix to the positions of the wheels
        Matrix4x4 moveW1 = HW_Transforms.TranslationMat(targetPos1.x, targetPos1.y, targetPos1.z);
        Matrix4x4 moveW2 = HW_Transforms.TranslationMat(targetPos2.x, targetPos2.y, targetPos2.z);
        Matrix4x4 moveW3 = HW_Transforms.TranslationMat(targetPos3.x, targetPos3.y, targetPos3.z);
        Matrix4x4 moveW4 = HW_Transforms.TranslationMat(targetPos4.x, targetPos4.y, targetPos4.z);

        // Apply rotation to the wheels only
        Matrix4x4 rotateWheels = HW_Transforms.RotateMat(angle * Time.time, rotationAxis);


        // Lerp ------------------------------------------------------
        moveTime=1f;
        t = elapsedTime / moveTime;
        // Use a function to smooth the movement
        //t = t * t * (3.0f - 2.0f * t);

        // Interpolation function
        // Vector3 position = startPos + (finalPos - startPos) * t;
        Vector3 interpolated = Vector3.Lerp(startPos, finalPos, t);

        // To move using matrix tansformations, put the vector 3 into a 
        //  translation matrix, and apply to the vertices
        Matrix4x4 move = HW_Transforms.TranslationMat(interpolated.x, interpolated.y, interpolated.z);

        // Update time
        elapsedTime += Time.deltaTime;



       // ------------------------------------------------------
        //Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);


        Matrix4x4 rotate = HW_Transforms.RotateMat(angle * Time.time,
                                                    AXIS.X);

        Matrix4x4 rotateCar = HW_Transforms.RotateMat(giro, rotationAxis);

        Vector3 rotationVector = new Vector3(0,0,0);
        float angleRadians;
        float angle2;
        Matrix4x4 rotateObject;
        
        
        
        // float rotateAngle = Mathf.Atan2(startPos.z, startPos.x) * Mathf.Rad2Deg - 270;
        
        // Matrix4x4 rotateObject = HW_Transforms.RotateMat(rotateAngle,
        //                                                     AXIS.Y);

        Matrix4x4 scale = HW_Transforms.ScaleMat(0.09f, 0.09f, 0.09f);
        
        Matrix4x4 composite;

        Matrix4x4 compositeWheel1;
        Matrix4x4 compositeWheel2;
        Matrix4x4 compositeWheel3;
        Matrix4x4 compositeWheel4;

        Vector3 rotationVectorPrev = new Vector3(0,0,0);


        if (startPos != finalPos)
        {        
            rotationVector = finalPos - startPos;
            angleRadians = Mathf.Atan2(rotationVector.x, rotationVector.z);
            angle2 = angleRadians * Mathf.Rad2Deg;
            rotateObject = HW_Transforms.RotateMat(angle2, rotationAxis);

            composite = move * scale * rotateObject;

            compositeWheel1 = move * rotateObject * scale * moveW1 * rotate;
            compositeWheel2 = move * rotateObject * scale * moveW2 * rotate;
            compositeWheel3 = move * rotateObject * scale * moveW3 * rotate;
            compositeWheel4 = move * rotateObject * scale * moveW4 * rotate;

            angle3 = angle2;
        }
        else
        {   

            rotateObject = HW_Transforms.RotateMat(angle3, rotationAxis);

            composite = move * scale * rotateObject;
            compositeWheel1 = move * rotateObject * scale * moveW1;
            compositeWheel2 = move * rotateObject * scale * moveW2;
            compositeWheel3 = move * rotateObject * scale * moveW3;
            compositeWheel4 = move * rotateObject * scale * moveW4;
        }



        // Aplicar la transformación compuesta a los vértices
        for (int i = 0; i < newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = composite * temp;
        }

        // Aplicar la transformación compuesta a los vértices de wheel1
        for (int i = 0; i < newVerticesW1.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticesW1[i].x, baseVerticesW1[i].y, baseVerticesW1[i].z, 1);
            newVerticesW1[i] = compositeWheel1 * temp;
        }

        // Aplicar la transformación compuesta a los vértices de wheel2
        for (int i = 0; i < newVerticesW2.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticesW2[i].x, baseVerticesW2[i].y, baseVerticesW2[i].z, 1);
            newVerticesW2[i] = compositeWheel2 * temp;
        }

        // Aplicar la transformación compuesta a los vértices de wheel3
        for (int i = 0; i < newVerticesW3.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticesW3[i].x, baseVerticesW3[i].y, baseVerticesW3[i].z, 1);
            newVerticesW3[i] = compositeWheel3 * temp;
        }

        // Aplicar la transformación compuesta a los vértices de wheel4
        for (int i = 0; i < newVerticesW4.Length; i++)
        {
            Vector4 temp = new Vector4(baseVerticesW4[i].x, baseVerticesW4[i].y, baseVerticesW4[i].z, 1);
            newVerticesW4[i] = compositeWheel4 * temp;
        }



        // Replace the vertices in the mesh
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();

        // Replace the vertices in the mesh of wheel1
        meshW1.vertices = newVerticesW1;
        meshW1.RecalculateNormals();
        meshW1.RecalculateBounds();
        
        // Replace the vertices in the mesh of wheel2
        meshW2.vertices = newVerticesW2;
        meshW2.RecalculateNormals();
        meshW2.RecalculateBounds();
        // Replace the vertices in the mesh of wheel3
        meshW3.vertices = newVerticesW3;
        meshW3.RecalculateNormals();
        meshW3.RecalculateBounds();

        // Replace the vertices in the mesh of wheel4
        meshW4.vertices = newVerticesW4;
        meshW4.RecalculateNormals();
        meshW4.RecalculateBounds();
    }

    public void SetDestination(Vector3 destination, bool first)
    {
        if (first)
        {
            startPos = destination;
            finalPos = destination;
        }
        else
        {
            startPos = finalPos;
            finalPos = destination;
            elapsedTime = 0.0f;
        }
    }
}
