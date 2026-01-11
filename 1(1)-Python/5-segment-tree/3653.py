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