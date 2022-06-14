import chunk
import cv2 as cv
from tkinter import messagebox
from time import sleep
import os, io
import pyaudio
import wave
import threading
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
def capture_angles():
    cont = 3
    time = 10
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
                time = 0
                if cont == 0:
                    select = messagebox.askyesno("Control de concentracion","Estas distraido,¿Desea detener la alerta?")
                    if select == True:
                        cont = 30
                cont = cont-1
            else:
                time = 20
                cont = 30
            sleep(time)
        else:
            messagebox.showerror("Reconocimiento de Emociones","No se reconoce un rostro en la imagen o se reconocen mas de un rostro")
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
    
    
'''file_audio = wave.open(r"alarma.wav","rb")
paudio = pyaudio.PyAudio()
stream = paudio.open(format=paudio.get_format_from_width(file_audio.getsampwidth()),channels=file_audio.getnchannels(),rate=file_audio.getframerate(),output=True)
data = file_audio.readframes(chunk)
while data:
    stream.write(data)
    data = f.readframes(chunk)'''

