"""GA searches exam orders, PSO sorts random keys, ACO constructs whole orders."""
import random
import numpy as np
from exams import neighbors, degree_order, first_fit

SETTINGS = {'population': 18, 'iterations': 50, 'crossover': 'order crossover',
            'swap_mutation': .3, 'inertia': .65, 'c1': 1.5, 'c2': 1.5,
            'evaporation': .25, 'heuristic_power': 1.}


def solve(case, method, seed):
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    adj, n = neighbors(case), case['n']
    initial = degree_order(adj)
    population_size = SETTINGS['population']
    best_order, best_colors, best_count, evaluations, history = None, None, n + 1, 0, []

    def evaluate(order):
        nonlocal best_order, best_colors, best_count, evaluations
        colors, count = first_fit(order, adj)
        evaluations += 1
        if count < best_count:
            best_order, best_colors, best_count = list(map(int, order)), colors, count
        return count

    if method == 'GA':
        population = [initial.copy()] + [rng.sample(range(n), n) for _ in range(population_size - 1)]
        costs = [evaluate(order) for order in population]
        history.append(best_count)
        for _ in range(SETTINGS['iterations']):
            next_generation = [best_order.copy()]
            while len(next_generation) < population_size:
                parents = []
                for _ in range(2):
                    a, b = rng.sample(range(population_size), 2)
                    parents.append(population[a if costs[a] <= costs[b] else b])
                left, right = sorted(rng.sample(range(n + 1), 2))
                child = [-1] * n
                child[left:right] = parents[0][left:right]
                used = set(child[left:right])
                remaining = [v for v in parents[1] if v not in used]
                it = iter(remaining)
                for j in list(range(right, n)) + list(range(left)):
                    child[j] = next(it)
                if rng.random() < SETTINGS['swap_mutation'] and n >= 2:
                    a, b = rng.sample(range(n), 2)
                    child[a], child[b] = child[b], child[a]
                next_generation.append(child)
            population = next_generation
            costs = [evaluate(order) for order in population]
            history.append(best_count)
    elif method == 'PSO':
        positions = nrng.random((population_size, n))
        positions[0, initial] = np.arange(n) / n
        velocities = nrng.uniform(-.1, .1, positions.shape)
        decode = lambda row: np.argsort(row, kind='stable').tolist()
        costs = np.array([evaluate(decode(row)) for row in positions])
        personal, personal_cost = positions.copy(), costs.copy()
        global_position = personal[int(np.argmin(personal_cost))].copy()
        history.append(best_count)
        for _ in range(SETTINGS['iterations']):
            velocities = (.65 * velocities + 1.5 * nrng.random(positions.shape) * (personal - positions)
                          + 1.5 * nrng.random(positions.shape) * (global_position - positions))
            velocities = np.clip(velocities, -.4, .4)
            positions = np.clip(positions + velocities, -2, 2)
            costs = np.array([evaluate(decode(row)) for row in positions])
            improved = costs < personal_cost
            personal[improved], personal_cost[improved] = positions[improved], costs[improved]
            global_position = personal[int(np.argmin(personal_cost))].copy()
            history.append(best_count)
    else:
        raise ValueError('Unknown method')
    assert evaluations == population_size * (SETTINGS['iterations'] + 1)
    return {'order': best_order, 'colors': best_colors, 'objective': best_count,
            'history': history, 'evaluations': evaluations}
