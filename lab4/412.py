import json

def serialize(val):
    if val == "<missing>":
        return "<missing>"
    return json.dumps(val, separators=(',', ':'))

def find_diffs(src, tgt, path=""):
    diffs = []

    keys = set()
    if isinstance(src, dict):
        keys.update(src.keys())
    if isinstance(tgt, dict):
        keys.update(tgt.keys())

    for key in keys:
        full_path = f"{path}.{key}" if path else key

        src_val = src.get(key, "<missing>") if isinstance(src, dict) else "<missing>"
        tgt_val = tgt.get(key, "<missing>") if isinstance(tgt, dict) else "<missing>"
        if isinstance(src_val, dict) and isinstance(tgt_val, dict): #recurse
            diffs.extend(find_diffs(src_val, tgt_val, full_path))
        else:
            if src_val != tgt_val:
                diffs.append(f"{full_path} : {serialize(src_val)} -> {serialize(tgt_val)}")

    return diffs

src = json.loads(input())
tgt = json.loads(input())

diffs = find_diffs(src, tgt)

if diffs:
    for line in sorted(diffs):
        print(line)
else:
    print("No differences")