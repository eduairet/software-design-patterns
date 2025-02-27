class Journal:
    """
    A class used to represent a Journal.

    Attributes
    ----------
    entries : list
        a list to store journal entries
    count : int
        the number of entries in the journal

    Methods
    -------
    add_entry(text: str)
        Adds a new entry to the journal.

    remove_entry(pos: int)
        Removes an entry from the journal at the specified position.

    __str__()
        Returns a string representation of the journal entries.
    """

    def __init__(self):
        self.entries = []
        self.count = len(self.entries)

    def add_entry(self, text: str):
        self.entries.append(f"{self.count}: {text}")

    def remove_entry(self, pos: int):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)


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
