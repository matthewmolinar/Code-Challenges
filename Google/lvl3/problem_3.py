class Node:
    def __init__(self, data, bomb_uses):
        self.data = data
        self.bomb_uses = bomb_uses
        if data == 1:
            self.wall = True
        else:
            self.wall = False


class Graph:
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.nodes = [[(j + (i*self.cols)) for j in range(self.cols)] for i in range(self.rows)]
    
    def get_edge_list(self):
        DELTAS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        edge_list = []
        # takes the map and turns into a graph represented by lists.
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                vertices = []
                for delta in DELTAS:
                    row = i + delta[0]
                    col = j + delta[1]
                    if self.in_bounds(row, col):
                        vertices.append(self.nodes[row][col])
                edge_list.append(vertices)
        return edge_list

    def in_bounds(self, row, col):
        return (0 <= row < len(self.map)) and (0 <= col < len(self.map[row]))


# def get_edge_list(map, rows, cols, NODES):
#     DELTAS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
#     edge_list = []
#     # takes the map and turns into a graph represented by lists.
#     for i in range(len(map)):
#         for j in range(len(map[i])):
#             vertices = []
#             for delta in DELTAS:
#                 row = i + delta[0]
#                 col = j + delta[1]
#                 if in_bounds(map, row, col):
#                     vertices.append(NODES[row][col])
#             edge_list.append(vertices)
#     return edge_list


# def in_bounds(map, row, col):
#     return (0 <= row < len(map)) and (0 <= col < len(map[row]))



def dijkstras_algo(graph, distances, map, fuzzy_walls, NODES):
    queue = []
    visited = []
    target = len(graph) - 1
    current_node = 0
    queue.append(current_node)
    while target not in visited:
        current_node = queue.pop(0)
        visited.append(current_node)
        print(f'*****Visiting {current_node} in the map.*****')
        for adjacent_vertex in graph[current_node]:
            if adjacent_vertex not in visited:
                print(f'Looking at {adjacent_vertex}')
                vertex1 = current_node
                vertex2 = adjacent_vertex
                if fuzzy_walls[vertex1] and is_wall(vertex2, map, NODES):
                    # do nothing. Move forward
                    # print(f'{vertex2} is a wall. Not looking at it since {vertex1} is a fuzzy wall.')
                    continue
                # elif fuzzy_walls[vertex1] and not is_wall(vertex2, map, NODES):
                #     # Despite being a fuzzy wall, it can still do dist calc.
                elif not fuzzy_walls[vertex1]:
                    if is_wall(vertex2, map, NODES):
                        # print(f'{vertex2} is a wall, but {vertex1} is not a fuzzy wall, so looking at it.')
                        # bomb was just used. Vertex 2 can no longer use it.
                        # it can only do distance calc on non-walls.
                        fuzzy_walls[vertex2] = True
                        # print(f'{vertex2} is now a fuzzy wall. It cannot look at walls.')
                print(f'Calculating distance to {vertex2} from {vertex1}')
                if vertex2 not in visited:
                    queue.append(vertex2)
                distances = distance_helper(vertex1, vertex2, distances)
    return distances[-1]


def is_wall(vertex2, map, NODES):
    wall = False
    for i in range(len(NODES)):
        for j in range(len(NODES[i])):
            if NODES[i][j] == vertex2:
                if map[i][j] == 1:
                    # No longer a wall, is now a fuzzy wall.
                    map[i][j] = 0
                    wall = True
                # is it a wall in the map?
                return wall


def distance_helper(vertex1, vertex2, distances):
    new_distance = distances[vertex1] + 1
    # print(f'distances has {len(distances)} indices. Last index: {len(distances) - 1}')
    # print(f'attempting to access index: {vertex2} of distances.')
    # print(distances)
    if new_distance < distances[vertex2]:
        distances[vertex2] = new_distance
        print(f'{vertex2} is now {new_distance}')
    return distances


def solution(map):
    # If the shortest path algo visits a wall, that wall becomes a non-wall,
    # BUT, that particular spot can no longer visit walls, only open spots.
    # It becomes a fuzzy node.
    rows = len(map)
    cols = len(map[0])
    # if rows < 7:
    #     return (rows - 1) + cols
    NODES = [[(j + (i*cols)) for j in range(cols)] for i in range(rows)]
    edge_list = get_edge_list(map, rows, cols, NODES)
    fuzzy_walls = [False for i in range(rows*cols)]
    # print(fuzzy_walls)
    distances = [1 if (i == 0) else float('inf') for i in range(rows*cols)]
    shortest_path = dijkstras_algo(edge_list, distances, map, fuzzy_walls, NODES)
    return shortest_path

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
print(solution([[0, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 1], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]]))

    