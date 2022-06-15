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
'''
Clase rostro, realiza la funcion de tomar la imagen desde la camara del equipo 
'''
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

'''
Se utiliza el servicio de google para realizar el reconocimiento de emociones
Se seleciona la actividad activa por la hora del sistema 
almacena el diccionario de emociones en un objeto y este se vincula a la actividad con la hora exacta en la que se realizo el estudio de emociones
'''

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
                if len(faces) == 1:

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
                else:
                    messagebox.showerror("Reconocimiento de Emociones","No se reconoce un rostro en la imagen o se reconocen mas de un rostro")
                    tarea_paralela(estado)

                x1=faces_list[0]['vertices'][0]['x']
                y1=faces_list[0]['vertices'][0]['y']
                x2=faces_list[0]['vertices'][2]['x']
                y2=faces_list[0]['vertices'][2]['y']

                cv.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),3)
                hour = datetime.now()
                new_emotions = emotions(hour,face_expressions)
                ac.emotions.append(new_emotions)
                sleep(50)
            else:
                messagebox.showerror("Actividades","No hay ninguna actividad programada para esta hora")
                exit()
        else:
            exit()
'''
Se utiliza la libreria threading para crear hilos de ejecucion
'''
def capture_photos():
    
    estado=[True]
    parametros=[estado]
    proceso=threading.Thread(target=tarea_paralela,args=parametros)
    proceso.start()
    
'''
Seleciona la actividad que cumple con la hora del sistema
utilizando la funcion datetume.now se consigue la hora y la fecha del sistema 
para poder compararlos se convierten en string y despues de nuevo en objeto pero con los datos necesarios para la comparacion
'''
def select_activities():
    date = datetime.now()
    date = datetime.strftime(date, '%Y/%m/%d')
    date = datetime.strptime(date, '%Y/%m/%d')
    hour = datetime.now()
    hour = datetime.strftime(hour, '%H:%M')
    hour = datetime.strptime(hour, '%H:%M')
    for i in functions_students.list_students[0].activities:
        if i.date == date:
            if i.getStatus() == "En curso":
                
                if ((i.getStart_time() <= hour and hour <= i.getEnd_time())):
                    return i
def off():
    global check
    check = True
                       



