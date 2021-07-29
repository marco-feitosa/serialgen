mod = 12
card = 12

#sets, interval compositions, interval partitions
#ex.: print('[0, 2, 4, 8]'.translate(setstr))
setstr = str.maketrans('[]', '{}')
icstr = str.maketrans('[]', '<>')
ipstr = str.maketrans('[]', '()')

#interval composition
ic = [3,2,4,5,6,8,9,10,8,3,8,6]
print('ic:', str(ic).translate(icstr).replace(' ', ''))

#all rotations
def all_rot_func():
    all_rot = []
    for i in range(card):
        rot_ic = list(ic[i:] + ic[:i])
        all_rot.append(rot_ic)
    return all_rot

all_rot = list(all_rot_func())
print('all-rot:', str(all_rot).translate(icstr).replace(' ', ''))

#interval normal form
max_ci = max(ic)
min_ci = min(ic)
def inf_func():
    inf = list(all_rot)
    for i in range(card-1, -1, -1):
        if inf.count(inf[i]) > 1:
            inf.remove(inf[i])

    a = len(inf)
    for j in range(a-1, -1, -1):
        if inf[j][card-1] < max_ci:
            inf.remove(inf[j])

    b = len(inf)
    inc = 0
    if b > 1:
        while b > 1:
            x = []
            for k in range(b):
                y = sum(inf[k][0:card-1 - inc])
                x.append(y)
            for l in range(b-1, -1, -1):
                if x[l] > min(x):
                    inf.remove(inf[l])
            b = len(inf)
            inc += 1
        return inf[0]
    else:
        return inf[0]

inf = list(inf_func())
print('inf:', str(inf).translate(icstr).replace(' ', ''))