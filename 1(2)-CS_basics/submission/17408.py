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


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    try:
        line1 = input().strip()
        if not line1: return
        n = int(line1)
        
        line2 = input().strip()
        if not line2: return
        raw_arr = list(map(int, line2.split()))
        
        line3 = input().strip()
        if not line3: return
        m = int(line3)
    except ValueError:
        return

    data = [Pair.f_conv(x) for x in raw_arr]

    st = SegmentTree[Pair]()
    st.build(data, Pair.f_merge, Pair.default())

    for _ in range(m):
        query = list(map(int, input().split()))
        op = query[0]

        if op == 1:
            idx, val = query[1], query[2]
            st.update(idx - 1, Pair.f_conv(val))

        elif op == 2:
            l, r = query[1], query[2]
            res_pair = st.query(l - 1, r - 1)
            print(res_pair.sum())


if __name__ == "__main__":
    main()