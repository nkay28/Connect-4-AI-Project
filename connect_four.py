import numpy as np
import time
import random
import sys
import math

import pygame
from pygame.locals import *


def create_board(rows, columns):
    board = np.empty([rows, columns], dtype=object)  # can use dtype object
    board.fill("W")
    print(board.dtype, board.shape)
    print(board, "Board Created")

    return board

# drop a piece:
def add_piece(board, c, piece_player, turn):
    for row in reversed(range(board.shape[0])):
        if board[row, c] == "W":
            if turn == 0:
                board[row, c] = "R"
                print(board)
                print("Accepted")
                turn = 1
                return board, row, turn

            elif turn == 1:
                board[row, c] = "B"
                print(board)
                print("Accepted")
                turn = 0
                return board, row, turn

        else:
            continue

    print("this column full")
    # take_input_add(board, turn)
    return False


def take_input_add(board, turn):
    # take new slot and color input and pass to add_piece
    if turn == 0:

        in_c = input('Enter your player 1 position (Column): ')
        col = int(in_c)
        print("Dropping Piece")
        result_board, r, turn = add_piece(board, col, "R", turn)
        return result_board, (r, col), "R", turn

    elif turn == 1:

        in_c2 = input('Enter your player 2 position (Column): ')
        col2 = int(in_c2)
        # place the piece/play the player's move
        print("Dropping Piece P2")
        result_board2, r2, turn = add_piece(board, col2, "B", turn)
        return result_board2, (r2, col2), "B", turn


def check_win(board, tile_played, player_played, turn):
    col = player_played  # color of player
    i, j = tile_played

    ## check VERTICAL:
    # take the ith row n check all cases
    # u can only make vertical in the COLUMN you have just put the piece
    if i in range(0, 3):
        for row in range(0, 3):
            # print(col, board[row, j],board[row+1, j], board[row+2, j], board[row+3, j])
            # check for i and +3   # 3 cases
            if board[row, j] == col and board[row + 1, j] == col and board[row + 2, j] == col and board[row + 3, j] == col:
                if col == "W":
                    continue
                else:
                    print(col, "won", "won1")
                    return True, board

    if i in range(3, 6):
        for row in range(3, 6):
            # check for i and -3
            # print(col, board[row, j],board[row-1, j], board[row-2, j], board[row-3, j])
            if board[row, j] == col and board[row - 1, j] == col and board[row - 2, j] == col and board[row - 3, j] == col:
                if col == "W":
                    continue
                else:
                    print(col, "won", "won2")
                    return True, board

    ## Check HORIZONTAL:
    #
    # u can only make horizontal in the ROW you just put the piece
    if j in range(0, 4):
        for colm in range(0, 4):

            # check for i and +3   # 4 cases
            if board[i, colm] == col and board[i, colm + 1] == col and board[i, colm + 2] == col and board[i, colm + 3] == col:
                if col == "W":
                    continue
                else:
                    print(col, "won", "won3")
                    return True, board

    if j in range(3, 7):
        for colm in range(3, 7):
            # check for i and -3
            # print(colm, j)
            # print(col, board[i, colm], board[i, colm-1], board[i, colm-3])
            if board[i, colm] == col and board[i, colm - 1] == col and board[i, colm - 2] == col and board[i, colm - 3] == col:
                if col == "W":
                    continue
                else:
                    print(col, "won", "won4")
                    return True, board

    ## Check DIAGONAL:

    # https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python

    diags = [board[::-1, :].diagonal(i) for i in range(-3, 4)]
    diags.extend(board.diagonal(i) for i in range(3, -4, -1))
    dig = [i for i in diags if len(i) > 3]  # each element is numpy array

    for g in dig:
        # find 4 of same:
        for k in range(len(g) - 3):
            # print(g[k])
            if g[k] != "W":
                if g[k] == col and g[k + 1] == col and g[k + 2] == col and g[k + 3] == col:
                    if g[k] != "W" and g[k + 1] != "W" and g[k + 2] != "W" and g[k + 3] != "W":
                        # if col == "W":
                        #     continue
                        # else:
                        print(g[0], "won", "won5")
                        return True, board
                    else:
                        continue
                else:
                    continue
            else:
                continue

                # else call for next player turn:

    return False, board
    # take_input_add(board, turn)


#######    CALLING    #########:

# create the board
board = create_board(6, 7)

start_player = 0
turn = start_player
call = False
#
# while call == False:
#     # receive the player's play location & color, & put it on board
#     result_board, pos, state, turn = take_input_add(board, turn)
#
#     call, board = check_win(result_board, pos, state, turn)


#######################


# initialize pygame
pygame.init()

BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)

SQ_SIZE = 90
WIDTH = 7*SQ_SIZE
HEIGHT = (6+1)*SQ_SIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQ_SIZE/2) - 4
screen = pygame.display.set_mode(SIZE)

# pygame is event based
# piece drop depends on x position of mouse pointer

def draw_board(board):
    for c in range(7):
        for r in range(6):
            # rect(Surface, color, Rect, width=0), rect is area-needs (position)= x, y, width, height.
            pygame.draw.rect(screen, BLUE, (c * SQ_SIZE, r * SQ_SIZE + SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
            # circle(Surface, color, pos, radius, width=0)
            if board[r,c] == "W":
                pygame.draw.circle(screen, WHITE, (c * SQ_SIZE + int(SQ_SIZE/2), r * SQ_SIZE + SQ_SIZE + int(SQ_SIZE/2)), RADIUS)
            elif board[r,c] == "R":
                pygame.draw.circle(screen, RED, (c * SQ_SIZE + int(SQ_SIZE/2), r * SQ_SIZE + SQ_SIZE + int(SQ_SIZE/2)), RADIUS)
            if board[r,c] == "B":
                pygame.draw.circle(screen, GREEN, (c * SQ_SIZE + int(SQ_SIZE/2), r * SQ_SIZE + SQ_SIZE + int(SQ_SIZE/2)), RADIUS)
    pygame.display.update()


########

draw_board(board)
turn = 0

###################

# MAIN GUI CALLING:

##################

win_font = pygame.font.SysFont("helvetica", 80)

while call == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0, WIDTH, SQ_SIZE))

            pos_x_mou = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x_mou, int(SQ_SIZE/2)), RADIUS)
            elif turn == 1:
                pygame.draw.circle(screen, GREEN, (pos_x_mou, int(SQ_SIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, SQ_SIZE))
            print(event.pos)
            if turn == 0:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQ_SIZE))
                print("Dropping Piece P1")
                result_board, r, turn = add_piece(board, col, "R", turn)

                call, board = check_win(result_board, (r, col), "R", turn)
                label = win_font.render("player Red wins", 1, RED)
                pygame.display.update()

                #screen.blit(label, (40, 10))  # Displays WIN msg. how does this work ??


            elif turn == 1:
                pos_x = event.pos[0]
                col2 = int(math.floor(pos_x / SQ_SIZE))
                print("Dropping Piece P2")
                result_board2, r2, turn = add_piece(board, col2, "B", turn)

                call, board = check_win(result_board2, (r2, col2), "B", turn)
                label = win_font.render("player Green wins", 1, GREEN)
                pygame.display.update()


                #draw_board(board)
                # pygame.time.wait(3000) ## not here

            draw_board(board)
            print(call)

            if call:
                screen.blit(label, (40, 10))  # Displays WIN msg. how does this work ??

                #pygame.display.update()

            #draw_board(board)

            if call:
                pygame.time.wait(3000)





