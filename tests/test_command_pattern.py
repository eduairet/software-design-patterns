from software_design_patterns.behavioral.command_pattern import *


def test_command_poem_single():
    poem = Poem()
    command = PoemCommand(poem, PoemCommand.Action.WRITE, "Roses are red")
    assert command.execute() == True
    assert poem.text == "Roses are red"
    assert command.undo() == True
    assert poem.text == ""
    try:
        command.undo()
    except ValueError as e:
        assert str(e) == "Cannot delete more characters than present"


def test_command_poem_composite():
    poem = Poem()
    command1 = PoemCommand(poem, PoemCommand.Action.WRITE, "Roses are red")
    command2 = PoemCommand(poem, PoemCommand.Action.WRITE, "\nViolets are blue")
    command3 = PoemCommand(poem, PoemCommand.Action.DELETE, characters=5)
    command4 = PoemCommand(poem, PoemCommand.Action.WRITE, " yellows")
    command5 = PoemCommand(poem, PoemCommand.Action.DELETE, characters=1)
    compositePoemCommand = CompositePoemCommand(
        [command1, command2, command3, command4, command5]
    )
    compositePoemCommand.execute()
    assert poem.text == "Roses are red\nViolets are yellow"
    compositePoemCommand.undo()
    assert poem.text == ""


def test_command_poem_copy_from_poem():
    poem1 = Poem("Roses are red")
    poem2 = Poem("Violets are blue\n")
    command = CopyFromPoemCommand(poem1, poem2)
    command.execute()
    assert poem1.text == ""
    assert poem2.text == "Violets are blue\nRoses are red"
