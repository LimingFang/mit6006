from random import shuffle
from array import array
def counter_sort(arr):
    min_val = min(arr)
    max_val = max(arr)
    arr_list = []
    for i in range(max_val-min_val+1):
        arr_list.append(array('l'))
    for i in arr:
        arr_list[i-min_val].append(i)
    res = []
    for l in arr_list:
        res.extend(l)
    return res

if __name__ == "__main__":
    is_ok = True
    for i in range(0, 10):
        l = [i for i in range(0, 1000)]
        shuffle(l)
        l_ = counter_sort(l)
        if not sorted(l_):
            is_ok = False
    if is_ok:
        print("ok")
    else:
        print("not ok")