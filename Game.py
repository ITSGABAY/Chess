import pygame
import sys
from Pieces import *
from pprint import pprint
import time
class ChessGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Initialize selected_piece outside the game loop
        self.selected_piece = None
        self.target_box = None
        self.free_moves = []
        self.eat_moves = []
        self.turn = "white"
        self.winner = None
        self.whiteCheck = False
        self.blackCheck = False
        self.turnFinished = False

        # Set up the display
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Board")

        # Create a 2D array representing the chessboard
        self.chessboard = [[None for _ in range(8)] for _ in range(8)]

        # Add white pieces to the chessboard
        self.initialize_pieces("white", 0, 1)
        
        # Add black pieces to the chessboard
        self.initialize_pieces("black", 7, 6)

        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        
    def findKing(self , color):
        for piece in self.chessboard:    
            if isinstance(piece, King):
                if piece.color == color:
                    return piece

        
    def checkForCheck(self, color):
        piecesEatMoves = []
        for row in self.chessboard:
            for piece in row:
                if piece is not None:
                    if piece.color != color:
                        _, eatMoves = piece.organizeMoves(
                            piece.findMoves(self.chessboard), self.chessboard
                        )
                        piecesEatMoves.extend(eatMoves)

        for move in piecesEatMoves:
            print("🐍 File: Chess/Game.py | Line: 58 | checkForCheck ~ piecesEatMoves", piecesEatMoves)
            print("🐍 File: Chess/Game.py | Line: 58 | checkForCheck ~ move", move)
            piece = self.chessboard[move[0]][move[1]]
            flag = False
            if piece is not None:
                if piece.name == "king" and piece.color != color:
                    flag = True
                    if color == "white":
                        self.whiteCheck = True
                    else:
                        self.blackCheck = True
            if not flag:
                self.whiteCheck = False
                self.blackCheck = False

    def initialize_pieces(self, color, back_row, front_row):
        self.chessboard[back_row][0] = Rook(color, back_row, 0)
        self.chessboard[back_row][1] = Knight(color, back_row, 1)
        self.chessboard[back_row][2] = Bishop(color, back_row, 2)
        self.chessboard[back_row][3] = Queen(color, back_row, 3)
        self.chessboard[back_row][4] = King(color, back_row, 4)
        self.chessboard[back_row][5] = Bishop(color, back_row, 5)
        self.chessboard[back_row][6] = Knight(color, back_row, 6)
        self.chessboard[back_row][7] = Rook(color, back_row, 7)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.screen, color, (col * self.WIDTH // 8, row * self.HEIGHT // 8,
                                                      self.WIDTH // 8, self.HEIGHT // 8))

    def draw_pieces(self):
        for col_index, row in enumerate(self.chessboard):
            for row_index, piece in enumerate(row):
                if piece is not None:
                    image = pygame.image.load(piece.image)
                    image = pygame.transform.scale(image, (100, 100))
                    self.screen.blit(image, (row_index * 100, col_index * 100))

    def draw_boxes_borders(self, moves, color):
        moves_list = list(moves)
        for move in moves_list:
            pygame.draw.rect(self.screen, color, (move[1] * 100, move[0] * 100, 100, 100), 5)

    def handle_piece_selection(self, row_clicked, col_clicked, color):
        piece_clicked = self.chessboard[row_clicked][col_clicked]
        if self.selected_piece is None and piece_clicked.color == color:
            if piece_clicked is not None:
                self.selected_piece = piece_clicked
                self.free_moves, self.eat_moves = self.selected_piece.organizeMoves(
                    self.selected_piece.findMoves(self.chessboard), self.chessboard
                )
                self.draw_boxes_borders(self.free_moves, self.BLUE)
                self.draw_boxes_borders(self.eat_moves, self.RED)
                pygame.display.flip()
        else:
            self.target_box = (row_clicked, col_clicked)
            if self.move_piece():
                self.selected_piece = None
                self.target_box = None
                pygame.display.flip()
                self.turnFinished = True  

    def handle_events(self , color):
        pass
    
    def checkForPawnUpgrade(self):
        for i in range(8):
            piece = self.chessboard[0][i]
            if piece is not None:
                if piece.name == "pawn" and piece.color == "black":
                    self.upgradePawn(0 , i)
        for i in range(8):
            piece = self.chessboard[7][i]
            if piece is not None:
                if piece.name == "pawn" and piece.color == "white":
                    self.chessboard[7][i] = self.upgradePawn(0 , i , piece.color)                
    
    def upgrade_pawn(x, y, color):
        # Display a menu or prompt for the player to choose the promotion piece
        promotion_options = ["Queen", "Rook", "Bishop", "Knight"]

        pygame.init()
        font = pygame.font.Font(None, 36)

        screen = pygame.display.set_mode((300, 200))
        pygame.display.set_caption("Pawn Promotion")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))

            text = font.render("Choose promotion:", True, (0, 0, 0))
            screen.blit(text, (20, 20))

            for i, option in enumerate(promotion_options):
                text = font.render(option, True, (0, 0, 0))
                screen.blit(text, (20, 60 + i * 40))

            pygame.display.flip()
            clock.tick(30)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                pygame.quit()
                return Queen(color, x, y)
            elif keys[pygame.K_2]:
                pygame.quit()
                return Rook(color, x, y)
            elif keys[pygame.K_3]:
                pygame.quit()
                return Bishop(color, x, y)
            elif keys[pygame.K_4]:
                pygame.quit()
                return Knight(color, x, y)
            
    def checkStalemate(self , color):
        flag = False
        for row in self.chessboard:
            for piece in row:
                if piece is not None:
                        if piece.color == color:
                            if piece.organizeMoves(
                            piece.findMoves(self.chessboard), self.chessboard
                            ) != ([] , []):
                                return False
        return True
    
    def display_end_message(result):
        pygame.init()
        font = pygame.font.Font(None, 36)

        screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Game Over")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))

            if result == "white":
                text = font.render("White Won!", True, (0, 0, 0))
            if result == "black":
                text = font.render("Black Won!", True, (0, 0, 0))
            elif result == "draw":
                text = font.render("It's a draw!", True, (0, 0, 0))
            else:
                pygame.quit()
                return

            screen.blit(text, (20, 20))

            pygame.display.flip()
            clock.tick(30)
    def display_check_alert(color):
        pygame.init()
        font = pygame.font.Font(None, 36)

        screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Check Alert")

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))

            text = font.render(color , " are in check!", True, (255, 0, 0))
            screen.blit(text, (20, 20))

            pygame.display.flip()
            clock.tick(30)
    
    def move_piece(self):
        pass

    
    def run_game(self):
        pass
    
class OfflineChessGame(ChessGame):
    def __init__(self):
        super().__init__()

    
    def handle_events(self , color):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    col_clicked = mouse_x // (self.WIDTH // 8)
                    row_clicked = mouse_y // (self.HEIGHT // 8)
                    self.handle_piece_selection(row_clicked, col_clicked ,  color)
        return True


    def move_piece(self):
        if self.selected_piece is not None and self.target_box is not None:
            if self.target_box in self.free_moves or self.target_box in self.eat_moves:
                self.chessboard[self.selected_piece.x][self.selected_piece.y] = None
                self.selected_piece.x , self.selected_piece.y = self.target_box[0] , self.target_box[1]
                self.chessboard[self.target_box[0]][self.target_box[1]] = self.selected_piece
                self.free_moves, self.eat_moves = [] , []
                return True
        return False

    def run_game(self):
        running = True
        self.draw_board()
        self.draw_pieces()
        pygame.display.update()
        self.turn = "white"
        
        while running:
            running = self.handle_events(self.turn)

            if self.turnFinished:
                self.turn = "black" if self.turn == "white" else "white"
                self.checkForPawnUpgrade()

                if self.checkStalemate(self.turn):
                    self.winner = "draw"
                    self.display_end_message("draw")
                    break

                self.checkForCheck(self.turn)
                self.turnFinished = False

            pygame.display.update()

        pygame.quit()
        sys.exit()





class OnlineChessGame(ChessGame):
    def __init__(self, playerColor , client):
        super().__init__()
        self.playerColor = playerColor
        self.client = client
        
    def move_piece(self):
        if self.selected_piece is not None and self.target_box is not None:
            if self.target_box in self.free_moves or self.target_box in self.eat_moves:
                self.chessboard[self.selected_piece.x][self.selected_piece.y] = None
                self.selected_piece.x , self.selected_piece.y = self.target_box[0] , self.target_box[1]
                self.chessboard[self.target_box[0]][self.target_box[1]] = self.selected_piece
                self.free_moves, self.eat_moves = [] , []
                action = f"{self.selected_piece.x},{self.selected_piece.y}, Move TO ,{self.target_box[0]},{self.target_box[1]}"
                self.client.send(action.encode())
                return True
        return False

    def moveOtherPlayer(self):
        action = self.client.recv(1024).decode()
        print("🐍 File: Chess/Game.py | Line: 336 | moveOtherPlayer ~ otherPlayerAction",action)
        actionParts = action.split(",")
        self.chessboard[actionParts[3]][actionParts[4]] = self.chessboard[int(actionParts[0])][actionParts[1]]
        self.chessboard[int(actionParts[0])][actionParts[1]] = None
        pygame.display.flip()
        self.turnFinished = True  
        
    def handle_events(self , color):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif self.playerColor!=self.turn : 
                self.moveOtherPlayer()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    col_clicked = mouse_x // (self.WIDTH // 8)
                    row_clicked = mouse_y // (self.HEIGHT // 8)
                    self.handle_piece_selection(row_clicked, col_clicked ,  color)
        return True


            

    def run_game(self):
        running = True
        self.draw_board()
        self.draw_pieces()
        pygame.display.update()
        self.turn = "white"
        
        while running:
            running = self.handle_events(self.turn)
            if self.turnFinished:
                self.turn = "black" if self.turn == "white" else "white"
                self.checkForPawnUpgrade()

                if self.checkStalemate(self.turn):
                    self.winner = "draw"
                    self.display_end_message("draw")
                    break

                self.checkForCheck(self.turn)
                self.turnFinished = False

            pygame.display.update()

        pygame.quit()
        sys.exit()