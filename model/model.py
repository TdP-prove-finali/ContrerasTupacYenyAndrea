from database.DAO import DAO
from model.simulatore import Simulatore

class Model():
    def __init__(self):

        self._prodotti = {}
        """ contiene tutti i prodotti presenti nei punti vendita"""
        p = DAO.AllProducts()
        for i in p:
            self._prodotti[i.Product_Name] = i.Product_Category

        self._negozi = {}
        """ contiene tutti i negozi presenti in una determinata località"""
        n = DAO.AllStores()
        t = []
        for i in n:
            if i.Store_Location not in self._negozi.keys():
                t = [i.Store_Name]
            else:
                t.append(i.Store_Name)
            self._negozi[i.Store_Location] = t

        self.a=None
        self.l=None

        self.d1 = {}
        self.d2 = {}
        self.d3 = {}

        self.s=None
        self.y1=None
#-----------------------------------
    def getProdotti(self, Pname):
        """ metodo per prendere i prodotti di una data categoria """

        return self._prodotti.get(Pname)

    def getNegozi(self, loc):
        """ metodo per prendere i negozi presenti in una determinata località"""

        return self._negozi.get(loc)

    def getLOCeDATE(self):
        """ metodo per ricavare le località e il periodo in cui si sono avuti le transazioni """

        loc=list(self._negozi.keys())

        date={}
        mese=[]
        d = DAO.YYeMM()
        for i in d:
            if i[0] not in date.keys():
                mese=[i[1]]
            else:
                mese.append(i[1])
            date.update({i[0]: mese})

        return loc, date

#----------------------------------
    def getAndamento(self, loc, yy):
        """ metodo per prendere i l'andamento mensile di ogni prodotto """

        # controllo che la location e l'anno siano sempre gli stessi per non richiamare il DAO
        if self.l!=loc or self.y != yy:
            self.l=loc
            self.y=yy

            self.d1 = {}
            d1 = DAO.andamentoProdotti(loc, yy)
            for i in d1:
                self.creazioneDizionario(i, i.mm, self.d1)

            self.d2 = {}
            d2 = DAO.prodByStore(loc, yy)
            for i in d2:
                self.creazioneDizionario(i, i.Sname, self.d2)

        return self.d1, self.d2

    def creazioneDizionario(self, i, key, d):

        if key not in d.keys():
            p = [i.Pname]
            q = [int(i.qtySell)]
            r = [float(i.revenue)]
            c = float(i.revenue) - float(i.cv)
            m = [c]
            d[key] = (p, q, r, m)
        else:
            p=d.get(key)[0]
            p.append(i.Pname)
            q = d.get(key)[1]
            q.append(int(i.qtySell))
            r = d.get(key)[2]
            r.append(float(i.revenue))
            c = float(i.revenue) - float(i.cv)
            m = d.get(key)[3]
            m.append(c)
            d[key] = (p, q, r, m)

        return d

    def getAndamentoProfitto(self, loc, yy):
        m=[]
        p, n = self.getAndamento(loc, yy)
        for t, i in p.items():
            m.append(sum(i[3]))
        return m

    def getIndicatori(self, loc, yy):

        q = 0
        r = 0
        m = 0
        p, n = self.getAndamento(loc, yy)
        for t, i in p.items():
            q = q+sum(i[1])
            r = r+sum(i[2])
            m = m+sum(i[3])

        return q, r, m

    def getProdottoMostRedditizio(self, loc, yy):
        """ metodo per ricavare il negozio che presenta il prodotto più redditizio e la categoria a cui appartiene """

        max=0
        x=0
        p, n = self.getAndamento(loc, yy)
        for t, i in n.items():
            l=self.ricorsione(i[3])
            for j in range(len(l)):
                if l[j][1]>=max:
                    max=l[j][1]
                    p= i[0][l[j][0]]
                    k = self._prodotti.get(p)

                    x=(t, f"Product:\n{p}\n[{k}]", f"Profit:\n${max:1.2f}")

        return x

    def ricorsione(self, lst, index=0, highest=None):
        ll=[]
        if index >= len(lst):
            for k in range(len(lst)):
                if lst[k] == highest:
                    ll.append((k, lst[k]))
            return ll

        if highest is None or lst[index] >= highest:
            highest = lst[index]

        return self.ricorsione(lst, index + 1, highest)



    def getCategory1(self, loc, yy):
        c = {}
        q = 0
        m=0
        p, n = self.getAndamento(loc, yy)
        for t, i in p.items():
            for j in range(len(i[0])):
                c1 = self.getProdotti(i[0][j])
                if c1 not in c.keys():
                    q = i[1][j]
                    m = i[3][j]
                else:
                    q = c.get(c1)[0] + i[1][j]
                    m = c.get(c1)[1] + i[3][j]
                c[c1] = (q, m)
        return c

    def getListaProdotti(self, loc, yy):
        pp={}
        q=0
        m=0
        p, n = self.getAndamento(loc, yy)
        for t, i in p.items():
            for j in range(len(i[0])):
                if i[0][j] not in pp.keys():
                    q=i[1][j]
                    m=i[3][j]
                else:
                    q = pp.get(i[0][j])[0] + i[1][j]
                    m = pp.get(i[0][j])[1] + i[3][j]
                pp[i[0][j]] = (q, m)

        # se prodotto non è presente allora assumo che qty e mdc siano nulli
        for j, i in self._prodotti.items():
            if j not in pp.keys():
                pp.update({j:(0,0)})

        pp=dict(sorted(pp.items(), key=lambda item: item[0]))
        return pp

    def getAndamentoProdotto(self, loc, yy, product):
        r=[]
        p, n =self.getAndamento(loc, yy)
        for t, i in p.items():
            # se il prodotto non è presente in quel mese allora il suo profitto è zero
            if product not in i[0]:
                r.append(0)
            else:
                for j in range(len(i[0])):
                    b = i[0][j]
                    if b == product:
                        r.append(i[3][j])
        return r

#----------------------------------------------------------------------------------------------
    def getListaNegozi(self, loc, yy):
        nn={}
        q=0
        m=0
        p, n = self.getAndamento(loc, yy)
        for t, i in n.items():
            q = sum(i[1])
            m = sum(i[3])
            nn[t] = (q, m)
        return nn

    def getRimanenze(self, loc, yy, shop):
        p,n =self.getAndamento(loc, yy)
        s=n.get(shop)[0]
        r=n.get(shop)[2]
        r.sort(reverse=True)
        s.sort(key=s.sort(reverse=True))
        return s, r


    def andamento1(self, shop, yy):
        """ metodo per ricavare l'andamento mensile di ogni prodotto presente nel negozio X"""

        if self.s!=shop or self.y1 != yy:
            self.s=shop
            self.y1=yy
            self.d3 = {}
            d3 = DAO.andamentoNegozio(shop, yy)
            for i in d3:
                self.creazioneDizionario(i, i.mm, self.d3)
        return self.d3

    def getAndamentoNegozio(self, shop, yy):
        m=[]
        n = self.andamento1(shop, yy)
        for t, i in n.items():
            m.append(sum(i[3]))
        return m



    #ANALISI CVP:
    def simula(self,shop, yy, mm, cf, target):
        t=self.andamento1(shop, yy)
        # passo il paramtro che viene dal model
        sim = Simulatore(t.get(mm))
        # passo i parametri che vengono dal controller
        sim.init(cf, target)
        # avvio la simulazione
        sim.run()
        # ricavo i risultati della simulazione
        self.s0 = sim.getRis()
        self.s1 = sim.getRetta()
        self.s2 = sim.getBEPeMDS()
        self.s3 = sim.getMix()

    def getRis(self):
        return self.s0
    def getRetta(self):
        return self.s1
    def getBEPeMDS(self):
        return self.s2
    def getMix(self):
        return self.s3