
import chess
import math

pieceValue = {
    chess.PAWN : 100,
    chess.KNIGHT : 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900
}


def getBoardEvaluation(square):

    if square == None :
        return 0

    file = chess.square_file(square)  # 0 à 7
    rank = chess.square_rank(square)  # 0 à 7

    center_distance = abs(3.5 - file) + abs(3.5 - rank)

    return 1 - (center_distance / 7)

def getKingBoardEvaluation(square, endgame=False):

    if square is None:
        return 0

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    edge_distance = min(file, 7-file) + min(rank, 7-rank)

    if endgame:
        # roi actif en fin de partie
        return (file - 3.5)**2 + (rank - 3.5)**2

    else:
        # roi protégé au bord
        score = 1 - (edge_distance / 7)

        if square in [chess.E4, chess.E5, chess.D4, chess.D5]:
            score -= 0.6

        return score

def movePriority(board, move):

    score = 0

    # capture
    if board.is_capture(move):
        score += 20

    # promotion
    if move.promotion:
        score += 50

    # échec
    board.push(move)
    if board.is_check():
        score += 10
    if board.is_checkmate():
        score += 999
    board.pop()

    return score




def getCaseEvaluation(board, case):
    
    #recuperer la case en square
    square = chess.parse_square(case)
   
    #ecuperer l'evaluation de la case
    caseValue = getBoardEvaluation(square)

    #recuperer la piece sur la case
    piece = board.piece_at(square)
    
    if piece is None:
        valuePiece = pieceValue[None]
    else:
        valuePiece = pieceValue[piece]

    return(caseValue*valuePiece)


def getPositionEvaluation(board):

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -math.inf
        else:
            return math.inf


    score = 0
    for piece_type in pieceValue:

        if piece_type == None  or piece_type == chess.KING:
            continue

        for square in board.pieces(piece_type, chess.WHITE):
            score += pieceValue[piece_type]
            score += getBoardEvaluation(square) * 10

        for square in board.pieces(piece_type, chess.BLACK) : 
            score -= pieceValue[piece_type]
            score -= getBoardEvaluation(square) * 10




    white_king = board.king(chess.WHITE)
    black_king = board.king(chess.BLACK)


    score += getKingBoardEvaluation(white_king) * 2
    score -= getKingBoardEvaluation(black_king) * 2

    if not board.has_castling_rights(chess.WHITE):
        score -= 0.3

    if not board.has_castling_rights(chess.BLACK):
        score += 0.3


    score += len(list(board.legal_moves)) * 2

    return score




#miniMax permet de trouver le score le plus haut si tu est les blancs ou le score le plus bas si tu est les noirs pour avoir l'aventage 

#alpha est le max trouver
#beta est le min trouver

#return(best_move, evaluation)

def miniMax(board, depth, is_maximizing, alpha = -math.inf, beta = math.inf):
    
    if depth <= 0 or board.is_game_over() :
        return getPositionEvaluation(board)


    movesSorted = list(board.legal_moves)
    movesSorted.sort(key=lambda move: movePriority(board, move), reverse=True)

    # avoir le plus haut score si c'est les blanc (voir READMY)
    if is_maximizing :
        
        best_score = -math.inf    
      
        for moveTest in movesSorted:
            board.push(moveTest)
            score = miniMax(board, depth - 1, False, alpha, beta)
            board.pop()

            best_score = max(best_score, score)

            alpha = max(alpha, best_score)

            if beta <= alpha :
                break


        return best_score

            

    # avoir le plus bas score si tu est les noirs (voir READMY)
    else :

        best_score = math.inf
        
        for moveTest in movesSorted : 
            board.push(moveTest)
            score = miniMax(board, depth - 1, True, alpha, beta)
            board.pop()

            best_score = min(best_score, score)

            beta = min(beta, best_score)

            if beta <= alpha :
                break




        return best_score