'''
TPRG 2131 Fall 2024 Project 1 - Pytest
November 14th, 2024
Cornell Falconer-Lawson <Cornell.FalconerLawson@dcmail.ca>

This program is strictly my own work. Any material
beyond course learning materials that is taken from
the Web or other sources is properly cited, giving
credit to the original author(s).

For the 'vending_machine_graphical.py' script - WORKS
'''


from vending_machine_CFL import VendingMachine, WaitingState, AddCoinsState, DeliverProductState, CountChangeState

def test_VendingMachine():
   # new machine object
    vending = VendingMachine()
   # Add the states - ORG
   #     vending.add_state(WaitingState())
   #     vending.add_state(CoinsState())
   #     vending.add_state(DispenseState())
   #     vending.add_state(ChangeState())

  # My revisions
    vending.add_state(WaitingState())
    vending.add_state(AddCoinsState())
    vending.add_state(DeliverProductState())
    vending.add_state(CountChangeState())

    # Reset state is "waiting for first coin"
    vending.go_to_state('waiting')
    assert vending.state.name == 'waiting'

    # test that the first coin causes a transition to 'coins'
    vending.event = '$2'  # a toonie
    vending.update()
    assert vending.state.name == 'add_coins'
    assert vending.amount == 200  # pennies, was .total

    vending.event = '$1'  # a loonie
    vending.update()
    assert vending.state.name == 'add_coins'
    assert vending.amount == 300  # pennies, was .total

    vending.event = '¢25'  # a quarter
    vending.update()
    assert vending.state.name == 'add_coins'
    assert vending.amount == 325  # pennies, was .total

    vending.event = '¢10'  # a dime
    vending.update()
    assert vending.state.name == 'add_coins'
    assert vending.amount == 335  # pennies, was .total

    vending.event = '¢5'  # a nickel
    vending.update()
    assert vending.state.name == 'add_coins'
    assert vending.amount == 340  # pennies, was .total

