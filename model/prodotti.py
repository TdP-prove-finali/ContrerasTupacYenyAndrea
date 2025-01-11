from dataclasses import dataclass

@dataclass
class Prodotti:
    Product_ID: int
    Product_Name: str
    Product_Category: str
    Product_Cost: str
    Product_Price: int

    def __hash__(self):
        return hash(self.Product_ID)

    def __str__(self):
        return f"{self.Product_Name} : {self.Product_Category}, {self.Product_Price}, {self.Product_Cost}"