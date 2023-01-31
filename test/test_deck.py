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
