# Observer Pattern

- An observer is an object that is notified of changes in another object (observable).
- A common scenario to use this pattern is to trigger an event when a certain condition is met.

  ```Python
  class Event(list):
      def __call__(self, *args, **kwargs):
          for item in self:
              item(*args, **kwargs)


  class Person:
      def __init__(self, name, address):
          self.name = name
          self.address = address
          self.falls_ill = Event()

      def catch_a_cold(self):
          self.falls_ill(self.name, self.address)


  def call_doctor(name, address):
      print(f'A doctor has been called to {address}')


  person = Person('Sherlock', '221B Baker St')

  person.falls_ill.append(lambda name, addr: print(f'{name} is ill'))

  person.falls_ill.append(call_doctor)

  person.catch_a_cold()

  person.falls_ill.remove(call_doctor)  # remove the observer
  person.catch_a_cold()
  ```

- Another approach is to observe properties of an object

  ```Python
  class Event(list):
      def __call__(self, *args, **kwargs):
          for item in self:
              item(*args, **kwargs)


  class PropertyObservable:
      def __init__(self):
          self.property_changed = Event()


  class Person(PropertyObservable):
      def __init__(self, age=0):
          super().__init__()
          self._age = age

      @property
      def age(self):
          return self._age

      @age.setter
      def age(self, value):
          if self._age == value:
              return
          self._age = value
          self.property_changed("age", value)


  class TrafficAuthority:
      def __init__(self, person):
          self.person = person
          person.property_changed.append(self.person_changed)

      def person_changed(self, name, value):
          if name == "age":
              if value < 16:
                  print("Sorry, you still cannot drive")
              else:
                  print("Okay, you can drive now")
                  self.person.property_changed.remove(self.person_changed)


  p = Person()
  ta = TrafficAuthority(p)
  for age in range(14, 20):
      print(f"Setting age to {age}")
      p.age = age
  # Setting age to 14
  # Sorry, you still cannot drive
  # Setting age to 15
  # Sorry, you still cannot drive
  # Setting age to 16
  # Okay, you can drive now
  # Setting age to 17
  # Okay, you can drive now
  # Setting age to 18
  # Setting age to 19
  ```

- If the property has a dependency we need to cache the old value to check if the property has changed.

  ```Python
  class Event(list):
      def __call__(self, *args, **kwargs):
          for item in self:
              item(*args, **kwargs)


  class PropertyObservable:
      def __init__(self):
          self.property_changed = Event()


  class Person(PropertyObservable):
      def __init__(self, age=0):
          super().__init__()
          self._age = age

      @property
      def can_vote(self):
          return self._age >= 18

      @property
      def age(self):
          return self._age

      @age.setter
      def age(self, value):
          if self._age == value:
              return

          old_can_vote = self.can_vote # Property cached

          self._age = value
          self.property_changed("age", value)

          if old_can_vote != self.can_vote:
              self.property_changed("can_vote", self.can_vote) # Notify change


  def person_changed(name, value):
      if name == "can_vote":
          print(f"Voting status changed to {value}")


  p = Person()
  p.property_changed.append(person_changed)

  for age in range(16, 21):
      print(f"Changing age to {age}")
      p.age = age
      # Changing age to 16
      # Changing age to 17
      # Changing age to 18
      # Voting status changed to True
      # Changing age to 19
      # Changing age to 20
  ```
