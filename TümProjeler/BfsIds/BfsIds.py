import heapq

def ucs(graph, startNode, endNode):
    """
    UCS (Uniform Cost Search) algoritması: En düşük maliyetli yolu bulur.
    """
    # Öncelik kuyruğu (heapq modülü ile)
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, startNode))  # (maliyet, düğüm)

    # Ziyaret edilen düğümleri ve maliyetlerini tut
    visitedNodes = {}

    # Önceki düğümleri yol oluşturmak için tut
    predecessorNodes = {}

    while priorityQueue:
        currentCost, currentNode = heapq.heappop(priorityQueue)

        # Eğer düğüm daha önce ziyaret edilmediyse veya daha düşük maliyetliyse işleme al
        if currentNode in visitedNodes and visitedNodes[currentNode] <= currentCost:
            continue

        visitedNodes[currentNode] = currentCost

        # Eğer hedef düğüme ulaşıldıysa, yolu oluştur ve döndür
        if currentNode == endNode:
            # Yolu oluştur
            path = []
            while currentNode != startNode:
                path.append(currentNode)
                currentNode = predecessorNodes[currentNode]
            path.append(startNode)
            path.reverse()
            return path, currentCost

        # Komşuları araştır
        for neighbor, cost in graph[currentNode]:
            totalCost = currentCost + cost
            if neighbor not in visitedNodes or totalCost < visitedNodes[neighbor]:
                heapq.heappush(priorityQueue, (totalCost, neighbor))
                predecessorNodes[neighbor] = currentNode

    # Eğer buraya gelindiyse, hedef düğüme ulaşılamamış demektir
    return None, float('inf')

# Test
# Graf: (komşu, maliyet) çiftleriyle temsil edilen bir sözlük
testGraphUcs = {
    '0': [('3', 1), ('5', 2), ('9', 4)],
    '1': [('6', 2), ('7', 4), ('4', 3)],
    '2': [('10', 6), ('5', 1)],
    '3': [('0', 1)],
    '4': [('1', 3), ('5', 1), ('8', 2)],
    '5': [('2', 1), ('0', 2), ('4', 1)],
    '6': [('1', 2)],
    '7': [('1', 4)],
    '8': [('4', 2)],
    '9': [('0', 4)],
    '10': [('2', 6)]
}

# '0' düğümünden '1' düğümüne en düşük maliyetli yolu bul
path, cost = ucs(testGraphUcs, '0', '1')
print(f"UCS")
print(f"En kısa yol: {path}, Toplam maliyet: {cost}")

testGraph={'0' :['3','5','9'],
           '1' :['6','7','4'],
           '2' :['10','5'],
           '3' :['0'],
           '4' :['1','5','8'],
           '5' :['2','0','4'],
           '6' :['1'],
           '7' :['1'],
           '8' :['4'],
           '9' :['0'],
           '10' :['2']
}

def bfsShortestPath(graph,startNode,endNode):
    visitedNodes=[]
    queue=[startNode]
    predecessorNodes={}

    while queue:
        currentNode=queue.pop(0)
        visitedNodes.append(currentNode)
        for neighbor in graph[currentNode]:
            if neighbor not in visitedNodes:
                queue.append(neighbor)
                predecessorNodes[neighbor]=currentNode

    print(shortestPath(predecessorNodes,startNode,endNode))

def shortestPath(predecessorNode,startNode,endNode):
    path=[endNode]
    currentNode=endNode
    while currentNode != startNode:
        currentNode=predecessorNode[currentNode]
        path.append(currentNode)
    path.reverse()
    return path


def ids(graph, startNode, endNode, maxDepth):
    """
    IDS algoritması: Iterative Deepening Search
    """
    for depth in range(maxDepth + 1):
        path = []
        if dls(graph, startNode, endNode, depth, path, set()):
            return path  # Hedef bulunduğunda yolu döndür
    return None  # Hedef bulunamazsa

def dls(graph, currentNode, endNode, depth, path, visitedNodes):
    """
    DLS (Depth-Limited Search) bir düğümü belirli bir derinliğe kadar araştırır.
    """
    # Mevcut düğümü ziyaret listesine ekle ve yola ekle
    path.append(currentNode)
    visitedNodes.add(currentNode)

    # Eğer hedef düğüme ulaşıldıysa, True döndür
    if currentNode == endNode:
        return True

    # Derinlik sınırına ulaşıldıysa, daha fazla ilerleme yapılmaz
    if depth == 0:
        path.pop()
        visitedNodes.remove(currentNode)
        return False

    # Komşu düğümleri araştır
    for neighbor in graph[currentNode]:
        if neighbor not in visitedNodes:
            if dls(graph, neighbor, endNode, depth - 1, path, visitedNodes):
                return True

    # Geri izleme (backtracking)
    path.pop()
    visitedNodes.remove(currentNode)
    return False

print(f"BFS")
bfsShortestPath(testGraph,'0','1')
maxDepth = 5  # Maksimum derinlik sınırı
print(f"IDS")
print(ids(testGraph, '0','1',maxDepth))