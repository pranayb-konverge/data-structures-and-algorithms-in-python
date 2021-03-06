"""
lets represent the nodes and edges in the graphs
nodes are the points and edges are the connection between the points
for ref we can create nodes and edges using this image https://i.imgur.com/xkgMnwx.png
"""

print("\n---------------Adjacency List - Print a simple graph with node and edges--------------\n")

num_nodes = 5
edges  = [(0,1), (0,4), (1,2), (1,3), (1,4), (2,3),(3,4)]

class Graph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        # create list of empty list 
        self.list_of_nodes = [[] for _ in range(num_nodes)]
        
    def add_edge(self, node_a, node_b):
        self.list_of_nodes[node_a].append(node_b)
        self.list_of_nodes[node_b].append(node_a)
    
    def remove_edge(self, edge):
        for _, neighbour in enumerate(self.list_of_nodes):
            if neighbour == list(edge):
                self.list_of_nodes.remove(list(edge))
        
    # lets print the graph in a better way
    def display_graph(self):
        print(
            "\n".join(
            ["Node {}: Edge connected with {}".format(
                node, neighbour) 
            for node, neighbour in enumerate(
                self.list_of_nodes)])
            )
# end of Graph class

new_graph = Graph(num_nodes)
for edge_a, edge_b in edges:
    new_graph.add_edge(edge_a, edge_b)
new_graph.display_graph()
new_graph.remove_edge((1,4))
print()
new_graph.display_graph()

print("\n---------------Adjacency Matrix represent the nodes as 1-0 in the matrix--------------\n")

class GraphMatrix:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        # create list of empty list 
        self.adj_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        
    def add_edge(self, node_a, node_b):
        if node_a == node_b:
            print("Same Node %d and %d" % (node_a, node_b))
        # insert in the correct adj_matrix
        self.adj_matrix[node_a][node_b] = 1
        self.adj_matrix[node_b][node_a] = 1
    
    def remove_edge(self, node_a,node_b):
        if self.adj_matrix[node_a][node_b] == 0:
            print("No edge between %d and %d" % (node_a, node_b))
            return
        self.adj_matrix[node_a][node_b] = 0
        self.adj_matrix[node_b][node_a] = 0

    # lets print the graph in a better way
    def display_graph_matrix(self):
         print('{}'.format(self.adj_matrix)) 
# end of GraphMatrix class              

new_graph_matrix = GraphMatrix(num_nodes)
for edge_a, edge_b in edges:
    new_graph_matrix.add_edge(edge_a, edge_b)
new_graph_matrix.display_graph_matrix()
new_graph_matrix.remove_edge(1,4)
print()
new_graph_matrix.display_graph_matrix()

print("\n---------------Graph traversal - breadth-first search--------------\n")
"""
BFS pseudocode:

 1  procedure BFS(G, root) is
 2      let Q be a queue
 3      label root as discovered
 4      Q.enqueue(root)
 5      while Q is not empty do
 6          v := Q.dequeue()
 9          for all edges from v to w in G.adjacentEdges(v) do
10              if w is not labeled as discovered then
11                  label w as discovered
12                  Q.enqueue(w)
"""

def breadth_first_search(graph, root):
    queue = []
    data = graph.list_of_nodes
    discovered = [False] * len(data)
    distance = [None] * len(data)
    parent = [None] * len(data)

    discovered[root]  = True
    distance[root]  = 0
    queue.append(root)
    connected = True
    # to dequeue the list we will have an index which will track the first 
    # element in the queues list
    idx = 0

    while idx < len(queue):
        # get most recently inserted element in the queue, dequeue operation
        current = queue[idx]
        # as we got the current/discovered value in the queue increment the index
        idx += 1  
        # check all the edges of the current node
        # for example the root/current is 0 then data[current] will be [1,4] 
        for node in data[current]:
            # yet to discover, so here 0 is discovered but not 1 (node) from [1,4]
            if not discovered[node]:
                # current nodes distance is 1 + self
                distance[node] = 1 + distance[current]
                # Parent node will be current as it is not discovered yet
                parent[node] = current
                # so we can set the note as discovered 
                discovered[node] = True
                # and append the node in queue
                queue.append(node)
    
    # check if the graph is connected or not
    if len(queue) < len(data):
        connected = False

    return queue, distance, parent, connected
# end of breadth_first_search()

# uncomment to test the all nodes connected scenario 
# num_nodes = 9
# edges = [(0, 1), (0, 3), (1, 2), (2, 3), (4, 5), (4, 6), (5, 6), (7, 8)]
new_graph = Graph(num_nodes)
for edge_a, edge_b in edges:
    new_graph.add_edge(edge_a, edge_b)
new_graph.display_graph()

root = 3
edges, distance, parent, connected = breadth_first_search(new_graph, root)
print(f"\nThe {root} has {edges} nodes associated, \
distance (order of nodes) is {distance} and \
the parent (order of nodes) is {parent}. Is the graph connected? {connected}.")

print("\n--Get the componentes which are connected in a graph--\n")

def is_component_util(graph, node, discovered, connected_graph_edge):
    # If the node/neighbour is not discovered mark it discovered 
    discovered[node] = True
    # append the node/neighbour in the list
    connected_graph_edge.append(node)
    # if node = 0 so in a graph like [[0,1],[1,2], [3]], the graph[node]=[0,1] 
    # so value of neighbour will be 0 then 1 then 1 then 2 
    for neighbour in graph[node]:   
        # only discover if the neighbour is not discovered
        if not discovered[neighbour]:            
            is_component_util(graph, neighbour, discovered, connected_graph_edge)

def bfs_component_connected(graph, num_nodes):
    discovered = [False] * num_nodes
    components = []

    # iterate over the range of num_nudes
    for node in range(num_nodes):
        if not discovered[node]:
            connected_graph_edge = []
            is_component_util(graph, node, discovered, connected_graph_edge)
            # here the list of connected nodes will be appended
            components.append(connected_graph_edge)
    
    return components
# end of bfs_component_connected

result = bfs_component_connected(new_graph.list_of_nodes, num_nodes)
print("List of connected components in graph:", result)


print("\n---------------Graph traversal - depth-first search--------------\n")
"""
Question: Define a class to represent weighted and directed graphs in Python.
"""

class DepthGraph:
    def __init__(self, num_nodes, edges, directed=False, weighted=False):
        self.num_nodes = num_nodes
        self.directed = directed
        self.weighted = weighted
        self.data = [[] for _ in range(num_nodes)]
        self.weight = [[] for _ in range(num_nodes)]
        
        for edge in edges:
            if self.weighted:
                # include weights
                node_a, node_b, weight = edge
                # pair the nodes_b with node_a
                self.data[node_a].append(node_b)
                # pair the weight with node_a
                self.weight[node_a].append(weight)
                if not directed:
                    self.data[node_b].append(node_a)
                    self.weight[node_b].append(weight)
            else:
                # work without weights
                node_a, node_b = edge
                self.data[node_a].append(node_b)
                if not directed:
                    self.data[node_b].append(node_a)

    def __repr__(self) -> str:
        result  = ""
        if self.weighted:
            for i, (nodes, weights) in enumerate(zip(self.data, self.weight)):
                result += "{}:{}\n".format(i, list(zip(nodes, weights)))
        else:
            for i, nodes in enumerate(self.data):
                result += "{}:{}\n".format(i, nodes)
        return result
    
    def __str__(self):
        return self.__repr__()

# Graph with weights
# graph link https://i.imgur.com/wy7ZHRW.png
num_nodes = 9
edges = [(0, 1, 3), (0, 3, 2), (0, 8, 4), (1, 7, 4), (2, 7, 2), (2, 3, 6), 
          (2, 5, 1), (3, 4, 1), (4, 8, 8), (5, 6, 8)]

print("Graph with weights:(node,weight)")
new_graph = DepthGraph(num_nodes, edges, weighted=True)
print(new_graph)

# Graph with direction
num_nodes = 5
edges = [(0, 1), (1, 2), (2, 3), (2, 4), (4, 2), (3, 0)]

print("Graph with direction:")
new_graph = DepthGraph(num_nodes, edges, directed=True)
print(new_graph)

print("\n---- search in the Depth graph-----\n")
def depth_first_search(graph, source):
    visited = [False] * len(graph.data)
    # visited node
    stack = [source]
    result = []
    
    # While the stack list is not empty
    while len(stack) > 0:
        # get the current value from stack by poping the last element LIFO 
        current = stack.pop()
        # if not visited then visite the node and add in result
        if not visited[current]:
            result.append(current)
            visited[current] = True
            # now we need to get the value from grap to populate the stack, 
            # think this as a push in LIFO
            for v in graph.data[current]:
                stack.append(v)
                
    return result
# end of depth_first_search()

source = 4
result = depth_first_search(new_graph, source)
print(f"\nWe can traverse from {source} to these nodes {result}.")

print("\n---------------Graph traversal - shortest path--------------\n")
def shortest_path(graph, source, target):
    visited = [False] * len(graph.data)
    parent = [None] * len(graph.data)
    # this is the distance of the node we have not discovered yet so its infinity
    distance = [float('inf')] * len(graph.data)
    queue = []

    distance[source] = 0
    queue.append(source)
    idx = 0

    # Here the target is not visited so we can take the current node from 
    # the queue as idx. lets mark the current node as visited (True).
    while idx < len(queue) and not visited[target]:
        current = queue[idx]
        visited[current] = True
        idx += 1

        # update the distance of all the neighbours
        update_distances(graph, current, distance, parent)

        # find the first unvisited node with smallest distance 
        next_node = pick_next_node(distance, visited)

        if next_node:
            queue.append(next_node)
    
    return distance[target], parent

def update_distances(graph, current, distance, parent=None):
    """Update the distances of the current node's neighbors"""
    neighbors = graph.data[current] # from (0, 1, 4), (0,1) are the neighbours
    weights = graph.weight[current] # weight of the edge is 4
    for i, node in enumerate(neighbors):
        weight = weights[i]
        # if the length = distance + weight of the current node is less than the next 
        # or adjacent node, update the length to distance of node
        if (distance[current] + weight) < distance[node]:
            distance[node] = distance[current] + weight
            if parent:
                parent[node] = current

def pick_next_node(distance, visited):
    """Pick the next univisited node at the smallest distance"""
    min_distance = float('inf')
    min_node = None
    for node in range(len(distance)):
        # if visited is false and distance of node is less than infinity 
        # return the min_node/next_node
        if not visited[node] and distance[node] < min_distance:
            min_node = node
            # update the min_distance to the discovered node
            min_distance = distance[node]
    return min_node


num_nodes = 6
# node1, node2, weight of edge
# graph link https://i.imgur.com/Zn5cUkO.png
edges = [(0, 1, 4), (0, 2, 2), (1, 2, 5), (1, 3, 10), (2, 4, 3), (4, 3, 4), (3, 5, 11)]
new_graph = DepthGraph(num_nodes, edges, weighted=True, directed=True)

print("Graph with weight & direction:")
print("Data:",new_graph.data)
print("Weight:",new_graph.weight)
print("Direction:",new_graph.directed)
print()

source = 0
target = 5
shorted_path, visited_nodes = shortest_path(new_graph, source, target)
print(f"The shortest path between {source} & {target} is {shorted_path}.")
print("Path follwed was:(Node: Parent)")
for i in range(source, target+1):
    print(f"{i}:{visited_nodes[i]}")
