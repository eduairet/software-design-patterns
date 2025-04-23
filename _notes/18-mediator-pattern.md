# Mediator Pattern

- This pattern defines a central object that defines the communication between different objects that may go in and out of the system.
  - Massive multiplayer online games
  - Chat applications
- It's not aware of the objects and their states, but it knows how to communicate with them.

  ```Python
  class Person:
      def __init__(self, name):
          self.name = name
          self.chat_log = []
          self.room = None

      def receive(self, sender, message):
          s = f"{sender}: {message}"
          print(f"[{self.name}'s chat session] {s}")
          self.chat_log.append(s)

      def say(self, message):
          self.room.broadcast(self.name, message)

      def private_message(self, who, message):
          self.room.message(self.name, who, message)


  class ChatRoom:
      def __init__(self):
          self.people = []

      def broadcast(self, source, message):
          for p in self.people:
              if p.name != source:
                  p.receive(source, message)

      def join(self, person):
          join_msg = f"{person.name} joins the chat"
          self.broadcast("room", join_msg)
          person.room = self
          self.people.append(person)

      def message(self, source, destination, message):
          for p in self.people:
              if p.name == destination:
                  p.receive(source, message)


  room = ChatRoom()

  john = Person("John")
  jane = Person("Jane")

  room.join(john)
  room.join(jane)

  john.say("hi room")
  jane.say("oh, hey john")

  simon = Person("Simon")
  room.join(simon)
  simon.say("hi everyone!")

  jane.private_message("Simon", "glad you could join us!")
  ```

- It's very common to use this pattern with events.

  ```Python
  class Event(list):
      def __call__(self, *args, **kwargs):
          for item in self:
              item(*args, **kwargs)


  class Game:
      def __init__(self):
          self.events = Event()

      def fire(self, args):
          self.events(args)


  class GoalScoredInfo:
      def __init__(self, who_scored, goals_scored):
          self.goals_scored = goals_scored
          self.who_scored = who_scored


  class Player:
      def __init__(self, name, game):
          self.name = name
          self.game = game
          self.goals_scored = 0

      def score(self):
          self.goals_scored += 1
          args = GoalScoredInfo(self.name, self.goals_scored)
          self.game.fire(args)


  class Coach:
      def __init__(self, game):
          game.events.append(self.celebrate_goal)

      def celebrate_goal(self, args):
          if isinstance(args, GoalScoredInfo) and args.goals_scored < 3:
              print(f"Coach says: well done, {args.who_scored}!")


  game = Game()
  player = Player("Sam", game)
  coach = Coach(game)

  player.score()  # Coach says: well done, Sam!
  player.score()  # Coach says: well done, Sam!
  player.score()  # ignored by coach
  ```
