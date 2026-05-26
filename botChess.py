#pip install python-chess
import random
import time

import chess
import math
from evaluationChess import getCaseEvaluation, getBoardEvaluation, getPositionEvaluation, miniMax
from boardChess import boardChess


b = boardChess()
board = b.getBoard()


def deplacement(move):

    if move in board.legal_moves :
        board.push(move)
        return True
    return False







def botMove(depth, color):
    best_move = random.choice(list(board.legal_moves))
    best_score = math.inf


    if color == chess.WHITE :
        best_score = -math.inf
        

    for move in list(board.legal_moves):

        board.push(move)
        score = miniMax(board, depth - 1, not color)
        board.pop()


        if color == chess.BLACK and score < best_score :
            best_score = score
            best_move = move
        
        if color == chess.WHITE and score > best_score :
            best_score = score
            best_move = move

        
        
    return best_move






while not board.is_game_over() :

    print(getPositionEvaluation(board))
    print(board)
    if board.turn == chess.WHITE:
        print("white turn")

        move = botMove(3, chess.WHITE)

        if not deplacement(move):
            continue

    
    

    print(getPositionEvaluation(board))
    print(board)
    time.sleep(1)

    print("black turn")
    
    move = botMove(3, chess.BLACK)

    print(move)

    if not deplacement(move):
        continue

    print(getPositionEvaluation(board))
    print(board)

    time.sleep(1)


def inputMove(): 
            
        move = input("piece move : ")
        

        try :
            moveObj = chess.Move.from_uci(move)
        except:
            print("format invalid")
