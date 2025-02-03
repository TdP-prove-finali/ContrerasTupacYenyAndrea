from dataclasses import dataclass


@dataclass
class AndamentoNegozio:
    _mm: int
    _nameP: str
    _qtySell: int
    _revenue: float
    _cv: float

    @property
    def month(self):
        return self._mm

    @property
    def name_prod(self):
        return self._nameP

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
