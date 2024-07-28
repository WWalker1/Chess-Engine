import chess
import random
from gui import *
import time
from tables import PSQT
import pygame

def play_against_ai(ai_engine, search_depth=4, player_color=chess.WHITE):
    clock = pygame.time.Clock()
    board = fen_to_board(ai_engine.board.fen())
    selected_square = None

    running = True
    while running and not ai_engine.board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ai_engine.board.turn == player_color:
                x, y = pygame.mouse.get_pos()
                clicked_square = (y // SQ_SIZE, x // SQ_SIZE)

                if selected_square is None:
                    selected_square = clicked_square
                else:
                    move = chess.Move(chess.square(selected_square[1], 7 - selected_square[0]),
                                      chess.square(clicked_square[1], 7 - clicked_square[0]))
                    if move in ai_engine.board.legal_moves:
                        ai_engine.make_move(move)
                        selected_square = None
                    else:
                        selected_square = clicked_square

        if ai_engine.board.turn != player_color:
            move = ai_engine.search_best_move(depth=search_depth)
            ai_engine.make_move(move)

        board = fen_to_board(ai_engine.board.fen())

        screen.fill(WHITE)
        draw_board(screen)
        draw_pieces(screen, board)
        if selected_square:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(selected_square[1] * SQ_SIZE,
                                                                selected_square[0] * SQ_SIZE,
                                                                SQ_SIZE, SQ_SIZE), 4)
        pygame.display.flip()
        clock.tick(FPS)

    if ai_engine.board.is_checkmate():
        print("Checkmate!")
    elif ai_engine.board.is_stalemate():
        print("Stalemate!")
    elif ai_engine.board.is_insufficient_material():
        print("Draw due to insufficient material!")

class ChessEngine:
    def __init__(self, use_ai=True):
        self.board = chess.Board()
        self.use_ai = use_ai
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None

    def is_endgame(self):
        total_material = sum(len(self.board.pieces(piece_type, chess.WHITE) | self.board.pieces(piece_type, chess.BLACK)) * value
                             for piece_type, value in self.piece_values.items() if piece_type != chess.KING)
        return total_material <= 2600  # Threshold for endgame (roughly equivalent to a queen and a rook)

    def evaluate_position(self):
        if self.board.is_checkmate():
            return -1000000 if self.board.turn else 1000000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        
        score = 0
        is_endgame = self.is_endgame()
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_value = self.piece_values[piece.piece_type]
                psqt_value = PSQT[piece.piece_type][square if piece.color == chess.WHITE else chess.square_mirror(square)]
                
                if is_endgame:
                    score += (piece_value + psqt_value[1]) if piece.color == chess.WHITE else -(piece_value + psqt_value[1])
                else:
                    score += (piece_value + psqt_value[0]) if piece.color == chess.WHITE else -(piece_value + psqt_value[0])
        
        return score

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_position() if self.board.turn == chess.WHITE else -self.evaluate_position()
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_position() if self.board.turn == chess.WHITE else -self.evaluate_position()
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.alpha_beta(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.alpha_beta(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def search_best_move(self, depth):
        if not self.use_ai:
            return self.get_random_move()
        
        best_move = None
        if self.board.turn == chess.WHITE:
            best_eval = float('-inf')
        else:
            best_eval = float('inf')

        alpha = float('-inf')
        beta = float('inf')

        start_time = time.time()

        for move in self.board.legal_moves:
            self.board.push(move)
            eval = self.alpha_beta(depth - 1, alpha, beta, self.board.turn != chess.WHITE)
            self.board.pop()
            
            if self.board.turn == chess.WHITE:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                alpha = max(alpha, best_eval)
            else:
                if eval < best_eval:
                    best_eval = eval
                    best_move = move
                beta = min(beta, best_eval)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time < 0.5:
            time.sleep(0.5 - elapsed_time)
        
        return best_move
    def make_move(self, move):
        self.board.push(move)

    def get_board_fen(self):
        return self.board.fen()

def play_game(ai_engine1, ai_engine2, search_depth=3):
    clock = pygame.time.Clock()
    board = fen_to_board(ai_engine1.board.fen())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        while not ai_engine1.board.is_game_over():
            if ai_engine1.board.turn == chess.WHITE:
                move = ai_engine1.search_best_move(depth=search_depth)
                ai_engine1.make_move(move)
                ai_engine2.make_move(move)  # Synchronize the boards
            else:
                move = ai_engine2.search_best_move(depth=search_depth)
                ai_engine1.make_move(move)
                ai_engine2.make_move(move)  # Both engines make the same move

            board = fen_to_board(ai_engine1.board.fen())

            screen.fill(WHITE)
            draw_board(screen)
            draw_pieces(screen, board)
            pygame.display.flip()
            clock.tick(FPS)

        print("Game Over!")
        print("Result:", ai_engine1.board.result())
        input("Press Enter to continue...")
        running = False
        pygame.quit()

    result = ai_engine1.board.result()
    if result == "1-0":
        return 1  # White wins
    elif result == "0-1":
        return -1  # Black wins
    else:
        return 0  # Draw

def play_multiple_games(num_games, mode='ai_vs_ai', search_depth=3):
    ai_wins = 0
    player_wins = 0
    draws = 0

    for game_num in range(num_games):
        pygame.init()  # Reinitialize Pygame for each game
        screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Recreate the screen
        pygame.display.set_caption('Chess Game')

        ai_engine1 = ChessEngine(use_ai=True)
        ai_engine2 = ChessEngine(use_ai=True)
        
        if mode == 'ai_vs_ai':
            print(f"\nGame {game_num + 1}:")
            result = play_game(ai_engine1, ai_engine2, search_depth=search_depth)
            
            if result == 1:
                ai_wins += 1
                print("White wins!")
            elif result == -1:
                player_wins += 1
                print("Black wins!")
            else:
                draws += 1
                print("It's a draw!")
        elif mode == 'player_vs_ai':
            play_against_ai(ai_engine1, search_depth=search_depth, player_color=chess.WHITE)
        
        pygame.quit()  # Quit Pygame after each game
    
    if mode == 'ai_vs_ai':
        print(f"\nFinal Results:")
        print(f"White Wins: {ai_wins}")
        print(f"Black Wins: {player_wins}")
        print(f"Draws: {draws}")

if __name__ == "__main__":
    mode = input("Select mode (ai_vs_ai/player_vs_ai): ")
    if mode == 'ai_vs_ai':
        num_games = int(input("Enter the number of games to play: "))
        search_depth = int(input("Enter search depth for AI (3-4 recommended): "))
        play_multiple_games(num_games, mode=mode, search_depth=search_depth)
    elif mode == 'player_vs_ai':
        search_depth = int(input("Enter search depth for AI (3-4 recommended): "))
        play_multiple_games(1, mode=mode, search_depth=search_depth)
    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    play_multiple_games(1)