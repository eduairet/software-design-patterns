from abc import ABC, abstractmethod
from enum import Enum


class Poem:
    def __init__(self, text: str = ""):
        self.text = text

    def write(self, text: str):
        self.text += text

    def delete(self, characters: int):
        if characters > len(self.text):
            raise ValueError("Cannot delete more characters than present")
        self.text = self.text[:-characters]

    def __str__(self):
        return self.text


class Command(ABC):
    def __init__(self):
        self.success = False

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class PoemCommand(Command):
    class Action(Enum):
        WRITE = "write"
        DELETE = "delete"

    def __init__(self, poem: Poem, action: Action, text: str = "", characters: int = 0):
        super().__init__()
        self.poem = poem
        self.action = action
        self.undo_text = [self.poem.text]
        self.text = text
        self.characters = characters

    def execute(self):
        if self.action == self.Action.WRITE:
            self.undo_text.append(self.poem.text)
            self.poem.write(self.text)
            self.success = True
        elif self.action == self.Action.DELETE:
            try:
                self.undo_text.append(self.poem.text)
                self.poem.delete(self.characters)
                self.success = True
            except ValueError:
                self.success = False
        return self.success

    def undo(self):
        if self.success and self.action in [self.Action.WRITE, self.Action.DELETE]:
            self.poem.text = self.undo_text.pop()
            return True
        return False


class CompositePoemCommand(Command, list):
    def __init__(self, commands=[]):
        super().__init__()
        for i in commands:
            self.append(i)

    def execute(self):
        for command in self:
            command.execute()

    def undo(self):
        for command in reversed(self):
            command.undo()


class CopyFromPoemCommand(CompositePoemCommand):
    def __init__(self, from_poem: Poem, to_poem: Poem):
        super().__init__(
            [
                PoemCommand(
                    from_poem, PoemCommand.Action.DELETE, characters=len(from_poem.text)
                ),
                PoemCommand(
                    to_poem,
                    PoemCommand.Action.WRITE,
                    from_poem.text,
                ),
            ]
        )

    def execute(self):
        ok = [command.execute() for command in self]
        return all(ok)
