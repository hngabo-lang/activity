"""
algorithms.py
--------------
This file holds every algorithm we can test, plus some simple
dictionaries that describe them (their Big-O complexity, and the
biggest "n" we should let someone test them with, so the server
doesn't freeze on a huge run).

Each algorithm function takes one number, n, builds its own test
data of that size, and does some work. We don't care what it
returns - we only care how long it takes to run.
"""

import random


def linear_search(n):
    # Look through every item one at a time. Worst case: the target
    # isn't in the list, so we check all n items. This is O(n).
    numbers = list(range(n))
    target = -1  # not in the list, so we always search everything
    for i in range(len(numbers)):
        if numbers[i] == target:
            return i
    return -1


def binary_search(n):
    # Cuts the search area in half every time. Much faster than
    # linear search for big lists. This is O(log n).
    numbers = list(range(n))
    target = -1  # not in the list, so we search until nothing is left
    low = 0
    high = len(numbers) - 1
    while low <= high:
        middle = (low + high) // 2
        if numbers[middle] == target:
            return middle
        elif numbers[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def bubble_sort(n):
    # Compares neighbors and swaps them if they're out of order,
    # over and over. Slow: O(n^2). We start with a backwards list,
    # which is the worst case (the most possible swaps).
    numbers = list(range(n, 0, -1))
    for i in range(len(numbers)):
        for j in range(len(numbers) - i - 1):
            if numbers[j] > numbers[j + 1]:
                temp = numbers[j]
                numbers[j] = numbers[j + 1]
                numbers[j + 1] = temp
    return numbers


def nested_loops(n):
    # A plain example of O(n^2): one loop inside another, both
    # running n times.
    count = 0
    for i in range(n):
        for j in range(n):
            count = count + 1
    return count


def selection_sort(n):
    # Finds the smallest remaining number and moves it into place,
    # again and again. Also O(n^2).
    numbers = list(range(n, 0, -1))
    for i in range(len(numbers)):
        smallest_index = i
        for j in range(i + 1, len(numbers)):
            if numbers[j] < numbers[smallest_index]:
                smallest_index = j
        temp = numbers[i]
        numbers[i] = numbers[smallest_index]
        numbers[smallest_index] = temp
    return numbers


def insertion_sort(n):
    # Builds a sorted list one item at a time by sliding each new
    # number into the right spot. O(n^2) in the worst case (a
    # backwards list, like we use here).
    numbers = list(range(n, 0, -1))
    for i in range(1, len(numbers)):
        current = numbers[i]
        j = i - 1
        while j >= 0 and numbers[j] > current:
            numbers[j + 1] = numbers[j]
            j = j - 1
        numbers[j + 1] = current
    return numbers


def _merge_sort_helper(numbers):
    if len(numbers) <= 1:
        return numbers

    middle = len(numbers) // 2
    left_half = _merge_sort_helper(numbers[:middle])
    right_half = _merge_sort_helper(numbers[middle:])

    merged = []
    i = 0
    j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            merged.append(left_half[i])
            i = i + 1
        else:
            merged.append(right_half[j])
            j = j + 1
    merged.extend(left_half[i:])
    merged.extend(right_half[j:])
    return merged


def merge_sort(n):
    # Splits the list in half, sorts each half, then merges them
    # back together. O(n log n) - faster than the O(n^2) sorts
    # above once n gets big.
    numbers = list(range(n, 0, -1))
    return _merge_sort_helper(numbers)


def _quick_sort_helper(numbers):
    if len(numbers) <= 1:
        return numbers

    pivot = numbers[len(numbers) // 2]
    smaller = [x for x in numbers if x < pivot]
    equal = [x for x in numbers if x == pivot]
    bigger = [x for x in numbers if x > pivot]

    return _quick_sort_helper(smaller) + equal + _quick_sort_helper(bigger)


def quick_sort(n):
    # Picks a "pivot" number, puts everything smaller on one side and
    # everything bigger on the other, then repeats. O(n log n) on
    # average.
    numbers = list(range(n, 0, -1))
    return _quick_sort_helper(numbers)


def _sift_down(numbers, root, end):
    # Used by heap_sort to push a number down into the right spot.
    while True:
        child = 2 * root + 1
        if child >= end:
            return
        if child + 1 < end and numbers[child] < numbers[child + 1]:
            child = child + 1
        if numbers[root] >= numbers[child]:
            return
        temp = numbers[root]
        numbers[root] = numbers[child]
        numbers[child] = temp
        root = child


def heap_sort(n):
    # Builds a "heap" (a special tree shape stored in a list) and
    # repeatedly pulls the biggest number out of it. O(n log n).
    numbers = list(range(n, 0, -1))
    size = len(numbers)

    start = size // 2 - 1
    while start >= 0:
        _sift_down(numbers, start, size)
        start = start - 1

    end = size - 1
    while end > 0:
        temp = numbers[0]
        numbers[0] = numbers[end]
        numbers[end] = temp
        _sift_down(numbers, 0, end)
        end = end - 1

    return numbers


def constant_time(n):
    # Always does the same amount of work no matter how big n is.
    # This is O(1) - useful to see as a flat line on the graph.
    numbers = list(range(n))
    if len(numbers) > 0:
        return numbers[0]
    return None


def jump_search(n):
    # Jumps ahead in blocks instead of checking one item at a time,
    # then searches the last block normally. O(sqrt(n)).
    numbers = list(range(n))
    target = n  # bigger than every item, so this is the worst case

    if n == 0:
        return -1

    block_size = int(n ** 0.5)
    if block_size == 0:
        block_size = 1

    previous = 0
    while previous < n and numbers[min(previous + block_size, n) - 1] < target:
        previous = previous + block_size

    end_of_block = min(previous + block_size, n)
    for i in range(previous, end_of_block):
        if numbers[i] == target:
            return i
    return -1


def matrix_multiplication(n):
    # Multiplies two n-by-n matrices together the "textbook" way,
    # with three nested loops. O(n^3) - gets slow fast, so we keep
    # n small for this one.
    random.seed(42)  # same random numbers every time, for fair comparisons
    matrix_a = [[random.random() for _ in range(n)] for _ in range(n)]
    matrix_b = [[random.random() for _ in range(n)] for _ in range(n)]
    result = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total = total + matrix_a[i][k] * matrix_b[k][j]
            result[i][j] = total
    return result


def fibonacci_recursive(n):
    # The classic "slow" way to calculate Fibonacci numbers, by
    # calling itself twice for every number. O(2^n) - grows
    # extremely fast, so only test this with small n.
    if n < 2:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def permutations(n):
    # Counts every possible ordering of n items. O(n!) - grows so
    # fast that even n=10 takes a noticeable moment.
    items = list(range(n))
    count_holder = [0]  # a list so the inner function can change it

    def try_all_orders(remaining_items):
        if len(remaining_items) == 0:
            count_holder[0] = count_holder[0] + 1
            return
        for i in range(len(remaining_items)):
            rest = remaining_items[:i] + remaining_items[i + 1:]
            try_all_orders(rest)

    try_all_orders(items)
    return count_holder[0]


# This connects each algorithm's name (what you type in the URL) to
# the function that actually runs it.
ALGORITHMS = {
    'linear_search': linear_search,
    'binary_search': binary_search,
    'bubble_sort': bubble_sort,
    'nested_loops': nested_loops,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort,
    'quick_sort': quick_sort,
    'heap_sort': heap_sort,
    'constant_time': constant_time,
    'jump_search': jump_search,
    'matrix_multiplication': matrix_multiplication,
    'fibonacci_recursive': fibonacci_recursive,
    'permutations': permutations,
}

# Some of these algorithms get incredibly slow with a big n (like
# fibonacci_recursive or permutations). This dictionary sets a safe
# upper limit for each one, so someone can't accidentally freeze
# the server by asking for too large a test.
MAX_SIZES = {
    'linear_search': 1000000,
    'binary_search': 1000000,
    'bubble_sort': 10000,
    'nested_loops': 10000,
    'selection_sort': 10000,
    'insertion_sort': 10000,
    'merge_sort': 1000000,
    'quick_sort': 1000000,
    'heap_sort': 1000000,
    'constant_time': 1000000,
    'jump_search': 1000000,
    'matrix_multiplication': 250,
    'fibonacci_recursive': 32,
    'permutations': 10,
}

# A simple label for what Big-O complexity each algorithm is, just
# so we can include it in the response and it's easy to understand.
COMPLEXITY_LABELS = {
    'linear_search': 'O(n)',
    'binary_search': 'O(log n)',
    'bubble_sort': 'O(n^2)',
    'nested_loops': 'O(n^2)',
    'selection_sort': 'O(n^2)',
    'insertion_sort': 'O(n^2)',
    'merge_sort': 'O(n log n)',
    'quick_sort': 'O(n log n)',
    'heap_sort': 'O(n log n)',
    'constant_time': 'O(1)',
    'jump_search': 'O(sqrt n)',
    'matrix_multiplication': 'O(n^3)',
    'fibonacci_recursive': 'O(2^n)',
    'permutations': 'O(n!)',
}
