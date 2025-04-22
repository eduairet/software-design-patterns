class PatriciaTrieNode:
    def __init__(self, key: str = ""):
        self.key = key
        self.children = {}
        self.is_end_of_word = False


def traverse(node: PatriciaTrieNode, prefix: str):
    if node.is_end_of_word:
        yield prefix
    for child in node.children.values():
        yield from traverse(child, prefix + child.key)


class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaTrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = PatriciaTrieNode(char)
            node = node.children[char]
        node.is_end_of_word = True

    def __iter__(self):
        return traverse(self.root, "")
