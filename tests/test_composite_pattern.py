from software_design_patterns.structural.composite_pattern import *


def test_composite_subconscious():
    dream = Dream(DreamType.NIGHTMARE)
    hallucination = Hallucination(HallucinationType.VISUAL)

    composite_subconscious = SubconsciousComposite()
    composite_subconscious.add(dream)
    composite_subconscious.add(hallucination)

    result = composite_subconscious.operation()
    assert (
        "Composite Subconscious: Dreaming in nightmare mode, Experiencing visual hallucination"
        in result
    )

    new_hallucination = Hallucination(HallucinationType.AUDITORY)
    composite_subconscious.add(new_hallucination)
    assert len(composite_subconscious.subconscious_elements) == 3

    composite_subconscious.remove(hallucination)
    assert len(composite_subconscious.subconscious_elements) == 2
