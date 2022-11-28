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
        [sg.Text("Choix :",font = ("Ubuntu"),key="CHOISE")],
        [sg.Listbox(values="", font=("Ubuntu",15), enable_events=True, size=(40, 10), key="ANSWERLIST")],
        [sg.Input("",key="filename",font=("Ubuntu",8),size=(30))],
        [sg.Button("NEW",key="NEW",font=("Ubuntu")),sg.Button("DELETE",key="REM",font=("Ubuntu"))],
    ]
    viewer_column = [
        [sg.Text("Note actelle : ",font = ("Ubuntu", 7),text_color="lightgrey",key="CURRENTNOTE"),sg.Text("",font = ("Ubuntu", 7),text_color="lightgrey",key="OKNOTE")],
        [sg.Text("\nQue signifie : ",font = ("Ubuntu"),key="QUESIGNIFIE")],
        [sg.Listbox(values="", font=("Ubuntu",10), enable_events=True, size=(40, 7), key="QUESTION")],
        [sg.Input("",key="Question",font=("Ubuntu",8),size=(30)),sg.Input("",key="Responce",font=("Ubuntu",8),size=(30))],
        [sg.Button("EDIT",key="OK",font=("Ubuntu")),sg.Button("ADD",key="ADD",font=("Ubuntu")),sg.Button("REMOVE",key="DEL",font=("Ubuntu"))],
    ]
    layout = [[
            sg.Column(answer_column,key="column1"),
            sg.VSeperator(),
            sg.Column(viewer_column,key="column2"),
        ]]
    global window
    window = sg.Window("EDITOR", layout,resizable=False,finalize=True,icon="LogoEditor.png")
    window.bind("<Return>","OK")


def choice_interface(listlecon,question):
    window["QUESTIONNUM"].Update("Editer la leçon")
    window["ANSWERLIST"].Update(listlecon)
    window["CURRENTNOTE"].Update("")
    window["QUESTION"].Update(question)
    window["QUESIGNIFIE"].Update("Éditer les questions :")
    window.TKroot.title('EDITOR')
    while True:
        event, values = window.read()
        if event == "Quitter" or event == sg.WIN_CLOSED:
            break
        if event == "QUESTION":
            if (len(values["QUESTION"])):
                window["Question"].Update(values["QUESTION"][0][0])
                window["Responce"].Update(values["QUESTION"][0][1])
        if event == "ANSWERLIST":
            if (len(values["ANSWERLIST"])):
                window["CURRENTNOTE"].Update("Meilleur note : "+str(getnote(values["ANSWERLIST"][0])))
                listquestion = getapercu(exofolder,values["ANSWERLIST"][0],100000)
                window["QUESTION"].Update(listquestion)
                window["QUESTION"].set_size((48,14))
        if event == "ADD":
            addanswer(values["ANSWERLIST"][0],[values["Question"],values["Responce"]])
            listquestion = getapercu(exofolder,values["ANSWERLIST"][0],100000)
            window["QUESTION"].Update(listquestion)
            window["Question"].Update("")
            window["Responce"].Update("")
        if event == "DEL":
            if (len(values["QUESTION"])):
                delanswer(values["ANSWERLIST"][0],values["QUESTION"][0])
                listquestion = getapercu(exofolder,values["ANSWERLIST"][0],100000)
                window["QUESTION"].Update(listquestion)
                window["Question"].Update("")
                window["Responce"].Update("")
        if event == "OK" or event == "OK_Enter":
            if (len(values["QUESTION"])):
                editanswer(values["ANSWERLIST"][0],values["QUESTION"][0],[values["Question"],values["Responce"]])
                listquestion = getapercu(exofolder,values["ANSWERLIST"][0],100000)
                window["QUESTION"].Update(listquestion)
                window["Question"].Update("")
                window["Responce"].Update("")
        if event == "NEW":
            newlecon(values["filename"])
            listlecon=genexo()
            window["ANSWERLIST"].Update(listlecon)
        if event == "REM":
            os.remove(exofolder+values["ANSWERLIST"][0]+".json")
            listlecon=genexo()
            window["ANSWERLIST"].Update(listlecon)

def newlecon(filename):
    leconfile=open(exofolder+filename+".json","w")
    leconfile.write(json.dumps({}))
    leconfile.close()
    pass

def delanswer(EXO,OLDQUESTION):
    leconfile = open(exofolder+EXO+".json")
    jsonlecon = json.loads(leconfile.read())
    leconfile.close()
    jsonlecon.pop(OLDQUESTION[0],None)
    leconfile = open(exofolder+EXO+".json","w")
    leconfile.write(json.dumps(jsonlecon,indent = 4))

def editanswer(EXO,OLDQUESTION,NEWQUESTION):
    leconfile = open(exofolder+EXO+".json")
    jsonlecon = json.loads(leconfile.read())
    leconfile.close()
    jsonlecon.pop(OLDQUESTION[0],None)
    jsonlecon[NEWQUESTION[0]] = NEWQUESTION[1]
    leconfile = open(exofolder+EXO+".json","w")
    leconfile.write(json.dumps(jsonlecon,indent = 4))
    
def addanswer(EXO,NEWQUESTION):
    leconfile = open(exofolder+EXO+".json")
    jsonlecon = json.loads(leconfile.read())
    leconfile.close()
    if not NEWQUESTION[0] in jsonlecon:
        jsonlecon[NEWQUESTION[0]] = NEWQUESTION[1]
        leconfile = open(exofolder+EXO+".json","w")
        leconfile.write(json.dumps(jsonlecon,indent = 4))

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
    return(leconlist)

def jsonfileopen(exofolder,lecon):
    leconfile = open(exofolder+lecon+".json")
    jsonlecon = json.loads(leconfile.read())
    leconlist = []
    for i in jsonlecon:
        leconlist.append([i,jsonlecon[i]])
    return(leconlist)

def genexo():
    listexo = []
    for i in sorted(os.listdir(exofolder)):
        if i[-5:] == ".json":
            listexo.append(i[:-5])
    return(listexo)

listexo = []
for i in sorted(os.listdir(exofolder)):
    if i[-5:] == ".json":
        listexo.append(i[:-5])

prepare_windows()
lecon = choice_interface(listexo,"")
