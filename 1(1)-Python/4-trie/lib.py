from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        current_index = 0  

        for element in seq:
            current_node = self[current_index]

            found_in_children = False
            for child_index in current_node.children:
                child_node = self[child_index]
                if child_node.body == element:
                    current_index = child_index
                    found_in_children = True
                    break

            if not found_in_children:
                new_node = TrieNode(body=element)
                self.append(new_node)
                new_node_index = len(self) - 1
                current_node.children.append(new_node_index)

                current_index = new_node_index

        self[current_index].is_end = True

