users = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 2}]

unique_users = []
for i in range(len(users)):
    seen = False
    for j in range(len(unique_users)):
        if users[i] == unique_users[j]:
            seen = True
            break
    if not seen:
        unique_users.append(users[i])
        

import time
import matplotlib.pyplot as plt


def time_complexity_visualizer(algorithm, n_min, n_max, n_step, title=None):
    """
    Runs 'algorithm' for n = n_min, n_min + n_step, ... up to n_max.
    Each time, it times how long the run took and adds a new point
    to a graph that is visibly updating as the loop runs.

    'algorithm' needs to be a function that takes just one number, n,
    and does some work with it.

    'title' is optional - if you don't pass one, we just use the
    function's own name, so you can tell graphs apart when testing
    several algorithms in a row.
    """
    if title is None:
        title = algorithm.__name__

    input_sizes = []
    times_taken = []

    plt.ion()  # turn on "interactive mode" so the window can update live
    figure, axis = plt.subplots()
    axis.set_xlabel('Input Size')
    axis.set_ylabel('Time Taken (seconds)')
    axis.set_title('Time Complexity Visualizer (Live) - ' + title)
    line, = axis.plot([], [], 'o-')

    n = n_min
    while n <= n_max:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()

        input_sizes.append(n)
        times_taken.append(end_time - start_time)

        # update the line with every point we have so far, then
        # redraw the window so it looks like it's animating
        line.set_data(input_sizes, times_taken)
        axis.relim()
        axis.autoscale_view()
        plt.draw()
        plt.pause(0.1)

        n = n + n_step

    plt.ioff()  # turn interactive mode back off, we're done updating
    plt.show()  # keep the finished window open on screen

    return input_sizes, times_taken

def deduplicate_users(n):
    # Build a list of n user dictionaries, with some repeated ids
    # on purpose, so there's something to remove.
    users = []
    for i in range(n):
        repeated_id = i % (n // 2 + 1)
        users.append({'id': repeated_id})

    unique_users = []
    for i in range(len(users)):
        seen = False
        for j in range(len(unique_users)):
            if users[i] == unique_users[j]:
                seen = True
                break
        if not seen:
            unique_users.append(users[i])

    return unique_users


if __name__ == '__main__':
    time_complexity_visualizer(deduplicate_users, 10, 1000, 10)
