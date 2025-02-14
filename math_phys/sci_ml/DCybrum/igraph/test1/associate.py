import random

import igraph
import matplotlib.pyplot as plt
import time

attention_capacity = 100


g = igraph.read('2.edgelist')

n = 0
edge_ids = [0, 1, 2]
while n < 7:
    edge_ids_ = []
    for edge_id in edge_ids:
        edge = g.es[edge_id]
        # print(n, g.vs[edge.source]['status'] if 'status' in g.vs[edge.source].attributes() else 0, edge.source, '->', edge.target)

        vertex, v = g.vs[edge.source], g.vs[edge.target]
        if 'status' not in vertex.attributes() or vertex['status'] is None or vertex['status'] == 0:
            vertex['status'] = 1
        else:
            vertex['status'] = 0

        for edge_ in v.incident():
            if edge_.index not in edge_ids_:
                edge_ids_.append(edge_.index)
            if len(edge_ids_) > attention_capacity:
                edge_ids_.pop(0)
    edge_ids += edge_ids_
    n += 1

    if n % 1 == 0:
        fig, ax = plt.subplots()
        layout = g.layout('kk')
        igraph.plot(g, layout=layout, target=ax, vertex_size=7,
                    vertex_color=['blue' if status else 'gray' for status in g.vs['status']],
                    vertex_label=[str(v.index) for v in g.vs])
        plt.show()
        # print(g.get_adjacency_sparse())


