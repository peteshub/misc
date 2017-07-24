import networkx as nx
import requests
import numpy as np

def get_ticker(sym):
    url = "https://api.bitfinex.com/v1/pubticker/{}".format(sym)
    response = requests.request("GET", url)
    resp = response.json()

    a = sym[:3]
    b = sym[3:]

    bid = float(resp['bid'])
    ask = float(resp['ask'])

    return [(a, b, np.log(1/ask*0.998)),(b ,a,np.log(bid*0.998))]
    #return [(a, b, 1 / ask), (b, a, bid)]

def get_symbols():
    url = "https://api.bitfinex.com/v1/symbols"
    response = requests.request("GET", url)
    return response.json()


def calc_circuit_paths(G, node, start_node, visited_nodes=set(), path=dict()):

    visited_nodes.add(node)
    for neighbor in G.neighbors_iter(node):
        if neighbor == start_node:
            path[neighbor] = {"weight" : G.get_edge_data(node, neighbor)['weight'],"path":None}
        elif neighbor not in visited_nodes:
            path[neighbor] = {"weight": G.get_edge_data(node, neighbor)['weight'], "path":dict()}
            calc_circuit_paths(G, neighbor, start_node, visited_nodes.copy(), path=path[neighbor]["path"])


def traverse_paths(path, accumulated_weight=0, lst=[]):
    for key in path:
        if path[key]["path"] is None:
            weight = np.power(np.e, accumulated_weight+path[key]["weight"])
            if weight > 1:
                print(weight, " ", lst+[key])
        else:
            traverse_paths(path[key]["path"], accumulated_weight + path[key]["weight"], lst.copy()+[key])


syms = get_symbols()

nodes = set()
edges = set()

curr = ["eth","iot","btc","usd"]
for sym in syms:
    a = sym[:3]
    b = sym[3:]

    if a in curr and b in curr:

        nodes.add(a)
        nodes.add(b)

        e = get_ticker(sym)

        edges.add(e[0])
        edges.add(e[1])

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

path = dict()

calc_circuit_paths(G,"usd","usd",path=path)

traverse_paths(path)