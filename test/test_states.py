import pytest

import common.table


@pytest.fixture(scope='function')
def table_init() -> common.table.Table():
    return common.table.Table()


class TestInit:

    @staticmethod
    def test_init_state_is_init(table_init):
        assert type(table_init.state) == common.table.Init

    @staticmethod
    def test_init_auto_transitions_to_preflop(table_init):
        table = table_init
        table.run()
        assert type(table.state) == common.table.PreFlop
