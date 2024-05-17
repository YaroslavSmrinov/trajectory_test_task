from typing import List

from vehicle_manager import VehicleManager, Vehicle

manager = VehicleManager(url="https://test.tspb.su/test-task")

# Получение списка всех автомобилей
resp: List[Vehicle] = manager.get_vehicles()
assert isinstance(resp, list)
assert isinstance(resp[0], Vehicle)


# Получение списка автомобилей, у которых поле name равно 'Toyota'
resp: List[Vehicle] = manager.filter_vehicles(params={"name": "Toyota"})
assert resp[0].name == "Toyota"

resp: Vehicle = manager.add_vehicle(
    vehicle=Vehicle(
        name='Toyota',
        model='Camry',
        year=2021,
        color='red',
        price=21000,
        latitude=55.753215,
        longitude=37.620393
    )
)
assert isinstance(resp, Vehicle)

# Удаление автомобиля с id=1
manager.delete_vehicle(id=1)

# Расчет расстояния между автомобилями с id=1 и id=2
resp: float = manager.get_distance(id1=1, id2=2)
assert resp == 638005.0864183258

# Нахождение ближайшего автомобиля к автомобилю с id=1
resp: Vehicle = manager.get_nearest_vehicle(id=1)
assert (resp.name, resp.model) == ('Tesla', 'Model 3')  # тесла сейчас находится ближе к камри чем к Kia
