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
career = careers("Computacion")
st = students("Leiner Alvarado","leiner@gmail.com",career,12345)
functions_students.list_students.append(st)
files.read_file()
cont = 0
def main_window():
    
    on = True
    main = tk.Tk()
    main.title("Aplicación principal")
    main.minsize(600,400)
    
    #boton agregar actividad
    tk.Button(main, text="Agregar actividades", command=lambda:add_activities.menuaddactivities(st), height=2,width=20).place(x=168, y=170)
    tk.Button(main, text="Concluir actividades", command=print, height=2,width=20).place(x=340, y=170)
    
    #boton Reconocimiento de emociones
    tk.Button(main, text="Reconocimiento de emociones", command=lambda:[emotion_recognition.capture_photos()], height=2,width=30).place(x=100, y=30)
    tk.Button(main, text="Desactivar reconocimiento", command=emotion_recognition.off, height=2,width=30).place(x=340, y=30)
    #concentracion
    tk.Button(main, text="Control de concentracion", command=print, height=2,width=30).place(x=100, y=100)
    tk.Button(main, text="Desactivar control", command=print, height=2,width=30).place(x=340, y=100)
    tk.Button(main, text="Reportes", command=print, height=2,width=20).place(x=340, y=240)
    tk.Button(main, text="Graficos", command=print, height=2,width=20).place(x=168, y=240)
    tk.Button(main, text="Salir ", command=lambda:[files.file_activities(st),close(main)], height=2,width=20).place(x=260, y=300)
    
    #salir 
    
    
    main.mainloop()

def close(win):
    win.destroy()
main_window()
