from datetime import date, datetime
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
import add_activities
from obStudents import students
from obCareers import careers
import functions_students
import files
import emotion_recognition
import Concentration_control
##########################################
#Datos quemados en el sistema
career = careers("Computacion")
st = students("Leiner Alvarado","leiner@gmail.com",career,12345)
functions_students.list_students.append(st)
################################################

files.read_file()# Lee el archivo para cargar las actividades ya existentes
functions_students.all_change_status(st)# Cambia el status de todas las actividades que ya pasaron a realizadas
cont = 0
#------------Menu principal------------------------
def main_window():
    
    on = True
    main = tk.Tk()
    main.title("Aplicación principal")
    main.minsize(600,400)
    
    #boton agregar actividad
    tk.Button(main, text="Agregar actividades", command=lambda:add_activities.menuaddactivities(st), height=2,width=20).place(x=168, y=170)
    tk.Button(main, text="Concluir actividades", command=printactivities, height=2,width=20).place(x=340, y=170)
    
    #boton Reconocimiento de emociones
    tk.Button(main, text="Reconocimiento de emociones", command=lambda:[emotion_recognition.capture_photos()], height=2,width=30).place(x=100, y=30)
    tk.Button(main, text="Desactivar reconocimiento", command=emotion_recognition.off, height=2,width=30).place(x=340, y=30)
    #concentracion
    tk.Button(main, text="Control de concentracion", command=Concentration_control.start_control, height=2,width=30).place(x=100, y=100)
    tk.Button(main, text="Desactivar control", command=Concentration_control.off, height=2,width=30).place(x=340, y=100)
    tk.Button(main, text="Reportes", command=print, height=2,width=20).place(x=340, y=240)
    tk.Button(main, text="Graficos", command=print, height=2,width=20).place(x=168, y=240)
    tk.Button(main, text="Salir ", command=lambda:[files.file_activities(st),emotion_recognition.off(),close(main)], height=2,width=20).place(x=260, y=300)
    
    #salir 
    
    
    main.mainloop()
#------------funcion cerrar ventanas------------------------
def close(win):
    win.destroy()
#------------Menu para cambio de estado de actividades------------------------
def printactivities():
    winmenuactivities = tk.Toplevel()
    winmenuactivities.title("Cambiar estado de actividades")
    winmenuactivities.minsize(700,400)
    fontStyle = tkFont.Font(family="Lucida Grande", size=12)
    listac = list_activities(st)
    lb_activities= tk.Label(winmenuactivities,text="Actividad:").place(x=10, y=40)
    sv_activities = tk.StringVar()
    combobox_activities = ttk.Combobox(winmenuactivities,values =listac,textvariable=sv_activities,state="readonly").place(x=80,y=40)
    
    lb_status= tk.Label(winmenuactivities,text="Estado:").place(x=10, y=70)
    sv_status = tk.StringVar()
    combobox_status = ttk.Combobox(winmenuactivities,values =["Realizada"],textvariable=sv_status,state="readonly").place(x=80,y=70)
    
    tk.Button(winmenuactivities, text="Realizar el cambio",font=fontStyle, command=lambda:[mod_activities(sv_status,sv_activities,st)],height=2,width=14).place(x=85, y=130)
    tk.Button(winmenuactivities, text="Salir",font=fontStyle, command=lambda:close(winmenuactivities),height=2,width=14).place(x=85, y=210)
    
    winmenuactivities.mainloop()
def list_activities(student):
    auxlist = []
    for i in student.activities:
        if i.status == "En curso":
            des = i.getDescripcion()
            course = i.course
            ac = str(des)+"/"+str(course)
            auxlist.append(ac)
    return auxlist
def mod_activities(status,ac,student):
        ac = ac.get()
        ac = ac.split("/")
        status = status.get()
        for i in student.activities:
            if i.getDescripcion() == ac[0] and i.getCourse() == ac[1]:
                i.setStatus(status)
                messagebox.showinfo("Actividades","Su actividad cambio con exito de estado")
                break
                

main_window()
