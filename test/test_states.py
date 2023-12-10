import pytest

import common.table


prompt_options = {
    'START_OVER': 'N',
    'QUIT': 'Q',
    'HERO_CHANGE_HAND': 'H',
    'HERO_CHANGE_SEAT': 'S',
    'VILLAIN_CHANGE_SEAT': 'V',
    'FLOP': 'F',
}


@pytest.fixture(scope='function')
def table_init() -> common.table.Table():
    return common.table.Table()


@pytest.fixture(scope='function')
def table_preflop(table_init) -> common.table.Table():
    table = table_init
    table.run()
    return table


@pytest.fixture(scope='function')
def table_preflop_after_start_over(monkeypatch, table_preflop) -> common.table.Table():
    table = table_preflop

    monkeypatch.setattr('builtins.input', lambda _: prompt_options['START_OVER'])
    table.run()
    # table is now in Init state
    table.run()
    # table is now in PreFlop state

    return table


@pytest.fixture(scope='function')
def table_preflop_after_hero_hand_change(monkeypatch, table_preflop) -> common.table.Table():
    table = table_preflop

    monkeypatch.setattr('builtins.input', lambda _: prompt_options['HERO_CHANGE_HAND'])
    table.run()

    return table


@pytest.fixture(scope='function')
def table_flop(monkeypatch, table_preflop) -> common.table.Table():
    table = table_preflop

    monkeypatch.setattr('builtins.input', lambda _: prompt_options['FLOP'])
    table.run()

    return table


@pytest.fixture(scope='function')
def table_flop_after_reflop(monkeypatch, table_flop) -> common.table.Table():
    table = table_flop

    monkeypatch.setattr('builtins.input', lambda _: prompt_options['FLOP'])
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


class TestPreFlopAfterStartOver:

    @staticmethod
    def test_deck_stub_has_50_cards(table_preflop_after_start_over):
        assert table_preflop_after_start_over.deck.number_of_cards_not_dealt == 50


class TestPreFlop:

    # Table properties

    @staticmethod
    def test_deck_stub_has_50_cards(table_preflop):
        assert table_preflop.deck.number_of_cards_not_dealt == 50

    # State transitions

    @staticmethod
    def test_start_over_transitions_to_init(monkeypatch, table_preflop):
        monkeypatch.setattr('builtins.input', lambda _: prompt_options['START_OVER'])

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.Init

    @staticmethod
    def test_hero_change_hand_transitions_to_preflop(monkeypatch, table_preflop):
        # Monkeypatch the input(), simulate user intput "1":
        monkeypatch.setattr('builtins.input', lambda _: prompt_options['HERO_CHANGE_HAND'])

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.PreFlop

    @staticmethod
    def test_hero_change_seat_transitions_to_preflop(monkeypatch, table_preflop):
        monkeypatch.setattr('builtins.input', lambda _: prompt_options['HERO_CHANGE_SEAT'])

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.PreFlop

    @staticmethod
    def test_villain_change_seat_transitions_to_preflop(monkeypatch, table_preflop):
        monkeypatch.setattr('builtins.input', lambda _: prompt_options['VILLAIN_CHANGE_SEAT'])

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.PreFlop

    @staticmethod
    def test_flop_transitions_to_flop(monkeypatch, table_preflop):
        monkeypatch.setattr('builtins.input', lambda _: prompt_options['FLOP'])

        table = table_preflop
        table.run()
        assert type(table.state) == common.table.Flop


class TestPreFlopAfterHeroHandChange:

    @staticmethod
    def test_deck_stub_has_50_cards(table_preflop_after_hero_hand_change):
        assert table_preflop_after_hero_hand_change.deck.number_of_cards_not_dealt == 50


class TestFlop:

    @staticmethod
    def test_deck_stub_has_47_cards(table_flop):
        assert table_flop.deck.number_of_cards_not_dealt == 47


class TestFlopAfterReFlop:

    @staticmethod
    def test_deck_stub_has_47_cards(table_flop_after_reflop):
        assert table_flop_after_reflop.deck.number_of_cards_not_dealt == 47
