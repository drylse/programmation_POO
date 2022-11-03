# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 15:46:32 2021

@author: Admin
"""

from pylab import *
import tkinter as tk
import xlrd
import csv
from PIL import Image, ImageTk


## Création d'une classe 

class Cochon(object):
    """ 
    Permet de définir un cochon 
    """
    def __init__(self, age, sexe):
        self.age = age
        self.sexe = sexe 
        self.coordonnees = []
        self.baillement = []
    
    def get(self):
        return [self.age, self.sexe]
    
    def nv_baillement(self, n):
        self.baillement.append(n)
        
    def get_baillement(self):
        return self.baillement
        
    def position(self, x, y):
        self.coordonnees.append([x,y])
    
    def get_position(self):
        return self.coordonnees


## Fonctions 


def deplacement(): 
     """ fonction qui définit le déplacement des cochons de n en n+1 """
     for i in range(len(liste_cochons)):
         choix = randint(0,4)
         cochon = liste_cochons[i]
         position = cochon.get_position()
         x = position[-1][0]
         y = position[-1][1]
         if choix == 0 and x < n-2 :
             if len(canvas.find_overlapping(x*30+70, y*30+10, x*30+80, y*30+20)) == 0: 
                 cochon.position(x + 2, y) # va a droite
             else:
                 cochon.position(x,y)
         elif choix == 1 and x > 1: # va a gauche
             if len(canvas.find_overlapping(x*30-50, y*30+10, x*30-40, y*30+20)) == 0:
                 cochon.position(x - 2, y)
             else:
                 cochon.position(x,y)
         elif choix == 2 and y < n-2: # va en dessous
             if len(canvas.find_overlapping(x*30+10, y*30+70, x*30+20, y*30+80)) == 0:
                 cochon.position(x, y + 2)
             else:
                 cochon.position(x,y)
         elif choix == 3 and y > 1:  # va au dessus 
             if len(canvas.find_overlapping(x*30+10, y*30-50, x*30+20, y*30-40)) == 0:
                 cochon.position(x, y - 2)
             else:
                 cochon.position(x,y)
         else:
             cochon.position(x,y)
    


def baillement():    
    global t
    global T
    
    while t < T:
        
        liste_emetteurs = []

        if t == 0 :
            amorce = randint(0,len(liste_cochons))
            liste_emetteurs = [amorce]
            liste_cochons[amorce].nv_baillement(0)
        else:
            for i in range(len(liste_cochons)):
                if len(liste_cochons[i].get_baillement()) > 0 and liste_cochons[i].get_baillement()[-1] == t:
                    liste_emetteurs.append(i)
                    
        if len(liste_emetteurs) > 0:
            for j in range(len(liste_emetteurs)):
                ind_e = liste_emetteurs[j]
                position_e = liste_cochons[ind_e].get_position()[-1]
                x = position_e[0]
                y = position_e[1]
                sexe = liste_cochons[ind_e].get()[1]
                if sexe == 1:
                    fr_sexe = 0.40
                else:
                    fr_sexe = 0.28
                    
                for i in range(len(liste_cochons)):
                    fr_age = freq_rep[ages.index(liste_cochons[i].get()[0])]
                    if i == ind_e:
                        ind_e = ind_e
                    else:
                        position_c = liste_cochons[i].get_position()[-1]
                        x1 = position_c[0]
                        y1 = position_c[1]
                        
                        if x-1 <= x1 < x+2 and y-1 <= y < y+2:
                            fr_dist = 0.65
                            if random() < fr_sexe * fr_age * fr_dist:
                                if len(liste_cochons[i].get_baillement()) > 0:
                                    if t-liste_cochons[i].get_baillement()[-1] >= 3:
                                        liste_cochons[i].nv_baillement(t+1)
                                else:
                                    liste_cochons[i].nv_baillement(t+1)
                                    
                        elif x1 < x - 20 or y1 < x - 20 or x1 >= x + 20 or y1 >= y + 20:
                            fr_dist = 0.25
                            if random() < fr_sexe * fr_age * fr_dist:
                                if len(liste_cochons[i].get_baillement()) > 0:
                                    if t-liste_cochons[i].get_baillement()[-1] >= 3:
                                        liste_cochons[i].nv_baillement(t+1)
                                else:
                                    liste_cochons[i].nv_baillement(t+1)

                        else:
                            fr_dist = 0.20
                            if random() < fr_sexe * fr_age * fr_dist:
                                if len(liste_cochons[i].get_baillement()) > 0:
                                    if t-liste_cochons[i].get_baillement()[-1] >= 3:
                                        liste_cochons[i].nv_baillement(t+1)
                                else:
                                    liste_cochons[i].nv_baillement(t+1)
        t+=1

        deplacement()

        baillement()   

## Graphique 

def grille_de_repartition(n): 
    """ constitution de la grille dans laquelle seront situés les cochons
        une unité = 0.5m """
    end = len(liste_cochons)
    a= 0
    for i in range(n):
        for j in range(n):
            if random() < 0.2 and a < end:
                cochon = liste_cochons[a]
                if cochon.get()[1] == 2:
                    canvas.create_oval(i*30, j*30, (i*30)+30, (j*30)+30, fill='yellow')
                    cochon.position(i,j)
                    a += 1
                else:
                    canvas.create_oval(i*30, j*30, (i*30)+30, (j*30)+30, fill='red')
                    cochon.position(i,j)
                    a += 1
                    
def couleur(event):
    global k 
    
    touche = event.keysym
    if touche == 'Right':
        canvas.delete('all')
        for i in range(len(liste_cochons)):
            x = liste_cochons[i].get_position()[k][0]
            y = liste_cochons[i].get_position()[k][1]
            if len(liste_cochons[i].get_baillement()) > 0:
                if k in liste_cochons[i].get_baillement():
                    canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='blue')
                elif k-1 in liste_cochons[i].get_baillement():
                    canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='green')
                elif k-2 in liste_cochons[i].get_baillement():
                    canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='green')
                elif k-3 in liste_cochons[i].get_baillement(): 
                    canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='green')
                else:
                    if liste_cochons[i].get()[1] == 2:
                        canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='yellow')    
                    else:
                        canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='red')
            elif len(liste_cochons[i].get_baillement()) == 0:
                if liste_cochons[i].get()[1] == 2:
                    canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='yellow')    
                else:
                    canvas.create_oval(x*30, y*30, (x*30)+30, (y*30)+30, fill='red')
    k=k+1

## Programme principal

## Importation des donnees

ages = []
freq_rep = []

donnees = xlrd.open_workbook("donnees.xlsx")
frequences = donnees.sheet_by_index(0)
for i in range (1, frequences.nrows):
    ages.append(int(frequences.cell_value(rowx = i, colx= 0)))
    freq_rep.append(frequences.cell_value(rowx = i, colx= 1))

## Déclaration des variables

global T,t,k
n = 20
T = 50
t = 0
k = 0

## Création de l'interface graphique

fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, width = n*30, height= n*30, bg="white")
canvas.pack()

## Constitution du groupe de cochons 

liste_cochons = []
for i in range(30):
    if random() < 0.5:
        liste_cochons.append(Cochon((randint(9,23)),1))
    else:
        liste_cochons.append(Cochon((randint(9,23)),2))

grille_de_repartition(n)
baillement()

## Récupération des données

baillements = {}
for i in range(len(liste_cochons)):
    if (len(liste_cochons[i].get_baillement())) > 0:
        for j in range(len(liste_cochons[i].get_baillement())):
            if liste_cochons[i].get_baillement()[j] in baillements.keys():
                baillements[liste_cochons[i].get_baillement()[j]] += 1
            else:
                baillements[liste_cochons[i].get_baillement()[j]] = 1
                
bar(baillements.keys(), baillements.values(), width = 0.4, color = 'b')
savefig('graph.png')

# def graphique(): 

# fenetre1 = tk.Tk()
# fenetre1.title('Histogramme')
# histo = ImageTk.PhotoImage(file = "graph.png")
# print(histo)
# can1 = tk.Canvas(fenetre1, width = 800, height = 300)
# #g = tk.Label(fenetre1, image = histo)
# can1.pack()
# graph = can1.create_image(0,0, image = histo)
# fenetre1.update()
# fenetre1.mainloop()


with open('document.csv', 'a') as document:
    for keys, values in baillements.items():
        document.write(str(keys) + ';' + str(values) + '\n')
    document.write('stop' + '\n')


canvas.focus_set()
canvas.bind("<Key>", couleur)

## Mise en forme de la fenetre

fenetre.title('Modele transmission baillements')

menubar = tk.Menu(fenetre)

menu1 = tk.Menu(menubar, tearoff=0)
#menu1.add_command(label="Paramètres")
#menu1.add_command(label="Graphique",command=graphique)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.destroy)
menubar.add_cascade(label="Action", menu=menu1)

fenetre.config(menu=menubar)

fenetre.mainloop()
