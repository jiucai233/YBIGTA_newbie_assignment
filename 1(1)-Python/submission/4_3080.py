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
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    names = input_data[1:]
    names.sort()
    trie = Trie() 
    
    for name in names:
        trie.push(map(ord, name))
        
    MOD = 1_000_000_007
    max_k = 3005
    fact = [1] * max_k
    for i in range(2, max_k):
        fact[i] = (fact[i-1] * i) % MOD

    def get_ans(current_index: int) -> int:
        node = trie[current_index]
        res = 1
        for child_index in node.children:
            res = (res * get_ans(child_index)) % MOD
        
        k = len(node.children) + (1 if node.is_end else 0)
        res = (res * fact[k]) % MOD
        return res

    print(get_ans(0))



if __name__ == "__main__":
    main()