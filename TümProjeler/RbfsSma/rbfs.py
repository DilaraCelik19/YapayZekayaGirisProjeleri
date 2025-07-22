# RBFS algoritması
def rbfs(node, value, bound, visited=None):
    if visited is None:
        visited = set()

    # Ziyaret edilen düğümleri kontrol et
    if node['name'] in visited:
        print(f"Node {node['name']} already visited. Skipping.")
        return float('inf'), None
    visited.add(node['name'])

    print(f"Processing node: {node['name']} with value: {value}, bound: {bound}")

    # Çocuğu olmayan düğümse işlemi durdur
    children = node.get('children', [])
    if not children:
        print(f"Node {node['name']} has no children. Returning its f value: {node['f']}.")
        return node['f'], node['name']

    # Çocukları sıralama
    sorted_children = sorted([(child, child['f']) for child in children], key=lambda x: x[1])
    print(f"Sorted children for node {node['name']}: {[c[0]['name'] for c in sorted_children]}")

    while sorted_children:
        best_child, best_f = sorted_children[0]
        second_best_f = sorted_children[1][1] if len(sorted_children) > 1 else float('inf')

        # Sınırı aşarsa işlemi durdur
        if best_f > bound:
            print(f"Bound {bound} exceeded by best child {best_child['name']}. Returning {best_f}.")
            return best_f, None

        # Yeni bound değeri
        new_bound = min(bound, second_best_f)
        print(f"Exploring child: {best_child['name']} with new bound: {new_bound}")

        # Recursive çağrı
        result, result_node = rbfs(best_child, best_f, new_bound, visited)
        sorted_children[0] = (best_child, result)
        sorted_children = sorted(sorted_children, key=lambda x: x[1])

        # En kısa yol düğümünü döndür
        if result_node:
            return result, result_node

    return float('inf'), None


# Test Grafiği
graph = {
    'name': 'A',
    'f': 10,
    'children': [
        {
            'name': 'B',
            'f': 5,
            'children': [
                {'name': 'D', 'f': 7, 'children': []},
                {'name': 'E', 'f': 4, 'children': []}
            ]
        },
        {
            'name': 'C',
            'f': 15,
            'children': [
                {'name': 'F', 'f': 12, 'children': []},
                {'name': 'G', 'f': 20, 'children': []}
            ]
        }
    ]
}

# RBFS algoritmasını çalıştır
result, result_node = rbfs(graph, float('inf'), float('inf'))
print(f"RBFS result: f={result}, node={result_node}")
print(f"---------------------------------------------------------")
print(f"SMA")
import heapq

class Node:
    def __init__(self, state, cost, heuristic, parent=None):
        self.state = state
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent
        self.f = cost + heuristic

    def __lt__(self, other):
        return self.f < other.f  # heapq için düğümleri `f` değerine göre sıralar.

class Problem:
    def __init__(self, heuristics, neighbors, goal_state):
        self.heuristics = heuristics
        self.neighbors = neighbors
        self.goal_state = goal_state

    def is_goal(self, state):
        return state == self.goal_state

    def get_neighbors(self, state):
        return self.neighbors.get(state, [])

def sma_star(problem, memory_limit):
    queue = []
    initial_node = Node("S", 0, problem.heuristics["S"], None)
    heapq.heappush(queue, initial_node)

    while queue:
        node = heapq.heappop(queue)

        if problem.is_goal(node.state):
            return node

        for neighbor_state, cost in problem.get_neighbors(node.state):
            neighbor_heuristic = problem.heuristics.get(neighbor_state, float('inf'))
            child = Node(neighbor_state, node.cost + cost, neighbor_heuristic, node)
            child.f = max(node.f, child.cost + child.heuristic)

            if len(queue) >= memory_limit:
                heapq.heappop(queue)  # Bellek sınırını aşan düğümü çıkar

            heapq.heappush(queue, child)

    return None

# Örnek Problem Tanımı
heuristics = {
    "S": 10,
    "A": 7,
    "B": 4,
    "C": 2,
    "G": 0
}

neighbors = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("C", 1), ("G", 5)],
    "C": [("G", 3)]
}

goal_state = "G"
problem = Problem(heuristics, neighbors, goal_state)

# SMA* Algoritmasını Çalıştır
memory_limit = 5
result = sma_star(problem, memory_limit)

# Çözüm Yolu
if result:
    path = []
    while result:
        path.append(result.state)
        result = result.parent
    print("Path to goal:", " -> ".join(reversed(path)))
else:
    print("Goal not found within memory limit.")

