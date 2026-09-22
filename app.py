import time
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from flask import Flask, request, jsonify 



def time_complexity_visualiser(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)


    fig, ax = plt.subplots()
    ax.plot(input_sizes, times, 'o-')
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Running Time (seconds)')
    ax.set_title('Algorithm Time Complexity Visualiser')


    fig.savefig('time_complexity_plot.png')
    plt.close(fig)

    with open ('time_complexity_plot.png', 'rb') as f:
        imag_base64 = base64.b64encode(f.read()).decode('utf-8')
    return imag_base64
    # plt.ion()
    # fig, ax = plt.subplots()
    # ax.set_xlabel('Input Size')
    # ax.set_ylabel('Running Time (seconds)')
    # ax.set_title('Algorithm Time Complexity Visualiser (Live)')
    # line, = ax.plot([], [], 'o-')

    # for i, n in enumerate(input_sizes):
    #     start_time = time.time()
    #     algorithm(n)
    #     end_time = time.time()
    #     times.append(end_time - start_time)

    #     line.set_data(input_sizes[:i + 1], times)
    #     ax.relim()
    #     ax.autoscale_view()
    #     plt.draw()
    #     plt.pause(0.1)

    # plt.ioff()
    # plt.show()


def binary_search(n):
    arr = list(range(n))
    target = n - 1
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
def linear_search(n):
    arr = list(range(n))
    target = n - 1
    for i in range(len(arr)):
        if arr[i] == target:
            return i
def bubble_sort(n):
    arr = list(range(n, 0, -1))
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
def nested_loop(n):
    for i in range(n):
        for j in range(n):
            pass


Algorithms = {
    'binary_search': binary_search,
    'linear_search': linear_search,
    'bubble_sort': bubble_sort,
    'nested_loop': nested_loop
}

app = Flask(__name__)
@app.route('/analyze')
def analyze():
    algo = request.args.get('algo')
    step = request.args.get('step', type=int)
    n_max = request.args.get('n_max', type=int)

    algorithm = Algorithms[algo]
    image_base64 = time_complexity_visualiser(algorithm, 0, n_max, step)
    return jsonify({
        'algorithm': algo,
        'step': step,
        'n_max': n_max,
        'image_base64': image_base64
    })


#time_complexity_visualiser(binary_search, 100, 10000, 500)
#time_complexity_visualiser(linear_search, 100, 10000, 500)
#time_complexity_visualiser(bubble_sort, 100, 10000, 100)
#time_complexity_visualiser(nested_loop, 100, 1000, 100)
