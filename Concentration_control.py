
import cv2 as cv
from tkinter import messagebox
from time import sleep
import os, io
import pygame
import threading
pygame.mixer.init()
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
            cv.imwrite("foto1.png", imagen)
            if vista:
                cv.imshow('Toma de fotografia',imagen)
                cv.waitKey(0)
        else:
            messagebox.showerror(
                title='Error en la toma de imagen', 
                message='No fue posible capturar la imagen con esta dispositivo!')
        return imagen

'''
utiliza el servicio de google vision para registrar los angulos de la cara
compara los angulos para averiguar si el usuario esta distraido, si todos los angulos dan negativo significa que el usuario esta viendo hacia abajo
si el angulo pan_angle es es mayor a 30 o menor que -30 significa que le usuario esta viendo hacia la izquierda o la derecha
se utiliza la libreria pygame para cargar el archivo de audio para la alerta 

'''
def capture_angles():
    if check == False:
        cont = 5
        time = 0
        while True:
            distracted = True
            
            mi_rostro=rostro()
            imagen=mi_rostro.capturar_imagen(vista=False,cuenta_regresiva=False)

            from google.cloud import vision
            os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
            client=vision.ImageAnnotatorClient()

            with io.open('foto1.png','rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)

            response = client.face_detection(image=image)

            faces = response.face_annotations
            if len(faces) == 1:
                faces_list=[]

                for face in faces:
                    #dicccionario con los angulos asociados a la detección de la cara
                    face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)
                distracted = select_distracted(face_angles)
                if distracted == True:
                    cont = cont-1
                    time = 0
                    if cont == 0:
                        pygame.mixer.music.load("alarma.mp3") 
                        pygame.mixer.music.play(loops=0) 
                        select = messagebox.askyesno("Control de concentracion","Estas distraido,¿Desea detener la alerta?")
                        if select == True:
                            pygame.mixer.music.pause()
                            cont = 5
                else:
                    time = 20
                    cont = 5
                sleep(time)
            else:
                messagebox.showerror("Control de concentracion","No se reconoce un rostro en la imagen o se reconocen mas de un rostro")
    else:
        exit()
def select_distracted(dic):
    dis = False
    if (dic["roll_angle"] < 0) and (dic["pan_angle"] <0)  and (dic["tilt_angle"] < 0):
        return True
    elif dic["pan_angle"] <30 and dic["pan_angle"] > -30:
        return False
    else:
        return True

def start_control():
    
    proceso=threading.Thread(target=capture_angles)
    proceso.start() 
    
def off():
    global check
    check = True

