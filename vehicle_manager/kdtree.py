import math


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Метод для расчёта расстояния между точками на поверхности земли."""
    R = 6371000  # Радиус Земли в метрах
    latitude_radians1 = math.radians(lat1)
    latitude_radians2 = math.radians(lat2)
    delta_latitude_radians = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_latitude_radians / 2) ** 2 + math.cos(latitude_radians1) * math.cos(latitude_radians2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


class Node:
    def __init__(self, point, vehicle_id, left=None, right=None):
        self.point = point
        self.vehicle_id = vehicle_id
        self.left = left
        self.right = right


class KdTree:
    def __init__(self, points):
        self.root = self.build_kdtree(points)

    def build_kdtree(self, points, depth=0):
        if not points:
            return None

        k = len(points[0][0])
        axis = depth % k
        points.sort(key=lambda x: x[0][axis])
        median = len(points) // 2

        return Node(
            point=points[median][0],
            vehicle_id=points[median][1],
            left=self.build_kdtree(points[:median], depth + 1),
            right=self.build_kdtree(points[median + 1:], depth + 1)
        )

    def closest_vehicle_id(self, target_point):
        best = [None, float('inf')]

        def search(node, depth=0):
            nonlocal best
            if node is None:
                return
            axis = depth % len(target_point)

            next_branch = node.left if target_point[axis] < node.point[axis] else node.right
            opposite_branch = node.right if target_point[axis] < node.point[axis] else node.left

            current_distance = calculate_distance(target_point[0], target_point[1], node.point[0], node.point[1])
            if current_distance < best[1]:
                best = [node.vehicle_id, current_distance]

            search(next_branch, depth + 1)
            if abs(target_point[axis] - node.point[axis]) < best[1]:
                search(opposite_branch, depth + 1)

        search(self.root)
        return best[0]
