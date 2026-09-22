import time

import base64
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from flask import Flask, request, jsonify, send_file
from stack_queue import Stack, Queue



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

    fig2, ax2 = plt.subplots()
    ax2.set_xlim(0, max(input_sizes))
    ax2.set_ylim(0, max(times) * 1.1 if max(times) > 0 else 1)
    ax2.set_xlabel('Input Size')
    ax2.set_ylabel('Running Time (seconds)')
    ax2.set_title('Algorithm Time Complexity Visualiser (Animated)')
    line, = ax2.plot([], [], 'o-')

    def update(frame):
        line.set_data(input_sizes[:frame + 1], times[:frame + 1])
        return line,

    animation = anim.FuncAnimation(fig2, update, frames=len(input_sizes), interval=200)
    animation.save('time_complexity_animation.gif', writer='pillow')
    plt.close(fig2)

    with open('time_complexity_animation.gif', 'rb') as f:
        gif_base64 = base64.b64encode(f.read()).decode('utf-8')

    return imag_base64, gif_base64
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
def stack_push_pop(n):
    s = Stack()
    for i in range(n):
        s.push(i)
    print("stack_push_pop: pushed", s.size(), "items using Stack class")
    while not s.is_empty():
        s.pop()
    print("stack_push_pop: stack is now empty:", s.is_empty())
def queue_enqueue_dequeue(n):
    q = Queue()
    for i in range(n):
        q.enqueue(i)
    print("queue_enqueue_dequeue: enqueued", q.size(), "items using Queue class")
    while not q.is_empty():
        q.dequeue()
    print("queue_enqueue_dequeue: queue is now empty:", q.is_empty())


Algorithms = {
    'binary_search': binary_search,
    'linear_search': linear_search,
    'bubble_sort': bubble_sort,
    'nested_loop': nested_loop,
    'stack_push_pop': stack_push_pop,
    'queue_enqueue_dequeue': queue_enqueue_dequeue
}

app = Flask(__name__)
@app.route('/')
def index():
    return jsonify({
        'usage': '/analyze?algo=<name>&step=<int>&n_max=<int>',
        'available_algorithms': list(Algorithms.keys())
    })


@app.route('/analyze')
def analyze():
    algo = request.args.get('algo')
    step = request.args.get('step', type=int)
    n_max = request.args.get('n_max', type=int)

    algorithm = Algorithms[algo]
    image_base64, gif_base64 = time_complexity_visualiser(algorithm, 0, n_max, step)
    return jsonify({
        'algorithm': algo,
        'step': step,
        'n_max': n_max,
        'image_base64': image_base64,
        'gif_base64': gif_base64
    })


@app.route('/plot')
def plot():
    return send_file('time_complexity_plot.png', mimetype='image/png')


@app.route('/animation')
def animation_view():
    return send_file('time_complexity_animation.gif', mimetype='image/gif')


#time_complexity_visualiser(binary_search, 100, 10000, 500)
#time_complexity_visualiser(linear_search, 100, 10000, 500)
#time_complexity_visualiser(bubble_sort, 100, 10000, 100)
time_complexity_visualiser(nested_loop, 100, 1000, 100)

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
