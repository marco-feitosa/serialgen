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

def quart_circle(series):
    return [(5 * x) % 12 for x in series]

def rotations(x):
    result = []
    for i in range(len(x)):
        b = x[i:] + x[:i]
        result.append(b)
    return result

def with_rotations(forms):
    return [x for y in forms for x in rotations(y)]

def lowest_by_snd(pairs):
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

def most_compact(forms):
    for b in range(12, 0, -1):
        sums = [(x, sum(x[0:b])) for x in forms]
        candidates = lowest_by_snd(sums)
        if len(candidates) == 1:
            return candidates[0][0]
        else:
            forms = [x[0] for x in candidates]
    return min(forms, key=sum)

def tr_normalization(series):
    forms = [series, retrograde(series)]
    return most_compact(forms)

def tir_normalization(series):
    forms = [series, inversion(series), retrograde(series), retrograde_inversion(series)]
    return most_compact(forms)

def ts_normalization(series):
    forms = rotations(series)
    return most_compact(forms)

def tis_normalization(series):
    forms = with_rotations([series, inversion(series)])
    return most_compact(forms)

def tisr_normalization(series):
    forms = with_rotations([series, inversion(series), retrograde(series), retrograde_inversion(series)])
    return most_compact(forms)

def tisr_normalization(series):
    forms = with_rotations([series, inversion(series), retrograde(series), retrograde_inversion(series)])
    return most_compact(forms)

def tiqsr_normalization(series):
    forms = [series, inversion(series), retrograde(series), retrograde_inversion(series)]
    for i in range(len(forms)):
        forms.append(quart_circle(forms[i]))
    forms = with_rotations(forms)
    return most_compact(forms)

def read_series(line):
    try:
        return [int(x) for x in line.strip(" \n()").split(",")]
    except:
        return None

methods = {
  "tr": tr_normalization,
  "tir": tir_normalization,
  "ts": ts_normalization,
  "tis": tis_normalization,
  "tisr": tisr_normalization,
  "tiqsr": tiqsr_normalization
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
