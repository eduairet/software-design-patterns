class Journal:
    """
    A class to represent a journal that maintains a list of entries.

    Attributes
    ----------
    entries : list
        A list to store journal entries.

    Methods
    -------
    count:
        Returns the number of entries in the journal.
    add_entry(text: str):
        Adds a new entry to the journal.
    remove_entry(position: int = 0):
        Removes an entry from the journal at the specified position.
    __str__():
        Returns a string representation of the journal entries.
    """

    def __init__(self, entries: list = []):
        self.entries = entries

    @property
    def count(self):
        return len(self.entries)

    def add_entry(self, text: str):
        self.entries.append(text)

    def remove_entry(self, position: int = 0):
        if position > self.count - 1:
            raise ValueError("Invalid position.")
        del self.entries[position]

    def __str__(self):
        format_entry = lambda entry: f"{entry[0]}: {entry[1]}"
        return "\n".join(map(format_entry, enumerate(self.entries)))


class PersistenceManager:
    """
    A class used to represent a Persistence Manager.

    Methods
    -------
    save_to_file(journal: Journal, filename: str)
        Saves the journal entries to a file.

    load_from_file(filename: str)
        Loads journal entries from a file.
    """

    @staticmethod
    def save_to_file(journal: Journal, filename: str):
        with open(filename, "w") as file:
            file.write(str(journal))

    @staticmethod
    def load_from_file(filename: str):
        with open(filename, "r") as file:
            return file.read()
