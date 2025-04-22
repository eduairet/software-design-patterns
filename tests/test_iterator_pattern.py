from software_design_patterns.behavioral.iterator_pattern import *


def test_iterator_patricia_trie():
    trie = PatriciaTrie()
    trie.insert("cat")
    trie.insert("car")
    trie.insert("cart")
    trie.insert("dog")

    words = [word for word in trie]
    assert words == ["cat", "car", "cart", "dog"]
    assert len(words) == 4
    assert "cat" in words
