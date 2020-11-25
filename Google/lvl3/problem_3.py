from collections import defaultdict
class Node(object):
    def __init__(self, label, data, bomb_uses):
        self.label = label
        self.data = data
        # Critical for finding shortest path.
        # If a node uses its bomb, all nodes in that path
        # being generated lose this ability.
        self.bomb_uses = bomb_uses
        self.distance = float('inf')
        self.visited = False
        if data == 1:
            self.is_wall = True
        else:
            self.is_wall = False

    def __hash__(self):
        return hash((self.label, self.data, self.bomb_uses, self.visited))
        

    def __eq__(self, other):
        return (isinstance(other, type(self)) and (self.label, self.data, self.bomb_uses, self.visited) == 
            (other.label, other.data, other.bomb_uses, other.visited))

    def __repr__(self):
        return str(self.label)



class Graph(object):
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.graph = defaultdict(list)
    
    def generate_graph(self):
        # Adding the vertex label as key, and its adjacent vertices as values to graph.
        num_parallel_list = [[(j + (i*self.cols)) for j in range(self.cols)] for i in range(self.rows)]
        deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                vertices = []
                for delta in deltas:
                    row = i + delta[0]
                    col = j + delta[1]
                    if self.in_bounds(row, col):
                        label = num_parallel_list[row][col]
                        adjacent_vertice = Node(label, self.map[i][j], 1)
                        vertices.append(adjacent_vertice)
                label = num_parallel_list[i][j]
                new_vertice = Node(label, self.map[i][j], 1)
                self.graph[new_vertice] = vertices

    def in_bounds(self, row, col):
        return (0 <= row < len(self.map)) and (0 <= col < len(self.map[row]))
    
    def distance_calculator(self, other):
        # Add the distance on current node, to the other node if its lower than other
        # node's distance.
        # However, if the other node is not a wall, and has lower bomb_uses, the distance
        # will be added regardless.
        pass

    def print_graph(self):
        print(self.graph)

    def dijkstras_shortest(self, source):
        queue = []
        visited = []
        source.distance = 1
        queue.append(source)
        while queue:
            current_node = queue.pop(0)
            for adjacent in self.graph[current_node]
                if current_node.bomb_uses = 0:
                    # If this node is out of bomb_uses,
                    # then it cannot look at walls. 
                    # It can only look at non-walls.
                    continue
                else:
                    # If this node still has bomb_uses, it can look at walls.
                    # But if it looks at a wall, that wall is out of bomb_uses.
                    # Also, when that wall is visited, and if it looks at an
                    # open spot, that spot no longer has bomb_uses.
                    continue 
        return

            


    # Not adding edges. The distance will always increase by 1.

    def bfs_modified(self, source):
        # queue = []
        # visited = []
        # queue.append(source)
        # visited.append(source)
        pass





# def dijkstras_algo(graph, distances, map, fuzzy_walls, NODES):
#     queue = []
#     visited = []
#     target = len(graph) - 1
#     current_node = 0
#     queue.append(current_node)
#     while target not in visited:
#         current_node = queue.pop(0)
#         visited.append(current_node)
#         for adjacent_vertex in graph[current_node]:
#             if adjacent_vertex not in visited:
#                 vertex1 = current_node
#                 vertex2 = adjacent_vertex
#                 if fuzzy_walls[vertex1] and is_wall(vertex2, map, NODES):
#                     # do nothing. Move forward
#                     continue
#                 elif not fuzzy_walls[vertex1]:
#                     if is_wall(vertex2, map, NODES):
#                         # print(f'{vertex2} is a wall, but {vertex1} is not a fuzzy wall, so looking at it.')
#                         # bomb was just used. Vertex 2 can no longer use it.
#                         # it can only do distance calc on non-walls.
#                         fuzzy_walls[vertex2] = True
#                 if vertex2 not in visited:
#                     queue.append(vertex2)
#                 distances = distance_helper(vertex1, vertex2, distances)
#     return distances[-1]


# def is_wall(vertex2, map, NODES):
#     wall = False
#     for i in range(len(NODES)):
#         for j in range(len(NODES[i])):
#             if NODES[i][j] == vertex2:
#                 if map[i][j] == 1:
#                     # No longer a wall, is now a fuzzy wall.
#                     map[i][j] = 0
#                     wall = True
#                 # is it a wall in the map?
#                 return wall


# def distance_helper(vertex1, vertex2, distances):
#     new_distance = distances[vertex1] + 1
#     # print(f'distances has {len(distances)} indices. Last index: {len(distances) - 1}')
#     # print(f'attempting to access index: {vertex2} of distances.')
#     # print(distances)
#     if new_distance < distances[vertex2]:
#         distances[vertex2] = new_distance
#         print(f'{vertex2} is now {new_distance}')
#     return distances


def solution(map):
    maze = Graph(map)
    maze.print_graph()
    maze.generate_graph()
    maze.print_graph()

maze_1 = [
        [0, 1, 0, 0], 
        [0, 0, 0, 0], 
        [0, 0, 1, 1], 
        [0, 1, 1, 0],
        [0, 1, 1, 0]
    ]
maze_2 = [
        [0, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 0], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]
    ]
maze_3 =[
        [0, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 0], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]
    ]

def test_solution():
    print('test case 1')
    assert solution([
        [0, 1, 0, 0], 
        [0, 0, 0, 0], 
        [0, 0, 1, 1], 
        [0, 1, 1, 0],
        [0, 1, 1, 0]
    ]) == 8

    
    assert solution([
        [0, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 0], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]
    ]) == 9
    
    assert solution([
        [0, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 1], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]
    ]) == 11
    
    assert solution([
        [0, 1, 0, 0, 0], 
        [0, 1, 0, 1, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 1], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]
    ]) == 14
    
    assert solution([
        [0, 1, 0, 0, 0], 
        [0, 1, 0, 1, 0], 
        [0, 0, 0, 1, 0], 
        [0, 1, 1, 1, 1],
        [0, 1, 1, 1, 0]
    ]) == 13
    
    
    assert solution([
        [0, 1, 1, 0], 
        [0, 0, 0, 1], 
        [1, 1, 0, 0], 
        [1, 1, 1, 0]
    ]) == 7
    
 

    assert solution([
        [0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 1, 1, 1], 
        [0, 1, 1, 1, 1, 1], 
        [0, 0, 0, 0, 0, 0]
    ]) == 11

    assert solution([
        [0, 0],
        [0, 0]
    ]) == 3
    
    assert solution([
        [0, 0],
        [0, 1]
    ]) == 3



# test_solution()
solution(maze_1)


    