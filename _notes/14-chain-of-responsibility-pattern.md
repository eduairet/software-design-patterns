# Chain of Responsibility Pattern

- It is a behavioral design pattern that allows an object to pass a request along a chain of handlers.
- It can have the default processing implementation and the ability to terminate the process chain.
- One way of implementing this pattern is chaining methods together:

  ```Python
  class Creature:
      def __init__(self, name, attack, defense):
          self.defense = defense
          self.attack = attack
          self.name = name

      def __str__(self):
          return f'{self.name} ({self.attack}/{self.defense})'


  class CreatureModifier:
      def __init__(self, creature):
          self.creature = creature
          self.next_modifier = None

      def add_modifier(self, modifier):
          if self.next_modifier:
              self.next_modifier.add_modifier(modifier)
          else:
              self.next_modifier = modifier

      def handle(self):
          if self.next_modifier:
              self.next_modifier.handle()


  class NoBonusesModifier(CreatureModifier):
      def handle(self):
          print('No bonuses for you!')


  class DoubleAttackModifier(CreatureModifier):
      def handle(self):
          print(f'Doubling {self.creature.name}''s attack')
          self.creature.attack *= 2
          super().handle()


  class IncreaseDefenseModifier(CreatureModifier):
      def handle(self):
          if self.creature.attack <= 2:
              print(f'Increasing {self.creature.name}''s defense')
              self.creature.defense += 1
          super().handle()


  goblin = Creature('Goblin', 1, 1)
  print(goblin)

  root = CreatureModifier(goblin)

  root.add_modifier(NoBonusesModifier(goblin))

  root.add_modifier(DoubleAttackModifier(goblin))
  root.add_modifier(DoubleAttackModifier(goblin))

  # no effect
  root.add_modifier(IncreaseDefenseModifier(goblin))

  root.handle()  # apply modifiers
  print(goblin)
  ```

- An important concept in this pattern is the **Command Query Separation**:
  - **Command**: a method that changes the state of an object.
  - **Query**: a method that returns the state of an object.
  - **Command Query Separation**: a method should either be a command or a query, but not both.
- Another way to implement this method is with a **Broker Chain**

  - A broker chain is a chain of objects that can handle a request.
  - Each object in the chain can either handle the request or pass it to the next object in the chain.

    ```Python
    from abc import ABC
    from enum import Enum


    class Event(list):
        def __call__(self, *args, **kwargs):
            for item in self:
                item(*args, **kwargs)


    class WhatToQuery(Enum):
        ATTACK = 1
        DEFENSE = 2


    class Query:
        def __init__(self, creature_name, what_to_query, default_value):
            self.value = default_value  # bidirectional
            self.what_to_query = what_to_query
            self.creature_name = creature_name


    # This is the event broker and it will allow to make the queries accessible to the objects and modifiers
    class Game:
        def __init__(self):
            self.queries = Event()

        def perform_query(self, sender, query):
            self.queries(sender, query)


    class Creature:
        def __init__(self, game, name, attack, defense):
            self.initial_defense = defense
            self.initial_attack = attack
            self.name = name
            self.game = game

        @property
        def attack(self):
            q = Query(self.name, WhatToQuery.ATTACK, self.initial_attack)
            self.game.perform_query(self, q)
            return q.value

        @property
        def defense(self):
            q = Query(self.name, WhatToQuery.DEFENSE, self.initial_attack)
            self.game.perform_query(self, q)
            return q.value

        def __str__(self):
            return f'{self.name} ({self.attack}/{self.defense})'


    class CreatureModifier(ABC):
        def __init__(self, game, creature):
            self.creature = creature
            self.game = game
            self.game.queries.append(self.handle)

        def handle(self, sender, query):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.game.queries.remove(self.handle)


    class DoubleAttackModifier(CreatureModifier):
        def handle(self, sender, query):
            if (sender.name == self.creature.name and
                    query.what_to_query == WhatToQuery.ATTACK):
                query.value *= 2


    class IncreaseDefenseModifier(CreatureModifier):
        def handle(self, sender, query):
            if (sender.name == self.creature.name and
                    query.what_to_query == WhatToQuery.DEFENSE):
                query.value += 3


    game = Game()
    goblin = Creature(game, 'Strong Goblin', 2, 2)
    print(goblin)

    with DoubleAttackModifier(game, goblin):
        print(goblin)
        with IncreaseDefenseModifier(game, goblin):
            print(goblin)

    print(goblin)
    ```
