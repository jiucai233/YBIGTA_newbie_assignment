from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    try:
        line = input().strip()
        if not line:
            return
        n = int(line)
    except ValueError:
        return
    MAX_FLAVOR = 1_000_000
    
    initial_data = [0] * (MAX_FLAVOR + 1)

    st = SegmentTree[int, int]()
    
    st.build(initial_data, lambda a, b: a + b, 0)

    for _ in range(n):
        args = list(map(int, input().split()))
        cmd = args[0]

        if cmd == 1:
            rank = args[1]
            
            flavor_idx = st.query_kth(rank)
            print(flavor_idx)
            
            st.update(flavor_idx, -1)

        elif cmd == 2:
            flavor_idx = args[1]
            count = args[2]
            
            st.update(flavor_idx, count)


if __name__ == "__main__":
    main()