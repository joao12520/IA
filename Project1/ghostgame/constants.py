import pygame
import math

MINIMAX_DEPTH = 4
MCTS_ITER = 20000
MCTS_EXPL_FACTOR = math.sqrt(2)
MCTS_DEPTH = 7

WIDTH, HEIGHT = 1010, 800
PIECE_SIZE = 120
DUNGEON_PIECE_SIZE = 53
DUNGEON_TOP_OFFSET = (810, 31)
DUNGEON_BOTTOM_OFFSET = (810, 720)
DUNGEON_PIECE_GAP = 5

BOARD_IMAGE = pygame.image.load("assets/board.png")
BOARD_IMAGE = pygame.transform.scale(BOARD_IMAGE, (WIDTH, HEIGHT))

GHOST1BLUE = pygame.image.load("assets/ghost1blue.png")
GHOST1BLUE = pygame.transform.scale(GHOST1BLUE, (PIECE_SIZE, PIECE_SIZE))
GHOST1RED = pygame.image.load("assets/ghost1red.png")
GHOST1RED = pygame.transform.scale(GHOST1RED, (PIECE_SIZE, PIECE_SIZE))
GHOST1YELLOW = pygame.image.load("assets/ghost1yellow.png")
GHOST1YELLOW = pygame.transform.scale(GHOST1YELLOW, (PIECE_SIZE, PIECE_SIZE))
GHOST2BLUE = pygame.image.load("assets/ghost2blue.png")
GHOST2BLUE = pygame.transform.scale(GHOST2BLUE, (PIECE_SIZE, PIECE_SIZE))
GHOST2RED = pygame.image.load("assets/ghost2red.png")
GHOST2RED = pygame.transform.scale(GHOST2RED, (PIECE_SIZE, PIECE_SIZE))
GHOST2YELLOW = pygame.image.load("assets/ghost2yellow.png")
GHOST2YELLOW = pygame.transform.scale(GHOST2YELLOW, (PIECE_SIZE, PIECE_SIZE))
EXITBLUE = pygame.image.load("assets/exitBlue.png")
EXITBLUE = pygame.transform.scale(EXITBLUE, (PIECE_SIZE, PIECE_SIZE))
EXITRED = pygame.image.load("assets/exitRed.png")
EXITRED = pygame.transform.scale(EXITRED, (PIECE_SIZE, PIECE_SIZE))
EXITYELLOW = pygame.image.load("assets/exitYellow.png")
EXITYELLOW = pygame.transform.scale(EXITYELLOW, (PIECE_SIZE, PIECE_SIZE))

POS_IMG_OFFSET = {(0, 0): (36, 31),  (0, 1): (193, 31),  (0, 2): (346, 31),  (0, 3): (498, 31),  (0, 4): (655, 31),
                  (1, 0): (36, 187), (1, 1): (193, 187), (1, 2): (346, 187), (1, 3): (498, 187), (1, 4): (655, 187),
                  (2, 0): (36, 341), (2, 1): (193, 341), (2, 2): (346, 341), (2, 3): (498, 341), (2, 4): (655, 341),
                  (3, 0): (36, 495), (3, 1): (193, 495), (3, 2): (346, 495), (3, 3): (498, 495), (3, 4): (655, 495),
                  (4, 0): (36, 651), (4, 1): (193, 651), (4, 2): (346, 651), (4, 3): (498, 651), (4, 4): (655, 651)}

POS_COLOR = [["blue", "red", "red", "blue", "red"],
             ["yellow", "none", "yellow", "none", "yellow"],
             ["red", "blue", "red", "blue", "yellow"],
             ["blue", "none", "yellow", "none", "red"],
             ["yellow", "red", "blue", "blue", "yellow"]]

PIECE_IMG = {"blueghost1": GHOST1BLUE, "redghost1": GHOST1RED, "yellowghost1": GHOST1YELLOW,
             "blueghost2": GHOST2BLUE, "redghost2": GHOST2RED, "yellowghost2": GHOST2YELLOW,
             "blueexit": EXITBLUE, "redexit": EXITRED, "yellowexit": EXITYELLOW}