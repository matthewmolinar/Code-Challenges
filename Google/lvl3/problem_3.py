from collections import OrderedDict
# A Very Powerful Node
class Node(object):
    def __init__(self, label, data, bomb_uses_left):
        self.label = label
        self.data = data
        # Critical for finding shortest path.
        # If a node uses its bomb, all nodes in that path
        # being generated lose this ability.
        self.bomb_uses_left = bomb_uses_left
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

    def __repr__(self):
        return str(self.label)
    




class Graph(object):
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.graph = list()
        self.queue = []


    def generate_graph(self):
        # Adding the vertex label as key, and its adjacent vertices as values to graph.
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
                # label = num_parallel_list[i][j]
                # new_vertice = Node(label, self.map[i][j], 1)
                self.graph.append(new_node)


    def in_bounds(self, row, col):
        return (0 <= row < len(self.map)) and (0 <= col < len(self.map[row]))
    
    def distance_calculator(self, current, other):
        # Add the distance on current node, to the other node if its lower than other
        # node's distance.
        print '/ distance of current,' +  str(self.graph[current.label].distance)
        new_distance = self.graph[current.label].distance + 1
        print('new distance', new_distance)

        adjacent_distance = self.graph[other.label].distance
        print('adjacent distance', adjacent_distance)
        if new_distance < self.graph[other.label].distance:
            self.graph[other.label].distance = new_distance
            print('/ adjacent distance now:', new_distance, 'line 77')
            self.queue.append(other)
            print('/just added', other, 'to the queue')
            print('adjacent is a wall', other.is_wall)
            print('adjacent data:', other.data)
            if self.graph[other.label].is_wall:
                self.graph[other.label].bomb_uses_left = 0
                print('/ adjacent bomb use == 0 now line 84')
            if self.graph[current.label].bomb_uses_left == 0:
                print('/ adjacent bomb use == 0 now line 87')
                self.graph[other.label].bomb_uses_left = 0
        # if other.is_wall or current.bomb_uses_left == 0:
        #     other.bomb_uses_left = 0
        #     print('/ adjacent does not have bomb use anymore.', other.bomb_uses_left)
        # However, if the other node is not a wall, and has lower bomb_uses, the distance
        # will be added regardless.
        elif self.graph[current.label].bomb_uses_left > self.graph[other.label].bomb_uses_left: 
            self.graph[other.label].distance = new_distance
            print('/ adjacent distance now:', new_distance, 'line 95')
            self.queue.append(other)
            print('/just added', other, 'to the queue')

        
        

    def print_graph(self):
        for i in range(len(self.graph)):
            print('Node: ' + str(self.graph[i].label) + ' ')
            print('Adjacents: ' + str(self.graph[i].adjacents) + ' ')

    def dijkstras_shortest(self, source):
        source.distance = 1
        self.queue.append(source)
        while self.queue:
            current_node = self.queue.pop(0)
            print('just popped', current_node, 'from the queue')
            for adjacent in self.graph[current_node.label].adjacents:
                # print(type(current_node))
                if current_node.bomb_uses_left == 0:
                    print 'current ' +  str(current_node) + ' does not have any bombs left',
                    print '/adjacent: ' + str(adjacent),
                    # If this node is out of bomb_uses,
                    # then it cannot look at walls. 
                    # It can only look at non-walls.
                    if not adjacent.is_wall:
                        self.distance_calculator(current_node, adjacent)
                else:
                    print 'current ' + str(self.graph[current_node.label]) + ' has bombs left to use',
                    print '/adjacent: ' + str(adjacent),

                    # If this node still has bomb_uses, it can look at walls.
                    # But if it looks at a wall, that wall is out of bomb_uses.
                    # Also, when that wall is visited, and if it looks at an
                    # open spot, that spot no longer has bomb_uses.
                    self.distance_calculator(current_node, adjacent)

        return self.graph[-1].distance


def solution(map):
    maze = Graph(map)
    # maze.print_graph()
    maze.generate_graph()
    # maze.print_graph()
    # print(maze.graph[0].adjacents)
    source = maze.graph[0]
    # for node in maze.graph:
    #     print node,
    #     print node.adjacents
    #     for adjacent in node.adjacents:
    #         print '**** adjacents ****'
    #         print adjacent
    #         print 'data:', adjacent.data 
    #         print adjacent.is_wall
    source = maze.graph[0]
    # try:
    #     shortest = maze.dijkstras_shortest(source)
    #     # print(shortest)
    #     return shortest
    # except Exception as e:
    #     print(e)
    # finally:
    #     for node in maze.graph:
    #         print node.distance
    shortest = maze.dijkstras_shortest(source)
    return shortest
    # return shortest

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
print(solution([
        [0, 1, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [0, 0, 1, 1, 1], 
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0]
    ]))


    