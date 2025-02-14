import random

import igraph
import matplotlib.pyplot as plt

g = igraph.Graph()


def loop(id_: list, n):
    m = id_[0]
    for j in range(3):
        g.add_vertex(m)
        g.add_edge(m, id_[0] + 1, weight=random.uniform(0, 1))
        id_[0] += 1
        if n > 0:
            loop(id_, n - 1)


g.add_vertex(0)
id_ = [0]
loop(id_, 2)

fig, ax = plt.subplots()
layout = g.layout('kk')
igraph.plot(g, layout=layout, target=ax)
plt.show()

'''i = 0
while i < 100:
    for j in range(random.randint(0, 5)):
        g.add_vertex(i + 1 + j)
        g.add_edge(i, i + 1, weight=random.uniform(0, 1))
    i += 1
    fig, ax = plt.subplots()
    layout = g.layout('kk')
    igraph.plot(g, layout=layout, target=ax)
    plt.show()
    # time.sleep(1)
    plt.close(fig)'''

g.write_edgelist('2.edgelist')
print('完成')
