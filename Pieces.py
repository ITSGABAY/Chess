from pprint import pprint

class Piece:
    def __init__(self, color, name, x, y):
        self.color = color.lower()
        self.name = name.lower()
        self.x = x
        self.y = y
        self.image = f"images/{self.color} {self.name}.png"
        self.isDown = False
        
    def organizeMoves(self, moves, chessboard):
        freeMoves = []
        eatMoves = []
        for move in moves:
            if chessboard[move[0]][move[1]] is not None:
                if chessboard[move[0]][move[1]].color != self.color:
                    eatMoves.append(move)
            else:
                freeMoves.append(move)
        return freeMoves, eatMoves

class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, "pawn", x, y)
        self.firstMove = True
        
    def findMoves(self, chessboard):
        moves = []
        direction = 1 if self.color == "black" else -1
        moves.append((self.x, self.y + direction))

        if self.firstMove:
            moves.append((self.x, self.y + 2 * direction))

        for i in [-1, 1]:
            new_x = self.x + i
            new_y = self.y + direction
            if 0 <= new_x < 8 and 0 <= new_y < 8 and chessboard[new_x][new_y] is not None:
                moves.append((new_x, new_y))

        return moves

class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, "rook", x, y)

    def findMoves(self,chessboard):
        moves = []
        # Left
        for i in range(self.x - 1, -1, -1):
            if chessboard[i][self.y] is None:
                moves.append((i, self.y))
            else:
                break

        # Right
        for i in range(self.x + 1, len(chessboard)):
            if chessboard[i][self.y] is None:
                moves.append((i, self.y))
            else:
                break

        # Up
        for i in range(self.y - 1, -1, -1):
            if chessboard[self.x][i] is None:
                moves.append((self.x, i))
            else:
                break

        # Down
        for i in range(self.y + 1, len(chessboard[0])):
            if chessboard[self.x][i] is None:
                moves.append((self.x, i))
            else:
                break

        return moves


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, "knight", x, y)

    def findMoves(self , chessboard):
        x, y = self.x, self.y
        moves = [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                 (x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2)]

        valid_moves = [(x, y) for x, y in moves if 0 <= x < 8 and 0 <= y < 8]
        return valid_moves
class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, "bishop", x, y)

    def findMoves(self, chessboard):
        moves = []
        x, y = self.x, self.y

        # Top-right diagonal
        for i in range(1, min(7 - x, 7 - y)+1):
            if chessboard[x + i][y + i] is None:
                moves.append((x + i, y + i))
            else:
                if chessboard[x + i][y + i].color != self.color:
                    moves.append((x + i, y + i))
                break

        # Top-left diagonal
        for i in range(1, min(x, 7 - y)+1):
            if chessboard[x - i][y + i] is None:
                moves.append((x - i, y + i))
            else:
                if chessboard[x - i][y + i].color != self.color:
                    moves.append((x - i, y + i))
                break

        # Bottom-right diagonal
        for i in range(1, min(7 - x, y)+1):
            if chessboard[x + i][y - i] is None:
                moves.append((x + i, y - i))
            else:
                if chessboard[x + i][y - i].color != self.color:
                    moves.append((x + i, y - i))
                break

        # Bottom-left diagonal
        for i in range(1, min(x, y)+1):
            if chessboard[x - i][y - i] is None:
                moves.append((x - i, y - i))
            else:
                if chessboard[x - i][y - i].color != self.color:
                    moves.append((x - i, y - i))
                break

        return moves




class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, "queen", x, y)

    def findMoves(self , chessboard):
        moves = []
        x, y = self.x, self.y
        # Left
        for i in range(self.x - 1, -1, -1):
            if chessboard[i][self.y] is None:
                moves.append((i, self.y))
            else:
                break

        # Right
        for i in range(self.x + 1, len(chessboard)):
            if chessboard[i][self.y] is None:
                moves.append((i, self.y))
            else:
                break

        # Up
        for i in range(self.y - 1, -1, -1):
            if chessboard[self.x][i] is None:
                moves.append((self.x, i))
            else:
                break

        # Down
        for i in range(self.y + 1, len(chessboard[0])):
            if chessboard[self.x][i] is None:
                moves.append((self.x, i))
            else:
                break
            
        # Top-right diagonal
        for i in range(1, min(7 - x, 7 - y)+1):
            if chessboard[x + i][y + i] is None:
                moves.append((x + i, y + i))
            else:
                if chessboard[x + i][y + i].color != self.color:
                    moves.append((x + i, y + i))
                break

        # Top-left diagonal
        for i in range(1, min(x, 7 - y)+1):
            if chessboard[x - i][y + i] is None:
                moves.append((x - i, y + i))
            else:
                if chessboard[x - i][y + i].color != self.color:
                    moves.append((x - i, y + i))
                break

        # Bottom-right diagonal
        for i in range(1, min(7 - x, y)+1):
            if chessboard[x + i][y - i] is None:
                moves.append((x + i, y - i))
            else:
                if chessboard[x + i][y - i].color != self.color:
                    moves.append((x + i, y - i))
                break

        # Bottom-left diagonal
        for i in range(1, min(x, y)+1):
            if chessboard[x - i][y - i] is None:
                moves.append((x - i, y - i))
            else:
                if chessboard[x - i][y - i].color != self.color:
                    moves.append((x - i, y - i))
                break
        return moves


    
    
class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, "king", x, y)

    def findMoves(self , chessboard):
        moves = [
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
            (self.x + 1, self.y + 1),
            (self.x - 1, self.y - 1),
            (self.x + 1, self.y - 1),
            (self.x - 1, self.y + 1),
        ]

        valid_moves = [(x, y) for x, y in moves if 0 <= x < 8 and 0 <= y < 8]
        return valid_moves

