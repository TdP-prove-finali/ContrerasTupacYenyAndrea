import numpy as np
class Simulatore:
    def __init__(self, lista):
        self.lista=lista
    def init(self, cf, target):
        self.cf=cf
        self.target=target

        self.ris = []
        self.mixx = []
        self.Pname = None

    def run(self):
        #condizione di terminazione
        while (len(self.ris)==0):
            self.processo()


    def processo(self):
        self.Pname = self.lista[0]
        qty = self.lista[1]
        rr = self.lista[2]
        cv = self.lista[3]
        q = sum(qty)
        r = sum(rr)
        c = sum(cv)
        mdcu = []
        wamdc = []
        self.mixx = []

        for i in range(len(qty)):
            u = (rr[i] - cv[i]) / qty[i]
            mdcu.append(u)
            mixu = qty[i] / q
            t = mixu * u
            wamdc.append(t)
            mixr = rr[i] / r
            self.mixx.append(mixr)

        self.ris = (q, r, c, wamdc)

    def getRis(self):
        return self.ris

    def getMix(self):
        return self.Pname, self.mixx

    def getBEPeMDS(self):
        r=self.ris[1]
        c=self.ris[2]
        wamdc=sum(self.ris[3])

        rbep = (self.cf + self.target) / ((r - c) / r)
        qbep = (self.cf + self.target) / (wamdc)
        mds = r - rbep

        return qbep, rbep, mds


    def getRetta(self):
        q=self.ris[0]
        qbep, rbep, mds= self.getBEPeMDS()
        x1 = np.linspace(0, q + qbep)
        y = []

        for i in (0, 2):
            if i == 0:
                a = (0, 0)
                b = (qbep, rbep)
            else:
                a = (0, self.cf)
                b = (qbep, rbep)

            retta = self.creazioneRetta(a, b, x1)
            y.append(retta)
        return y


    def creazioneRetta(self, a, b, x1):
        m=(b[1]-a[1])/(b[0]-a[0])
        q=(-m*a[0])+a[1]
        y=(m*x1)+q
        return y
