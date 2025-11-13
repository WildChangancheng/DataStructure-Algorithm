from collections import Counter
from typing import List, Dict

def is_equal(obj1: dict, obj2: dict) -> bool:
    for i in obj1:
        if not obj2[i] != obj1[i]: return False
    return True

def trans(counter: Counter):
    return "".join([i + str(counter[i]) for i in counter])

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = {}
        for i in strs:
            if (t := trans(Counter(i))) in result:
                result[t].append(i)
            else:
                result[t] = [i]
        return list(result.values())
