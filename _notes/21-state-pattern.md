# State Pattern

- this pattern determines the object's behavior depending on its state.
- The object that handles state and transitions is called the state machine.
- The classic implementation of the pattern is to handle each state in a separate class, but this can lead to a large number of classes and wasting a lot of time.

  ```Python
  from abc import ABC


  class Switch:
      def __init__(self):
          self.state = OffState()

      def on(self):
          self.state.on(self)

      def off(self):
          self.state.off(self)


  class State(ABC):
      def on(self, switch):
          print("Light is already on")

      def off(self, switch):
          print("Light is already off")


  class OnState(State):
      def __init__(self):
          print("Light turned on")

      def off(self, switch):
          print("Turning light off...") # Transition to OffState
          switch.state = OffState()


  class OffState(State):
      def __init__(self):
          print("Light turned off")

      def on(self, switch):
          print("Turning light on...") # Transition to OnState
          switch.state = OnState()


  sw = Switch()

  sw.on()
  """
  Turning light on...
  Light turned on
  """
  sw.off()
  """
  Turning light off...
  Light turned off
  """
  sw.off()  # Light is already off
  ```

- The above implementation is not efficient because it creates a new instance of the state class every time the state changes, instead we can create a set of state classes and use them to change the state of the object.

  ```Python
  from enum import Enum, auto


  class State(Enum):
      OFF_HOOK = auto()
      CONNECTING = auto()
      CONNECTED = auto()
      ON_HOLD = auto()
      ON_HOOK = auto()


  class Trigger(Enum):
      CALL_DIALED = auto()
      HUNG_UP = auto()
      CALL_CONNECTED = auto()
      PLACED_ON_HOLD = auto()
      TAKEN_OFF_HOLD = auto()
      LEFT_MESSAGE = auto()

  # This set of rules are going to define the state machine
  # and the transitions between states
  rules = {
      State.OFF_HOOK: [(Trigger.CALL_DIALED, State.CONNECTING)],
      State.CONNECTING: [
          (Trigger.HUNG_UP, State.ON_HOOK),
          (Trigger.CALL_CONNECTED, State.CONNECTED),
      ],
      State.CONNECTED: [
          (Trigger.LEFT_MESSAGE, State.ON_HOOK),
          (Trigger.HUNG_UP, State.ON_HOOK),
          (Trigger.PLACED_ON_HOLD, State.ON_HOLD),
      ],
      State.ON_HOLD: [
          (Trigger.TAKEN_OFF_HOLD, State.CONNECTED),
          (Trigger.HUNG_UP, State.ON_HOOK),
      ],
  }

  state = State.OFF_HOOK
  exit_state = State.ON_HOOK

  while state != exit_state:
      print(f"The phone is currently {state}")

      for i in range(len(rules[state])):
          t = rules[state][i][0]
          print(f"{i}: {t}")

      idx = int(input("Select a trigger:"))
      s = rules[state][idx][1]
      state = s

  print("We are done using the phone.")
  ```

- Another way to implement the state pattern is by using a Switch-Based State Machine which is a more efficient way to implement the state pattern since it doesn't add extra data structures to the code, in languages without switch statements we can handle this with an enum or a dictionary.

```Python
from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    FAILED = auto()
    UNLOCKED = auto()


code = "1234"
state = State.LOCKED
entry = ""

while True:
    if state == State.LOCKED:
        entry += input(entry)

        if entry == code:
            state = State.UNLOCKED

        if not code.startswith(entry):
            # the code is wrong
            state = State.FAILED
    elif state == State.FAILED:
        print("\nFAILED")
        entry = ""
        state = State.LOCKED
    elif state == State.UNLOCKED:
        print("\nUNLOCKED")
        break
```
