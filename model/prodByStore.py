from dataclasses import dataclass


@dataclass
class ProdByStore:
    _nameP: str
    _nameS: str
    _stock: int
    _qtySell: int
    _revenue: float
    _cv: float

    @property
    def name_prod(self):
        return self._nameP

    @property
    def name_store(self):
        return self._nameS

    @property
    def stock(self):
        return self._stock

    @property
    def qty_sell(self):
        return self._qtySell

    @property
    def revenue(self):
        return self._revenue

    @property
    def cv(self):
        return self._cv

    def __hash__(self):
        return hash(self._nameP)

    def __str__(self):
        return f"{self._nameP}"
