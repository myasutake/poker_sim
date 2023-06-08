import pytest

from common import cards


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


class TestCardBelongsToDeck:

    def test_card_belongs_to_this_deck(self, deck) -> None:
        card_from_this_deck = deck.deal_card()
        try:
            deck._verify_card_belongs_to_this_deck(card=card_from_this_deck)
        except ValueError:
            assert False, 'Deck thinks card pulled from its own deck came from another deck.'
        except:
            assert False, 'Wrong exception raised.'
        return

    def test_card_from_another_deck(self, deck) -> None:
        card_from_another_deck = cards.Card(rank='K', suit='c')
        try:
            deck._verify_card_belongs_to_this_deck(card=card_from_another_deck)
        except ValueError:
            return
        except:
            assert False, 'Wrong exception raised.'
        else:
            assert False, 'Deck thinks card pulled from another deck came from its own deck.'


class TestReturnCardToDeck:

    def test_card_not_dealt_after_returned(self, deck) -> None:
        card = deck.deal_card()
        deck.return_card_to_deck(card=card)
        assert not card.dealt
        return

    def test_number_of_cards_dealt_after_card_returned(self, deck) -> None:
        card = deck.deal_card()
        deck.return_card_to_deck(card=card)
        assert deck.number_of_cards_dealt == 0
        return

    def test_number_of_cards_not_dealt_after_card_returned(self, deck) -> None:
        card = deck.deal_card()
        deck.return_card_to_deck(card=card)
        assert deck.number_of_cards_not_dealt == 52
        return
