from datetime import date, datetime
from tkinter import messagebox
from obActivities import activities
import functions_students
from obEmotions import emotions
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
            list_emotions = create_listemotions(i.emotions)
            fileActivities.write(str(description)+"-"+str(course)+"-"+str(date)+"-"+str(start_time)+"-"+str(end_time)+"-"+str(status)+"-"+str(list_emotions)+"\n")
        fileActivities.close()
    except:
        messagebox.showerror("Archivos","Hay un problema con la escritura del archivo")
def create_listemotions(lista):
    auxlist = []
    for i in lista:
        auxlist2 = []
        auxlist2.append(datetime.strftime(i.hour,'%H:%M'))
        for a in i.list_emotions:
            
             auxlist2.append(i.list_emotions[a])
        auxlist.append(auxlist2)
    return auxlist
        

def read_file(student):
    try:
        fileActivities = open("Activities.txt","r")
    except FileNotFoundError:
        file_activities(student)
        return
    try:
        flag = True
        while flag == True:
            line = fileActivities.readline()
            if line != '':
                line = line.split("-")
                description = line[0]
                course = line[1]
                date = datetime.strptime(line[2], '%Y/%m/%d')
                start_time = line[3]
                start_time = datetime.strptime(start_time, '%H:%M')
                end_time = line[4]
                end_time = datetime.strptime(end_time, '%H:%M')
                status = line[5]
                list_emotions = line[6].replace("\n",'')
                list_emotions = eval(list_emotions)
                list_emotions = read_emotions(list_emotions)
                ob = activities(description,course,date,start_time,end_time,status)
                
                ob.emotions = list_emotions
                functions_students.list_students[0].activities.append(ob)
            else:
                flag = False
    except:
        
        messagebox.showerror("Lectura de archivos","Error en la lectura del archivo")

def read_emotions(list):
    auxlist2 = []
    
    for i in list:
        dic = {}
        date = datetime.strptime(i[0], '%H:%M')
        dic["joy_likelihood"] = i[1]
        dic["sorrow_likelihood"] = i[2]
        dic["anger_likelihood"] = i[3]
        dic["surprise_likelihood"] = i[4]
        dic["under_exposed_likelihood"] = i[5]
        dic["blurred_likelihood"] = i[6]
        dic["headwear_likelihood"] = i[7]
        new = emotions(date,dic)
        auxlist2.append(new)
    return auxlist2