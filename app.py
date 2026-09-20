"""
This is the actual web server. It has one main job: when someone
visits /analyze with an algorithm name, a step size, and a max size,
it runs that algorithm at increasing sizes, times it, makes a graph,
and sends back a JSON response with the timing data and the graph
(both saved as a file and included as base64 text).

"""

from flask import Flask, jsonify, request

from algorithms import ALGORITHMS, MAX_SIZES, COMPLEXITY_LABELS
from visualizer import run_and_time_algorithm, make_graph_and_save

app = Flask(__name__)


@app.route('/')
def home_page():
    # A friendly message so people know the server is alive and
    # know how to use it.
    return jsonify({
        'message': 'Time Complexity Visualizer is running!',
        'try_this': '/analyze?algo=linear_search&step=1000&n_max=10000',
        'supported_algorithms': list(ALGORITHMS.keys())
    })


@app.route('/algorithms')
def list_algorithms():
    # Shows every algorithm we support, along with its Big-O label
    # and the biggest size we'll let someone test it with.
    algorithm_info = {}
    for name in ALGORITHMS:
        algorithm_info[name] = {
            'complexity': COMPLEXITY_LABELS[name],
            'max_n': MAX_SIZES[name]
        }
    return jsonify(algorithm_info)


@app.route('/analyze', methods=['GET'])
def analyze():
    # Read the query parameters from the URL, e.g.
    # ?algo=linear_search&step=1000&n_max=10000
    algo_name = request.args.get('algo')
    step_text = request.args.get('step')
    n_max_text = request.args.get('n_max')

    # People sometimes type the algo name with quotes or brackets by
    # accident (like algo=['linear_search'), so we clean that up.
    if algo_name is not None:
        algo_name = algo_name.strip()
        algo_name = algo_name.strip("[]'\"")

    # Make sure all three parameters were actually given.
    if algo_name is None or step_text is None or n_max_text is None:
        return jsonify({
            'error': 'Please provide algo, step, and n_max as query parameters.'
        }), 400

    # Check the algorithm name is one we actually support.
    if algo_name not in ALGORITHMS:
        return jsonify({
            'error': "I don't know an algorithm called '" + algo_name + "'.",
            'supported_algorithms': list(ALGORITHMS.keys())
        }), 400

    # step and n_max need to be whole numbers. People might type
    # commas like 10,000, so we remove those before converting.
    try:
        step = int(step_text.replace(',', ''))
        n_max = int(n_max_text.replace(',', ''))
    except ValueError:
        return jsonify({'error': 'step and n_max must be whole numbers.'}), 400

    if step <= 0:
        return jsonify({'error': 'step must be greater than 0.'}), 400
    if n_max < 0:
        return jsonify({'error': 'n_max cannot be negative.'}), 400

    # Some algorithms get extremely slow with a big n, so we check
    # against the safe limit we set for this one.
    biggest_allowed = MAX_SIZES[algo_name]
    if n_max > biggest_allowed:
        return jsonify({
            'error': ('n_max for ' + algo_name + ' cannot be more than '
                       + str(biggest_allowed) + ' (a run that big would take too long).')
        }), 400

    # The minimum size is always assumed to be 0.
    n_min = 0

    sizes_tested, times_taken = run_and_time_algorithm(algo_name, n_min, n_max, step)
    filename, base64_image = make_graph_and_save(algo_name, sizes_tested, times_taken)

    return jsonify({
        'algorithm': algo_name,
        'complexity': COMPLEXITY_LABELS[algo_name],
        'n_min': n_min,
        'n_max': n_max,
        'step': step,
        'input_sizes': sizes_tested,
        'execution_times': times_taken,
        'image_path': filename,
        'image_base64': base64_image
    })


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
