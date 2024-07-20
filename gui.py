import pygame
import sys
from chess_bot import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQ_SIZE = HEIGHT // 8
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
board_image = pygame.image.load('assets/board.svg')  # Replace with your own chessboard image
pieces_images = {
    'r': pygame.image.load('assets/bR.svg'),
    'n': pygame.image.load('assets/bN.svg'),
    'b': pygame.image.load('assets/bB.svg'),
    'q': pygame.image.load('assets/bQ.svg'),
    'k': pygame.image.load('assets/bK.svg'),
    'p': pygame.image.load('assets/bP.svg'),
    'R': pygame.image.load('assets/wR.svg'),
    'N': pygame.image.load('assets/wN.svg'),
    'B': pygame.image.load('assets/wB.svg'),
    'Q': pygame.image.load('assets/wQ.svg'),
    'K': pygame.image.load('assets/wK.svg'),
    'P': pygame.image.load('assets/wP.svg')
}

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Function to draw the chessboard
def draw_board(screen):
    colors = [WHITE, BLACK]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Function to draw pieces on the board
def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != ' ':
                piece_image = pieces_images[piece]
                # Resize the piece image to fit the square size
                piece_image = pygame.transform.scale(piece_image, (SQ_SIZE*3.5, SQ_SIZE*3.5))
                # Calculate the position to center the piece in the square
                x_pos = col * SQ_SIZE
                y_pos = row * SQ_SIZE
                # Draw the piece image at the calculated position
                screen.blit(piece_image, (x_pos, y_pos))

def fen_to_board(fen):
    board = []
    # Split the FEN string into its components
    parts = fen.split()
    # Piece placement is the first part of the FEN string
    piece_placement = parts[0]
    
    # Convert each rank from FEN to a list of pieces
    ranks = piece_placement.split('/')
    
    for rank in ranks:
        board_row = []
        for char in rank:
            if char.isdigit():
                # If the character is a number, it represents empty squares
                for _ in range(int(char)):
                    board_row.append(' ')
            else:
                # Otherwise, it represents a piece
                board_row.append(char)
        board.append(board_row)
    
    return board

# Main game loop
def main():
    clock = pygame.time.Clock()
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
