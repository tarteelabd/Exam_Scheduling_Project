"""Exam conflict graphs: every edge forbids placing two exams in one period."""
import numpy as np


def make_case(size, replicate):
    n, students = {'Small': (16, 36), 'Medium': (32, 96), 'Large': (60, 210)}[size]
    seed = 5000 + n * 10 + replicate
    rng = np.random.default_rng(seed)
    registrations = [sorted(rng.choice(n, int(rng.integers(2, 5)), replace=False).tolist()) for _ in range(students)]
    edges = sorted({(a, b) for exams in registrations for i, a in enumerate(exams) for b in exams[i + 1:]})
    return {'id': f'{size}_{replicate}', 'size': size, 'seed': seed,
            'n': n, 'students': registrations, 'edges': [list(e) for e in edges]}


def neighbors(case):
    adj = [set() for _ in range(case['n'])]
    for a, b in case['edges']:
        adj[a].add(b); adj[b].add(a)
    return adj


def degree_order(adj):
    return sorted(range(len(adj)), key=lambda v: (-len(adj[v]), v))


def first_fit(order, adj):
    colors = [-1] * len(adj)
    for v in order:
        forbidden = {colors[u] for u in adj[v] if colors[u] >= 0}
        color = 0
        while color in forbidden:
            color += 1
        colors[v] = color
    return colors, max(colors) + 1


def clique_bound(adj):
    best = []
    for start in degree_order(adj):
        clique = [start]
        for v in degree_order(adj):
            if v != start and all(v in adj[u] for u in clique):
                clique.append(v)
        if len(clique) > len(best):best = clique
    return best


def exact_small(adj):
    if len(adj) > 16:raise ValueError('Exact search restricted to small cases')
    order = degree_order(adj)
    _, upper = first_fit(order, adj)
    for limit in range(len(clique_bound(adj)), upper + 1):
        colors = [-1] * len(adj)
        def visit(position, used):
            if position == len(order):return colors.copy()
            v = order[position]
            banned = {colors[u] for u in adj[v] if colors[u] >= 0}
            for color in range(min(limit, used + 1)):
                if color in banned:continue
                colors[v] = color
                result = visit(position + 1, max(used, color + 1))
                if result is not None:return result
            colors[v] = -1
            return None
        answer = visit(0, 0)
        if answer is not None:return {'kind': 'exact', 'value': limit, 'colors': answer}
    raise AssertionError('Exact coloring not found')
