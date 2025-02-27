# SOLID Design Principles

- Set of design principles introduced by Robert C. Martin in early 2000s.

## Single Responsibility Principle (SRP) or Separation of Concerns (SoC)

- A class should have only one reason to change or a class should have only one responsibility.

  ```py
  # This class has the only responsibility of managing the entries of a journal.
  class Journal:
      def __init__(self):
          self.entries = []
          self.count = 0

      def add_entry(self, text):
          self.entries.append(f"{self.count}: {text}")
          self.count += 1

      def remove_entry(self, pos):
          del self.entries[pos]

      def __str__(self):
          return "\n".join(self.entries)

      # If we want to save the entries to a file, we should create a separate class to avoid breaking the SRP.

  class PersistenceManager:
      @staticmethod
      def save_to_file(journal, filename):
          with open(filename,
                    "w") as file:
              file.write(str(journal))
  ```

- Making a class doing to much can lead to an anti-pattern called "God Object", which is a class that knows too much or does too much.
