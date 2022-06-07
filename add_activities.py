from datetime import date, datetime
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
import functions_students
#-----------MENU AGREGAR ACTIVIDADES-----------#
def menuaddactivities(student):
    winmenuactivities = tk.Toplevel()
    winmenuactivities.title("Agregar actividad")
    winmenuactivities.minsize(800,600)
    fontStyle = tkFont.Font(family="Lucida Grande", size=12)
    listcourses = coursestudent(student)
    
    lb_name_acti=tk.Label(winmenuactivities,text="Descripcion de la actividad:").place(x=10, y=40)
    sv_name_acti = tk.StringVar()
    e_name_acti= ttk.Entry(winmenuactivities, textvariable = sv_name_acti, width=30).place(x=165, y=40)
    
    lb_course= tk.Label(winmenuactivities,text="Asociar curso(opcional):").place(x=10, y=70)
    sv_course = tk.StringVar()
    combobox_course = ttk.Combobox(winmenuactivities,values =listcourses,textvariable=sv_course,state="readonly").place(x=150,y=70)
    
    lb_date=tk.Label(winmenuactivities,text="Fecha(aaaa/mm/dd):").place(x=10, y=100)
    sv_date = tk.StringVar()
    e_date= ttk.Entry(winmenuactivities, textvariable = sv_date, width=30).place(x=130, y=100)
    
    lb_startime=tk.Label(winmenuactivities,text="Hora de inicio(HH:MM):").place(x=10, y=130)
    sv_startime = tk.StringVar()
    e_startime= ttk.Entry(winmenuactivities, textvariable = sv_startime, width=30).place(x=150, y=130)
        
    lb_endtime=tk.Label(winmenuactivities,text="Hora de finalización(HH:MM):").place(x=10, y=160)
    sv_endtime = tk.StringVar()
    e_endtime= ttk.Entry(winmenuactivities, textvariable = sv_endtime, width=30).place(x=180, y=160)
    
    tk.Button(winmenuactivities, text="Agregar actividad",font=fontStyle, command=lambda:add_activities(student,sv_name_acti,sv_course,sv_date,sv_startime,sv_endtime),height=2,width=14).place(x=300, y=220)
    tk.Button(winmenuactivities, text="Salir",font=fontStyle, command=lambda:winmenuactivities.destroy(),height=2,width=14).place(x=450, y=220)
    
    
    winmenuactivities.mainloop()
def add_activities(student,name,course,date,start_time,end_time):
    strname = name.get()
    strcourse = course.get()
    strdate = date.get()
    strstart_time = start_time.get()
    strend_time = end_time.get()
    functions_students.add_activities(student,strname,strcourse,strdate,strstart_time,strend_time)
    clearwin(name,course,date,start_time,end_time)
    
    
        
def coursestudent(student):
    auxlist = []
    for i in student.courses:
        if i.status == "En curso":
            auxlist.append(i.getName())
    return auxlist


#-----------FUNCION LIMPIAR VENTANA PRINCIPAL-----------#
def clearwin(name,course,date,start_time,end_time):
    name.set('')
    course.set('')
    date.set('')
    start_time.set('')
    end_time.set('')
    

#-----------FUNCION CERRAR VENTANAS-----------#
def close(win):
    win.destroy()
