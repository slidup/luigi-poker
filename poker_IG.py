import time
import sys, pygame
from random import *
from PIL import Image
from poker import *
import os

pygame.init()
screen = pygame.display.set_mode((1000,600))#pygame.RESIZABLE  
screen.fill((0,0,0))
size = width, height = screen.get_size()
clock = pygame.time.Clock()

def load_and_resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size)
    image.save(path)
    return pygame.image.load(path)

background = load_and_resize_image("img/poker_background.png", (width, height))
piece_surf = load_and_resize_image("img/piece.png", (45, 45))
etoile_surf = load_and_resize_image("img/etoile_icon.png", (75, 75))

text_font = pygame.font.Font(None,50)
piece_font = pygame.font.Font(None,75)
classement_carte_surf = load_and_resize_image("img/classement_carte.png",(round(width/16.67),round(height/2.061)))
classement_carte_rect = classement_carte_surf.get_rect(center = (width-50,height/2))
combinaisons_carte_surf = load_and_resize_image("img/combinaisons.jpg",(round(width/8.333),round(height/2.715)))
combinaisons_carte_rect = classement_carte_surf.get_rect(bottomleft = (10,height+50))
text_win_surf = pygame.image.load("img/gagne.png")
text_win_rect = text_win_surf.get_rect(center= ((width/2+30),height/2-10))
text_loose_surf = pygame.image.load("img/game_over.png")
text_loose_rect = text_win_surf.get_rect(center= ((width/2+30),height/2-10))
text_egalite_surf = text_font.render("égalité", False, "Blue")
text_egalite_rect = text_egalite_surf.get_rect(center = ((width/2+30),height/2-10))
text_draw_surf = text_font.render("DRAW", False, "Blue")
text_draw_rect = text_draw_surf.get_rect(center = ((width/2+30),height/2-10))
text_bet_surf = text_font.render("BET!", False, "Orange")
text_bet_rect = text_bet_surf.get_rect(topleft = (20,180))
text_allin_surf = text_font.render("ALL IN!", False, "blue")
text_allin_rect = text_allin_surf.get_rect(topleft = (20,280))
text_mise_surf = text_font.render("mise:", False, "Orange")
text_mise_rect = text_mise_surf.get_rect(topleft = (20,100))
text_save1_surf = text_font.render("erase", False, "blue")
text_save1_rect = text_save1_surf.get_rect(topright = (width-10,10))
text_save2_surf = text_font.render("save", False, "blue")
text_save2_rect = text_save2_surf.get_rect(topright = (width-15,60))
draw_surf = pygame.Surface((300,37))
draw_surf.fill("white")
draw_rect = draw_surf.get_rect(topleft = (width/2-120, height/2-30))
save_surf = pygame.Surface((100,95))
save_surf.fill("lightgreen")
save_rect = save_surf.get_rect(topright = (width-5, 5))
piece_rect = piece_surf.get_rect(topleft = (10,10))
etoile_rect = piece_surf.get_rect(bottomright = (width-35,height-40))
def pieces(piece):
    text_pieces_surf = piece_font.render(str(piece), False, "black")
    text_pieces_rect = text_pieces_surf.get_rect(topleft = (55,10))
    return text_pieces_surf, text_pieces_rect
def etoiles(etoile):
    text_etoiles_surf = piece_font.render(str(etoile), False, "red")
    text_etoiles_rect = text_etoiles_surf.get_rect(bottomright = (width-28,height-18))
    return text_etoiles_surf, text_etoiles_rect
def bet(piece):
    text_pieces_surf = text_font.render(str(piece), False, "black")
    text_pieces_rect = text_pieces_surf.get_rect(topleft = (120,100))
    return text_pieces_surf, text_pieces_rect
def text_main(main,joueur):
    if joueur: hauteur = height - height/3-10
    else: hauteur = height/3
    text_main_surf = text_font.render(str(main), False, "red")
    text_main_rect = text_main_surf.get_rect(center = (width/2+30,hauteur))
    return text_main_surf,text_main_rect
def gagner_pieces(piece):
    text_pieces_surf = piece_font.render("+"+ str(piece), False, "black")
    text_pieces_rect = text_pieces_surf.get_rect(topleft = (20,60))
    return text_pieces_surf, text_pieces_rect
pygame.display.set_icon(piece_surf)

carte_nuage_surf = load_and_resize_image("img/nuage.png",(round(width/10.41), round(height/4.16)))
carte_champignon_surf = load_and_resize_image("img/champignon.png",(round(width/10.41), round(height/4.16)))
carte_fleur_de_feu_surf = load_and_resize_image("img/fleur_de_feu.png",(round(width/10.41), round(height/4.16)))
carte_luigi_surf = load_and_resize_image("img/luigi.png",(round(width/10.41), round(height/4.16)))
carte_mario_surf = load_and_resize_image("img/mario.png",(round(width/10.41), round(height/4.16)))
carte_etoile_surf = load_and_resize_image("img/etoile.png",(round(width/10.41), round(height/4.16)))
carte_dos_surf = load_and_resize_image("img/dos.png",(round(width/10.41), round(height/4.16)))
cartes = [carte_dos_surf,carte_etoile_surf,carte_mario_surf,carte_luigi_surf,carte_fleur_de_feu_surf,carte_champignon_surf,carte_nuage_surf]

def definir_carte(carte1,carte2,carte3,carte4,carte5,joueur):
    if joueur: hauteur = height-50
    else: hauteur = round(height/4.16) + 50
    carte_rect1 = carte1.get_rect(midbottom = ((width/2-270),hauteur))
    carte_rect2 = carte2.get_rect(midbottom = ((width/2-120),hauteur))
    carte_rect3 = carte3.get_rect(midbottom = ((width/2+30),hauteur))
    carte_rect4 = carte4.get_rect(midbottom = ((width/2+180),hauteur))
    carte_rect5 = carte5.get_rect(midbottom = ((width/2+330),hauteur))
    return [carte_rect1,carte_rect2,carte_rect3,carte_rect4,carte_rect5]

def times(temps):
    return temp < pygame.time.get_ticks() - temps

def selectionner_carte(carte,state):
    if carte.collidepoint(mouse_pos):
        if mouse_press[0] and carte.bottom == height-50:state = True
        if mouse_press[0] and carte.bottom == height-110:state = False
    if state and carte.bottom != height-110:
        carte.bottom -=10
    if not(state) and carte.bottom != height-50:
        carte.bottom +=10
    return state

def commencer_partie(jeux):
    jeux.jeu.refaire_paquet()
    jeux.jeu.melanger()
    jeux.joueur.effacer_jeu()
    jeux.banque.effacer_jeu()
    for i in range(5):
        jeux.joueur.attribuer_carte(jeux.jeu.prendre_carte(),-1)
        jeux.banque.attribuer_carte(jeux.jeu.prendre_carte(),-1)
    jeux.banque.trier_jeu()
    return jeux

def lire():
    with open ("save.txt","r") as file:
        save = file.read()
    mot1 = ""
    mot2 = ""
    for lettre in save:
        if lettre == "/":
            mot2 = save[save.index("/")+1:]
            break
        mot1 += lettre
    return mot1,mot2

def save(pieces,etoiles):
    with open ("save.txt", "w") as file:
        file.write(str(pieces)+"/"+str(etoiles))
        file.close()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save(jeux.joueur.pieces, jeux.joueur.etoile)
            sys.exit()

def render_screen():
    screen.blit(background,(0,0))
    screen.blit(classement_carte_surf,classement_carte_rect)
    screen.blit(combinaisons_carte_surf,combinaisons_carte_rect)
    screen.blit(save_surf,save_rect)
    screen.blit(text_save1_surf,text_save1_rect)
    screen.blit(text_save2_surf,text_save2_rect)
    joueur_pieces_surf,joueur_pieces_rect = pieces(jeux.joueur.pieces)
    screen.blit(joueur_pieces_surf,joueur_pieces_rect)
    screen.blit(piece_surf,piece_rect)
    screen.blit(text_mise_surf,text_mise_rect)
    joueur_mise_surf, joueur_mise_rect = bet(mise)
    screen.blit(joueur_mise_surf,joueur_mise_rect)
    joueur_etoile_surf,joueur_etoile_rect = etoiles(jeux.joueur.etoile)
    screen.blit(etoile_surf,etoile_rect)
    screen.blit(joueur_etoile_surf,joueur_etoile_rect)

temp = pygame.time.get_ticks()
jeux = Partie()
if not(os.stat("save.txt").st_size == 0):
    pieces_save, etoiles_save = lire()
    jeux.joueur.pieces = int(pieces_save)
    jeux.joueur.etoile = int(etoiles_save)

debut_partie = True; selecting = True; qui_gagne = False;son = True; parier = True; mise = 1;banque_cacher = True; monter = [True] * 5; descendre = [False] * 5
mettre_la_musique()

while 1:
    handle_events()
    render_screen()
    mouse_pos = pygame.mouse.get_pos()  
    mouse_press = pygame.mouse.get_pressed()

    if save_rect.collidepoint(mouse_pos) and mouse_press[0]:
        jeux.joueur.pieces = 10
        jeux.joueur.etoile = 0

    if debut_partie:
        if jeux.joueur.pieces == 0:
            print("appuyer erase save")
        jeux = commencer_partie(jeux)
        liste_carte_joueur = definir_carte(cartes[jeux.joueur.jeu_en_main[0].valeur],cartes[jeux.joueur.jeu_en_main[1].valeur],cartes[jeux.joueur.jeu_en_main[2].valeur],cartes[jeux.joueur.jeu_en_main[3].valeur],cartes[jeux.joueur.jeu_en_main[4].valeur],True)
        liste_carte_banque = definir_carte(cartes[jeux.banque.jeu_en_main[0].valeur],cartes[jeux.banque.jeu_en_main[1].valeur],cartes[jeux.banque.jeu_en_main[2].valeur],cartes[jeux.banque.jeu_en_main[3].valeur],cartes[jeux.banque.jeu_en_main[4].valeur],False)
        debut_partie = False

    for i in range(5):
        if selecting:
            screen.blit(cartes[jeux.joueur.jeu_en_main[i].valeur],liste_carte_joueur[i])
            jeux.joueur.jeu_en_main[i].state = selectionner_carte(liste_carte_joueur[i],jeux.joueur.jeu_en_main[i].state)
            screen.blit(draw_surf,draw_rect)
            pygame.draw.rect(screen,"White",(width/2-125, height/2-30, 310, 37),6,6)
            screen.blit(text_draw_surf,text_draw_rect)
            if draw_rect.collidepoint(mouse_pos) and mouse_press[0]:
                for num in range(5):
                    if jeux.joueur.jeu_en_main[num].state:
                        carte_prise = jeux.joueur.changer_carte(num)
                        jeux.joueur.attribuer_carte(jeux.jeu.prendre_carte(),num)
                        jeux.joueur.jeu_en_main[num].state = True
                        jeux.jeu.remettre_carte(carte_prise)
                parier = False
                selecting = False
                qui_gagne = True
                montrer_jeu_joueur = True
                jeux.joueur.ajouter_pieces(-mise)
                temp = pygame.time.get_ticks()

    
    if banque_cacher:
        for num in range(5):
            screen.blit(cartes[0],liste_carte_banque[num])
    else:
        for num in range(5):
            screen.blit(cartes[jeux.banque.jeu_en_main[num].valeur],liste_carte_banque[num])
    
    if parier:
        bet_collision = pygame.draw.polygon(screen,"yellow",[(60,160),(20,225),(100,225)])
        allin_collision = pygame.draw.polygon(screen,"red",[(60,260),(20,325),(100,325)])
        screen.blit(text_bet_surf,text_bet_rect)
        screen.blit(text_allin_surf,text_allin_rect)
        if bet_collision.collidepoint(mouse_pos) and mouse_press[0]:
            if mise < jeux.joueur.pieces/2 and times(200):
                mise += 1
                temp = pygame.time.get_ticks()
        if allin_collision.collidepoint(mouse_pos) and mouse_press[0]:
            if mise < 10 and times(200):
                mise = jeux.joueur.pieces
                temp = pygame.time.get_ticks()

    if qui_gagne:
        if montrer_jeu_joueur:
            for num in range(5):
                if jeux.joueur.jeu_en_main[num].state:
                    if monter[num]:
                        screen.blit(cartes[0],liste_carte_joueur[num])
                        liste_carte_joueur[num].bottom -= 15
                    if liste_carte_joueur[num].bottom <= 0:
                        monter[num] = False
                        descendre[num] = True
                    if descendre[num]:
                        liste_carte_joueur[num].bottom += 15
                        screen.blit(cartes[jeux.joueur.jeu_en_main[num].valeur],liste_carte_joueur[num])
                        if liste_carte_joueur[num].bottom == height-50:
                            jeux.joueur.jeu_en_main[num].state = False
                            descendre[num] = False
                else:
                    screen.blit(cartes[jeux.joueur.jeu_en_main[num].valeur],liste_carte_joueur[num])
                    if times(4000):
                        montrer_jeu_joueur = False
                        banque_cacher = False
                        jeux.joueur.trier_jeu()
                        jeu_joueur = jeux.joueur.calculer_main()
                        jeu_banque = jeux.banque.calculer_main()    
                        gagnant = trouver_gagnant(jeu_joueur, jeu_banque)
                        temp = pygame.time.get_ticks()
        else:
            for num in range(5):
                screen.blit(cartes[jeux.joueur.jeu_en_main[num].valeur],liste_carte_joueur[num])
            text_main_joueur_surf,text_main_joueur_rect = text_main(jeu_joueur[0],True)
            text_main_banque_surf,text_main_banque_rect = text_main(jeu_banque[0],False)
            screen.blit(text_main_joueur_surf,text_main_joueur_rect)
            screen.blit(text_main_banque_surf,text_main_banque_rect)
            if times(500):
                if gagnant == 1:
                    screen.blit(text_win_surf,text_win_rect)
                    gain_surf,gain_rect = gagner_pieces(multiplicateur(jeu_joueur,mise)*mise)
                    screen.blit(gain_surf,gain_rect)
                    if son:
                            pygame.mixer.music.pause()
                            pygame.mixer.music.set_volume(1)
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound('musique/you_win.mp3'))
                            son = False
                    if not(pygame.mixer.Channel(0).get_busy()) and not(pygame.mixer.music.get_busy()):
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.unpause()
                    if times(3500):
                        jeux.joueur.ajouter_etoile()
                        jeux.joueur.ajouter_pieces(multiplicateur(jeu_joueur,mise) * mise)
                elif gagnant == 2:
                    screen.blit(text_loose_surf,text_loose_rect)
                    if son:
                        pygame.mixer.music.pause()
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('musique/luigi.mp3'))
                        son = False
                    if not(pygame.mixer.Channel(0).get_busy()) and not(pygame.mixer.music.get_busy()):
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.unpause()
                    if times(3500):
                        if jeux.joueur.etoile > 0:
                            jeux.joueur.retirer_etoile()
                elif gagnant == 3:
                    screen.blit(text_egalite_surf,text_egalite_rect)
                    if times(3500):
                        jeux.joueur.ajouter_pieces(mise)
                if times(3500):
                    temp = pygame.time.get_ticks()
                    debut_partie = True; qui_gagne = False; parier = True; banque_cacher = True; mise = 1;son = True; selecting = True;monter = [True] * 5; descendre = [False] * 5
            
    pygame.display.update()
    clock.tick(60)