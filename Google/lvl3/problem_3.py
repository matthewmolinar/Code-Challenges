# A Very Powerful Node
class Node(object):
    def __init__(self, label, data, bomb_uses_left):
        self.label = label
        self.data = data
        # Critical for finding shortest path.
        # If a node uses its bomb, all nodes in that path
        # being generated lose this ability.
        self.bomb_uses_left = bomb_uses_left
        # nodes are infinitely far away until checked.
        self.distance = float('inf')
        self.adjacents = []
        if data == 1:
            self.is_wall = True
        else:
            self.is_wall = False

    def __hash__(self):
        return hash((self.label, self.data, self.bomb_uses_left, self.adjacents))
        
    def __eq__(self, other):
        return (isinstance(other, type(self)) and (self.label, self.data, self.bomb_uses_left, self.adjacents) == 
            (other.label, other.data, other.bomb_uses_left, other.adjacents))
    
    # Useful for debugging.
    def __repr__(self):
        return str(self.label)


class Graph(object):
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.graph = list()
        # queue is here instead of in dijkstra's shortest path
        self.queue = []

    def generate_graph(self):
        # Adding nodes to the graph attribute. Each node has
        # a adjacent node generated.
        num_parallel_list = [[(j + (i*self.cols)) for j in range(self.cols)] for i in range(self.rows)]
        deltas = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                label = num_parallel_list[i][j]
                data = self.map[i][j]    
                new_node = Node(label, data, 1)
                for delta in deltas:
                    row = i + delta[0]
                    col = j + delta[1]
                    if self.in_bounds(row, col):
                        label = num_parallel_list[row][col]
                        adjacent_vertice = Node(label, self.map[row][col], 1)
                        new_node.adjacents.append(adjacent_vertice)
                self.graph.append(new_node)

    # Making sure that the row and col being attempted to
    # add is within bounds to avoid index error.
    def in_bounds(self, row, col):
        return (0 <= row < len(self.map)) and (0 <= col < len(self.map[row]))
    
    # Critical method, works with bomb_uses to determine appropriate
    # distances.
    def distance_calculator(self, current, other):
        # Add the distance on current node, to the other node if its lower than other
        # node's distance.
        new_distance = self.graph[current.label].distance + 1
        adjacent_distance = self.graph[other.label].distance
        if new_distance < self.graph[other.label].distance:
            self.graph[other.label].distance = new_distance
            self.queue.append(other)
            if self.graph[other.label].is_wall:
                self.graph[other.label].bomb_uses_left = 0
            if self.graph[current.label].bomb_uses_left == 0:
                self.graph[other.label].bomb_uses_left = 0
        # However, if the other node is not a wall, and has lower bomb_uses, the distance
        # will be added regardless.
        elif (self.graph[current.label].bomb_uses_left > self.graph[other.label].bomb_uses_left) and (not self.graph[other.label].is_wall): 
            self.graph[other.label].distance = new_distance
            self.graph[other.label].bomb_uses_left = 1
            self.queue.append(other)

    # For debugging purposes.
    def print_graph(self):
        for i in range(len(self.graph)):
            print('Node: ' + str(self.graph[i].label) + ' ')
            print('Adjacents: ' + str(self.graph[i].adjacents) + ' ')

    # Dijkstras shortest path, but with some modifications.
    # Visited list or attributes is not needed.
    # Relies on bomb_uses instead.
    def dijkstras_shortest(self, source):
        source.distance = 1
        self.queue.append(source)
        while self.queue:
            current_node = self.queue.pop(0)
            if self.graph[current_node.label] == self.graph[-1]:
                return self.graph[current_node.label].distance
            for adjacent in self.graph[current_node.label].adjacents:
                if self.graph[current_node.label].bomb_uses_left == 0:
                    # If this node is out of bomb_uses,
                    # then it cannot look at walls. 
                    # It can only look at non-walls.
                    if not self.graph[adjacent.label].is_wall:
                        self.distance_calculator(current_node, adjacent)
                else:
                    # If this node still has bomb_uses, it can look at walls.
                    # But if it looks at a wall, that wall is out of bomb_uses.
                    # further paths are out of bomb uses as well.
                    self.distance_calculator(current_node, adjacent)


def solution(map):
    maze = Graph(map)
    maze.generate_graph()
    source = maze.graph[0]
    shortest = maze.dijkstras_shortest(source)
    return shortest


print(solution([[0, 0, 0, 0, 0, 0], [1,1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0,0, 0, 0, 0, 0]]))