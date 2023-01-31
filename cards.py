import random


class Card:

    def __init__(self, rank: str, suit: str) -> None:
        self._verify_rank(value=rank)
        self._verify_suit(value=suit)
        self._rank = rank
        self._suit = suit
        self._dealt = False
        return

    @property
    def rank(self) -> str:
        return self._rank.upper()

    @property
    def suit(self) -> str:
        return self._suit.lower()

    @property
    def dealt(self) -> bool:
        return self._dealt

    @dealt.setter
    def dealt(self, value) -> None:
        self._dealt = value
        return

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


class Deck:

    def __init__(self) -> None:
        self._cards = []
        self.shuffle()
        return

    # Properties

    @property
    def list_of_all_cards(self) -> list[Card]:
        return self._cards

    @property
    def list_of_all_cards_dealt(self) -> list[Card]:
        card_list = []
        for i_card in self.list_of_all_cards:
            if i_card.dealt:
                card_list.append(i_card)
        return card_list

    @property
    def list_of_all_cards_not_dealt(self) -> list[Card]:
        card_list = []
        for i_card in self.list_of_all_cards:
            if not i_card.dealt:
                card_list.append(i_card)
        return card_list

    @property
    def number_of_cards_dealt(self) -> int:
        return len(self.list_of_all_cards_dealt)

    @property
    def number_of_cards_not_dealt(self) -> int:
        return len(self.list_of_all_cards_not_dealt)

    # Actions

    def deal_card(self) -> Card:
        card = random.choice(self.list_of_all_cards_not_dealt)
        card.dealt = True
        return card

    def deal_cards(self, number_of_cards) -> list[Card]:
        cards = []
        for i in range(0, number_of_cards):
            cards.append(self.deal_card())
        return cards

    def shuffle(self) -> None:
        self._cards = []
        for i_rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']:
            for i_suit in ['c', 'd', 'h', 's']:
                i_card = Card(rank=i_rank, suit=i_suit)
                self._cards.append(i_card)
        return
