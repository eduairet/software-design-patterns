from software_design_patterns.behavioral.mediator_pattern import *


def test_mediator_boxing():
    ring = Ring()
    canelo = Boxer("Canelo", ring)
    floyd = Boxer("Floyd", ring)
    referee = Referee(ring)

    Knockout = canelo.KnockOut(floyd)
    assert referee(Knockout) == "Referee: Floyd was knocked out by Canelo in round 1"
    assert canelo.knockouts == 1
