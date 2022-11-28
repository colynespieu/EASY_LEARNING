#!/usr/bin/python3
from datetime import datetime,timedelta
from ctypes import alignment
import os,subprocess,json,random
from tkinter import CENTER
from turtle import position
import PySimpleGUI as sg

global exofolder
global note
folder = os.getcwd()
exofolder = os.getcwd()+"/exo/"
notefile = "/result.json"

def prepare_windows():
    answer_column = [
        [sg.Text("Appuyer sur OK pour commencer ",font = ("Ubuntu",7),text_color="lightgrey",key="QUESTIONNUM"),],
        [sg.Text("",font = ("Ubuntu"),text_color="LightCoral",key="GOODANSWER")],
        [sg.Text("Choix :",font = ("Ubuntu"),key="CHOISE")],
        [sg.Listbox(values="", font=("Ubuntu",15), enable_events=True, size=(40, 10), key="ANSWERLIST")],
    ]
    viewer_column = [
        [sg.Text("Note actelle : ",font = ("Ubuntu", 7),text_color="lightgrey",key="CURRENTNOTE"),sg.Text("",font = ("Ubuntu", 7),text_color="lightgrey",key="OKNOTE")],
        [sg.Text("\nQue signifie : ",font = ("Ubuntu"),key="QUESIGNIFIE")],
        [sg.Text("",justification='c',font = ("Ubuntu", 50),size=(10, 3), key="QUESTION")],
        [sg.Button("OK",key="OK",font=("Ubuntu"))],
    ]
    layout = [[
            sg.Column(answer_column,key="column1"),
            sg.VSeperator(),
            sg.Column(viewer_column,key="column2"),
        ]]
    global window
    window = sg.Window("EXERCISER", layout,resizable=False,finalize=True,icon="Logo.png")
    window.bind("<Return>","OK")


def choice_interface(listlecon,question):
    window["QUESTIONNUM"].Update("Choix de la leçon")
    window["GOODANSWER"].Update("")
    window["ANSWERLIST"].Update(listlecon)
    window["CURRENTNOTE"].Update("")
    window["QUESTION"].Update(question)
    window["QUESIGNIFIE"].Update("Aperçu des questions :")
    window.TKroot.title('EXERCISER')
    while True:
        event, values = window.read()
        if event == "Quitter" or event == sg.WIN_CLOSED:
            break
        if event == "ANSWERLIST":
            window["CURRENTNOTE"].Update("Meilleur note : "+str(getnote(values["ANSWERLIST"][0])))
            window["QUESTION"].Update(getapercu(exofolder,values["ANSWERLIST"][0],14),font=("Ubuntu", 10))
            window["QUESTION"].set_size((48,14))
            pass
        if event == "OK" or event == "OK_Enter":
            if (values["ANSWERLIST"]):
                window["QUESIGNIFIE"].Update("\nQue signifie : ")
                window["QUESTION"].Update("",font=("Ubuntu", 48))
                window["QUESTION"].set_size((10,3))
                window.TKroot.title('EXERCISER - '+values["ANSWERLIST"][0])
                return(values["ANSWERLIST"][0])
            elif (len(listlecon) == 0):
                return("")
            pass

def exerciser_interface(listanswer,question,currentnote,color,goodanswer,questionnumber):
    window["QUESTIONNUM"].Update("Question "+str(questionnumber))
    window["GOODANSWER"].Update(goodanswer)
    window["ANSWERLIST"].Update(listanswer)
    window["CURRENTNOTE"].Update("Note actelle : "+currentnote)
    window["QUESTION"].Update(question)
    timeoutnow = datetime.now()
    timeouttime = timeoutnow + timedelta(seconds=6)
    while True:
        timeout = timeouttime - datetime.now()
        timeout = max(0,int(timeout.total_seconds()*100))
        window["OKNOTE"].Update(str(timeout))
        event, values = window.read(timeout=20)
        if event == "Quitter" or event == sg.WIN_CLOSED:
            break
        if event == "OK" or event == "OK_Enter":
            if (values["ANSWERLIST"]):
                return([values["ANSWERLIST"][0],timeout])
            elif (len(listanswer) == 0):
                window["OKNOTE"].Update("")
                return("")
            pass

def savenote(note,lecon):
    with open(folder+notefile, "r") as jsonfile:
        jsonnote = json.loads(jsonfile.read())
    if ( lecon not in jsonnote):
        jsonnote[lecon] = 0
    if jsonnote[lecon] < note:
        jsonnote[lecon] = note
    with open(folder+notefile, "w") as jsonfile:
        json.dump(jsonnote, jsonfile)

def getnote(lecon):
    with open(folder+notefile, "r") as jsonfile:
        jsonnote = json.loads(jsonfile.read())
    if ( lecon not in jsonnote):
        jsonnote[lecon] = 0
    return(jsonnote[lecon])

def randomiser(liste,passage):
    tmpval = ""
    for i in range(0,passage):
        for z in range (0,len(liste)-1):
            if random.choice([True,True, False]):
                tmpval = liste[z]
                liste[z] = liste[z+1]
                liste[z+1] = tmpval
    return(liste)

def generateexo(liste,possi):
    exolist = []
    for i in liste:
        possivalue = []
        response = i[1]
        possivalue.append(i[1])
        for z in range(1,possi):
            tmp = ""
            while (tmp == ""):
                for j in liste:
                    if (random.choice([True, False,False,False,False,False,False,False,False,False,False,False]) and tmp == "" and j[1] not in possivalue):
                        tmp = j[1]
                        break
            possivalue.append(tmp)
        exolist.append([i[0],randomiser(possivalue,possi),response])
    return(exolist)

def getapercu(exofolder,lecon,max):
    toreturn = ""
    leconlist = jsonfileopen(exofolder,lecon)
    for i in range(0,min(max-1,len(leconlist))):
        toreturn = toreturn + leconlist[i][0]+" : "+leconlist[i][1] +"\n"
    if (len(leconlist) >= max):
        toreturn = toreturn + "..."
    return(toreturn)

def jsonfileopen(exofolder,lecon):
    leconfile = open(exofolder+lecon+".json")
    jsonlecon = json.loads(leconfile.read())
    leconlist = []
    for i in jsonlecon:
        leconlist.append([i,jsonlecon[i]])
    return(leconlist)

listexo = []
for i in sorted(os.listdir(exofolder)):
    if i[-5:] == ".json":
        listexo.append(i[:-5])

prepare_windows()

while True:
    lecon = choice_interface(listexo,"")
    if lecon == "" or lecon == None :
        window.close()
        exit(1)

    leconlist = jsonfileopen(exofolder,lecon)
    leconlist = randomiser(leconlist,len(leconlist))
    exolist = generateexo(leconlist,7)

    note,totalquestion,color,goodanswer,questionnumber = 0,str(len(exolist)),"white","",1
    for i in exolist:
        question,answer=i[0],i[1]
        responselist = exerciser_interface(answer,question,str(note),color,goodanswer,str(questionnumber)+"/"+totalquestion)
        questionnumber+=1
        if responselist == None:
            window.close()
            exit(1)
        response = responselist[0]
        notetoadd = responselist[1]
        if (response == i[2]):
            note+=notetoadd
            color="LawnGreen"
            goodanswer = ""
        else:
            goodanswer = "La bonne réponse était : "+i[2]+"\n"
            color="LightCoral"

    question,answer="",[]
    exerciser_interface(answer,question,str(note),color,goodanswer,"fin")
    savenote(note,lecon)
