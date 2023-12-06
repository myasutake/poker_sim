import pytest

from common import table


@pytest.fixture(scope='function')
def t() -> table.Table():
    return table.Table()


class TestInit:

    @staticmethod
    def test_init_state_is_init(t):
        assert type(t.state) == table.Init

    @staticmethod
    def test_init_auto_transitions_to_preflop(t):
        t.run()
        assert type(t.state) == table.PreFlop
