""" test_watercooler.py - Test the water cooler state machine with PyTest


Import the state machine and state classes, initialize the state machine,
then run scenarios by feeding events to the state machine object and checking
that it is in the correct state.
"""

import time  # needed to produce the timeout event

# Import the machine and state classes, and also the event constants
from watercooler import WaterCoolerMachine, \
        WaitingState, FillingState, TimedoutState, \
        EVENT_DETECT, EVENT_UNDETECT

# Pytest will find this function and run it.
# After every event, run the update() method to process the event.
def test_WaterCoolerMachine():
    # new machine object
    watercooler = WaterCoolerMachine()

    # Add the states
    watercooler.add_state(WaitingState())  
    watercooler.add_state(FillingState())
    watercooler.add_state(TimedoutState())

    # Reset state is "waiting for water bottle"
    watercooler.go_to_state('waiting')
    assert watercooler.state.name == 'waiting'

    #
    # Test scenario 1: normal, bottle detected then undetected.
    #
    # Detect a bottle
    watercooler.event = EVENT_DETECT
    watercooler.update()
    assert watercooler.state.name == 'filling'

    # Un-detect a bottle, removed normally
    watercooler.event = EVENT_UNDETECT
    watercooler.update()
    assert watercooler.state.name == 'waiting'

    #
    # Test scenario 2: timed out, bottle detected then wait 5 seconds.
    #
    # Detect a bottle
    watercooler.event = EVENT_DETECT
    watercooler.update()
    assert watercooler.state.name == 'filling'

    # No undetect event after 5 seconds, timed out
    time.sleep(5.01)  # Exceeds the 5 second timeout
    watercooler.update()
    assert watercooler.state.name == 'timedout'

    # Send a Detect event but should stay in timed out state
    watercooler.event = EVENT_DETECT
    watercooler.update()
    assert watercooler.state.name == 'timedout'

    # Un-detect a bottle, timedout resets back to waiting
    watercooler.event = EVENT_UNDETECT
    watercooler.update()
    assert watercooler.state.name == 'waiting'

    # Add more scenarios here as needed (be creatively evil!)
