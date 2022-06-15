
from matplotlib import pyplot
emotions_list = ["joy","Sorrow","Anger","Surprise"]


def cont_emotions(ac):
    #[[1,2,1],[1,1,1]]
    #result = gen_result(ac)
    aux = []
    
    cont_joy = 0
    cont_sorrow = 0
    cont_anger = 0
    cont_surprise = 0
    for i in ac.emotions:
        for a in i.list_emotions:
            if i.list_emotions[a] not in ["UNKNOWN", "VERY_UNLIKELY","UNLIKELY"]:
                if  a== "joy_likelihood":
                    cont_joy = cont_joy+1
                elif a == "sorrow_likelihood":
                    cont_sorrow = cont_sorrow+1
                elif a == "anger_likelihood":
                    cont_anger = cont_anger+1
                elif a == "surprise_likelihood":
                    cont_surprise = cont_surprise+1

    aux.append(cont_joy)
    aux.append(cont_sorrow)
    aux.append(cont_anger)
    aux.append(cont_surprise)
    return aux
def gen_result(ac):
    aux = []
    for i in ac.emotions:
        aux_list2 = []
        for a in i.list_emotions:
            aux_list2.append(i.list_emotions[a])
        aux.append(aux_list2)
    return aux
def gen_graphs(ac):
    num_emotions = cont_emotions(ac)
    fig, ax = pyplot.subplots()
    pyplot.bar(emotions_list,num_emotions)
    pyplot.show()
    