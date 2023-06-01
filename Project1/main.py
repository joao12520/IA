from ghostgame.AI import *
from ghostgame.board import Board
from ghostgame.constants import *

import rules

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
white = (255, 255, 255)
black = (0, 0, 0)
color_dark = (100, 100, 100)

smallfont = pygame.font.SysFont('Calibri', 35)
bigfont = pygame.font.SysFont('Calibri Bold', 50)

text_title = bigfont.render("18 GHOSTS", True, color_dark)
text_menu = smallfont.render("MENU", True, color_dark)
text_rules = smallfont.render('Rules', True, white)
text_play = smallfont.render('Play', True, white)
text_exit = smallfont.render('Exit', True, white)

size_width = WIDTH / 2
size_height = HEIGHT / 2

FULL_WIDTH = 1250
FULL_HEIGHT = 800

WIN = pygame.display.set_mode((FULL_WIDTH, FULL_HEIGHT))

pygame.display.set_caption("18 Ghosts")
FPS = 30


def draw_menu():
    while True:
        screen.fill((169, 169, 169))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if size_width <= mouse[0] <= size_width + 140 and size_height <= mouse[1] <= size_height + 40:
                    draw_option_game()

                elif size_width <= mouse[0] <= size_width + 140 and size_height - 100 <= mouse[1] <= size_height - 60:
                    rules.draw_rules()

                elif size_width <= mouse[0] <= size_width + 140 and size_height + 100 <= mouse[1] <= size_height + 140:
                    pygame.quit()

        mouse = pygame.mouse.get_pos()

        if size_width <= mouse[0] <= size_width + 140 and size_height <= mouse[1] <= size_height + 40:
            pygame.draw.rect(screen, black, [size_width - 10, size_height, 100, 40])

        elif size_width <= mouse[0] <= size_width + 140 and size_height - 100 <= mouse[1] <= size_height - 60:
            pygame.draw.rect(screen, black, [size_width - 10, size_height - 100, 100, 40])

        elif size_width <= mouse[0] <= size_width + 140 and size_height + 100 <= mouse[1] <= size_height + 140:
            pygame.draw.rect(screen, black, [size_width - 10, size_height + 100, 100, 40])

        else:
            pygame.draw.rect(screen, color_dark, [size_width - 10, size_height - 100, 100, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 10, size_height, 100, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 10, size_height + 100, 100, 40])

        screen.blit(text_title, (size_width - 45, 100))
        screen.blit(text_menu, (size_width - 5, 200))
        screen.blit(text_rules, (size_width, size_height - 100))
        screen.blit(text_play, (size_width, size_height))
        screen.blit(text_exit, (size_width, size_height + 100))

        pygame.display.update()


text_option1 = smallfont.render('Player vs Player', True, white)
text_option2 = smallfont.render('Player vs Computer - Minimax', True, white)
text_option3 = smallfont.render('Player vs Computer - MCTS', True, white)
text_option4 = smallfont.render('Computer vs Computers - Minimax', True, white)
text_option5 = smallfont.render('Computer vs Computers - MCTS', True, white)
text_option6 = smallfont.render('Minimax vs MCTS', True, white)


def draw_option_game():
    while True:
        screen.fill((169, 169, 169))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if size_width <= mouse[0] <= size_width + 200 and size_height - 200 <= mouse[1] <= size_height - 100:
                    play("players")

                elif size_width <= mouse[0] <= size_width + 200 and size_height - 100 <= mouse[1] <= size_height:
                    play("player-computer-minimax")

                elif size_width <= mouse[0] <= size_width + 200 and size_height <= mouse[1] <= size_height + 100:
                    play("player-computer-mcts")

                elif size_width <= mouse[0] <= size_width + 200 and size_height + 100 <= mouse[1] <= size_height + 200:
                    play("computer-computer-minimax")

                elif size_width <= mouse[0] <= size_width + 200 and size_height + 200 <= mouse[1] <= size_height + 300:
                    play("computer-computer-mcts")

                elif size_width <= mouse[0] <= size_width + 200 and size_height + 300 <= mouse[1] <= size_height + 400:
                    play("minimax-mcts")

        mouse = pygame.mouse.get_pos()

        if size_width <= mouse[0] <= size_width + 200 and size_height-200 <= mouse[1] <= size_height-100:
            pygame.draw.rect(screen, black, [size_width - 80, size_height - 200, 490, 40])

        elif size_width <= mouse[0] <= size_width + 200 and size_height - 100 <= mouse[1] <= size_height:
            pygame.draw.rect(screen, black, [size_width - 80, size_height - 100, 490, 40])

        elif size_width <= mouse[0] <= size_width + 200 and size_height <= mouse[1] <= size_height + 100:
            pygame.draw.rect(screen, black, [size_width - 80, size_height, 490, 40])

        elif size_width <= mouse[0] <= size_width + 200 and size_height + 100 <= mouse[1] <= size_height + 200:
            pygame.draw.rect(screen, black, [size_width - 80, size_height + 100, 490, 40])

        elif size_width <= mouse[0] <= size_width + 200 and size_height + 200 <= mouse[1] <= size_height + 300:
            pygame.draw.rect(screen, black, [size_width - 80, size_height + 200, 490, 40])

        elif size_width <= mouse[0] <= size_width + 200 and size_height + 300 <= mouse[1] <= size_height + 400:
            pygame.draw.rect(screen, black, [size_width - 80, size_height + 300, 490, 40])

        else:
            pygame.draw.rect(screen, color_dark, [size_width - 80, size_height - 200, 490, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 80, size_height - 100, 490, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 80, size_height, 490, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 80, size_height + 100, 490, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 80, size_height + 200, 490, 40])
            pygame.draw.rect(screen, color_dark, [size_width - 80, size_height + 300, 490, 40])

        screen.blit(text_menu, (size_width - 5, 100))
        screen.blit(text_option1, (size_width - 80, size_height - 200))
        screen.blit(text_option2, (size_width - 80, size_height - 100))
        screen.blit(text_option3, (size_width - 80, size_height))
        screen.blit(text_option4, (size_width - 80, size_height + 100))
        screen.blit(text_option5, (size_width - 80, size_height + 200))

        pygame.display.update()


def change_turn(turn):
    textX = 1020
    textY = 10
    font = pygame.font.Font('freesansbold.ttf', 35)

    # Fill the area with a black rectangle to erase the previous text
    pygame.draw.rect(WIN, (0, 0, 0), (textX, textY, 200, 40))

    if turn == 1:
        turn_text = "Player 1 turn"
    else:
        turn_text = "Player 2 turn"

    turn_display = font.render(turn_text, True, (255, 255, 255))

    WIN.blit(turn_display, (textX, textY))

    pygame.display.update((textX, textY, 200, 80))


def highlight_ghost(selected_pos):
    if selected_pos is not None:
        if selected_pos[0] == "board":
            board_pos = selected_pos[1]
            x, y = POS_IMG_OFFSET[board_pos]
            pygame.draw.rect(WIN, (255, 255, 0), (x, y, PIECE_SIZE, PIECE_SIZE), 3)
        elif selected_pos[0] == "dungeon1":
            row, col = selected_pos[1]
            x = DUNGEON_TOP_OFFSET[0] + row * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)
            y = DUNGEON_TOP_OFFSET[1] + col * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)
            pygame.draw.rect(WIN, (255, 255, 0), (x, y, DUNGEON_PIECE_SIZE, DUNGEON_PIECE_SIZE), 3)
        elif selected_pos[0] == "dungeon2":
            row, col = selected_pos[1]
            x = DUNGEON_BOTTOM_OFFSET[0] + row * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)
            y = DUNGEON_BOTTOM_OFFSET[1] - col * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)
            pygame.draw.rect(WIN, (255, 255, 0), (x, y, DUNGEON_PIECE_SIZE, DUNGEON_PIECE_SIZE), 3)


def get_row_col_from_mouse(pos):
    x, y = pos

    for item in POS_IMG_OFFSET.items():
        boardPos, coords = item
        if coords[0] <= x <= coords[0] + PIECE_SIZE and coords[1] <= y <= coords[1] + PIECE_SIZE:
            return "board", boardPos

    if (DUNGEON_TOP_OFFSET[0] <= x <= DUNGEON_TOP_OFFSET[0] + 3 * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)) and (
            DUNGEON_TOP_OFFSET[1] <= y <= DUNGEON_TOP_OFFSET[1] + 3 * (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)):
        row = ((x - DUNGEON_TOP_OFFSET[0]) // (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
        col = ((y - DUNGEON_TOP_OFFSET[1]) // (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
        return "dungeon1", (row, col)

    elif (DUNGEON_BOTTOM_OFFSET[0] <= x <= DUNGEON_BOTTOM_OFFSET[0] + 3 * (
            DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)) and (
            DUNGEON_BOTTOM_OFFSET[1] + (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP) >= y >= DUNGEON_BOTTOM_OFFSET[1] - 2 * (
            DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP)):
        row = ((x - DUNGEON_BOTTOM_OFFSET[0]) // (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
        col = abs((y - DUNGEON_BOTTOM_OFFSET[1]) // (DUNGEON_PIECE_SIZE + DUNGEON_PIECE_GAP))
        return "dungeon2", (row, col)


def play(option):
    run = True
    clock = pygame.time.Clock()
    board = Board()
    mm = Minimax()
    clicked_pos = None
    WIN.fill((0, 0, 0))

    while not board.isOver():
        clock.tick(FPS)
        pygame.display.update()
        if option == "player-computer-minimax":
            if board.turn == 2:
                _, best_board = mm.minimax(board, MINIMAX_DEPTH, True, -math.inf, math.inf)
                board = best_board
                pygame.display.update()

        if option == "player-computer-mcts":
            if board.turn == 2:
                board = mcts(MCTS_Node(board), MCTS_ITER)
                pygame.display.update()

        elif option == "computer-computer-minimax":
           if board.turn == 1:
                _, best_board = mm.minimax(board, MINIMAX_DEPTH, True, -math.inf, math.inf)
                board = best_board

           else:
                _, best_board = mm.minimax(board, MINIMAX_DEPTH, True, -math.inf, math.inf)
                board = best_board
           pygame.display.update()

        elif option == "computer-computer-mcts":
            if board.turn == 1:
                board = mcts(MCTS_Node(board), MCTS_ITER)
            else:
                board = mcts(MCTS_Node(board), MCTS_ITER)
            pygame.display.update()

        elif option == "minimax-mcts":
            if board.turn == 1:
                _, best_board = mm.minimax(board, 4, True, -math.inf, math.inf)
                board = best_board
            else:
                board = mcts(MCTS_Node(board), MCTS_ITER)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if clicked_pos is None:
                    pos = pygame.mouse.get_pos()
                    clicked_pos = get_row_col_from_mouse(pos)
                    print(clicked_pos)
                else:
                    pos = pygame.mouse.get_pos()
                    new_pos = get_row_col_from_mouse(pos)
                    print(new_pos)
                    if clicked_pos is not None and new_pos is not None and board.move(clicked_pos, new_pos):
                        clicked_pos = None
                    else:
                        clicked_pos = new_pos

        board.draw(WIN)
        highlight_ghost(clicked_pos)
        board.print_ghosts_escaped(WIN)
        change_turn(board.turn)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    draw_menu()
