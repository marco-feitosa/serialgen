def constrained_compositions(n, k, min_elem, max_elem):
    allowed = range(max_elem, min_elem-1, -1)

    def helper(n, k, t):
        if k == 0:
            if n == 0:
                yield t
        elif k == 1:
            if n in allowed:
                yield t + (n,)
        elif min_elem * k <= n <= max_elem * k:
            for v in allowed:
                yield from helper(n - v, k - 1, t + (v,))

    return helper(n, k, ())

# Original
'''
for p in constrained_compositions(12, 3, 3, 7):
    print(p)
'''

for p in constrained_compositions(72, 12, 1, 11):
    n = 12
    d = 2
    k = 12
    intervals = []
    for i in range(k):
        if i == 0:
            for j in range(i, k-1):
                summation = (sum(p[i:j+1])) % n
                intervals.append(summation)
            
        else:
            for j in range(i, k):
                summation = (sum(p[i:j+1])) % n
                intervals.append(summation)
            
    if (0 not in intervals) and (p.count(1) == 1):
        print(p)