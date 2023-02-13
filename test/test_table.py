import pytest

from common import table


@pytest.fixture(scope='function')
def t() -> table.Table():
    return table.Table()


class TestTable:

    def test_get_seat_returns_correct_number(self, t):
        seat_number = 3
        seat = t.get_seat_by_number(seat_number=seat_number)
        assert seat.number == seat_number

    def test_get_seat_index_error(self, t):
        seat_number = 11
        try:
            t.get_seat_by_number(seat_number=seat_number)
        except IndexError:
            pass
        except:
            assert False, 'Wrong exception raised.'
        else:
            assert False, 'No exception raised.'
