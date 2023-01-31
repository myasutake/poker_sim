import pytest

import cards


@pytest.fixture(scope='function')
def deck() -> cards.Deck:
    return cards.Deck()


class TestDeck:

    def test_new_deck_has_0_cards_dealt(self, deck) -> None:
        assert deck.number_of_cards_dealt == 0
        return

    def test_new_deck_has_52_cards_not_dealt(self, deck) -> None:
        assert deck.number_of_cards_not_dealt == 52
        return

    def test_shuffle_returns_0_cards_dealt(self, deck) -> None:
        deck.shuffle()
        assert deck.number_of_cards_dealt == 0
        return

    def test_shuffle_returns_52_cards_not_dealt(self, deck) -> None:
        deck.shuffle()
        assert deck.number_of_cards_not_dealt == 52
        return


class TestDealCard:

    def test_deal_card_increments_cards_dealt(self, deck) -> None:
        deck.deal_card()
        assert deck.number_of_cards_dealt == 1
        return

    def test_deal_card_decrements_cards_not_dealt(self, deck) -> None:
        deck.deal_card()
        assert deck.number_of_cards_not_dealt == 51
        return

    def test_deal_cards_returns_correct_number_of_cards(self, deck) -> None:
        cards_dealt = deck.deal_cards(number_of_cards=5)
        assert len(cards_dealt) == 5
        return