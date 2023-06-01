import pygame
from ghostgame.constants import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
white = (255, 255, 255)
black = (0, 0, 0)
color_dark = (100, 100, 100)

smallfont = pygame.font.SysFont('Calibri', 35)
verysmallfont = pygame.font.SysFont('Calibri', 20)
bigfont = pygame.font.SysFont('Calibri Bold', 50)
text_title = bigfont.render("18 GHOSTS", True, color_dark)
text_menu = smallfont.render("Rules of the game", True, color_dark)

text_rules_1 = verysmallfont.render("1- You can put a ghost from the dungeon in the board if the room that you choose is "
                              "the same colort of the ghost", True, color_dark)
text_rules_2 = verysmallfont.render("2- In the first round, the second player can make 2 moves", True, color_dark)
text_rules_3 = verysmallfont.render("3- Ghosts can only move ortogonally", True, color_dark)
text_rules_4 = verysmallfont.render("4- Ghosts can escaped if the portal in turned in the same direction that ghost are", True, color_dark)
text_rules_5 = verysmallfont.render("5- Two ghosts (from the same team or not) can flight if they are in the same room:", True, color_dark)
text_rules_5_1 = verysmallfont.render("5.1- Red beats blue", True, color_dark)
text_rules_5_2 = verysmallfont.render("5.2- Blue beats yellow", True, color_dark)
text_rules_5_3 = verysmallfont.render("5.3- Yellow beats red", True, color_dark)
text_rules_5_4 = verysmallfont.render("Ghosts defetead return to the dungeons", True, color_dark)
text_rules_6 = verysmallfont.render("6- When a ghosts is beated, the portal with the same colour turn 90 degrees", True, color_dark)
text_rules_7 = verysmallfont.render("7- You win if you 3 of your ghosts (with different colours) escaped", True, color_dark)

def draw_rules():
    while True:
        screen.fill((169, 169, 169))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(text_title, (WIDTH/2 - 45, 100))
        screen.blit(text_menu, (WIDTH/2 - 70, 160))
        screen.blit(text_rules_1, (20, 260))
        screen.blit(text_rules_2, (20, 300))
        screen.blit(text_rules_3, (20, 340))
        screen.blit(text_rules_4, (20, 380))
        screen.blit(text_rules_5, (20, 420))
        screen.blit(text_rules_5_1, (35, 460))
        screen.blit(text_rules_5_2, (35, 500))
        screen.blit(text_rules_5_3, (35, 540))
        screen.blit(text_rules_5_4, (20, 580))
        screen.blit(text_rules_6, (20, 620))
        screen.blit(text_rules_7, (20, 660))

        pygame.display.update()
