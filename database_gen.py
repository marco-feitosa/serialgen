def restricted_compositions(s, k, n):
    allowed = range(1, n)

    def restrict(r, part, composition):
        if len(composition) == 0:
            return []
        else:
            return [(summation + part) % n for summation in r] + [(composition[-1] + part) % n]
    
    def compute(s, k, composition = (), r = []):
        if k == 0:
            if s == 0:
                yield composition
        
        elif not 0 in r:
            if k == 1:
                if s in allowed:
                    yield composition + (s,)
                
            elif k <= s <= (n-1)*k:
                for part in allowed:
                    yield from compute(s - part, k - 1, composition + (part,), restrict(r, part, composition))
    
    return compute(s, k)


f = open('comp_of_24.txt', 'w')
counter = 0
for p in restricted_compositions(24, 12, 1, 11):
    f.write(f'{p}\n')
    counter+=1
f.write(f'\nNUMBER OF SERIES: {counter}')
f.close()