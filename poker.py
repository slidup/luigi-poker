import time
import pygame, sys, os
from random import *

def resource_path(relative_path):
    """Obtenir le chemin absolu d'une ressource (fonctionne pour l'exécutable et en mode développement)"""
    try:
        # PyInstaller crée un dossier temporaire et y place l'exécutable
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def mettre_la_musique():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    musiques = ["card_party.mp3", "casino.mp3", "big_shot_jazz_remix.mp3","bingo.mp3","bowser_jr.mp3"]
    choix = randint(0,4)
    musique = "musique/" +  musiques[choix]
    pygame.mixer.music.load(resource_path(musique))
    if choix == 3:
        pygame.mixer.music.play(-1,9.45)
    else:
        pygame.mixer.music.play(-1)

def trouver_gagnant(j1, j2):
    if j1[-1] > j2[-1]:
        return 1
    elif j1[-1] < j2[-1]:
        return 2
    elif j1[-1] == j2[-1]:
        if j1[0] != "double paire" and j1[0] != "full":
            if j1[1] < j2[1]:
                return 1
            elif j1[1] > j2[1]:
                return 2
            elif j1[1] == j2[1]:
                return 3
        elif j1[0] == "double paire" or j1[0] == "full":
            if j1[1] < j2[1]:
                return 1
            elif j1[1] > j2[1]:
                return 2
            elif j1[1] == j2[1]:
                if j1[2] < j2[2]:
                    return 1
                elif j1[2] > j2[2]:
                    return 2
                elif j1[2] == j2[2]:
                    return 3

def multiplicateur(gagnant, mise):
    if gagnant[-1] == 0:
        return 1
    elif gagnant[-1] == 1:
        return 2
    elif gagnant[-1] == 2:
        return 3
    elif gagnant[-1] == 3:
        return 4
    elif gagnant[-1] == 4:
        return 6
    elif gagnant[-1] == 5:
        return  8
    elif gagnant[-1] == 6:
        return 16

class Carte():
    def __init__(self, valeur, symbole):
        self.symbole = symbole
        self.valeur = valeur
        self.state = False
        return
    
    def obtenir_valeur(self):
        return self.valeur

    def obtenir_symbole(self):
        return self.symbole
    
    def afficher_carte(self):
        print("{}".format(self.symbole))

class JeuDe30Cartes():
    def __init__(self):
        self.paquet = []
        for i in range(0, 5):
            for valeur, symbole in enumerate(["etoile", "mario", "luigi", "fleur de feu", "champigon", "nuage"]):
                self.paquet.append(Carte(valeur+1, symbole))
        return
    
    def melanger(self):
        shuffle(self.paquet)
        return
    
    def prendre_carte(self):
        choix = randint(0, len(self.paquet) - 1)
        return self.paquet.pop(choix)
    
    def remettre_carte(self, carte):
        self.paquet.append(carte)

    def nombre_cartes(self):
        return len(self.paquet)
    
    def refaire_paquet(self):
        self.paquet = []
        for i in range(0, 5):
            for valeur, symbole in enumerate(["etoile", "mario", "luigi", "fleur de feu", "champigon", "nuage"]):
                self.paquet.append(Carte(valeur+1, symbole))
        return

class Joueur():
    def __init__(self):
        self.pieces = 10
        self.jeu_en_main = []
        self.etoile = 0
    
    def effacer_jeu(self):
        self.jeu_en_main = []

    def attribuer_carte(self,carte,num):
        self.jeu_en_main.insert(num,carte)
        return 
    
    def afficher_jeu(self):
        for carte in self.jeu_en_main:
            carte.afficher_carte()
    
    def trier_jeu(self):
        self.jeu_en_main = sorted(self.jeu_en_main, key=lambda carte: carte.valeur)
        paire = []
        for k in range(4,0,-1):
            if self.jeu_en_main[k].obtenir_symbole() == self.jeu_en_main[k-1].obtenir_symbole():
                paire.append(self.jeu_en_main[k])
                if k != 1:
                    if self.jeu_en_main[k-1].obtenir_symbole() != self.jeu_en_main[k-2].obtenir_symbole():
                        paire.append(self.jeu_en_main[k-1])
                else:
                    paire.append(self.jeu_en_main[k-1])
        for carte in paire:
            self.jeu_en_main.remove(carte)
            self.jeu_en_main.insert(0,carte)

    def changer_carte(self, num):
        carte = self.jeu_en_main.pop(num)
        return carte
    
    def calculer_main(self):
        i = 0
        for k in range(4):
            if self.jeu_en_main[k].obtenir_symbole() == self.jeu_en_main[k+1].obtenir_symbole():
                i += 1
        if i == 0:
            return ["pas de main", self.jeu_en_main[0].obtenir_valeur(), 0]
        if i == 1:
            return ["paire", self.jeu_en_main[0].obtenir_valeur(), 1]
        if i == 2:
            if self.jeu_en_main[0].obtenir_symbole() == self.jeu_en_main[1].obtenir_symbole() and self.jeu_en_main[1].obtenir_symbole() == self.jeu_en_main[2].obtenir_symbole():
                return ["brelan", self.jeu_en_main[0].obtenir_valeur(), 3]
            else:
                return ["double paire", self.jeu_en_main[0].obtenir_valeur(), self.jeu_en_main[2].obtenir_valeur(), 2]
        if i == 3:
            if self.jeu_en_main[0].obtenir_symbole() == self.jeu_en_main[3].obtenir_symbole():
                return ["carré", self.jeu_en_main[0].obtenir_valeur(), 5]
            else:
                return ["full", self.jeu_en_main[0].obtenir_valeur(), self.jeu_en_main[3].obtenir_valeur(), 4]
        if i == 4:
            return ["flush", self.jeu_en_main[0].obtenir_valeur(), 6]

    def ajouter_pieces(self, nb_pieces):
        self.pieces += nb_pieces

    def ajouter_etoile(self):
        self.etoile += 1
    
    def retirer_etoile(self):
        self.etoile -= 1

    def obtenir_etoile(self):
        return self.etoile
    
    def obtenir_pieces(self):
        return self.pieces
    
class Partie():
    def __init__(self):
        self.jeu = JeuDe30Cartes()
        self.joueur = Joueur()
        self.banque = Joueur()
        
    def jouer(self):
        mettre_la_musique()
        continu = True
        while continu == True:
            nb_partie = int(input("combien de partie ? "))
            print("")
            print("vous avez {} pieces".format(self.joueur.obtenir_pieces()))
            for i in range(nb_partie):
                self.jeu.refaire_paquet()
                self.jeu.melanger()
                self.joueur.effacer_jeu()
                self.banque.effacer_jeu()
                for i in range(5):
                    self.joueur.attribuer_carte(self.jeu.prendre_carte(),-1)
                    self.banque.attribuer_carte(self.jeu.prendre_carte(),-1)
                mise = 0
                print("")
                while (mise > self.joueur.obtenir_pieces()) or (mise >= 6) or (mise == 0):
                    mise = int(input("quelle mise (entre 1 et 5) ? "))
                print("la mise est de",mise)
                print("")
                self.joueur.ajouter_pieces(-(mise))
                time.sleep(1)
                print("Votre jeu:")
                self.joueur.afficher_jeu()
                print("")
                num = int(input("quelle carte changer(une par une et 0 pour finir) "))
                while num != 0:
                    carte_prise = self.joueur.changer_carte(num-1)
                    self.joueur.attribuer_carte(self.jeu.prendre_carte(),num-1)
                    self.jeu.remettre_carte(carte_prise)
                    num = int(input("quelle carte changer(une par une et 0 pour finir) "))
                self.joueur.trier_jeu()
                self.banque.trier_jeu()
                print("")
                time.sleep(1)
                print("votre jeu:")
                self.joueur.afficher_jeu()
                print("")
                print("jeu de luigi:")
                self.banque.afficher_jeu()
                print("")
                time.sleep(6)
                jeu_joueur = self.joueur.calculer_main()
                jeu_banque = self.banque.calculer_main()
                gagnant = trouver_gagnant(jeu_joueur, jeu_banque)
                if gagnant == 1:
                    print("le gagnant est le joueur avec",jeu_joueur[0])
                    self.joueur.ajouter_etoile()
                    multipli = multiplicateur(jeu_joueur,mise)
                    self.joueur.ajouter_pieces(multipli*mise)
                    print("vous avez gagné",mise,"X",multipli,", soit", mise * multipli,"pièces")
                    print("vous avez gagné une étoile")
                elif gagnant == 2:
                    print("le gagnant est luigi avec",jeu_banque[0])
                    self.joueur.retirer_etoile()
                    print("vous avez perdu",mise,"pièces et une étoile")
                    pygame.mixer.music.pause()
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('musique/luigi.mp3'), 1)
                    time.sleep(3.5)
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.unpause()
                elif gagnant == 3:
                    print("égalité")
                    self.joueur.ajouter_pieces(mise)
                print("vous avez {} etoiles".format(self.joueur.obtenir_etoile()))
                if self.joueur.obtenir_pieces() <= 0:
                    print("plus de pieces perdu!!!")
                    return
                print("vous avez {} pieces".format(self.joueur.obtenir_pieces()))
            continu = bool(input("continuer (oui ou non) ? ") == "oui")

#jeu = Partie()
#jeu.jouer()