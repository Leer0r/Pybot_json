#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import shutil
import copy
from sty import fg, bg, ef, rs, RgbFg, Style

class CUSTOM():
    def __init__(self):
        fg.orange = Style(RgbFg(255, 150, 50))

        #######Help_Crochet###########
        self.couleur_help_crochet = fg.orange
        self.bg_help_crochet = ""
        self.end_couleur_help_crochet = fg.rs
        self.end_bg_help_crochet = ""

        ########Help_Crochet##########
        self.couleur_help = fg.da_green
        self.bg_help = ""
        self.end_couleur_help = fg.rs
        self.end_bg_help = ""

        ########Error#################
        self.couleur_error = fg.red
        self.bg_error = ""
        self.end_couleur_error = fg.rs
        self.end_bg_error = ""

        ########Info##################
        self.couleur_info = ""
        self.bg_info = bg.li_green
        self.end_couleur_info = ""
        self.end_bg_info = bg.rs

    def personalisation(self):
        pass


class JSON_MASTER(CUSTOM):
    def __init__(self):
        CUSTOM.__init__(self)
        self.current_json_path = ""
        self.current_json = ""
        self.current_name = ""
        self.current_familyname = ""
        self.current_path = ""
        self.phase = "alpha"
        self.version = "0.0.6"
        self.dict_fonction = {
            1: "ajoute une nouvelle personne",
            2: "supprime cette personne",
            3: "cible une personne",
            4: "donne moi les informations",
            5: "édite les informations",
            6: "supprime toutes les données",
            7: "personalise l'interface",
            "h": "h",
            "stop": "stop"
        }
        self.dict_explication = {
            1: "Ajouter une nouvelle personne dans la base de donnée",
            2: "Supprimer une personne de la base de donnée",
            3: "Cibler une personne dans la base de donnée (la crée si elle n'existe pas)",
            4: "Donne les informations stocké de la personne précédement ciblée",
            5: "Edite les informations stocké de la personne précédement ciblée",
            6: "Supprime toutes les données stockées",
            7: "Personnalisation de l'interface"
            "stop": "Arrete le programme"
        }

    ###########################NOUVELLE PERSONNE###########################################

    def nouvelle_personne(self, booleen):
        """
        Va créer un nouveau dossier de la forme <nom_prenom> avec un fichier data.json a l'interrieur
        @param : booleen -> True si on appelle la fonction en ayant le nom et le prenon, False sinon

        """
        tmp_current_familyname = self.current_familyname
        temp_current_name = self.current_name

        if not booleen:
            self.current_familyname = input(
                "Quel est le nom de la personne ? : ").lower()
            self.current_name = input(
                "Quel est le prénom de la personne ? : ").lower()
        # Si la personne a déjà un dossier
        if os.path.exists("data/" + self.current_familyname + "_" + self.current_name):
            print("Erreur, cette personne est déjà inscrite dans la base de donée")
            return
        self.current_json_path = "data/"+self.current_familyname + "_" + self.current_name
        os.mkdir(self.current_json_path)

        # on ouvre le template et on le stoque sous forme de dictionnaire
        with open("data/template.json", "r") as template:
            self.current_json = json.load(template)
            self.current_json["nom"] = self.current_familyname
            self.current_json["prenom"] = self.current_name

        # on crée un nouveau fichier data pour la personne et on met les info basiques dedans
        with open(self.current_json_path+"/data.json", "w") as current_file:
            current_file.write(json.dumps(
                self.current_json, sort_keys=True, indent=4))

        print("Le dossier à été crée")
        if not booleen:
            choix = input(
                "Voulez vous continuez a éditer ce dossier ?(y pour confirmer) : ")
            if choix != "y":
                self.current_name = temp_current_name
                self.current_familyname = tmp_current_familyname
        else:
            self.current_json_path = ""

    #########################################################################################
    #################################SUPPRIMER PERSONNE######################################

    def supprimer_personne(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        # Si la personne a déjà été supprimée
        if not os.path.exists("data/" + self.current_familyname + "_" + self.current_name):
            print("Erreur,la personne n'existe pas ou a déja été éffacée")
            return 2

        choix = input("Cette action va supprimer toutes les donnée de la personne suivante : " +
                      self.current_familyname + " " + self.current_name + ", tappez y pour confirmer : ")
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
        if len(os.listdir("data/")) == 2:
            liste = os.listdir("data/")
            liste.remove("template.json")
            choix = self.input_current(
                "Il n'y a qu'un seul répertoire, celui de %s \nVoulez vous le cibler ?(y pour valider) " % (liste[0]))
            if choix == "y":
                personne = liste[0].split("_")
                self.current_familyname = personne[0]
                self.current_name = personne[1]
                self.current_json_path = "data/"+self.current_familyname + "_" + self.current_name
                with open(self.current_json_path+"/data.json", "r") as fichier:
                    self.current_json = json.load(fichier)
                print("Les donnée ont bien été chargée \n")
                print("Le répertoire courrant est maintenant sur la personne nommée " +
                    self.current_familyname + " " + self.current_name)
                return
        print("Liste des dossiers : ", end="")
        self.afficher_dossier_data_general()
        tmp_current_familyname = input(
            "Quel est le nom de la personne a définir comme reperoire courrant ? : ").lower()
        print("Liste des choix : ", end="")
        if len(self.return_dossier_data_specif(tmp_current_familyname)) == 1:
            fullname = self.return_dossier_data_specif(
                tmp_current_familyname)[0]
            self.current_familyname = tmp_current_familyname
            self.print_info("Il n'un a qu'une seule personne dans la base de donnée avec le nom {} ({}), cette personne a donc été ciblée automatiquement".format(
                self.current_familyname, fullname))
            self.current_name = self.juste_prenom(fullname)
        else:
            self.afficher_dossier_data_specif(tmp_current_familyname)
            tmp_current_name = input(
                "Quel est le prenom de la personne a définir comme reperoire courrant ? : ").lower()
            if not os.path.exists("data/" + tmp_current_familyname + "_" + tmp_current_name):
                choix = self.input_current(
                    "La personne n'a pas de dossier, voulez vous en créer un ? : (y pour valider) ")
                if choix == "y":
                    self.current_name = tmp_current_name
                    self.current_familyname = tmp_current_familyname
                    self.nouvelle_personne(True)
                else:
                    print("Abandon")
                    return
            else:
                self.current_name = tmp_current_name
                self.current_familyname = tmp_current_familyname
        self.current_json_path = "data/"+self.current_familyname + "_" + self.current_name
        with open(self.current_json_path+"/data.json", "r") as fichier:
            self.current_json = json.load(fichier)
            print("Les donnée ont bien été chargée \n")
        print("Le répertoire courrant est maintenant sur la personne nommée " +
              self.current_familyname + " " + self.current_name)

    #########################################################################################
    ################################Lire les donnée de la cible##############################

    def lire_donnee(self):
        print()
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        for caract in self.current_json:
            if self.current_json[caract] != "":
                print(caract + " -> " + str(self.current_json[caract]))
        print()
        self.wait()

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
            choix = self.input_current(
                "Hub de choix : 0 pour quitter, 1 pour editer une information déjà existante, 2 pour en créer une autre, 3 pour supprimer une information, 4 pour ajouter une annécdote : ")
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
                choix2 = self.input_current(
                    "Quel est l'information a éditer ? : ")
                if choix2 not in tab_cle:
                    self.print_current(
                        "Désolé, je ne trouve pas cette caractéristique")
                else:
                    if self.current_json[choix2] == "":
                        Nouvelle_caract = self.input_current(
                            "Quelle est la nouvelle caractéristique a attibuer ? : ")
                        self.current_json[choix2] = Nouvelle_caract
                    else:
                        choix = self.input_current("L'élément {} a déjà la caractéristique {}, voulez vous la remplacer ou la completer ? (r/c) : ".format(choix2,self.current_json[choix2]))
                        while(choix != "c" and choix != "r"):
                            self.print_error("ce n'est pas une réponse valide")
                            choix = self.input_current("L'élément {} a déjà la caractéristique {}, voulez vous la remplacer ou la completer ? (r/c) : ".format(choix2,self.current_json[choix2]))
                        if choix == "r":
                            nouv_caract = self.input_current(
                                "Quelle est la nouvelle caractéristique a attibuer ? : ")
                            choix3 = self.input_current(
                                "Attention, la caractéristique {} {} {} va etre remplacer par {} {} {} \nAppuiller sur y pour valider (autre touche pour annuler) : ".format(
                                    bg(255, 150, 50), self.current_json[choix2], bg.rs, bg.cyan, nouv_caract, bg.rs))
                            if choix3 == "y":
                                self.current_json[choix2] = nouv_caract
                                self.print_current(
                                    "La caractéristique a été changée")
                            else:
                                self.print_current("Abandon")
                        else : 
                            add_caract = self.input_current(
                                "Quelle est la caractéristique à ajouter ? : ")
                            choix3 = self.input_current(
                                "Attention, la caractéristique {} {} {} va etre remplacer par {} {} {} \nAppuiller sur y pour valider (autre touche pour annuler) : ".format(
                                    bg(255, 150, 50), self.current_json[choix2], bg.rs, bg.cyan, self.current_json[choix2] + ", " + add_caract, bg.rs))
                            if choix3 == "y":
                                self.current_json[choix2] = self.current_json[choix2] + ", " + add_caract
                                self.print_current(
                                    "La caractéristique a été changée")
                            else:
                                self.print_current("Abandon")
            elif choix == 2:
                self.print_current("Creation de l'information")
                choix = self.input_current(
                    "Quel est le nom de la catégorie a créer ? : ")
                choix2 = self.input_current(
                    "Que voulez vous mettre dans cette catégorie ? : ")
                self.current_json.update({choix: choix2})
            elif choix == 3:
                self.print_current("Suppression de l'information")
                tab_cle = [cle for cle in self.current_json]
                self.afficher_option_dict()
                choix2 = self.input_current(
                    "Quel est l'information à supprimer ? : ")
                if choix2 not in tab_cle:
                    self.print_current(
                        "Désolé, je ne trouve pas cette caractéristique")
                else:
                    del self.current_json[choix2]
                    self.print_current("L'élément à été supprimé")
            elif choix == 4:
                self.print_current("Ajout d'une annécdote")
                path = "anecdote"
                self.current_json[path]["nb"] += 1
                annecdote = self.input_current(
                    "Quel est l'anecdote à ajouter ? : \n")
                nom = self.input_current("\n\n Voulez vous lui donner un nom particulier ? Par défault ça sera %s : " % (
                    "anecdote_" + str(self.current_json[path]["nb"])))
                if nom == "":
                    nom = "anecdote" + str(self.current_json[path]["nb"])
                self.current_json[path][nom] = annecdote
                self.print_current("L'annecdote a été sauvegardée localement")
            else:
                self.print_current("Désolé, la commande est inconnue")
            if choix != 0 and choix != 2:
                self.wait()

        if json_initial != self.current_json:
            self.print_current("Des modifications ont été effectuée : ")
            self.print_current("Fichier initial : ")
            print(json.dumps(json_initial, sort_keys=True, indent=4))
            print()
            self.print_current("Fichier après modification : ")
            print(json.dumps(self.current_json, sort_keys=True, indent=4))
            print()
            choix = self.input_current(
                "Voulez vous sauvegarder ces modifications ? (y pour valider / n pour refuser) : ")
            while choix != "y" and choix != "n":
                self.print_error("ce n'est pas un choix valide")
                choix = self.input_current(
                    "Voulez vous sauvegarder ces modifications ? (y pour valider / n pour refuser) : ")
            if choix == "y":
                self.print_current(
                    "Les nouvelles donnée vont etre écrite dans le fichier...")
                with open(self.current_json_path + "/data.json", "w", encoding="utf-8") as fichier:
                    json.dump(self.current_json, fichier, indent=4)
                self.print_info("Le fichier a été mis à jours")
            else:
                self.print_info("le fichier n'a pas été mis à jours")

    ##########################################################################################
    ################################SUPPRIMER LES DONNEE######################################

    def suppr_all(self):
        choix = self.input_current(
            "Attention, vous allez supprimer toutes les données locales, tappez y pour confirmer : ")
        if choix == "y":
            for fichier in os.listdir("data/"):
                if fichier != "template.json":
                    shutil.rmtree("data/" + fichier)
            self.current_familyname = ""
            self.current_name = ""
            print("Les fichier on été supprimé")
    #########################################################################################

    def afficher_donnee(self):
        if not self.verifier_current():
            print("Veuiller cibler une personne avant cette action")
            return
        for caract in self.current_json:
            print(caract + " -> " + str(self.current_json[caract]))
        print()

    def verifier_current(self):
        if self.current_name == "" or self.current_familyname == "" or self.current_json_path == "":
            return False
        return True

    def print_current(self, txt):
        if self.verifier_path():
            print("[" + fg.red + self.current_name + " " + self.current_familyname + fg.rs +
                  "] " + "(" + self.current_path + ") " + txt)
        else:
            if self.verifier_current():
                print("[" + fg.red + self.current_name + " " +
                      self.current_familyname + fg.rs + "] " + txt)
            else:
                print("[Vide] " + txt)

    def print_error(self, txt):
        print("\n {}{}Erreur : {}{}{}".format(self.bg_error,self.couleur_error,txt,self.end_couleur_error,self.end_bg_error))

    def print_info(self, txt):
        print("\n{}{}INFO : {}{}{}".format(self.bg_info,self.couleur_help,txt,self.end_couleur_info,self.end_bg_info))

    def input_current(self, txt):
        if self.verifier_current():
            choix = input("[" + fg.red + self.current_name + " " +
                          self.current_familyname + fg.rs + "] " + txt)
        else:
            choix = input("[Vide] " + txt)
        return choix

    def input_current_int(self, txt):
        if self.verifier_current():
            choix = int(input("[" + fg.red + self.current_name + " " +
                              self.current_familyname + fg.rs + "] " + txt))
        else:
            choix = int(input("[Vide] " + txt))
        return choix

    def verifier_path(self):
        if self.current_path != "":
            return True
        return False

    def afficher_dossier_data_general(self):
        for i in os.listdir("data/"):
            if i != "template.json":
                print(i, end="    ")
        print()

    def afficher_dossier_data_specif(self, nom):
        for i in os.listdir("data/"):
            if i != "template.json" and nom in i:
                print(i, end="    ")
        print()

    def return_dossier_data_specif(self, nom):
        data_return = []
        for i in os.listdir("data/"):
            if i != "template.json" and nom in i:
                data_return.append(i)
        return data_return

    def afficher_option_dict(self):
        for cle in self.current_json:
            print(cle, end="   ")
        print()

    def juste_prenom(self, txt):
        ecrire = False
        prenom = ""
        for i in txt:
            if ecrire:
                prenom += i
            elif i == "_":
                ecrire = True
        return prenom

    def wait(self):
        input("Appuyez sur la touche ENTREE pour continuer...")


class MAIN(JSON_MASTER):
    def __init__(self):
        self.arret = False
        JSON_MASTER.__init__(self)
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/template.json"):
            with open("data/template.json","w") as template:
                template.write("""{
    "nom":"",
    "prenom":"",
    "age":"",
    "interet":"",
    "autre":"",
    "anecdote":{
        "nb":0
    }
}""")


    def lire_fichier(self, f):
        with open(f, "r") as fichier:
            fichier_str = fichier.read()
        return fichier_str

    def split_str(self, txt):
        dict_option = {}
        compt = 1
        for i in range(len(txt)):
            if txt[i] == "@":
                param = ""
                arg = ""
                # On prend le paramètre
                while txt[i] != " " and txt[i] != "\n":
                    param += txt[i]
                    i += 1
                if "@begin:" in param:
                    param = param.replace("@begin:", "")
                    save_param = param
                    while txt[i] != "@":
                        arg += txt[i]
                        i += 1
                    dict_option[param] = arg
                    param = ""
                    while i < len(txt) and txt[i] != " " and txt[i] != "\n":
                        param += txt[i]
                        i += 1
                    if "@end:" + save_param not in param:
                        print("Attention, la balise d'entrée se nome {} alors que la balise de sortie de somme {}, veuiller corriger ce problème".format(
                            save_param, param))
                elif "@end:" in param:
                    continue
                else:
                    i += 3
                    while i < len(txt) and txt[i] != "\n":
                        arg += txt[i]
                        i += 1
                    if "|" in arg:
                        arg = arg.split("|")
                    dict_option[param.replace('@', '')] = arg
                compt += 1
        return dict_option

    def aide(self):
        print("Voici comment utiliser les fonctions : ")

    def print_dict(self, dico):
        for key in dico:
            print(str(key) + " --> " + dico[key])

    def aide_plus(self):
        os.system("clear")
        print("Voici la liste des fonctions qui possède un fichier aide : ")
        liste_choix = []
        for fichier in os.listdir("help/"):
            print(fg.da_green + fichier.replace(".help", "") + fg.rs)
            liste_choix.append(fichier.replace(".help", ""))
        choix = self.input_current(
            "Quel est la fonction qui nécéssite de l'aide ? [q pour quitter] : ")
        while choix not in liste_choix and choix != "q":
            print("Désolé, cette fonction n'existe pas...")
            choix = self.input_current(
                "Quel est la fonction qui nécéssite de l'aide ? [q pour quitter] : ")
        if choix == "q":
            return
        txt_aide = self.lire_fichier("help/" + choix + ".help")
        dict_option = self.split_str(txt_aide)
        for key in dict_option:
            print(key + " -> " + str(dict_option[key]) + "\n")
        self.wait()

    def decision(self, str_decision):
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
        elif str_decision == "supprime toutes les données":
            self.suppr_all()
        elif str_decision == "personalise l'interface":
            self.personalisation()
        else:
            print("Désolé, je ne connais pas cette fonction....")

    def mainfonction(self):
        while(not self.arret):
            print("\n{}{}[{}{}{}{}h pour avoir accès a la rubrique d'aide{}{}{}{}]{}{}".format(self.bg_help_crochet,self.couleur_help_crochet,self.end_couleur_help_crochet,self.end_bg_help_crochet,self.bg_help,self.couleur_help,self.end_couleur_help,self.end_bg_help,self.bg_help_crochet,self.couleur_help_crochet,self.end_couleur_help_crochet,self.end_bg_help_crochet))
            self.print_dict(self.dict_explication)
            try:
                choix = self.input_current("Que voulez vous faire ? : ")
                if choix == "stop":
                    self.arret = True
                elif choix == "h":
                    self.aide_plus()
                else:
                    choix = self.dict_fonction[int(choix)]
                    self.decision(choix)
            except KeyError:
                self.print_error("ce n'est pas un indice valide de fonction")
            except ValueError:
                self.print_error("le nombre entré n'est pas valide")
            except:
                self.print_error("Abandon. Retour au menu")
        print(ef.b + "Au revoir" + rs.bold_dim)

########################################################################################################################################


Lilian = MAIN()
Lilian.__init__()

Lilian.mainfonction()
