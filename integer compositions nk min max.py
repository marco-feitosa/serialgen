def restricted_compositions(s, k, n):
    allowed = range(1, n)

    def restrict(r, alpha_j, alpha):
        if len(alpha) == 0:
            return []
        else:
            return [(summ+alpha_j)%n for summ in r] + [(alpha[-1]+alpha_j) % n]
    
    def compose(s, k, alpha = (), r = []):
        if k == 0:
            if s == 0:
                yield alpha
        
        elif not 0 in r:
            if k == 1:
                if s in allowed:
                    yield alpha + (s,)
                
            elif k <= s <= (n-1)*k:
                for alpha_j in allowed:
                    yield from compose(s - alpha_j, k - 1, alpha + (alpha_j,), restrict(r, alpha_j, alpha))
    
    return compose(s, k)


f = open('comp_of_24.txt', 'w')
counter = 0
for p in restricted_compositions(24, 12, 1, 11):
    f.write(f'{p}\n')
    counter+=1
f.write(f'\nNUMBER OF SERIES: {counter}')
f.close()