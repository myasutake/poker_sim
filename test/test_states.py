import pytest

import common.table


@pytest.fixture(scope='function')
def table_init() -> common.table.Table():
    return common.table.Table()


@pytest.fixture(scope='function')
def table_preflop(table_init) -> common.table.Table():
    table = table_init
    table.run()
    return table


@pytest.fixture(scope='function')
def table_preflop_after_hero_hand_change(monkeypatch, table_preflop) -> common.table.Table():
    table = table_preflop

    monkeypatch.setattr('builtins.input', lambda _: "1")
    table.run()

    return table


class TestInit:

    @staticmethod
    def test_init_state_is_init(table_init):
        assert type(table_init.state) == common.table.Init

    @staticmethod
    def test_init_auto_transitions_to_preflop(table_init):
        table = table_init
        table.run()
        assert type(table.state) == common.table.PreFlop


class TestPreFlop:

    # Table properties

    @staticmethod
    def test_deck_stub_has_50_cards(table_preflop):
        assert table_preflop.deck.number_of_cards_not_dealt == 50

    # State transitions

    @staticmethod
    def test_hero_change_hand_transitions_to_preflop(monkeypatch, table_preflop):
        # Monkeypatch the input(), simulate user intput "1":
        monkeypatch.setattr('builtins.input', lambda _: "1")

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.PreFlop

    @staticmethod
    def test_hero_change_seat_transitions_to_preflop(monkeypatch, table_preflop):
        monkeypatch.setattr('builtins.input', lambda _: "2")

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.PreFlop

    @staticmethod
    def test_villain_change_seat_transitions_to_preflop(monkeypatch, table_preflop):
        monkeypatch.setattr('builtins.input', lambda _: "3")

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.PreFlop


class TestPreFlopAfterHeroHandChange:

    @staticmethod
    def test_deck_stub_has_50_cards(table_preflop_after_hero_hand_change):
        assert table_preflop_after_hero_hand_change.deck.number_of_cards_not_dealt == 50
