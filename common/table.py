import random
from typing import Union

from common import cards


class BaseClass:

    @staticmethod
    def _verify_role(value: str) -> None:
        if value not in [None, 'H', 'V']:
            raise ValueError(f"Invalid role {value} assigned to seat.")
        return


class Table(BaseClass):

    def __init__(self) -> None:
        self._seats = []
        self._populate_seats()
        self._deck = cards.Deck()
        return

    def deal(self, number_of_cards: int, seat_number: int) -> None:
        seat = self.get_seat_by_number(seat_number=seat_number)
        seat.hand = self._deck.deal_cards(number_of_cards=number_of_cards)
        return

    def deal_hand_to_random_seat(self) -> None:
        number_of_seats = len(self._seats)
        seat_number = random.randint(1, number_of_seats)
        self.deal(number_of_cards=2, seat_number=seat_number)
        return

    # Seats

    def get_seat_by_number(self, seat_number: int) -> 'Seat':
        for i_seat in self._seats:
            if i_seat.number == seat_number:
                return i_seat
        raise IndexError(f'Seat number {seat_number} not found.')

    def assign_role_to_seat(self, seat_number: int, role: str) -> None:
        self._verify_role(value=role)

        seat = self.get_seat_by_number(seat_number=seat_number)
        seat.role = role
        return

    def get_seats_by_role(self, role: Union[str, None]) -> list['Seat']:
        self._verify_role(value=role)

        seats = []
        for i_seat in self._seats:
            if i_seat.role == role:
                seats.append(i_seat)
        return seats

    def get_hero_seat(self) -> Union['Seat', None]:
        seats = self.get_seats_by_role(role='H')
        if len(seats) > 1:
            raise RuntimeError(f"{len(seats)} seats found with role 'H'.")
        if len(seats) == 1:
            return seats[0]
        return None

    def get_random_empty_seat(self) -> 'Seat':
        seats = self.get_seats_by_role(role=None)
        return random.choice(seats)

    def assign_hero_role_to_random_empty_seat(self) -> None:
        seat = self.get_random_empty_seat()
        self.assign_role_to_seat(seat_number=seat.number, role='H')
        return

    def _populate_seats(self) -> None:
        seat_numbers = range(1, 10)
        seat_names = ['UTG', 'UTG+1', 'UTG+2', 'LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        for (i_seat_number, i_seat_name) in zip(seat_numbers, seat_names):
            self._seats.append(Seat(number=i_seat_number, name=i_seat_name))
        return

    # Misc

    def __str__(self) -> str:
        s = ''
        for i_seat in self._seats:
            s += f'Seat {i_seat.number} - {i_seat.name:5} - {i_seat.hand}\n'
        return s


class Seat(BaseClass):

    def __init__(self, number: int, name: str) -> None:
        self._number = number
        self._name = name
        self._cards = []
        self._role = None
        return

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return self._name

    @property
    def hand(self) -> list[cards.Card]:
        return self._cards

    @hand.setter
    def hand(self, value: list[cards.Card]) -> None:
        self._cards = value
        return

    # Role

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        self._verify_role(value=value)
        self._role = value
        return