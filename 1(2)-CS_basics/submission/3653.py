from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


@dataclass
class SetmentTree(Generic[T,U]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False

class SegmentTree(Generic[T, U]):
    def __init__(self):
        self.tree: list[Optional[U]] = []
        self.n = 0
        self.func: Callable[[U, U], U] = None
        self.default: U = None

    def build(self, data: list[T], func: Callable[[U, U], U], default: U) -> None:
        """
        data: initial data list
        func: merging function (e.g., sum, min, max)
        default: -
        """
        self.n = len(data)
        self.func = func
        self.default = default
        self.tree = [default] * (4 * self.n)
        
        self._build_recursive(data, 1, 0, self.n - 1)

    def _build_recursive(self, data: list[T], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start] 
            return

        mid = (start + end) // 2
        self._build_recursive(data, 2 * node, start, mid)
        self._build_recursive(data, 2 * node + 1, mid + 1, end)
        
        self.tree[node] = self.func(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, idx: int, diff: U) -> None:
        self._update_recursive(1, 0, self.n - 1, idx, diff)

    def _update_recursive(self, node: int, start: int, end: int, idx: int, diff: U) -> None:
        if idx < start or idx > end:
            return

        self.tree[node] = self.func(self.tree[node], diff)

        if start != end:
            mid = (start + end) // 2
            self._update_recursive(2 * node, start, mid, idx, diff)
            self._update_recursive(2 * node + 1, mid + 1, end, idx, diff)

    def query_kth(self, k: int) -> int:
        return self._query_kth_recursive(1, 0, self.n - 1, k)

    def _query_kth_recursive(self, node: int, start: int, end: int, k: int) -> int:
        if start == end:
            return start

        mid = (start + end) // 2
        left_val = self.tree[2 * node]

        if k <= left_val:
            return self._query_kth_recursive(2 * node, start, mid, k)
        else:
            return self._query_kth_recursive(2 * node + 1, mid + 1, end, k - left_val)


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    try:
        line = input().strip()
        if not line: return
        num_test_cases = int(line)
    except ValueError:
        return

    for _ in range(num_test_cases):
        try:
            line = input().split()
            if not line: break
            n, m = map(int, line)
            query_seq = list(map(int, input().split()))
        except ValueError:
            break
        
        MAX_LEN = n + m + 1

        init_data = [0] * MAX_LEN
        pos = [0] * (n + 1) 

        for i in range(1, n + 1):
            pos[i] = m + i
            init_data[m + i] = 1
        
        st = SegmentTree[int, int]()
        st.build(init_data, lambda a, b: a + b, 0)
        
        results = []
        current_top_pos = m 

        for dvd_num in query_seq:
            curr_idx = pos[dvd_num]
            
            ans = st.query_sum(1, curr_idx - 1)
            results.append(str(ans))
            
            st.update(curr_idx, 0)
            
            st.update(current_top_pos, 1)
            pos[dvd_num] = current_top_pos
            
            current_top_pos -= 1
            
        print(" ".join(results))


if __name__ == "__main__":
    main()