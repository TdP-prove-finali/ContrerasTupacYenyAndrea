from dataclasses import dataclass

@dataclass
class Negozi:
    Store_ID: int
    Store_Name: str
    Store_City: str
    Store_Location: str
    Store_Open_Date: int

    def __hash__(self):
        return hash(self.Store_ID)

    def __str__(self):
        return f"{self.Store_Name} : {self.Store_City}, {self.Store_Location}"