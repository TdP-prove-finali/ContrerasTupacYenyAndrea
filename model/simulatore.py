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
        Pname = self.lista[0]
        qty = self.lista[1]
        rr = self.lista[2]
        cv = self.lista[3]

        self.ro=sum(rr)-sum(cv)-self.cf

        wamdcr=(sum(rr) - sum(cv)) / sum(rr)  # un altro modo: mdcratio(mdcu/p) * salesmix(rr[i]/sum[rr])
        self.rbep = (self.cf + self.target) / wamdcr

        mdcu = []
        wamdc = []
        mixx = []

        for i in range(len(qty)):
            # per ricavare il MDC in unita per Qbep
            u = (rr[i] - cv[i]) / qty[i]
            mdcu.append(u)
            mixu = qty[i] / sum(qty) # <-- sales mix in % unit
            t1 = mixu * u
            wamdc.append(t1)
            # per ricavare il ricavo da ottenre per ogni prodotto
            mixr = rr[i] / sum(rr) #  <-- sales mix in % $
            rbepi = mixr * self.rbep
            mixx.append(rbepi)

        self.qbep = (self.cf + self.target) / sum(wamdc)
        self.mds = sum(rr) - self.rbep

        self.ris = (Pname, qty, rr, mixx)

    def getRis(self):
        return self.ris

    def getBEPeMDS(self):
        return self.qbep, self.rbep, self.mds, self.ro


    def getRetta(self):
        q=sum(self.ris[1])
        qbep, rbep, mds, ro = self.getBEPeMDS()
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
