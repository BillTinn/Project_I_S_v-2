import random
from typing import Optional
from schnapsen.game import Bot, Score, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove, GamePhase, Marriage
from schnapsen.deck import Card, Suit, Rank

class BullyBot(Bot):
    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rand = rand

    def __repr__(self) -> str:
        return f"BullyBot(rand={self.rand})"

    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        my_valid_moves = player_perspective.valid_moves()
        trump_suit_moves: list[Move] = []

        trump_suit: Suit = player_perspective.get_trump_suit()

        for move in my_valid_moves:
            cards_of_move: list[Card] = move.cards
            card_of_move: Card = cards_of_move[0]

            if card_of_move.suit == trump_suit:
                trump_suit_moves.append(move)

        if len(trump_suit_moves) > 0:
            random_trump_suit_move = self.rand.choice(trump_suit_moves)
            return random_trump_suit_move

        if not player_perspective.am_i_leader():
            assert leader_move is not None
            leader_suit: Suit = leader_move.cards[0].suit
            leaders_suit_moves: list[Move] = []

            for move in my_valid_moves:
                cards_of_move = move.cards
                card_of_move = cards_of_move[0]

                if card_of_move.suit == leader_suit:
                    leaders_suit_moves.append(move)

            if len(leaders_suit_moves) > 0:
                random_leader_suit_move = self.rand.choice(leaders_suit_moves)
                return random_leader_suit_move

        my_hand_cards: list[Card] = player_perspective.get_hand().cards

        schnapsen_trick_scorer = SchnapsenTrickScorer()

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