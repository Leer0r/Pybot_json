#!/usr/bin/python3.7
# -*- coding: utf-8 -*-

import os,json,shutil

class JSON_MASTER():
    def __init__(self):
        self.current_path = ""
        self.current_json = ""
        self.current_name = ""
        self.current_familyname = ""

    ###########################NOUVELLE PERSONNE###########################################

    def nouvelle_personne(self,booleen):
        """
        Va créer un nouveau dossier de la forme <nom_prenom> avec un fichier data.json a l'interrieur
        @param : booleen -> True si on appelle la fonction en ayant le nom et le prenon, False sinon

        """
        tmp_current_familyname = self.current_familyname
        temp_current_name = self.current_name

        if not booleen:
            self.current_familyname = input("Quel est le nom de la personne ? : ").lower()
            self.current_name = input("Quel est le prénom de la personne ? : ").lower()
        if os.path.exists("data/" + self.current_familyname + "_" + self.current_name): #Si la personne a déjà un dossier
            print("Erreur, cette personne est déjà inscrite dans la base de donée")
            return 
        self.current_path = "data/"+self.current_familyname + "_" + self.current_name
        os.mkdir(self.current_path)

        with open("data/template.json","r") as template: #on ouvre le template et on le stoque sous forme de dictionnaire
            self.current_json = json.load(template)
            self.current_json["nom"] = self.current_familyname
            self.current_json["prenom"] = self.current_name

        with open(self.current_path+"/data.json","w") as current_file: #on crée un nouveau fichier data pour la personne et on met les info basiques dedans
            current_file.write(json.dumps(self.current_json,sort_keys=True, indent=4))
        
        print("Le dossier à été crée")
        if not booleen:
            choix = input("Voulez vous continuez a éditer ce dossier ?(y pour confirmer) : ")
            if choix != "y":
                self.current_name = temp_current_name
                self.current_familyname = tmp_current_familyname
        else : 
            self.current_path = ""

    #########################################################################################
    #################################SUPPRIMER PERSONNE######################################
    
    def supprimer_personne(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        if not os.path.exists("data/" + self.current_familyname + "_" + self.current_name): #Si la personne a déjà été supprimée
            print("Erreur,la personne n'existe pas ou a déja été éffacée")
            return 2
        
        choix = input("Cette action va supprimer toutes les donnée de la personne suivante : " + self.current_familyname + " " + self.current_name + ", tappez y pour confirmer : ")
        if choix != "y":
            self.print_current("Action annulée")
            return
        shutil.rmtree(self.current_path)
        self.current_familyname = ""
        self.current_name = ""
        self.current_path = ""
    
    #########################################################################################
    ###############################Fixer la cible############################################

    def cible(self):
        if self.verifier_current():
            print("Le repertoire courrant va etre changer")
        print("Liste des dossiers : ",end = "")
        self.afficher_dossier_data_general()
        tmp_current_familyname = input("Quel est le nom de la personne a définir comme reperoire courrant ? : ").lower()
        print("Liste des choix : ",end = "")
        self.afficher_dossier_data_specif(tmp_current_familyname)
        tmp_current_name = input("Quel est le prenom de la personne a définir comme reperoire courrant ? : ").lower()
        if not os.path.exists("data/" + tmp_current_familyname + "_" + tmp_current_name):
            choix = self.input_current("La personne n'a pas de dossier, voulez vous en créer un ? : (y pour valider)")
            if choix == "y":
                self.current_name = tmp_current_name
                self.current_familyname = tmp_current_familyname
                self.nouvelle_personne(True)
            else:
                print("Abandon")
                return
        else :
            self.current_name = tmp_current_name
            self.current_familyname = tmp_current_familyname
        self.current_path = "data/"+self.current_familyname + "_" + self.current_name 
        print("Le répertoire courrant est maintenant sur la personne nommée " + self.current_familyname + " " + self.current_name)
        
    #########################################################################################
    ################################Lire les donnée de la cible##############################
    
    def lire_donnee(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        with open(self.current_path+"/data.json") as fichier:
            self.current_json = json.load(fichier)
            print("Les donnée ont bien été chargée \n")
        for caract in self.current_json:
            if self.current_json[caract] != "":
                print(caract + " -> " + self.current_json[caract])
        print()
        

    ##########################################################################################

    def verifier_current(self):
        if self.current_name == "" or self.current_familyname == "" or self.current_path == "":
            return False
        return True

    def print_current(self,txt):
        if self.verifier_current():
            print("[" + self.current_name + " " + self.current_familyname + "]" + " " + txt)
        else:
            print("[Vide]" + " " + txt)
    
    def input_current(self,txt):
        if self.verifier_current():
            choix = input("[" + self.current_name + " " + self.current_familyname + "]" + " " + txt)
        else:
            choix = input("[Vide]" + " " + txt)
        return choix
    
    def afficher_dossier_data_general(self):
        for i in os.listdir("data/"):
            if i != "template.json":
                print(i,end="    ")
        print()

    def afficher_dossier_data_specif(self,nom):
        for i in os.listdir("data/"):
            if i != "template.json" and nom in i:
                print(i,end="    ")
        print()


class MAIN(JSON_MASTER):
    def __init__(self):
        self.arret = False
        JSON_MASTER.__init__(self)
        if not os.path.exists("data"):
            os.mkdir("data")

    def decision(self,str_decision):
        if str_decision == "ajoute une nouvelle personne":
            self.nouvelle_personne(False)
        elif str_decision == "supprime cette personne":
            self.supprimer_personne()
        elif str_decision == "cible une personne":
            self.cible()
        elif str_decision == "donne moi les informations":
            self.lire_donnee()
        else:
            print("Désolé, je ne connais pas cette fonction....")

    def mainfonction(self):
        while(not self.arret):
            choix = self.input_current("Que voulez vous faire ? : ")
            choix = choix.lower()
            if choix == "stop":
                self.arret = True
            else:
                self.decision(choix)
        print("Au revoir")



Lilian = MAIN()
Lilian.__init__()

Lilian.mainfonction()