import igraph
import matplotlib.pyplot as plt
import time

import numpy as np
import torch
import torch.nn.functional as F


class Network(torch.nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.dense = torch.nn.Linear((2,), ())

    def forward(self, x_):
        x_ = self.dense(x_)

        return F.sigmoid(x_)


bases = [
    lambda x: 1,
    lambda x: x,
    lambda x: 2*x**2-1,
    lambda x: 4*x**3-3*x,
    lambda x: 8*x**4-8*x**2+1,
    lambda x: 16*x**5-20*x**3+5*x,
    lambda x: 32*x**6-48*x**4+18*x**2-1,
    lambda x: 64*x**7-112*x**5+56*x**3-7*x,
    # lambda x: 128*x**8-256*x**6+160*x**4-32*x**2+1,
]
n = 100
dead_threshold = 0.05

g = igraph.Graph()
weights = np.random.uniform(0, 1., (n, len(bases)))


def forward(source_, edge_i, source_value):
    return weights[source_, edge_i] * bases[edge_i](source_value)


def add(source_, i_, w_):
    global next_vertices
    g.add_vertex(len(g.vs), i=len(g.vs), value=1.)
    # print(source_, len(g.vs))
    g.add_edge(source_, len(g.vs)-1, index=i_, weight=w_)
    next_vertices[len(g.vs)-1] = 1


def get_colors(values):
    colors = []
    for value in values:
        color = value
        if color > 1.:
            color = 1.
        elif color < 0.:
            color = 0.
        colors.append((color, color, color))
    print(colors)
    return colors


g.add_vertex(0, i=0, value=0.2)

vertices = [0] * n
next_vertices = [1] + [0] * (n-1)

iter_edges = []
next_iter_edges = [0]

for step in range(100):
    if step % 1 == 0:
        vertices = next_vertices.copy()
        next_vertices = [0] * n
        for ind, vertex_exists in enumerate(vertices):
            if not g.vs.select(i=ind):
                next_vertices[ind] = 0
                continue
            next_vertices[ind] = 1
            source = g.vs.select(i=ind)[0].index
            edges = g.vs[source].incident()
            for i in range(len(bases)):
                e = g.es.select(_source=source)
                if ('index' not in e.attributes() or i not in e['index']) and weights[source, i] >= dead_threshold and len(g.vs) < n:
                    add(source, i, weights[source, i])
                '''elif 'index' in e.attributes() and i in e['index'] and weights[source, i] < dead_threshold:
                    ed = g.es.select(_source=source, index=i)
                    g.delete_edges(ed)'''

    if step % 1 == 0:
        iter_edges = next_iter_edges.copy()
        next_iter_edges.clear()
        for edge in g.es:
            v1, v2 = g.vs[edge.source], g.vs[edge.target]
            v2['value'] = forward(edge.source, edge['index'], v1['value'])
            edge['weight'] = weights[edge.source, edge['index']]

            if v2['value'] < dead_threshold:
                g.delete_vertices(v2)

    ve = g.vs.select(_degree=0)
    for v in ve:
        vertices[v['i']] = 0
    g.delete_vertices(ve)

    to_delete = []
    for v in g.vs:
        if v.index != 0 and not g.are_connected(0, v.index) and not g.vertex_connectivity(0, v.index):
            to_delete.append(v)
    g.delete_vertices(to_delete)

    # weights = np.random.uniform(0, 1., (n, len(bases)))

    fig, ax = plt.subplots()
    layout = g.layout('kk')
    igraph.plot(g, layout=layout, target=ax, vertex_size=5,
                vertex_color=get_colors(g.vs['value']))
    # , vertex_label=['{:.2f}'.format(val) for val in g.vs['value']])
    # igraph.plot(g, layout=layout, target=ax, vertex_size=5)
    plt.show()
    # print(g.get_adjacency_sparse())
    print('顶点数：', len(g.vs), '边数：', len(g.es))
    print(g.vs['value'])





