import math
from multiprocessing import Process, Queue
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

def five_step(series):
    repeated_series = series + series
    result = []
    for i in range(len(series)):
        start = (i * 5) % 12
        result.append(sum(repeated_series[start:start+5]) % 12)
    return result

def append_transform(transform, forms):
    for i in range(len(forms)):
        forms.append(transform(forms[i]))

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
    append_transform(quart_circle, forms)
    forms = with_rotations(forms)
    return most_compact(forms)

def tisrf_normalization(series):
    forms = [series, inversion(series), retrograde(series), retrograde_inversion(series)]
    append_transform(five_step, forms)
    forms = with_rotations(forms)
    return most_compact(forms)

def tiqsrf_normalization(series):
    forms = [series, inversion(series), retrograde(series), retrograde_inversion(series)]
    append_transform(quart_circle, forms)
    append_transform(five_step, forms)
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
  "tiqsr": tiqsr_normalization,
  "tisrf": tisrf_normalization,
  "tiqsrf": tiqsrf_normalization
}

def classify_from_lines(method_name, lines):
    method = methods[method_name]
    classes = {}
    len_str = str(len(lines))
    for i, line in enumerate(lines):
        series = read_series(line)
        if not series:
            continue
        normal_form = tuple(method(series))
        if normal_form in classes:
            classes[normal_form] += 1
        else:
            classes[normal_form] = 1
    return classes

def report_classes(classes):
    for series, count in classes.items():
        print(str(series), count)
    print("\ntotal: ", len(classes))

def merge(into, new):
    for form, count in new.items():
        if form in into:
            into[form] = into[form] + count
        else:
            into[form] = count

def child_process_classify(queue, method_name, lines):
    result = classify_from_lines(method_name, lines)
    queue.put(result)
    exit(0)

def create_process(queue, method_name, lines):
    return Process(target=child_process_classify, args=(queue, method_name, lines))

def parallel_classify_from_lines(method_name, lines, nr_processes):
    queue = Queue()
    batch_size = math.ceil(len(lines) / nr_processes)
    processes = [create_process(queue, method_name, lines[i:i + batch_size]) for i in range(0, len(lines), batch_size)]
    for process in processes:
        process.start()
    classes = {}
    for process in processes:
        process.join(1)
        while process.is_alive():
            process.join(1)
            if not queue.empty():
                merge(classes, queue.get())
    while not queue.empty():
        merge(classes, queue.get())
    return classes

def classify_from_file(method_name, file, nr_processes):
    with open(file, "rt") as fin:
        lines = fin.readlines()
    if nr_processes == 1:
        classes = classify_from_lines(method_name, lines)
    else:
        classes = parallel_classify_from_lines(method_name, lines, nr_processes)
    report_classes(classes)

if __name__ == '__main__':
    nr_processes = 1
    if len(sys.argv) > 3:
        nr_processes = int(sys.argv[3])
    classify_from_file(sys.argv[1], sys.argv[2], nr_processes)
