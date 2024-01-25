import random
from typing import Optional
from schnapsen.game import Bot, Score, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove, GamePhase, Marriage
from schnapsen.deck import Card, Suit, Rank
from typing import List

class RiskAverseBot(Bot):
    
    def play_marriage(self, perspective: PlayerPerspective) -> Move | None:
    # If the bot has a marriage, play it
        for move in perspective.valid_moves():
            if move.is_marriage:
                return move
        return None
    
    def play_low_value_card(self, valid_moves: List[Move]) -> Move | None:
        # Sort valid moves by card value (low to high)
        points_dict = {Rank.ACE: 11, Rank.TEN: 10, Rank.KING: 4, Rank.QUEEN: 3, Rank.JACK: 2}
        valid_moves = sorted(valid_moves, key=lambda move: points_dict[move.cards[0].rank])
        
        # Play the lowest value card
        return valid_moves[0] if valid_moves else None

    def avoid_trump_card(self, perspective: PlayerPerspective) -> Move | None:
        # Avoid playing a trump card if possible
        non_trump_moves = [move for move in perspective.valid_moves() if move.cards[0].suit != perspective.get_trump_suit()]
        
        # If there are non-trump moves, play the lowest value non-trump card
        if non_trump_moves:
            return self.play_low_value_card(non_trump_moves)
        
        # Play a trump card if available
        trump_moves = [move for move in perspective.valid_moves() if move.cards[0].suit == perspective.get_trump_suit()]
        return trump_moves[0] if trump_moves else None
    
    def play_high_value_card(self, valid_moves: List[Move]) -> Move | None:
        # Sort valid moves by card value (high to low)
        points_dict = {Rank.ACE: 11, Rank.TEN: 10, Rank.KING: 4, Rank.QUEEN: 3, Rank.JACK: 2}
        valid_moves = sorted(valid_moves, key=lambda move: points_dict[move.cards[0].rank], reverse=True)
        
        # Play the highest value card
        return valid_moves[0] if valid_moves else None
    
    def play_trump_card(self, perspective: PlayerPerspective) -> Move | None:
        # Play a trump card if available
        trump_moves = [move for move in perspective.valid_moves() if move.cards[0].suit == perspective.get_trump_suit()]
        return trump_moves[0] if trump_moves else None
    
    def total_points(self, score: Score) -> int:
        """Return the total points (direct points plus pending points)."""
        return score.direct_points + score.pending_points

    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        my_score = self.total_points(perspective.get_my_score())
        opponent_score = self.total_points(perspective.get_opponent_score())

        # If 10 or more points behind in score, play a trump card or highest card
        if my_score < opponent_score - 5:
            trump_move = self.play_trump_card(perspective)
            if trump_move:
                return trump_move
            else:
                high_value_move = self.play_high_value_card(perspective.valid_moves())
                if high_value_move:
                    return high_value_move

        # If 20 or more points ahead in score, play aggressively by playing a trump card or highest card
        if my_score > opponent_score + 5:
            trump_move = self.play_trump_card(perspective)
            if trump_move:
                return trump_move
            else:
                high_value_move = self.play_high_value_card(perspective.valid_moves())
                if high_value_move:
                    return high_value_move

        # If not significantly behind or ahead in score, play a marriage if possible and avoid trump cards
        return self.play_marriage(perspective) or self.avoid_trump_card(perspective)