from lib import Trie
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