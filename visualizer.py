"""
visualizer.py
--------------
This file has two jobs:
1. Run an algorithm at several different sizes and time each run.
2. Turn those timings into a graph, save it as a picture, and also
   turn that same picture into a base64 string (a way of writing an
   image as plain text, so it can be put inside a JSON response).
"""

import os
import time
import io
import base64

import matplotlib
matplotlib.use('Agg')  # we don't need a pop-up window, just a saved image
import matplotlib.pyplot as plt

from algorithms import ALGORITHMS, COMPLEXITY_LABELS

SNAPSHOT_FOLDER = 'snapshots'


def run_and_time_algorithm(algorithm_name, n_min, n_max, step):
    """
    Runs the algorithm for n = n_min, n_min + step, n_min + 2*step, ...
    up to n_max, timing each run with time.time().
    Returns two lists: the sizes we tested, and how long each one took.
    """
    algorithm_function = ALGORITHMS[algorithm_name]

    sizes_tested = []
    times_taken = []

    n = n_min
    while n <= n_max:
        start_time = time.time()
        algorithm_function(n)
        end_time = time.time()

        sizes_tested.append(n)
        times_taken.append(end_time - start_time)

        n = n + step

    return sizes_tested, times_taken


def make_graph_and_save(algorithm_name, sizes_tested, times_taken):
    """
    Draws a line graph of size vs. time, saves it to the snapshots
    folder, and returns the file path plus a base64 string of the
    same image.
    """
    if not os.path.exists(SNAPSHOT_FOLDER):
        os.makedirs(SNAPSHOT_FOLDER)

    figure = plt.figure()
    plt.plot(sizes_tested, times_taken, 'o-')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time Taken (seconds)')

    complexity_label = COMPLEXITY_LABELS.get(algorithm_name, '')
    plt.title('Time Complexity of ' + algorithm_name + ' - ' + complexity_label)
    plt.grid(True)

    timestamp = int(time.time())
    filename = SNAPSHOT_FOLDER + '/' + algorithm_name + '_' + str(timestamp) + '.png'
    figure.savefig(filename, bbox_inches='tight')

    # Also save a copy into memory so we can turn it into base64 text.
    image_bytes = io.BytesIO()
    figure.savefig(image_bytes, format='png', bbox_inches='tight')
    plt.close(figure)
    image_bytes.seek(0)

    base64_string = base64.b64encode(image_bytes.read()).decode('utf-8')

    return filename, base64_string
