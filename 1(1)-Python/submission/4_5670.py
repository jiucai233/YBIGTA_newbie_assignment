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




import sys


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - int: Used ASCII code of characters in the word to be queried
    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = None # 구현하세요!
        for child_index in trie[pointer].children:
            if trie[child_index].body == element:
                new_index = child_index
                break
        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    while True:
        try:
            line = input().strip()
            if not line:
                break
            n = int(line)
        except ValueError:
            break

        trie = Trie() 
        
        words_int: list[list[int]] = []

        for _ in range(n):
            line = input().strip()
            
            word_as_ints = list(map(ord, line))
            
            words_int.append(word_as_ints)
            trie.push(word_as_ints)

        total_strokes = 0
        for word in words_int:
            total_strokes += count(trie, word)

        print(f"{total_strokes / n:.2f}")


if __name__ == "__main__":
    main()