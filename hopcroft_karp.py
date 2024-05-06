from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

def has_augmenting_path(lefts, edges, to_matched_right, to_matched_left, distances, q):
    for left in lefts:
        if to_matched_right[left] == "":
            distances[left] = 0
            q.append(left)
        else:
            distances[left] = float("inf")

    distances[""] = float("inf")

    while len(q) > 0:
        left = q.popleft()

        if distances[left] < distances[""]:
            for right in edges[left]:
                next_left = to_matched_left[right]
                if distances[next_left] == float("inf"):
                    distances[next_left] = distances[left] + 1
                    q.append(next_left)

    return distances[""] != float("inf")

def try_matching(left, edges, to_matched_right, to_matched_left, distances):
    if left == "":
        return True

    for right in edges[left]:
        next_left = to_matched_left[right]
        if distances[next_left] == distances[left] + 1:
            if try_matching(next_left, edges, to_matched_right, to_matched_left, distances):
                to_matched_left[right] = left
                to_matched_right[left] = right
                return True

    distances[left] = float("inf")
    return False


def visualize_matching(lefts, rights, edges, matches):
    G = nx.Graph()

    # Sol düğümleri ekle
    G.add_nodes_from(lefts, bipartite=0)

    # Sağ düğümleri ekle
    G.add_nodes_from(rights, bipartite=1)

    # Kenarları ekle ve eşleşmeleri vurgula
    matched_edges = []
    for left, right_set in edges.items():
        for right in right_set:
            if left in matches and matches[left] == right:
                matched_edges.append((left, right))
                G.add_edge(left, right, color='red')
            else:
                G.add_edge(left, right, color='black')

    # Grafik çizimi
    pos = nx.bipartite_layout(G, lefts)
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color=edge_colors)
    plt.title('Bipartite Graph with Matching')
    plt.show()



def hopcroft_karp(lefts, rights, edges):
    distances = {}
    q = deque()

    to_matched_right = {left: "" for left in lefts}
    to_matched_left = {right: "" for right in rights}

    while has_augmenting_path(lefts, edges, to_matched_right, to_matched_left, distances, q):
        for unmatched_left in [left for left in lefts if to_matched_right[left] == ""]:
            try_matching(unmatched_left, edges, to_matched_right, to_matched_left, distances)

    # Remove unmatched items
    to_matched_right = {k: v for k, v in to_matched_right.items() if v != ""}

    return to_matched_right

def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    edges = {}
    for line in lines:
        line = line.strip().split(' ')
        node = line[0]
        neighbors = line[1].split(',')
        edges[node] = set(neighbors)

    lefts = set(edges.keys())
    rights = set()
    for neighbors in edges.values():
        rights.update(neighbors)

    return lefts, rights, edges

if __name__ == "__main__":
    filename = "graph_3.txt"  # Eğer dosyanızın adı farklıysa, dosya adını buraya yazın
    lefts, rights, edges = read_graph_from_file(filename)

    matches = hopcroft_karp(lefts, rights, edges)

    print("Number Of Match:", len(matches))
    for left, right in matches.items():
        print("Match:", left, "->", right)

    visualize_matching(lefts, rights, edges, matches)