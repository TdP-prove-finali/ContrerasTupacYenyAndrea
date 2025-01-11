from dataclasses import dataclass

@dataclass
class AndamentoNegozio:
    #ProdByMonth
    _mm:int
    _Pname:str
    _qtySell: int
    _revenue: float
    _cv: float

    @property
    def mm(self):
        return self._mm

    @property
    def Pname(self):
        return self._Pname


    @property
    def qtySell(self):
        return self._qtySell

    @property
    def revenue(self):
        return self._revenue

    @property
    def cv(self):
        return self._cv


    def __hash__(self):
        return hash(self._Pname)

    def __str__(self):
        return f"{self._Pname}"