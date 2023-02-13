class Table:

    def __init__(self) -> None:
        self._seats = []
        self._populate_seats()
        return

    def get_seat_by_number(self, seat_number: int) -> 'Seat':
        for i_seat in self._seats:
            if i_seat.number == seat_number:
                return i_seat
        raise IndexError(f'Seat number {seat_number} not found.')

    def _populate_seats(self) -> None:
        seat_numbers = range(1, 10)
        seat_names = ['UTG', 'UTG+1', 'UTG+2', 'LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        for (i_seat_number, i_seat_name) in zip(seat_numbers, seat_names):
            self._seats.append(Seat(number=i_seat_number, name=i_seat_name))
        return

    def __str__(self) -> str:
        s = ''
        for i_seat in self._seats:
            s += f'Seat {i_seat.number} - {i_seat.name}\n'
        return s


class Seat:

    def __init__(self, number: int, name: str) -> None:
        self._number = number
        self._name = name
        return

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return self._name
