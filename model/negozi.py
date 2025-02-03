from dataclasses import dataclass


@dataclass
class Negozi:
    store_ID: int
    store_name: str
    store_city: str
    store_location: str
    store_open_date: int

    def __hash__(self):
        return hash(self.store_name)

    def __str__(self):
        return f"{self.store_name}"
