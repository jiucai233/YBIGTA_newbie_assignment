from lib import Trie
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