import heapq


class Pathfinder:
    def __init__(self, original_point, destination, obstacles):
        self.original_point = original_point
        self.destination = destination
        self.obstacles = obstacles
        self.came_from = {}
        self.g_score = {self.original_point: 0}

    def heuristic(self, a, b):
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

    def astar(self):
        start_node = (self.original_point, 0)
        end_node = (self.destination, 0)

        open_set = [start_node]
        closed_set = set()

        f_score = {start_node: self.heuristic(start_node[0], end_node[0])}

        while open_set:
            current_node = heapq.heappop(open_set)[0]

            if current_node == end_node[0]:
                path = [current_node]
                while current_node in self.came_from:
                    current_node = self.came_from[current_node]
                    path.append(current_node)
                return path[::-1]

            closed_set.add(current_node)

            for neighbor in self.get_neighbors(current_node):
                tentative_g_score = self.g_score[current_node] + self.heuristic(current_node, neighbor)

                if neighbor in closed_set:
                    continue

                if neighbor not in open_set or tentative_g_score < self.g_score[neighbor]:
                    heapq.heappush(open_set, (neighbor, tentative_g_score))
                    self.came_from[neighbor] = current_node
                    self.g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end_node[0])

        return []

    def get_neighbors(self, node):
        x, y = node
        print(node)
        neighbors = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        return [neighbor for neighbor in neighbors if
                all(not obstacle.collides_with_obstacle(neighbor) for obstacle in self.obstacles)]

    def find_path(self):
        return self.astar()
