class Card:

    def __init__(self, rank: str, suit: str) -> None:
        self._verify_rank(value=rank)
        self._verify_suit(value=suit)
        self._rank = rank
        self._suit = suit
        return

    @property
    def rank(self) -> str:
        return self._rank.upper()

    @property
    def suit(self) -> str:
        return self._suit.lower()

    @staticmethod
    def _verify_rank(value: str) -> None:
        if value.upper() not in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']:
            raise ValueError(f"Invalid card rank '{value}' given.")
        return

    @staticmethod
    def _verify_suit(value: str) -> None:
        if value.lower() not in ['c', 'd', 'h', 's']:
            raise ValueError(f"Invalid card suit '{value}' given.")
        return
