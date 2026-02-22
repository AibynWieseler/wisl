import json
import re

def resolve_query(json_val, query):
    parts = re.findall(r'\w+|\[\d+\]', query)
    current = json_val

    try:
        for part in parts:
            if part.startswith('['):
                idx = int(part[1:-1])
                current = current[idx]
            else:
                current = current[part]
        return json.dumps(current, separators=(',', ':'))
    except (KeyError, IndexError, TypeError):
        return "NOT_FOUND"

json_val = json.loads(input())
q = int(input())
queries = [input().strip() for _ in range(q)]

for query in queries:
    print(resolve_query(json_val, query))