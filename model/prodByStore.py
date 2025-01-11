from dataclasses import dataclass

@dataclass
class ProdByStore:#shop
    _Pname:str
    _Sname:str
    _stock: int
    _qtySell: int
    _revenue: float
    _cv: float




    @property
    def Pname(self):
        return self._Pname

    @property
    def Sname(self):
        return self._Sname

    @property
    def stock(self):
        return self._stock

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