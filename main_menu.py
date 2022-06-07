from datetime import date, datetime
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
import add_activities
from obStudents import students
from obCareers import careers
import functions_students
import files
career = careers("Computacion")
st = students("Leiner Alvarado","leiner@gmail.com",career,12345)
functions_students.list_students.append(st)
files.read_file()

def main_window():
    main = tk.Tk()
    main.title("Aplicación principal")
    main.minsize(600,400)
    
    #boton agregar actividad
    tk.Button(main, text="Agregar actividades", command=lambda:add_activities.menuaddactivities(st), height=2,width=20).place(x=160, y=120)
    
    
    #boton Reconocimiento de emociones
    tk.Button(main, text="Reconocimiento de emociones", command=print, height=2,width=30).place(x=330, y=30)
    #concentracion
    tk.Button(main, text="Control de concentracion", command=print, height=2,width=30).place(x=90, y=30)
    tk.Button(main, text="Reportes", command=print, height=2,width=20).place(x=330, y=120)
    tk.Button(main, text="Graficos", command=print, height=2,width=20).place(x=160, y=210)
    tk.Button(main, text="Salir ", command=print, height=2,width=20).place(x=330, y=210)
    
    #salir 
    
    
    main.mainloop()
main_window()