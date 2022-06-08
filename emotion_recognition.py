import os, io
from time import sleep
from tkinter import messagebox
from tkinter.messagebox import showerror
import cv2 as cv
import threading
from google.cloud import vision
from obEmotions import emotions
from datetime import datetime
import functions_students
check = False
class rostro ():
    
    def __init__(self) -> None:
        pass

    def capturar_imagen(self,vista,cuenta_regresiva):

        camara = cv.VideoCapture(0)
        leido, imagen = camara.read()
        camara.release()

        if leido == True:
            cv.imwrite("foto.png", imagen)
            if vista:
                cv.imshow('Toma de fotografia',imagen)
                cv.waitKey(0)
        else:
            showerror(
                title='Error en la toma de imagen', 
                message='No fue posible capturar la imagen con esta dispositivo!')
        return imagen



def tarea_paralela(estado):
    while True:
        if check == False:
            ac = select_activities()
            if ac != None:
                mi_rostro=rostro()
                
                imagen = mi_rostro.capturar_imagen(vista=False,cuenta_regresiva=True)

                os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
                client=vision.ImageAnnotatorClient()

                with io.open('foto.png','rb') as image_file:
                    content = image_file.read()

                image = vision.Image(content=content)

                response = client.face_detection(image=image)

                faces = response.face_annotations

                likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

                faces_list=[]

                for face in faces:
                    #dicccionario con los angulos asociados a la detección de la cara
                    face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)

                    #confianza de detección (tipo float)
                    detection_confidence=face.detection_confidence

                    #Probabilidad de Expresiones
                    #Emociones: Alegría, pena, ira, sorpresa
                    face_expressions=dict(  joy_likelihood=likelihood_name[face.joy_likelihood],
                                            sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                                            anger_likelihood=likelihood_name[face.anger_likelihood],
                                            surprise_likelihood=likelihood_name[face.surprise_likelihood],
                                            under_exposed_likelihood=likelihood_name[face.under_exposed_likelihood],
                                            blurred_likelihood=likelihood_name[face.blurred_likelihood],
                                            headwear_likelihood=likelihood_name[face.headwear_likelihood])

                    #polígono de marco de cara
                    vertices=[]
                    for vertex in face.bounding_poly.vertices:
                        vertices.append (dict (x=vertex.x, y=vertex.y))

                    face_dict=dict( face_angles=face_angles,
                                    detection_confidence=detection_confidence,
                                    face_expressions=face_expressions,
                                    vertices=vertices
                                    )
                    faces_list.append(face_dict)

                x1=faces_list[0]['vertices'][0]['x']
                y1=faces_list[0]['vertices'][0]['y']
                x2=faces_list[0]['vertices'][2]['x']
                y2=faces_list[0]['vertices'][2]['y']

                cv.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),3)
                hour = datetime.now()
                new_emotions = emotions(hour,face_expressions)
                ac.emotions.append(new_emotions)
                sleep(10)
            else:
                messagebox.showerror("Actividades","No hay ninguna actividad programada para esta hora")
        else:
            exit()
def capture_photos():
    
    estado=[True]
    parametros=[estado]
    proceso=threading.Thread(target=tarea_paralela,args=parametros)
    proceso.start()
    

def select_activities():

    hour = datetime.now()
    hour = datetime.strftime(hour, '%H:%M')
    hour = datetime.strptime(hour, '%H:%M')
    for i in functions_students.list_students[0].activities:
        if i.getStatus() == "En curso":
            
            
            if ((i.getStart_time() <= hour and hour <= i.getEnd_time())):
                return i
def off():
    global check
    check = True
                       



