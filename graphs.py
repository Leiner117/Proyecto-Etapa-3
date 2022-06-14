
from matplotlib import pyplot
emotions_list = ["joy","Sorrow","Anger","Surprise","Under_exposed","blurred","headwear"]


def cont_emotions(ac):
    result = gen_result(ac)
    aux = []
    cont_joy = 0
    cont_sorrow = 0
    cont_anger = 0
    cont_surprise = 0
    cont_under_exposed = 0
    cont_blurred = 0
    cont_headwear = 0
    for i in result:
        
def gen_result(ac):
    aux = []
    for i in ac.emotions:
        aux_list2 = []
        for a in i.list_emotions:
            aux_list2.append(i.list_emotions[a])
        aux.append(aux_list2)
    return aux

    
        