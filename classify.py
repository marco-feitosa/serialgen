import sys

def inversion(series):
    return [12 - x for x in series]

def retrograde(series):
    result = inversion(series)
    result[0:11] = result[0:11][::-1]
    return result

def retrograde_inversion(series):
    result = series.copy()
    result[0:11] = result[0:11][::-1]
    return result

def lowest_by(pairs):
    val = None
    result = None 
    for x in pairs:
        if not val:
            val = x[1]
            result = [x]
        elif x[1] < val:
            val = x[1]
            result = [x]
        elif x[1] == val:
            result.append(x)
    return result

def schoenberg_normalization(series):
    forms = [series, inversion(series), retrograde(series), retrograde_inversion(series)]
    for b in range(12, 0, -1):
        sums = [(x, sum(x[0:b])) for x in forms]
        candidates = lowest_by(sums)
        if len(candidates) == 1:
            return candidates[0][0]
        else:
            forms = [x[0] for x in candidates]
    return min(forms, key=sum)

def read_series(line):
    try:
        return [int(x) for x in line.strip(" \n()").split(",")]
    except:
        return None

methods = {
  "schoenberg": schoenberg_normalization
}

def classify_from_file(method_name, file):
    method = methods[method_name]
    classes = {}
    with open(file, "rt") as fin:
        for line in fin.readlines():
            series = read_series(line)
            if not series:
                continue
            normal_form = tuple(method(series))
            if normal_form in classes:
                classes[normal_form] += 1
            else:
                classes[normal_form] = 1
        for series, count in classes.items():
            print(str(series), count)
        print("\ntotal: ", len(classes))

if __name__ == '__main__':
    classify_from_file(sys.argv[1], sys.argv[2])
