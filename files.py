from datetime import date, datetime
from tkinter import messagebox
from obActivities import activities
import functions_students
def file_activities(student):
    try:
        fileActivities = open("Activities.txt","w")
        for i in student.activities:
            description = i.getDescripcion()
            course = i.getCourse()
            date = datetime.strftime(i.getDate(),'%Y/%m/%d')
            start_time = datetime.strftime(i.getStart_time(),'%H:%M')
            end_time = datetime.strftime(i.getEnd_time(),'%H:%M')
            status = i.getStatus()
            list_emotions = []
            fileActivities.write(str(description)+"-"+str(course)+"-"+str(date)+"-"+str(start_time)+"-"+str(end_time)+"-"+str(status)+"-"+str(list_emotions)+"\n")
            fileActivities.close()
    except:
        messagebox.showerror("Archivos","Hay un problema con la escritura del archivo")


def read_file():
    try:
        fileActivities = open("Activities.txt","r")
    except FileNotFoundError:
        file_activities()
        return
    try:
        flag = True
        while flag == True:
            line = fileActivities.readline()
            if line != '':
                line = line.split("-")
                description = line[0]
                course = line[1]
                date = line[2]
                start_time = line[3]
                end_time = line[4]
                status = line[5]
                list_emotions = line[6].replace("\n",'')
                ob = activities(description,course,date,start_time,end_time,status)
                list_emotions = eval(list_emotions)
                ob.emotions = list_emotions
                functions_students.list_students[0].activities.append(ob)
            else:
                flag = False
    except:
        
        messagebox.showerror("Lectura de archivos","Error en la lectura del archivo")
        