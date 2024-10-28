"""watercooler.py - simulate a water bottle filling station

Louis Bertrand <louis.bertrand@durhamcollege.ca>
2019-09-29 -- Revised for fall 2020 week 4 assignment
2019-08-22 -- initial version

This is a demonstration of a simple state machine.
The filling station waits for a water bottle to be detected by the optical
sensor. When a bottle is detected, the valve is opened and water flows. The
valve is closed again when the bottle is no longer detected. However if the
user forgot the bottle or the sensor is defective, we want to prevent a spill
so we include a time-out. If the machine times out, the user must remove the
bottle and add it back to reset the time-out.
The state machine has three states: waiting, filling, timedout
[waiting ] -- EVENT_DETECT / open the valve --> [ filling ]
[filling ] -- EVENT_UNDETECT / close the valve --> [ waiting ]
[filling ] -- Timeout / close the valve --> [ timedout ]
[timedout ] -- EVENT_UNDETECT --> [ waiting ]

"""

import time
import msvcrt # built-in module to read keyboard in Windows


# System constants
TESTING = True
FILL_TIMEOUT = 5  # Filling timeout

# Event definitions
EVENT_DETECT = 'D' # Detector "sees" an object
EVENT_UNDETECT = 'U' # Detector "un-sees" an object (bottle removed)

# Support functions

def log(s):
    """Print the argument if testing/tracing is enabled."""
    if TESTING:
        print(s)

def get_event():
    """Non-blocking keyboard reader.
    Returns "" empty string if no key pressed."""
    x = msvcrt.kbhit()
    #print(x)
    if x: 
        ret = (msvcrt.getch().decode("utf-8")).upper()
        log("Event " + ret)
    else: 
        ret = ""
    return ret

###
# State machine
###
class WaterCoolerMachine(object):
    """Control a virtual water bottle filling station."""
    def __init__(self):
        self.state = None  # current state
        self.states = {}  # dictionary of states
        self.timeout = 0.0  # filling timeout deadline
        self.event = ""  # no event detected

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.on_exit(self)
        self.state = self.states[state_name]
        log('Entering %s' % (self.state.name))
        self.state.on_entry(self)

    def update(self):
        if self.state:
            #log('Updating %s' % (self.state.name))
            self.state.update(self)


###
# States
###
class State(object):
    """Abstract parent state class."""
    def __init__(self):
        pass

    def on_entry(self, machine):
        pass

    def on_exit(self, machine):
        pass

    def update(self, machine):
        pass


class WaitingState(State):
    """Waiting for event."""
    # Nothing to do in on_entry or on_exit so don't override them
    def __init__(self):
        self.name = "waiting"

    def update(self, machine):
        if machine.event == EVENT_DETECT:
            machine.go_to_state('filling')


class FillingState(State):
    """Filling the bottle."""
    def __init__(self):
        self.name = "filling"

    def on_entry(self, machine):
        print("opening valve")
        machine.stop_time = time.monotonic() + FILL_TIMEOUT

    def on_exit(self, machine):
        print("closing valve")

    def update(self, machine):
        if machine.event == EVENT_UNDETECT:
            machine.go_to_state('waiting')
        elif machine.stop_time <= time.monotonic():
            machine.go_to_state('timedout')
        else:
            print(".", end="", flush=True)
            time.sleep(0.2)  # simulation runs not too fast


class TimedoutState(State):
    """Filling timed out, wait for undetect."""
    def __init__(self):
        self.name = "timedout"

    def on_entry(self, machine):
        # redundant because FillingState.on_exit() closes the valve,
        # but safer to leave it in.
        print("closing valve")

    def update(self, machine):
        if machine.event == EVENT_UNDETECT:
            machine.go_to_state('waiting')

###
# Main program starts here
###
if __name__ == "__main__":
    # new machine object
    watercooler = WaterCoolerMachine()

    # Add the states
    watercooler.add_state(WaitingState())  
    watercooler.add_state(FillingState())
    watercooler.add_state(TimedoutState())

    # Reset state is "waiting for water bottle"
    watercooler.go_to_state('waiting')

    # begin continuous processing of events
    while True:
        watercooler.event = get_event()
        watercooler.update()

