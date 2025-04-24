from software_design_patterns.behavioral.memento_pattern import *


def test_memento_poem():
    VERSE_1 = "Que putas haces con mi corazón"
    VERSE_2 = "Deshidratado en el infierno"
    VERSE_3 = "De una vida sin anhelo"

    poem = Poem(VERSE_1)
    assert poem.text == VERSE_1

    memento1 = poem.set_text(VERSE_2)
    assert poem.text == VERSE_2

    memento2 = poem.set_text(VERSE_3)
    assert poem.text == VERSE_3

    poem.restore(memento1)
    assert poem.text == VERSE_2

    poem.restore(memento2)
    assert poem.text == VERSE_3

    memento3 = poem.undo()
    assert poem.text == VERSE_2
    assert memento3.get_state() == VERSE_2

    memento4 = poem.redo()
    assert poem.text == VERSE_3
    assert memento4.get_state() == VERSE_3
