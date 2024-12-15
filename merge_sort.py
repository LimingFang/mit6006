from datetime import datetime
from random import shuffle

# into ascending order.
def insertion_sort(data):
    for i in range(1,len(data)):
        for j in reversed(range(0,i)):
            if data[j+1] < data[j]:
                tmp = data[j]
                data[j] = data[j+1]
                data[j+1] = tmp
    return data

def merge_sort(data):
    if len(data) == 1:
        return data
    mid = int(len(data)/2)
    left = merge_sort(data[0:mid])
    right = merge_sort(data[mid:len(data)])
    return merge(left, right)

def merge(left, right):
    res = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend([left[k] for k in range(i,len(left))])
    res.extend([right[k] for k in range(j,len(right))])

    return res

if __name__ == "__main__":
    is_ok = True
    for i in range(0,10):
        l = [i for i in range(0,1000)]
        shuffle(l)
        l_ = merge_sort(l)
        if not sorted(l_):
            is_ok = False
    if is_ok:
        print("ok")
    else:
        print("not ok")

