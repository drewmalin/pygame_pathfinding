## Entry point into A* manager
import math
import pygame


class AStar:
    def __init__(self):
        pass

    # define the a* heuristic to be (euclidean distance)^2
    @staticmethod
    def dist_heuristic(source_node, dest_node):
        dx = int(math.fabs(source_node.pos[0] - dest_node.pos[0]))
        dy = int(math.fabs(source_node.pos[1] - dest_node.pos[1]))
        dist = dx ** 2 + dy ** 2
        return dist

    # real movement cost between two nodes. diagonal movement is allowed, so only the the larger of
    # the delta direction values is needed.
    @staticmethod
    def dist(source_node, dest_node):
        dx = int(math.fabs(source_node.pos[0] - dest_node.pos[0]))
        dy = int(math.fabs(source_node.pos[1] - dest_node.pos[1]))
        dist = dx
        if dy > dist:
            dist = dy
        return dist

    # reconstruct the chosen path after the end has been reached.
    @staticmethod
    def reconstruct_path(node, closed=None, open=None):
        path = AStarPath()
        path.generate(node, closed, open)
        return path

    # generate a path using the A* algorithm
    # (modeled after: http://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode)
    @staticmethod
    def generate(source, dest, map):
        open_list = AStarNodeList()
        closed_list = AStarNodeList()
        map.clear_scores()
        start_node = map.get_node(source)
        end_node = map.get_node(dest)
        open_list.add_or_replace(start_node)
        if map.blocked_nodes.contains(end_node):
            return AStar.reconstruct_path(start_node)
        while not open_list.is_empty():
            test_node = open_list.first()
            open_list.remove(test_node)
            closed_list.add_or_replace(test_node)
            for neighbor_node in map.get_neighbor_nodes(test_node, 5):
                if map.blocked_nodes.contains(neighbor_node) or closed_list.contains(neighbor_node):
                    continue
                if neighbor_node.close_enough(end_node):
                    neighbor_node.parent = test_node
                    return AStar.reconstruct_path(neighbor_node, closed_list, open_list)
                cost = test_node.g_score + AStar.dist(test_node, neighbor_node)
                if not open_list.contains(neighbor_node):
                    open_list.add_or_replace(neighbor_node)
                else:
                    if cost < neighbor_node.g_score:
                        map.get_node(neighbor_node.pos).parent = test_node
                neighbor_node.g_score = cost
                neighbor_node.h_score = AStar.dist_heuristic(neighbor_node, end_node)
                neighbor_node.f_score = neighbor_node.g_score + neighbor_node.h_score
        return AStar.reconstruct_path(start_node)


# A list of AStarNode objects. Allows 'contains' and 'isEmpty' checks, along with the ability to get the first
# node (ordered by f_score) in the list.
class AStarNodeList:
    def __init__(self):
        self.nodes = {}

    def add_or_replace(self, node):
        if node:
            self.nodes[node.pos] = node

    def first(self):
        if self.is_empty():
            return None
        return sorted(self.nodes.items(), key=lambda x: x[1].f_score)[0][1]

    def remove(self, node):
        if node:
            self.nodes.pop(node.pos)

    def get(self, pos):
        if not pos or pos not in self.nodes:
            return None
        return self.nodes[pos]

    def contains(self, node):
        if not node:
            return False
        return node.pos in self.nodes

    def is_empty(self):
        return len(self.nodes) == 0

    def get_position_list(self):
        pos_list = []
        for pos in self.nodes.keys():
            pos_list.append([pos[0], pos[1]])
        return pos_list


# Node representation of the map. Upon initialization, the map is populated with impassable 
class AStarMap:
    def __init__(self, obstacles=None):
        self.nodes = AStarNodeList()
        self.blocked_nodes = AStarNodeList()
        if obstacles:
            self.update_blocked_nodes(obstacles)

    def update_blocked_nodes(self, obstacles):
        self.blocked_nodes = AStarNodeList()
        for obstacle in obstacles:
            for y in range(obstacle.pos[1] - obstacle.h / 2, obstacle.pos[1] + obstacle.h / 2):
                for x in range(obstacle.pos[0] - obstacle.w / 2, obstacle.pos[0] + obstacle.w / 2):
                    self.blocked_nodes.add_or_replace(self.get_node((x, y)))

    def get_node(self, pos):
        if not self.nodes.get(pos):
            new_node = AStarNode(pos)
            self.nodes.add_or_replace(new_node)
        return self.nodes.get(pos)

    def get_neighbor_nodes(self, node, step_size=1):
        neighbors = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == y == 0:
                    continue
                else:
                    neighbors.append(self.get_node((node.pos[0] + x * step_size,
                                                    node.pos[1] + y * step_size)))
        return neighbors

    def clear_scores(self):
        for node in self.nodes.nodes.values():
            node.f_score = node.g_score = node.h_score = 0

## Path object to steer entity around static obstacles
class AStarPath:
    def __init__(self):
        self.path = []
        self.closed_list = None
        self.open_list = None

    def generate(self, node, closed_list=None, open_list=None):
        self.closed_list = closed_list
        self.open_list = open_list
        self.path.append(node)
        node = node.parent
        while node:
            self.path.append(node)
            node = node.parent
        self.path.reverse()

    # for debugging
    def print_path(self):
        for node in self.path:
            print node.pos

    def get_closed_list(self):
        if not self.closed_list or self.closed_list.is_empty():
            return []
        return self.closed_list.get_position_list()

    def get_open_list(self):
        if not self.open_list or self.open_list.is_empty():
            return []
        return self.open_list.get_position_list()

    # for debugging
    def get_path(self):
        node_list = []
        for node in self.path:
            node_list.append(node.pos)
        return node_list


## Node in path
class AStarNode:
    # pos -> a tuple representing the global (x, y) coordinates
    # cost -> the cost from the start node up to this point
    # parent -> the previous node (necessary?)
    def __init__(self, pos):
        self.pos = pos
        self.f_score = 0
        self.g_score = 0
        self.h_score = 0
        self.parent = None

    # close enough to the target? path determined!
    def close_enough(self, target):
        dx = self.pos[0] - target.pos[0]
        dy = self.pos[1] - target.pos[1]
        return (dx ** 2 + dy ** 2) <= 100