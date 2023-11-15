import pytest

from common import table


@pytest.fixture(scope='function')
def t() -> table.Table():
    return table.Table()


class TestTable:

    def test_get_seat_returns_correct_number(self, t):
        seat_number = 3
        seat = t.state.get_seat_by_number(seat_number=seat_number)
        assert seat.number == seat_number

    def test_get_seat_index_error(self, t):
        seat_number = 11
        try:
            t.state.get_seat_by_number(seat_number=seat_number)
        except IndexError:
            pass
        except:
            assert False, 'Wrong exception raised.'
        else:
            assert False, 'No exception raised.'


class TestAssignRoleToSeat:

    def test_valid_values(self, t):
        seat_number = 4
        seat = t.state.get_seat_by_number(seat_number=seat_number)
        for i_role in [None, 'H', 'V']:
            seat.role = i_role
        return

    def test_invalid_values(self, t):
        seat_number = 4
        seat = t.state.get_seat_by_number(seat_number=seat_number)
        for i_role in ['A', 'h', 'v', 1]:
            try:
                seat.role = i_role
            except ValueError:
                continue
            except:
                assert False, 'Wrong exception raised.'
            else:
                assert False, 'No exception raised.'


class TestGetSeatsByRole:

    def test_seat_number(self, t):
        seat_number = 3
        role = 'H'
        t.state.assign_role_to_seat(seat_number=seat_number, role=role)
        seats = t.get_seats_by_role(role=role)
        assert seats[0].number == seat_number

    def test_seat_role(self, t):
        seat_number = 3
        role = 'H'
        t.state.assign_role_to_seat(seat_number=seat_number, role=role)
        seats = t.get_seats_by_role(role=role)
        assert seats[0].role == role

    def test_no_hits(self, t):
        seats = t.get_seats_by_role(role='H')
        assert seats == []

    def test_multiple_hits(self, t):
        seat_numbers = [1, 3, 6]
        role = 'V'
        for i_seat_number in seat_numbers:
            t.state.assign_role_to_seat(seat_number=i_seat_number, role=role)
        seats = t.get_seats_by_role(role=role)
        assert len(seats) == 3


class TestGetHeroSeat:

    def test_no_hero_seat(self, t):
        seat = t.get_hero_seat()
        assert seat is None

    def test_one_hero_seat_verify_seat_number(self, t):
        seat_number = 6
        role = 'H'
        t.state.assign_role_to_seat(seat_number=seat_number, role=role)
        seat = t.get_hero_seat()
        assert seat.number == seat_number

    def test_multiple_hero_seats_raises_exception(self, t):
        seat_numbers = [1, 2, 8]
        role = 'H'
        for i_seat_number in seat_numbers:
            t.state.assign_role_to_seat(seat_number=i_seat_number, role=role)
        try:
            t.get_hero_seat()
        except RuntimeError:
            pass
        except:
            assert False, 'Wrong exception raised.'
        else:
            assert False, 'No exception raised.'
