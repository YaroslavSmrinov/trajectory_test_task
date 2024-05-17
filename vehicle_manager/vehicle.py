from typing import Optional


class Vehicle:
    def __init__(
            self,
            id: Optional[int] = None,  # NoQA
            name: Optional[str] = None,
            model: Optional[str] = None,
            year: Optional[int] = None,
            color: Optional[str] = None,
            price: Optional[float] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None
    ) -> None:
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"
