# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from common import cards, table


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    t = table.Table()
    t.assign_hero_role_to_random_empty_seat()
    hero_seat = t.get_hero_seat()
    t.deal(number_of_cards=2, seat_number=hero_seat.number)
    print(t)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
