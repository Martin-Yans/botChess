import chess

class boardChess:

    def __init__(self):
        self.board = chess.Board()

    def getBoard(self):
        return self.board