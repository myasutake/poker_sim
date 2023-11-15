from abc import ABC, abstractmethod
import random
from typing import Union

import common.cards


class BaseClass:

    @staticmethod
    def verify_role(value: str) -> None:
        if value not in [None, 'H', 'V']:
            raise ValueError(f"Invalid role {value} assigned to seat.")
        return


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
    def hand(self) -> list[common.cards.Card]:
        return self._cards

    @hand.setter
    def hand(self, value: list[common.cards.Card]) -> None:
        self._cards = value
        return

    # Role

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        self.verify_role(value=value)
        self._role = value
        return


class Table(BaseClass):

    def __init__(self) -> None:
        self.state = PreFlop()
        self.seats = []
        self._populate_seats()
        self.deck = common.cards.Deck()
        return

    # Seats

    def _populate_seats(self) -> None:
        seat_numbers = range(1, 10)
        seat_names = ['UTG', 'UTG+1', 'UTG+2', 'LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        for (i_seat_number, i_seat_name) in zip(seat_numbers, seat_names):
            self.seats.append(Seat(number=i_seat_number, name=i_seat_name))
        return

    # States

    @property
    def state(self) -> 'TableState':
        return self._state

    @state.setter
    def state(self, value) -> None:
        self._state = value
        self._state.table = self
        return

    def init_setup(self) -> None:
        self.state.init_setup()
        return

    def run(self) -> None:
        self.state.run()
        return

    # Misc

    def __str__(self) -> str:
        s = ''
        for i_seat in self.seats:
            s += f'Seat {i_seat.number} - {i_seat.name:5} - {i_seat.hand}\n'
        return s


class TableState(ABC):

    _table = None

    # Deal Cards

    def deal(self, number_of_cards: int, seat_number: int) -> None:
        seat = self.get_seat_by_number(seat_number=seat_number)
        seat.hand = self.table.deck.deal_cards(number_of_cards=number_of_cards)
        return

    def return_heros_cards_to_deck(self) -> None:
        seat = self.get_hero_seat()
        for i_card in seat.hand:
            self.table.deck.return_card_to_deck(card=i_card)
        seat.hand = []
        return

    # Seats

    def get_seat_by_number(self, seat_number: int) -> Seat:
        for i_seat in self.table.seats:
            if i_seat.number == seat_number:
                return i_seat
        raise IndexError(f'Seat number {seat_number} not found.')

    def get_seats_by_role(self, role: Union[str, None]) -> list[Seat]:
        self.table.verify_role(value=role)

        seats = []
        for i_seat in self.table.seats:
            if i_seat.role == role:
                seats.append(i_seat)
        return seats

    def get_hero_seat(self) -> Union[Seat, None]:
        seats = self.get_seats_by_role(role='H')
        if len(seats) > 1:
            raise RuntimeError(f"{len(seats)} seats found with role 'H'.")
        if len(seats) == 1:
            return seats[0]
        return None

    def get_random_empty_seat(self) -> Seat:
        seats = self.get_seats_by_role(role=None)
        return random.choice(seats)

    @abstractmethod
    def assign_role_to_seat(self, seat_number: int, role: str) -> None:
        pass

    @abstractmethod
    def assign_hero_role_to_random_empty_seat(self) -> None:
        pass

    # State Machine Methods

    @property
    def table(self) -> Table:
        return self._table

    @table.setter
    def table(self, value: Table) -> None:
        self._table = value
        return

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def init_setup(self) -> None:
        pass


class PreFlop(TableState):

    # Seats

    def assign_role_to_seat(self, seat_number: int, role: str) -> None:
        self.table.verify_role(value=role)

        seat = self.get_seat_by_number(seat_number=seat_number)
        seat.role = role
        return

    def assign_hero_role_to_random_empty_seat(self) -> None:
        seat = self.get_random_empty_seat()
        self.assign_role_to_seat(seat_number=seat.number, role='H')
        return

    # State Machine Methods

    def init_setup(self) -> None:
        self.assign_hero_role_to_random_empty_seat()
        hero_seat = self.get_hero_seat()
        self.deal(number_of_cards=2, seat_number=hero_seat.number)
        print(self.table)
        return

    def run(self) -> None:
        prompt_text = "1: Keep seat, change hand"
        prompt_text += "\nQ: Quit"
        prompt_text += "\n\n"
        print(prompt_text)

        value = None
        input_is_valid = False
        while not input_is_valid:
            value = input("> ").upper()
            input_is_valid = self._validate_input(value=value)

        if value == 'Q':
            quit()

        if value == '1':
            self.return_heros_cards_to_deck()
            hero_seat = self.get_hero_seat()
            self.deal(number_of_cards=2, seat_number=hero_seat.number)
            print(self.table)
        return

    @staticmethod
    def _validate_input(value: str) -> bool:
        if value.upper() in ['1', 'Q']:
            return True
        print("Invalid input.")
        return False
