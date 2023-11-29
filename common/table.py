"""
This module contains classes for the Table and its Seats.
"""
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
    """
    This class represents each seat at the table.

    Attributes:
        number: An integer identifying the seat number. Unique per table.
        name: A string identifying the seat position relative to the button.
        hand: A list of two Card objects dealt to the seat.
        role: A string indicating who is occupying the seat.
    """

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
    """
    This class represents a poker table.

    Also represents the dealer (i.e. any dealer actions would be defined here).

    This class is also run as a finite state machine. This class has a specific
    state (represented by a TableState subclass) and interacts with them via the
    state interface (TableClass class).

    Attributes:
        state: A TableState subclass indicating which state the Table is
          currently in.
        seats: A list of Seat objects at the Table.
        deck: A Deck object used at the Table.
    """

    def __init__(self) -> None:
        self.state = Init()
        self.seats = []
        self._populate_seats()
        self.deck = common.cards.Deck()
        return

    # Cards

    def deal(self, number_of_cards: int, seat_number: int) -> None:
        seat = self.get_seat_by_number(seat_number=seat_number)
        seat.hand = self.deck.deal_cards(number_of_cards=number_of_cards)
        return

    @staticmethod
    def assign_hand_to_seat(hand: list[common.cards.Card], seat: Seat) -> None:
        seat.hand = hand
        return

    @staticmethod
    def unassign_hand_from_seat(seat: Seat) -> None:
        seat.hand = []
        return

    def return_heros_cards_to_deck(self) -> None:
        seat = self.get_hero_seat()
        for i_card in seat.hand:
            self.deck.return_card_to_deck(card=i_card)
        seat.hand = []
        return

    def get_heros_hand(self) -> list[common.cards.Card]:
        hero_seat = self.get_hero_seat()
        return hero_seat.hand

    # Seats

    def get_seat_by_number(self, seat_number: int) -> Seat:
        for i_seat in self.seats:
            if i_seat.number == seat_number:
                return i_seat
        raise IndexError(f'Seat number {seat_number} not found.')

    def get_seats_by_role(self, role: Union[str, None]) -> list[Seat]:
        self.verify_role(value=role)

        seats = []
        for i_seat in self.seats:
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

    def assign_role_to_seat(self, seat: Seat, role: Union[str, None]) -> None:
        self.verify_role(value=role)
        seat.role = role
        return

    def assign_hero_role_to_random_empty_seat(self) -> None:
        seat = self.get_random_empty_seat()
        self.assign_role_to_seat(seat=seat, role='H')
        return

    def assign_villain_role_to_random_empty_seat(self) -> None:
        seat = self.get_random_empty_seat()
        self.assign_role_to_seat(seat=seat, role='V')
        return

    def _populate_seats(self) -> None:
        seat_numbers = range(1, 10)
        seat_names = ['UTG', 'UTG+1', 'UTG+2', 'LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        for (i_seat_number, i_seat_name) in zip(seat_numbers, seat_names):
            self.seats.append(Seat(number=i_seat_number, name=i_seat_name))
        return

    # States

    @property
    def state(self) -> 'TableState':
        """
        Getter/setter methods for state property.

        The setter method, in addition to the obvious (setting the Table's
        state), also sets the TableState's reference to the Table itself so that
        the TableState can access any Table's methods.
        """
        return self._state

    @state.setter
    def state(self, value) -> None:
        self._state = value
        self._state.table = self
        return

    def run(self) -> None:
        """
        This function executes the next step, depending on the Table's state.

        Because this is state-specific, this method is defined for each
        TableState subclass.
        """
        self.state.run()
        return

    # Misc

    def __str__(self) -> str:
        s = ''
        for i_seat in self.seats:
            s += f'Seat {i_seat.number} - {i_seat.name:5} - {i_seat.role or " "} - {i_seat.hand}\n'
        return s


class TableState(ABC):

    _table = None

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


class Init(TableState):
    """
    TableState representing the Init state.

    I felt it easier to execute this code in a dedicated state as opposed to
    Table.__init__(). See flow chart.
    """

    def run(self) -> None:
        self.table.assign_hero_role_to_random_empty_seat()
        self.table.assign_villain_role_to_random_empty_seat()
        hero_seat = self.table.get_hero_seat()
        self.table.deal(number_of_cards=2, seat_number=hero_seat.number)
        print(self.table)
        self.table.state = PreFlop()
        return


class PreFlop(TableState):

    # State Machine Methods

    def run(self) -> None:
        prompt_text = "1: Keep seat, change hand"
        prompt_text += "\n2: Keep hand, change seat"
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
            self.table.return_heros_cards_to_deck()
            hero_seat = self.table.get_hero_seat()
            self.table.deal(number_of_cards=2, seat_number=hero_seat.number)
            print(self.table)

        if value == '2':
            old_hero_seat = self.table.get_hero_seat()
            new_hero_seat = self.table.get_random_empty_seat()
            heros_hand = self.table.get_heros_hand()

            self.table.assign_role_to_seat(seat=old_hero_seat, role=None)
            self.table.assign_role_to_seat(seat=new_hero_seat, role='H')

            self.table.unassign_hand_from_seat(seat=old_hero_seat)
            self.table.assign_hand_to_seat(hand=heros_hand, seat=new_hero_seat)

            print(self.table)
        return

    @staticmethod
    def _validate_input(value: str) -> bool:
        if value.upper() in ['1', '2', 'Q']:
            return True
        print("Invalid input.")
        return False
