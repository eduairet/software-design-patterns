from software_design_patterns.structural.adapter_pattern import *


def test_adapter_knife():
    EXPECTED_KNIFE = "Knife: small, can_opener: False, screw_driver: False, scissors: False, nail_file: False"
    EXPECTED_UPDATED_KNIFE = "Knife: small, can_opener: True, screw_driver: False, scissors: False, nail_file: False"

    knife = Knife(KnifeSize.SMALL)
    adapter = KnifeToSwissKnifeAdapter(knife)
    assert adapter.size == KnifeSize.SMALL
    assert str(adapter) == EXPECTED_KNIFE

    adapter.can_opener = True
    assert str(adapter) == EXPECTED_UPDATED_KNIFE
