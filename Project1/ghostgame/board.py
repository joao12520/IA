import math

import pygame

from ghostgame.constants import *


class Board:
    def __init__(self):
        self.board = []
        self.turn = 1
        self._fillBoard()
        self.exitRotations = {"BlueExit": 0, "RedExit": 180, "YellowExit": 90}
        self.ghostsEscaped = {1: {"blue": 0, "red": 0, "yellow": 0}, 2: {"yellow": 0, "red": 0, "blue": 0}}
        self.ghostsInDungeon = {1: {"blue": 3, "red": 3, "yellow": 3}, 2: {"yellow": 3, "red": 3, "blue": 3}}
        self.nPiecesInBoard = {1: 0, 2: 0}
        self.selected_piece = None
        self.first_round = True
        self.winner = None
        self.placingPhase = True
        self.lastMove = ()
        self.selected_piece = None

    def print_ghosts_escaped(self, screen):
        font2 = pygame.font.Font('freesansbold.ttf', 20)

        # Player 1
        escaped_default1 = font2.render(f"Team 1 ghosts escaped", True, (255, 255, 255))

        # Fill the area with a black rectangle to erase the previous text
        pygame.draw.rect(screen, (0, 0, 0), (1015, 150, 300, 40))
        pygame.draw.rect(screen, (0, 0, 0), (1015, 180, 300, 40))

        blue_ghosts = self.ghostsEscaped[1]['blue']
        red_ghosts = self.ghostsEscaped[1]['red']
        yellow_ghosts = self.ghostsEscaped[1]['yellow']

        escaped_1 = font2.render(f"B:{blue_ghosts} R:{red_ghosts} Y:{yellow_ghosts}", True, (255, 255, 255))
        screen.blit(escaped_default1, (1015, 150))
        screen.blit(escaped_1, (1015, 180))
        pygame.display.update((1020, 10, 200, 80))

        # Player 2
        escaped_default2 = font2.render(f"Team 2 ghosts escaped", True, (255, 255, 255))

        # Fill the area with a black rectangle to erase the previous text
        pygame.draw.rect(screen, (0, 0, 0), (1015, 620, 300, 40))
        pygame.draw.rect(screen, (0, 0, 0), (1015, 650, 300, 40))

        blue_ghosts = self.ghostsEscaped[2]['blue']
        red_ghosts = self.ghostsEscaped[2]['red']
        yellow_ghosts = self.ghostsEscaped[2]['yellow']

        escaped_2 = font2.render(f"B:{blue_ghosts} R:{red_ghosts} Y:{yellow_ghosts}", True, (255, 255, 255))
        screen.blit(escaped_default2, (1015, 620))
        screen.blit(escaped_2, (1015, 650))
        pygame.display.update((1020, 10, 200, 80))

    def _fillBoard(self):
        for i in range(5):
            self.board.append([])
            for j in range(5):
                self.board[i].append({})
                self.board[i][j]["color"] = POS_COLOR[i][j]
                self.board[i][j]["type"] = "empty"
                self.board[i][j]["rotation"] = 0
                self.board[i][j]["team"] = ""

                if self.board[i][j]["color"] == "none":
                    self.board[i][j]["type"] = "mirror"

        self.board[0][2]["type"] = "exit"
        self.board[2][4]["type"] = "exit"
        self.board[4][2]["type"] = "exit"
        self.board[0][2]["rotation"] = 180
        self.board[2][4]["rotation"] = 90

    def move(self, posI, posF):
        if not self.valid_move(posI, posF):
            return False

        if "dungeon" in posI[0]:
            team, color = self._getDungeonPieceFromPos(posI)
            self.ghostsInDungeon[team][color] -= 1

            self.board[posF[1][0]][posF[1][1]]["type"] = "ghost"
            self.board[posF[1][0]][posF[1][1]]["team"] = team
            self.nPiecesInBoard[self.turn] += 1

        if posI[0] == "board":
            i, j = posI[1][0], posI[1][1]
            if self.board[posF[1][0]][posF[1][1]]["type"] == "ghost":
                self.board[posF[1][0]][posF[1][1]] = self.combat(self.board[i][j], self.board[posF[1][0]][posF[1][1]])

            elif self.board[posF[1][0]][posF[1][1]]["type"] == "exit":
                self.ghostsEscaped[self.board[i][j]["team"]][self.board[i][j]["color"]] += 1

            else:
                self.board[posF[1][0]][posF[1][1]] = self.board[i][j].copy()

            self.clearCell(i, j)

        self.changeTurn()
        self.lastMove = (posI, posF)
        self.placingPhaseCheck()

        return True

    def valid_move(self, posI, posF):
        if not (5 > posI[1][0] >= 0 and 5 > posI[1][1] >= 0 and 5 > posF[1][0] >= 0 and 5 > posF[1][1] >= 0):
            return False

        pieceI = self.board[posI[1][0]][posI[1][1]]; pieceF = self.board[posF[1][0]][posF[1][1]]

        if (posI[0] == "board" and pieceI["team"] != self.turn) or ("dungeon" in posI[0] and not str(self.turn) in posI[0]):
            return False

        if posI[0] == "board":
            if self.placingPhase:
                return False

            if pieceI["type"] != "ghost" or "dungeon" in posF[0] or (pieceI["type"] == pieceF["type"] == "ghost" and pieceI["color"] == pieceF["color"]):
                return False

            deltaRow = posF[1][0]-posI[1][0]
            deltaCol = posF[1][1] - posI[1][1]

            vert_move = abs(deltaRow) == 0 and abs(deltaCol) == 1
            hor_move = abs(deltaRow) == 1 and abs(deltaCol) == 0
            mirror_move = POS_COLOR[posI[1][0]][posI[1][1]] == "none" and "mirror" == pieceF["type"]

            if pieceF["type"] == "exit":
                if pieceI["color"] == pieceF["color"] and (deltaRow, deltaCol) == (round(-math.cos(math.radians(pieceF["rotation"]))), round(-math.sin(math.radians(pieceF["rotation"])))):
                    return True
                return False

            return vert_move or hor_move or mirror_move

        if "dungeon" in posI[0]:
            if "dungeon" in posF[0]:
                return False
            color = self._getDungeonPieceFromPos(posI)[1]
            return self.board[posF[1][0]][posF[1][1]]["color"] == color and pieceF["type"] == "empty"

    def _getDungeonPieceFromPos(self, pos):
        if '1' in pos[0]:
            team = 1
        else:
            team = 2

        ghostIndex = pos[1][0] + pos[1][1] * 3 + 1
        for item in self.ghostsInDungeon[team].items():
            ghostIndex -= item[1]
            if ghostIndex <= 0:
                color = item[0]
                return team, color

        print("F")

    def getDungeonPosFromColor(self, team, color):
        if self.ghostsInDungeon[team][color] == 0:
            return -1, -1

        i = 0
        for item in self.ghostsInDungeon[team].items():
            if item[0] != color:
                i += item[1]
            else:
                break

        return i % 3, i // 3

    def draw(self, win):
        win.blit(BOARD_IMAGE, (0, 0))
        self._drawBoard(win)
        self._drawDungeon(win)

    def _drawDungeon(self, win):
        i1 = 0
        i2 = 0

        for team in self.ghostsInDungeon.items():
            for ghost in team[1].items():
                for i in range(ghost[1]):
                    if team[0] == 1:
                        img = pygame.transform.scale(PIECE_IMG[ghost[0]+"ghost"+str(team[0])], (DUNGEON_PIECE_SIZE, DUNGEON_PIECE_SIZE))
                        horPos = DUNGEON_TOP_OFFSET[0] + ((i1 % 3) * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
                        vertPos = DUNGEON_TOP_OFFSET[1] + ((i1 // 3) * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
                        win.blit(img, (horPos, vertPos))
                        i1 += 1

                    if team[0] == 2:
                        img = pygame.transform.scale(PIECE_IMG[ghost[0]+"ghost"+str(team[0])], (DUNGEON_PIECE_SIZE, DUNGEON_PIECE_SIZE))
                        horPos = DUNGEON_BOTTOM_OFFSET[0] + ((i2 % 3) * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
                        vertPos = DUNGEON_BOTTOM_OFFSET[1] - ((i2 // 3) * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
                        win.blit(img, (horPos, vertPos))
                        i2 += 1

    def _drawBoard(self, win):
        for i in range(5):
            for j in range(5):
                self._drawBoardPiece(win, (i, j))

    def _drawBoardPiece(self, win, pos):
        piece = self.board[pos[0]][pos[1]]

        if piece["type"] != "empty" and piece["type"] != "mirror":
            if piece["type"] != "exit":
                win.blit(PIECE_IMG[piece["color"]+piece["type"]+str(piece["team"])], POS_IMG_OFFSET[(pos[0], pos[1])])
            else:
                img = PIECE_IMG[piece["color"]+piece["type"]+str(piece["team"])]
                rotated_image = pygame.transform.rotate(img, piece["rotation"])
                new_rect = rotated_image.get_rect(center=img.get_rect(topleft=POS_IMG_OFFSET[(pos[0], pos[1])]).center)
                win.blit(rotated_image, new_rect)

    def teamGhostsInDungeon(self, team):
        return sum(self.ghostsInDungeon[team].values())

    def rotateExit(self, color):
        if color == "blue":
            self.board[4][2]["rotation"] -= 90
        elif color == "red":
            self.board[0][2]["rotation"] -= 90
        elif color == "yellow":
            self.board[2][4]["rotation"] -= 90

    def otherTurn(self):
        if self.turn == 1:
            return 2
        return 1

    def changeTurn(self):
        if self.turn == 1:
            self.turn = 2

        elif not self.first_round:
            self.turn = 1
        else:
            self.first_round = False

    def combat(self, ghost1, ghost2):
        color1, color2 = ghost1["color"], ghost2["color"]

        if (color1 == "red" and color2 == "blue") or (color1 == "blue" and color2 == "yellow") or (color1 == "yellow" and color2 == "red"):
            self.ghostsInDungeon[ghost2["team"]][color2] += 1
            self.nPiecesInBoard[ghost2["team"]] -= 1
            self.rotateExit(color2)
            return ghost1.copy()

        else:
            self.ghostsInDungeon[ghost1["team"]][color1] += 1
            self.nPiecesInBoard[ghost1["team"]] -= 1
            self.rotateExit(color1)
            return ghost2.copy()

    def clearCell(self, i, j):
        self.board[i][j]["color"] = POS_COLOR[i][j]

        if self.board[i][j]["color"] == "none":
            self.board[i][j]["type"] = "mirror"
        else:
            self.board[i][j]["type"] = "empty"

        self.board[i][j]["team"] = ""

    def isOver(self):
        for team, dic in self.ghostsEscaped.items():
            counter = 0
            for escaped in dic.values():
                if escaped >= 1:
                    counter += 1

            if counter == 3:
                self.winner = team
                return True

        return False

    def getEscaped(self, team):
        escaped = []

        for i in self.ghostsEscaped[team].values():
            escaped.append(i)

        return escaped

    def getTurn(self):
        return self.turn

    def placingPhaseCheck(self):
        if self.placingPhase:
            if self.teamGhostsInDungeon(1) + self.teamGhostsInDungeon(2) == 0:
                self.placingPhase = False

    def possibleMoves(self):
        moves = []
        possibleDirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 2), (2, 0), (0, -2), (-2, 0), (2, -2), (-2, 2), (2, 2),
                        (-2, -2)]
        dungeonRedPos = self.getDungeonPosFromColor(self.turn, "red")
        dungeonBluePos = self.getDungeonPosFromColor(self.turn, "blue")
        dungeonYellowPos = self.getDungeonPosFromColor(self.turn, "yellow")

        for i in range(5):
            for j in range(5):
                piece = self.board[i][j]
                if piece["type"] == "ghost" and piece["team"] == self.turn:
                    for i1, j1 in possibleDirs:
                        move = (("board", (i, j)), ("board", (i + i1, j + j1)))
                        if self.valid_move(move[0], move[1]):
                            moves.append(move)

                elif piece["type"] == "empty":
                    if piece["color"] == "blue" and dungeonBluePos != (-1, -1):
                        moves.append((("dungeon" + str(self.turn), dungeonBluePos), ("board", (i, j))))
                    elif piece["color"] == "red" and dungeonRedPos != (-1, -1):
                        moves.append((("dungeon" + str(self.turn), dungeonRedPos), ("board", (i, j))))
                    elif piece["color"] == "yellow" and dungeonYellowPos != (-1, -1):
                        moves.append((("dungeon" + str(self.turn), dungeonYellowPos), ("board", (i, j))))

        return moves

    def sumOfDistsToExit(self):
        sum1 = 0
        sum2 = 0
        div1 = 0
        div2 = 0
        for i in range(5):
            for j in range(5):
                piece = self.board[i][j]
                if piece["type"] == "ghost":
                    if piece["team"] == self.turn and self.ghostsEscaped[self.turn][piece["color"]] == 0:
                        if piece["color"] == "blue":
                            sum1 += 8 - (abs(4 - i) + abs(2 - j))
                        elif piece["color"] == "red":
                            sum1 += 8 - (i + abs(2 - j))
                        elif piece["color"] == "yellow":
                            sum1 += 8 - (abs(2 - i) + abs(4 - j))
                        div1 += 1

                    elif self.ghostsEscaped[self.otherTurn()][piece["color"]] == 0:
                        if piece["color"] == "blue":
                            sum2 -= 8 - (abs(4 - i) + abs(2 - j))
                        elif piece["color"] == "red":
                            sum2 -= 8 - (i + abs(2 - j))
                        elif piece["color"] == "yellow":
                            sum2 -= 8 - (abs(2 - i) + abs(4 - j))
                        div2 += 1

        if div1 != 0:
            av1 = sum1 / div1
        else:
            av1 = 0

        if div2 != 0:
            av2 = sum2 / div2
        else:
            av2 = 0

        return av1 + av2
