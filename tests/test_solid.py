import os
from shared.constants.paths import TESTS_FILES_DIR
from software_design_patterns.solid.single_responsibility_principle import *


def test_single_responsibility_principle():
    EXPECTED_JOURNAL_CONTENT = "0: I cried today.\n0: I ate a bug."
    JOURNAL_FILE = "journal.txt"
    JOURNAL_FILE_PATH = os.path.join(TESTS_FILES_DIR, JOURNAL_FILE)

    journal = Journal()

    journal.add_entry("I cried today.")
    journal.add_entry("I ate a bug.")

    assert str(journal) == EXPECTED_JOURNAL_CONTENT

    PersistenceManager.save_to_file(journal, JOURNAL_FILE_PATH)
    assert os.path.exists(JOURNAL_FILE_PATH)

    with open(JOURNAL_FILE_PATH, "r") as file:
        assert file.read() == EXPECTED_JOURNAL_CONTENT

    os.remove(JOURNAL_FILE_PATH)
    assert not os.path.exists(JOURNAL_FILE_PATH)
