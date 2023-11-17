import pygame
import sys
from Pieces import *
from pprint import pprint

class ChessGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

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

        # Initialize selected_piece outside the game loop
        self.selected_piece = None
        self.target_box = None
        self.free_moves = []
        self.eat_moves = []

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

    def handle_piece_selection(self, row_clicked, col_clicked):
        piece_clicked = self.chessboard[row_clicked][col_clicked]
        print("-----------------------------------------------------------------------")
        print("🐍 File: Chess/Game.py | Line: 71 | handle_piece_selection ~ self.selected_piece",self.selected_piece)
        print("🐍 File: Chess/Game.py | Line: 83 | handle_piece_selection ~ self.target_box",self.target_box)
        print("🐍 File: Chess/Game.py | Line: 77 | handle_piece_selection ~ self.free_moves, self.eat_moves",self.free_moves, self.eat_moves)
        if self.selected_piece is None:
            self.selected_piece = piece_clicked
            self.free_moves, self.eat_moves = self.selected_piece.organizeMoves(
                self.selected_piece.findMoves(self.chessboard), self.chessboard
            )
            self.draw_boxes_borders(self.free_moves, self.BLUE)
            self.draw_boxes_borders(self.eat_moves, self.RED)
            pygame.display.flip()
            print("🐍 File: Chess/Game.py | Line: 71 | handle_piece_selection ~ self.selected_piece",self.selected_piece)
            print("🐍 File: Chess/Game.py | Line: 83 | handle_piece_selection ~ self.target_box",self.target_box)
        else:
            self.target_box = (row_clicked, col_clicked)
            self.move_piece()
            print("🐍 File: Chess/Game.py | Line: 71 | handle_piece_selection ~ self.selected_piece",self.selected_piece)
            print("🐍 File: Chess/Game.py | Line: 83 | handle_piece_selection ~ self.target_box",self.target_box)
            self.selected_piece = None
            self.target_box = None
            print("🐍 File: Chess/Game.py | Line: 77 | handle_piece_selection ~ self.free_moves, self.eat_moves",self.free_moves, self.eat_moves)
            pprint(self.chessboard)
            pygame.display.flip()




    def move_piece(self):
        if self.selected_piece is not None and self.target_box is not None:
            if self.target_box in self.free_moves or self.target_box in self.eat_moves:
                self.chessboard[self.selected_piece.x][self.selected_piece.y] = None
                self.selected_piece.x , self.selected_piece.y = self.target_box[0] , self.target_box[1]
                self.chessboard[self.target_box[0]][self.target_box[1]] = self.selected_piece
                self.free_moves, self.eat_moves = [] , []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    col_clicked = mouse_x // (self.WIDTH // 8)
                    row_clicked = mouse_y // (self.HEIGHT // 8)
                    self.handle_piece_selection(row_clicked, col_clicked)

        return True

    def run_game(self):
        running = True
        while running:
            self.draw_board()
            self.draw_pieces()
            running = self.handle_events()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGame()
    game.run_game()
