import cards


class TestCard:

    # Ranks

    def test_valid_ranks(self) -> None:
        for i_rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K']:
            card = cards.Card(rank=i_rank, suit='c')
            assert card.rank == i_rank
        return

    def test_lower_case_ranks_should_pass(self) -> None:
        for i_rank in ['a', 'j', 'q', 'k']:
            card = cards.Card(rank=i_rank, suit='c')
            assert card.rank == i_rank.upper()
        return

    def test_rank_1_raises_value_error(self) -> None:
        try:
            cards.Card(rank='1', suit='c')
        except ValueError:
            return
        else:
            assert False, 'No exception was raised.'

    # Suits

    def test_valid_suits(self) -> None:
        for i_suit in ['c', 'd', 'h', 's']:
            card = cards.Card(rank='2', suit=i_suit)
            assert card.suit == i_suit
        return

    def test_upper_case_suits_should_pass(self) -> None:
        for i_suit in ['C', 'D', 'H', 'S']:
            card = cards.Card(rank='2', suit=i_suit)
            assert card.suit == i_suit.lower()
        return
