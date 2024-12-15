from random import shuffle


# value of i-th node: data[i-1]
# value of i-th node's parent: data[int(i/2) - 1]
# value of i-th node's left child: data[i*2 - 1]

# max heapify the tree denoted by data[idx-1].
def max_heapify(data, n, idx):
    if idx > int(n / 2):
        return
    left = data[idx * 2 - 1]
    right = left - 1 if idx * 2 >= n else data[idx * 2]
    if data[idx - 1] >= left and data[idx] >= right:
        return
    if left > right:
        data[idx - 1], data[idx * 2 - 1] = data[idx * 2 - 1], data[idx - 1]
        max_heapify(data, n, idx * 2)
    else:
        data[idx - 1], data[idx * 2] = data[idx * 2], data[idx - 1]
        max_heapify(data, n, idx * 2 + 1)


def build_max_heap(data):
    for i in range(int(len(data) / 2), 0, -1):
        max_heapify(data, len(data), i)


def heap_sort(data):
    build_max_heap(data)
    heap_len = len(data)
    for i in range(0, len(data)):
        data[heap_len - 1], data[0] = data[0], data[heap_len - 1]
        heap_len -= 1
        max_heapify(data, heap_len, 1)

    return data


if __name__ == "__main__":
    is_ok = True
    for i in range(0, 10):
        l = [i for i in range(0, 1000)]
        shuffle(l)
        l_ = heap_sort(l)
        if not sorted(l_):
            is_ok = False
    if is_ok:
        print("ok")
    else:
        print("not ok")
