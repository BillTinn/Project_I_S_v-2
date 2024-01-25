import random
from typing import Optional
from schnapsen.game import Bot, Score, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove, GamePhase, Marriage
from schnapsen.deck import Card, Suit, Rank
from typing import List

class RiskSeekingBot(Bot):
    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rand = rand

    def __repr__(self) -> str:
        return f"RiskSeekingBot(rand={self.rand})"

    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
        schnapsen_trick_scorer = SchnapsenTrickScorer()

        # Check for marriage move
        marriage_move = self.play_marriage(player_perspective)
        if marriage_move is not None:
            return marriage_move
        else:
            # Get valid moves and trump suit
            my_valid_moves = player_perspective.valid_moves()
            trump_suit_moves: list[Move] = []
            trump_suit: Suit = player_perspective.get_trump_suit()

            # Filter valid moves with trump suit
            for move in my_valid_moves:
                cards_of_move: list[Card] = move.cards
                card_of_move: Card = cards_of_move[0]
                if card_of_move.suit == trump_suit:
                    trump_suit_moves.append(move)

            # If there are trump suit moves, play a random one
            if len(trump_suit_moves) > 0:
                random_trump_suit_move = self.rand.choice(trump_suit_moves)
                return random_trump_suit_move

            # If not the leader, play the highest-ranking card in the leader's suit
            if not player_perspective.am_i_leader():
                assert leader_move is not None
                leader_suit: Suit = leader_move.cards[0].suit
                leaders_suit_moves: list[Move] = []

                # Filter valid moves with leader's suit
                for move in my_valid_moves:
                    cards_of_move = move.cards
                    card_of_move = cards_of_move[0]

                    if card_of_move.suit == leader_suit:
                        leaders_suit_moves.append(move)

                # Play the highest-ranking card in the leader's suit
                if len(leaders_suit_moves) > 0:
                    sorted_leader_suit_move = sorted(leaders_suit_moves, key=lambda move: schnapsen_trick_scorer.rank_to_points(move.card.rank), reverse=True)
                    highest_leader_suit_move = sorted_leader_suit_move[0]
                    return highest_leader_suit_move

            # Play the highest-ranking card in the hand if no specific strategy applies
            my_hand_cards: list[Card] = player_perspective.get_hand().cards

            highest_card_score: int = -1
            card_with_highest_score: Optional[Card] = None
            for card in my_hand_cards:
                card_score = schnapsen_trick_scorer.rank_to_points(card.rank)
                if card_score > highest_card_score:
                    highest_card_score = card_score
                    card_with_highest_score = card

            assert card_with_highest_score is not None

            move_of_card_with_highest_score = RegularMove(card_with_highest_score)

            assert move_of_card_with_highest_score in my_valid_moves

            return move_of_card_with_highest_score
    
    def play_marriage(self, player_perspective: PlayerPerspective) -> Move | None:
        # Check for marriage move
        for move in player_perspective.valid_moves():
            if move.is_marriage():
                return move
        return None