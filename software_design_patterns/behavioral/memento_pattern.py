class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Poem:
    def __init__(self, text: str = ""):
        self._text = text
        self.changes = [Memento(self.text)]
        self._current = 0

    @property
    def text(self):
        return self._text

    def set_text(self, text: str):
        self._text = text
        m = Memento(self._text)
        self.changes.append(m)
        self._current += 1
        return m

    def restore(self, memento: Memento):
        self._text = memento.get_state()
        self.changes.append(memento)
        self._current = len(self.changes) - 1

    def undo(self):
        if self._current > 0:
            self._current -= 1
            m = self.changes[self._current]
            self._text = m.get_state()
            return m
        return None

    def redo(self):
        if self._current < len(self.changes) - 1:
            self._current += 1
            m = self.changes[self._current]
            self._text = m.get_state()
            return m
        return None

    def __str__(self):
        return self._text
