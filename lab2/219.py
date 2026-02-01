n = int(input())
episodes = {}
dorama_list = []

for _ in range(n):
    line = input().split()
    dorama = line[0]
    count = int(line[1])
    
    if dorama not in episodes:
        episodes[dorama] = count
        dorama_list.append(dorama)
    else:
        episodes[dorama] += count

for dorama in sorted(dorama_list):
    print(dorama, episodes[dorama])
