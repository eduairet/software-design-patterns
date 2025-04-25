from software_design_patterns.behavioral.observer_pattern import *


def test_observer_radio():
    EXPECTED_LOG = [
        "Now playing: Laisse-moi by KeBlack | Time: 1/2",
        "Now playing: Laisse-moi by KeBlack | Time: 2/2",
        "Next song: Chona by Los Tucanes de Tijuana",
        "Now playing: Chona by Los Tucanes de Tijuana | Time: 1/3",
        "Now playing: Chona by Los Tucanes de Tijuana | Time: 2/3",
        "Now playing: Chona by Los Tucanes de Tijuana | Time: 3/3",
        "No more songs in the queue.",
    ]

    laisse_moi = Song("Laisse-moi", "KeBlack", 2)
    chona = Song("Chona", "Los Tucanes de Tijuana", 3)

    radio = Radio().add_song(laisse_moi).add_song(chona)
    radio.property_changed.append(song_changed)
    print("\nPlaying radio...")
    radio.play()

    assert radio.log == EXPECTED_LOG

    radio.property_changed.remove(song_changed)

    assert len(radio.property_changed) == 0
