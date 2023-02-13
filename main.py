# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from common import cards


def main():
    deck = cards.Deck()
    hand = deck.deal_cards(number_of_cards=2)
    print(f'Starting hand: {hand}')
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
