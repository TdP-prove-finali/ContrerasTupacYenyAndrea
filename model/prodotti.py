from dataclasses import dataclass


@dataclass
class Prodotti:
    product_ID: int
    product_name: str
    product_category: str
    product_cost: str
    product_price: int

    def __hash__(self):
        return hash(self.product_ID)

    def __str__(self):
        return f"{self.product_name} : {self.product_category}, {self.product_price}, {self.product_cost}"
