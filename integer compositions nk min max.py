def constrained_compositions(n, k, min_elem, max_elem, equiv=12):
    allowed = range(max_elem, min_elem-1, -1)

    def update_sum(s, v, t):
        if len(t)==0:
            return []
        else:
            return [(x+v)%equiv for x in s] + [(t[-1]+v) % equiv]

    def helper(n, k, t, s):
        if k == 0:
            if n == 0:
                yield t
        
        elif not 0 in s:

            if k == 1:
                if n in allowed:
                    yield t + (n,)
        
            elif min_elem * k <= n <= max_elem * k:
                for v in allowed:
                    yield from helper(n - v, k - 1, t + (v,), update_sum(s, v, t))

    return helper(n, k, (), [])

# Original
'''
for p in constrained_compositions(12, 3, 3, 7):
    print(p)
'''

for p in constrained_compositions(72, 12, 1, 11):
    print(p)