import chess
import random

class ChessEngine:
    def __init__(self, use_ai=True):
        self.board = chess.Board()
        self.use_ai = use_ai

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves) if legal_moves else None

    def evaluate_position(self):
        if self.board.is_checkmate():
            return -1000 if self.board.turn else 1000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value
        
        return score

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_position()
        
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

    def search_best_move(self, depth):
        if not self.use_ai:
            return self.get_random_move()
        
        best_move = None
        best_eval = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = self.minimax(depth - 1, False)
            self.board.pop()
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

    def make_move(self, move):
        self.board.push(move)

    def get_board_fen(self):
        return self.board.fen()

def play_game(ai_engine, random_engine):
    while not ai_engine.board.is_game_over():
        if ai_engine.board.turn == chess.WHITE:
            move = ai_engine.search_best_move(depth=3)
        else:
            move = random_engine.get_random_move()
        
        ai_engine.make_move(move)
        random_engine.make_move(move)
    
    result = ai_engine.board.result()
    if result == "1-0":
        return 1  # AI wins
    elif result == "0-1":
        return -1  # Random wins
    else:
        return 0  # Draw

def play_multiple_games(num_games):
    ai_wins = 0
    random_wins = 0
    draws = 0

    for _ in range(num_games):
        ai_engine = ChessEngine(use_ai=True)
        random_engine = ChessEngine(use_ai=False)
        result = play_game(ai_engine, random_engine)
        
        if result == 1:
            ai_wins += 1
        elif result == -1:
            random_wins += 1
        else:
            draws += 1
    
    print(f"AI Wins: {ai_wins}")
    print(f"Random Wins: {random_wins}")
    print(f"Draws: {draws}")

if __name__ == "__main__":
    play_multiple_games(1)