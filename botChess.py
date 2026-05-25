#pip install python-chess
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







def botMove(depth):
    best_move = None
    best_score = -99999

    for move in list(board.legal_moves):

        board.push(move)
        score = miniMax(board, depth - 1, False)
        board.pop()


        if score > best_score :
            best_score = score
            best_move = move
        
    return best_move






while not board.is_game_over() :

    print(getPositionEvaluation(board))
    print(board)
    if board.turn == chess.WHITE:
        print("white turn")
        
        move = input("piece move : ")
        
        if (move == 'exit') : break

        try :
            moveObj = chess.Move.from_uci(move)
        except:
            print("format invalid")
            continue

        if not deplacement(moveObj):
            continue


    print(getPositionEvaluation(board))
    print(board)
    

    print("black turn")
    
    move = botMove(5)

    print(move)

    if not deplacement(move):
        continue

    print(getPositionEvaluation(board))

        