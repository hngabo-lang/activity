import time
import base64
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from flask import Flask, request, jsonify, send_file
from stack_queue import Stack, Queue
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///analysis.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class AnalysisResult(Base):
    __tablename__ = 'analysis_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    loop_name = Column(String, nullable=False)
    n_min = Column(Integer, nullable=False)
    n_max = Column(Integer, nullable=False)
    n_step = Column(Integer, nullable=False)
    plot_url = Column(String)
    animation_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(engine)


def save_run_to_db(run_info):
    session = Session()
    record = AnalysisResult(
        loop_name=run_info['loop'],
        n_min=run_info['n_min'],
        n_max=run_info['n_max'],
        n_step=run_info['n_step'],
        plot_url=run_info.get('plot_url'),
        animation_url=run_info.get('animation_url')
    )
    session.add(record)
    session.commit()
    new_id = record.id
    session.close()
    return new_id


# ---------------------------------------------------------------------------
# Small helpers (these replace the repeated blocks that used to appear
# 3x inside time_complexity_visualiser and again across the Flask routes)
# ---------------------------------------------------------------------------

def _dump_json(run_info, json_filename):
    """Write run_info to disk. Was previously duplicated 3 times inline."""
    with open(json_filename, 'w') as f:
        json.dump(run_info, f, indent=2)


def _file_to_base64(path):
    """Read a file and return its base64-encoded contents. Was duplicated
    once for the PNG plot and once for the GIF animation."""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def _build_arr_and_target(n):
    """Shared setup used identically by binary_search and linear_search."""
    arr = list(range(n))
    target = n - 1
    return arr, target


def _run_and_package(algorithm, algo_name, n_min, n_max, step):
    """Run the visualiser and build the JSON-ready result dict. This body
    was previously copy-pasted (with only key names changing) across the
    /analyze, /save_analysis and /analyze_all routes."""
    image_base64, gif_base64, json_filename = time_complexity_visualiser(
        algorithm, n_min, n_max, step
    )
    return {
        'algorithm': algo_name,
        'step': step,
        'n_max': n_max,
        'image_base64': image_base64,
        'gif_base64': gif_base64,
        'json_filename': json_filename
    }


def time_complexity_visualiser(algorithm, n_min, n_max, n_step, json_filename=None):
    times = []
    input_sizes = list(range(n_min, n_max + n_step, n_step))

    if json_filename is None:
        json_filename = f'{algorithm.__name__}_timing.json'

    run_info = {
        'loop': algorithm.__name__,
        'n_min': n_min,
        'n_max': n_max,
        'n_step': n_step
    }

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

        # write JSON after every point so the file updates as the loop runs
        _dump_json(run_info, json_filename)

    fig, ax = plt.subplots()
    ax.plot(input_sizes, times, 'o-')
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Running Time (seconds)')
    ax.set_title('Algorithm Time Complexity Visualiser')
    fig.savefig('time_complexity_plot.png')
    plt.close(fig)

    image_base64 = _file_to_base64('time_complexity_plot.png')

    run_info['plot_url'] = 'http://localhost:5000/plot'
    _dump_json(run_info, json_filename)

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

    gif_base64 = _file_to_base64('time_complexity_animation.gif')

    run_info['animation_url'] = 'http://localhost:5000/animation'
    _dump_json(run_info, json_filename)

    return image_base64, gif_base64, json_filename


def binary_search(n):
    arr, target = _build_arr_and_target(n)
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
    arr, target = _build_arr_and_target(n)
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
    n_min = request.args.get('n_min', type=int, default=0)

    result = _run_and_package(Algorithms[algo], algo, n_min, n_max, step)
    return jsonify(result)


@app.route('/save_analysis')
def save_analysis():
    algo = request.args.get('algo')
    step = request.args.get('step', type=int)
    n_max = request.args.get('n_max', type=int)
    n_min = request.args.get('n_min', type=int, default=0)

    result = _run_and_package(Algorithms[algo], algo, n_min, n_max, step)

    with open(result['json_filename']) as f:
        run_info = json.load(f)

    record_id = save_run_to_db(run_info)

    return jsonify({
        'status': 'saved',
        'id': record_id,
        'loop': run_info['loop'],
        'n_min': run_info['n_min'],
        'n_max': run_info['n_max'],
        'n_step': run_info['n_step'],
        'plot_url': run_info.get('plot_url'),
        'animation_url': run_info.get('animation_url')
    })


@app.route('/plot')
def plot():
    return send_file('time_complexity_plot.png', mimetype='image/png')


@app.route('/animation')
def animation_view():
    return send_file('time_complexity_animation.gif', mimetype='image/gif')


@app.route('/analyze_all')
def analyze_all():
    step = request.args.get('step', type=int, default=50)
    n_max = request.args.get('n_max', type=int, default=500)

    results = [
        _run_and_package(algorithm, algo_name, 0, n_max, step)
        for algo_name, algorithm in Algorithms.items()
    ]

    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    return jsonify(results)


if __name__ == '__main__':
    init_db()
    app.run(host='localhost', port=5000, debug=True)