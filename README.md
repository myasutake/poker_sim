# Poker Sim & State Machines

## Poker Sim

This program generates various random Hold 'Em scenarios. Use it to help drill various scenarios into your head and be better preprared at the table!

Features:
* Preflop
    * Hero and Villain
    * Deal a different hand to the Hero
    * Change the Hero's or Villain's seats
* Flop, Turn, and River
    * Re-deal the last action

Use your favorite preflop charts. Is your hand good enough given your and your opponent's positions? Switch up either of your seats and see if your answer changes.

Add Equilab to the mix and use it to create ranges from your preflop charts. You raise UTG, so your range is tiny. Villain UTG+1 hypothetically re-raises, so their range is even smaller. With your already tiny range, this may not be the most interesting scenario to flesh out a balanced raise/call/fold strategy. Move H's and V's seats and, if the same raise-re-raise sequence is still applicable, see if your situation becomes more interesting.

Deal a flop. Again, does it produce an easy path forward? Re-flop it and see how things change.

## Finite State Machine

I thought this program would be a good candidate for an example of a finite state machine. Most examples I've found followed similar patterns, so nothing should be groundbreaking here.

The Table class, found in [common/table.py](common/table.py), not only represents the poker table itself, but the hand being played out. As such, The Table will be represented with the FSM.
* The Table contains a reference to a Specific State Object, which indicates the table's current state.
* An Abstract Base Class is created as a superclass of each Specific State class. (An ABC isn't strictly necessary in Python, of course. You could just create it like any other class and simply never invoke it.)
* The ABC contains a reference back to the Table.

More notes can be found in the code docstrings.
