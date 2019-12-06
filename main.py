#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os,json,shutil,copy

class JSON_MASTER():
    def __init__(self):
        self.current_json_path = ""
        self.current_json = ""
        self.current_name = ""
        self.current_familyname = ""
        self.current_path = ""

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
        self.current_json_path = "data/"+self.current_familyname + "_" + self.current_name
        os.mkdir(self.current_json_path)

        with open("data/template.json","r") as template: #on ouvre le template et on le stoque sous forme de dictionnaire
            self.current_json = json.load(template)
            self.current_json["nom"] = self.current_familyname
            self.current_json["prenom"] = self.current_name

        with open(self.current_json_path+"/data.json","w") as current_file: #on crée un nouveau fichier data pour la personne et on met les info basiques dedans
            current_file.write(json.dumps(self.current_json,sort_keys=True, indent=4))

        print("Le dossier à été crée")
        if not booleen:
            choix = input("Voulez vous continuez a éditer ce dossier ?(y pour confirmer) : ")
            if choix != "y":
                self.current_name = temp_current_name
                self.current_familyname = tmp_current_familyname
        else :
            self.current_json_path = ""

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
        shutil.rmtree(self.current_json_path)
        self.current_familyname = ""
        self.current_name = ""
        self.current_json_path = ""

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
        self.current_json_path = "data/"+self.current_familyname + "_" + self.current_name
        with open(self.current_json_path+"/data.json","r") as fichier:
            self.current_json = json.load(fichier)
            print("Les donnée ont bien été chargée \n")
        print("Le répertoire courrant est maintenant sur la personne nommée " + self.current_familyname + " " + self.current_name)

    #########################################################################################
    ################################Lire les donnée de la cible##############################

    def lire_donnee(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        for caract in self.current_json:
            if self.current_json[caract] != "":
                print(caract + " -> " + self.current_json[caract])
        print()


    ##########################################################################################
    #################################Editer les donnée de la cible############################

    def editer_donnee(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        json_initial = {}
        json_initial = copy.deepcopy(self.current_json)
        stop2 = False
        while not stop2:
            os.system("clear")
            self.afficher_donnee()
            self.print_current("Edition des informations")
            self.print_current("________________________")
            choix = self.input_current("Hub de choix : 0 pour quitter, 1 pour editer une information déjà existante, 2 pour en créer une autre, 3 pour supprimer une information : ")
            try:
                choix = int(choix)
            except:
                print("Ce n'est pas un option valide")
                return
            if choix == 0:
                print("Arret de l'édition, retour au menu principal")
                stop2 = True
            elif choix == 1:
                self.print_current("Edition d'une information")
                tab_cle = [cle for cle in self.current_json]
                self.afficher_option_dict()
                choix2 = self.input_current("Quel est l'information a éditer ? : ")
                if choix2 not in tab_cle:
                    self.print_current("Désolé, je ne trouve pas cette caractéristique")
                else:
                    Nouvelle_caract = self.input_current("Quelle est la nouvelle caractéristique a attibuer ? : ")
                    if self.current_json[choix2] != "":
                        choix3 = self.input_current("Attention, la caractéristique " + self.current_json[choix2] + " va etre remplacer par " + Nouvelle_caract + " appuiller sur y pour valider : ")
                        if choix3 == "y":
                            self.current_json[choix2] = Nouvelle_caract
                            self.print_current("La caractéristique a été changée")
                        else:
                            self.print_current("Abandon")
                    self.current_json[choix2] = Nouvelle_caract
                    self.print_current("La caractéristique a été changée")
            elif choix == 2:
                self.print_current("Creation de l'information")
                choix = self.input_current("Quel est le nom de la catégorie a créer ? : ")
                choix2 =self.input_current("Que voulez vous mettre dans cette catégorie ? : ")
                self.current_json.update({choix:choix2})
            elif choix == 3:
                self.print_current("Suppression de l'information")
                tab_cle = [cle for cle in self.current_json]
                self.afficher_option_dict()
                choix2 = self.input_current("Quel est l'information à supprimer ? : ")
                if choix2 not in tab_cle:
                    self.print_current("Désolé, je ne trouve pas cette caractéristique")
                else:
                    del self.current_json[choix2]
                    self.print_current("L'élément à été supprimé")
                

            else :
                self.print_current("Désolé, la commande est inconnue")

        if json_initial != self.current_json:
            self.print_current("Des modifications ont été effectuée : ")
            self.print_current("Fichier initial : ")
            print(json.dumps(json_initial,sort_keys=True, indent=4))
            print()
            self.print_current("Fichier après modification : ")
            print(json.dumps(self.current_json,sort_keys=True, indent=4))
            print()
            choix = self.input_current("Voulez vous sauvegarder ces modifications ? (y pour valider) : ")
            if choix == "y":
                self.print_current("Les nouvelles donnée vont etre écrite dans le fichier...")
                with open(self.current_json_path + "/data.json","w",encoding="utf-8") as fichier:
                    json.dump(self.current_json,fichier,indent=4)
                print("Le fichier a été mis a jours")
                


    ##########################################################################################

    def afficher_donnee(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        for caract in self.current_json:
            print(caract + " -> " + self.current_json[caract])
        print()

    def verifier_current(self):
        if self.current_name == "" or self.current_familyname == "" or self.current_json_path == "":
            return False
        return True

    def print_current(self,txt):
        if self.verifier_path():
            print("[" + self.current_name + " " + self.current_familyname + "] "+ "(" + self.current_path + ") " + txt)
        else:
            if self.verifier_current():
                print("[" + self.current_name + " " + self.current_familyname + "] "+ txt)
            else:
                print("[Vide] " + txt)

    def input_current(self,txt):
        if self.verifier_current():
            choix = input("[" + self.current_name + " " + self.current_familyname + "] " + txt)
        else:
            choix = input("[Vide] " + txt)
        return choix

    def verifier_path(self):
        if self.current_path != "":
            return True
        return False

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

    def afficher_option_dict(self):
        for cle in self.current_json:
            print(cle,end = "   ")
        print()

    def aide(self):
        self.print_current("Bienvenu sur la rubrique d'aide. Ici est listé toutes les fonctionnalitée avec des exemples et des conseils d'utilisation")


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
        elif str_decision == "édite les informations":
            self.editer_donnee()
        elif str_decision == "h":
            pass
        else:
            print("Désolé, je ne connais pas cette fonction....")

    def mainfonction(self):
        while(not self.arret):
            print("[h pour avoir accès a la rubrique d'aide]")
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