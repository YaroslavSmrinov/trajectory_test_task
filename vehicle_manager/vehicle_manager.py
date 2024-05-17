from typing import List, Dict, Any
import requests

from .kdtree import KdTree, calculate_distance
from .vehicle import Vehicle


class VehicleManager:
    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self) -> List[Vehicle]:
        """Получение списка автомобилей"""
        response = requests.get(f"{self.url}/vehicles")
        response.raise_for_status()
        return [Vehicle(**vehicle) for vehicle in response.json()]

    def filter_vehicles(self, params: Dict[str, Any]) -> List[Vehicle]:
        """Получение списка автомобилей по заданным параметрам"""
        response = requests.get(f"{self.url}/vehicles", params=params)
        response.raise_for_status()

        def params_matches(vehicle_data: Dict[str, Any]) -> bool:
            """Проверка соответствия автомобиля заданным параметрам"""
            return all(vehicle_data.get(key) == value for key, value in params.items())

        filtered_data = filter(params_matches, response.json())
        return [Vehicle(**vehicle_data) for vehicle_data in filtered_data]

    def get_vehicle(self, id: int) -> Vehicle:  # NoQa
        """Получение информации об автомобиле по id"""
        response = requests.get(f"{self.url}/vehicles/{id}")
        response.raise_for_status()
        return Vehicle(**response.json())

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Добавление нового автомобиля"""
        delattr(vehicle, 'id')  # NoQA
        response = requests.post(f"{self.url}/vehicles", json=vehicle.__dict__)
        response.raise_for_status()
        return Vehicle(**response.json())

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Изменение информации об автомобиле"""
        response = requests.put(f"{self.url}/vehicles/{vehicle.id}", json=vehicle.__dict__)
        response.raise_for_status()
        return Vehicle(**response.json())

    def delete_vehicle(self, id: int) -> bool:  # NoQA
        """Удаление автомобиля"""
        response = requests.delete(f"{self.url}/vehicles/{id}")
        response.raise_for_status()
        return response.status_code == 204

    def get_distance(self, id1: int, id2: int) -> float:
        """Расчет расстояние между двумя автомобилями (в метрах)"""
        vehicle1: Vehicle = self.get_vehicle(id1)
        vehicle2: Vehicle = self.get_vehicle(id2)

        lat1, lon1 = vehicle1.latitude, vehicle1.longitude
        lat2, lon2 = vehicle2.latitude, vehicle2.longitude

        return calculate_distance(lat1, lon1, lat2, lon2)

    def get_nearest_vehicle(self, id: int) -> Vehicle:  # NoQA
        """Нахождение ближайшего автомобиля к заданному"""
        vehicles = self.get_vehicles()
        target_vehicle = self.get_vehicle(id)

        # Подготовка точек для дерева
        points = [((vehicle.latitude, vehicle.longitude), vehicle.id) for vehicle in vehicles if
                  vehicle.id != target_vehicle.id]

        # Построение дерева
        kdtree = KdTree(points)

        # Поиск ближайшего автомобиля
        nearest_id: int = kdtree.closest_vehicle_id((target_vehicle.latitude, target_vehicle.longitude))

        return self.get_vehicle(nearest_id)
