from database.DAO import DAO
from model.simulatore import Simulatore
import numpy as np


class Model:
    def __init__(self):
        pass

    def initialization(self):
        self._prodotti = {i.product_name: i for i in DAO.all_products()}
        """ contiene tutti i prodotti presenti nei punti vendita"""

        self._negozi = {}
        """ contiene tutti i negozi presenti in una determinata località"""
        # Recupera tutti i negozi attraverso il DAO
        n = DAO.all_stores()
        for i in n:
            if i.store_location not in self._negozi.keys():
                self._negozi[i.store_location] = [i.store_name]
            else:
                self._negozi[i.store_location].append(i.store_name)

        # Variabili per memorizzare :
        self._a1 = None   # anno selezionato
        self._l = None    # locale selezionato
        self._s = None      # store selezionato
        self._a2 = None     # anno selezionato per il grafico andamento negozio X

        # dizionari che conteranno i valori ricavati con il DAO
        self._d1 = {}
        self._d2 = {}
        self._d3 = {}

        # contenente i risultati dell'analisi cvp e variazioni
        self._ris1 = {}
        self._ris2 = {}

    def get_prodotti(self, nameprod):
        """ metodo che restituisce il prodotto corrispondente al nome fornito """
        return self._prodotti.get(nameprod)

    def get_negozi(self, loc):
        """ metodo che restituisce la lista dei negozi per la località fornita """

        lst_stores = self._negozi.get(loc)
        lst_stores.sort()   # ordino la lista alfabeticamente
        return lst_stores

    def get_loc_e_date(self):
        """ metodo per ricavare le località e il periodo delle transazioni """

        # lista che contiene le localita
        loc = list(self._negozi.keys())

        date = {}
        mese = []

        # recupero le date delle transazioni attraverso il DAO
        d = DAO.date_transiction()
        for i in d:
            # Crea un dizionario che associa ogni anno ai relativi mesi
            if i[0] not in date.keys():
                mese = [i[1]]
            else:
                mese.append(i[1])

            date[i[0]] = mese

        return loc, date

    def get_andamento(self, loc, yy):
        """ Metodo per creare i dizionari ed evitare chiamate ridondanti al DAO"""

        # controllo che la location e l'anno siano gli stessi per evitare chiamate ridondanti al DAO
        if self._l != loc or self._a1 != yy:
            self._l = loc  # aggiorna la località selezionata
            self._a1 = yy  # aggiorna l'anno selezionato

            self._d1 = {}
            # Recupero i dati sui prodotti per la località e l'anno
            d1 = DAO.andamento_prodotti(loc, yy)
            for i in d1:
                self.creazione_dizionario(i, i.month, self._d1, "no")

            self._d2 = {}
            # Recupero i dati sui negozi per la località e l'anno
            d2 = DAO.prod_by_store(loc, yy)
            for i in d2:
                self.creazione_dizionario(i, i.name_store, self._d2, "si")

        return self._d1, self._d2

    @staticmethod
    def creazione_dizionario(i, key, d, add):
        """  Popolo i dizionari creati"""

        # Calcolo il mdc
        mdc = lambda revenue, cost: float(revenue) - float(cost)

        # controllo che il dato non sia già presente nel dizionario
        if key not in d:
            d[key] = ([], [], [], [], []) if add != "no" else ([], [], [], [])

        # dati che devono essere inseriti nel dizionario
        values = d[key]
        values[0].append(i.name_prod)
        values[1].append(int(i.qty_sell))
        values[2].append(float(i.revenue))
        values[3].append(mdc(i.revenue, i.cv))

        # Controllo se si deve aggiungere un dato in più al dizionario
        if add != "no":
            values[4].append(int(i.stock))

        return d

    def get_andamento_profitto(self, loc, yy):
        """ Calcola il profitto totale per le località e gli anno specificato"""

        # Ricavo i dati di andamento
        p, n = self.get_andamento(loc, yy)
        # Restituisce una lista dei profitti totali per ogni negozio
        return [sum(i[3]) for i in p.values()]

    def get_indicatori(self, loc, yy):
        """ Calcola indicatori di quantita, ricavi e profitti totali per le località e gli anni specificati"""

        # Inizializzo le quantità, i ricavi e profitto
        qty, revenue, profit = 0, 0, 0
        # Ricavo i dati di andamento
        p, n = self.get_andamento(loc, yy)
        for t, i in p.items():
            qty += sum(i[1])
            revenue += sum(i[2])
            profit += sum(i[3])

        return qty, revenue, profit

    def get_prodotto_most_redditizio(self, loc, yy):
        """ metodo per ricavare il negozio che presenta il prodotto più redditizio e la categoria a cui appartiene """

        # Inizializzo le variabili contenti i risultati
        max_profit = 0
        best_solution = 0
        p, n = self.get_andamento(loc, yy)
        for t, i in n.items():
            # Calcolo i profitti tramite ricorsione
            profit, index = self.ricorsione1(i[3])
            # controllo se il profitto sia >= massimo profitto trovato
            if profit >= max_profit:
                max_profit = profit  # Aggiorno il profitto Maximo
                prod = i[0][index]  # ricavo il prodotto corrispondente
                category = self.get_prodotti(prod).product_category  # Ricavo la categoria del prodotto
                # Aggiorno la migliore soluzione
                best_solution = (t, f"Product:\n{prod}\n[{category}]", f"Profit:\n${max_profit:1.2f}")

        return best_solution

    def ricorsione1(self, lst, index=0, highest=None, i=None):
        """ Funzione ricorsiva per trovare gli indici e i valori max in una lista"""

        # Condizione di uscita dalla ricorsione
        if index >= len(lst):
            return highest, i

        if highest is None or lst[index] >= highest:
            highest = lst[index]  # Aggiorno il valore max
            i = index  # Aggiorno l'indice

        # Richiamo la ricorsione sul prossimo indice
        return self.ricorsione1(lst, index + 1, highest, i)

    def get_category(self, loc, yy):
        """ restituisce un dizionario delle categorie con quantità e profitto totale """

        c = {}
        # Ricavo i dati
        p, n = self.get_andamento(loc, yy)
        for t, i in p.items():
            for j in range(len(i[0])):
                # Ricavo la categoria del prodotto
                c1 = self.get_prodotti(i[0][j]).product_category
                # se non esiste allora inizializzo la quantita e il profitto
                if c1 not in c:
                    c[c1] = (0, 0)
                q, m = c[c1]
                c[c1] = (q+i[1][j], m+i[3][j])
        return c

    def get_lista_prodotti(self, loc, yy):
        """ Restituisce un dizionario dei prodotti con quantità e profitto totale """
        pp = {}
        # Ricavo i dati
        p, n = self.get_andamento(loc, yy)
        # Itero sul dizionario p
        for t, i in p.items():
            for j in range(len(i[0])):
                prod = i[0][j]
                category = self.get_prodotti(prod).product_category
                qty = i[1][j]
                profit = i[3][j]
                if prod not in pp:
                    pp[prod] = (category, qty, profit)
                else:
                    # Ricavo i valori correnti
                    category, current_qty, current_profit = pp[prod]
                    pp[prod] = (category, current_qty+qty, current_profit+profit)

        # se prodotto non è presente allora assumo che qty e mdc siano nulli
        pp.update({j: (self.get_prodotti(j).product_category, 0, 0) for j in self._prodotti.keys() if j not in pp})
        # Ordino il dizionario per nome del prodotto
        pp = dict(sorted(pp.items(), key=lambda item: item[0]))
        return pp

    def get_andamento_prodotto(self, loc, yy, product):
        """ Restituisce un elenco di profitti per un prodotto specifico """

        r = []
        p, n = self.get_andamento(loc, yy)
        for t, i in p.items():
            # se il prodotto non è presente in quel mese allora il suo profitto è zero
            if product not in i[0]:
                r.append(0)
            else:
                # trovo il profitto corrispondente al prodotto
                for j in range(len(i[0])):
                    if i[0][j] == product:
                        r.append(i[3][j])
                        # esco una volta trovato il profitto
                        break
        return r

# ----------------------------------------------------------------------------------------------
    def get_lista_negozi(self, loc, yy):
        """ Restituisce un dizionario con le quantità totali e i profitti realizzati
            per ogni negozio in una località specificata nell'anno indicato """

        # Inizializzo un dizionario vuoto per memorizzare i risultati
        nn = {}
        # Ricavo l'andamento delle vendite per la località e l'anno
        p, n = self.get_andamento(loc, yy)
        for t, i in n.items():
            qty = sum(i[1])
            profit = sum(i[3])
            # Memorizzo i risultati al dizionario
            nn[t] = (qty, profit)
        return nn

    def get_rimanenze(self, loc, yy, shop):
        """ Restituisce le rimanenze di un negozio specifico """

        # Ricavo l'andamento dei negozi
        p, n = self.get_andamento(loc, yy)
        # Estraggo i prodotti e le rimanenze dal dizionario
        prod = n.get(shop)[0]
        stock = n.get(shop)[4]

        # ordino la lista stock in ordine descrescente
        stock.sort(reverse=True)
        # Ordino la lista prodotti in base all'ordine delle rimanenze
        prod.sort(key=stock.sort(reverse=True))

        return prod, stock

    def andamento1(self, shop, yy):
        """ metodo per ricavare l'andamento mensile di ogni prodotto presente nel negozio X"""

        # Controllo se il negozio e l'anno sono cambiati
        if self._s != shop or self._a2 != yy:
            self._s = shop  # Aggiorno il negozio selezionato
            self._a2 = yy   # Aggiorno l'anno selezionato
            # Inizializzo un dizionario per memorizzare i dati
            self._d3 = {}
            # Ricavo i dati di andamento dal database
            d3 = DAO.andamento_negozio(shop, yy)
            for i in d3:
                self.creazione_dizionario(i, i.month, self._d3, "no")
        return self._d3

    def get_andamento_negozio(self, shop, yy):
        """ Restituisce una lista contenente i profitti mensili
            per un negozio specificato nell'anno indicato """

        # inizializzo una lista vuota per memorizzare i risultati
        profit = []
        # ottengo i dati di andamento per il negozio e l'anno specificato
        n = self.andamento1(shop, yy)
        for t, i in n.items():
            # calcola la somma delle vendite e lo aggiunge alla lista
            profit.append(sum(i[3]))

        return profit

    # ----ANALISI CVP----
    def calcolo_mdc(self, shop, yy, mm, cf, target):
        """ Calcola il MDC per il negozio specificato in base ai parametri forniti """

        # ricavo i dati per il mese specificato
        name_prod, qty, revenue, mdc = self.andamento1(shop, yy).get(mm)

        # calcola il RO sottraendo i costiFissi
        self.ro = sum(mdc) - cf

        # calcola il MDC medio
        wamdcr = sum(mdc) / sum(revenue)
        # calcolo il punto di pareggio in $
        self.rbep = (cf + target) / wamdcr

        tot_qty = sum(qty)
        tot_revenue = sum(revenue)
        # chiama la funzione ricorsiva per calcoli aggiuntivi
        wamdc, mixx = self.ricorsione2(qty, revenue, mdc, tot_qty, tot_revenue)

        # calcolo il punto di pareggio in unita
        self.qbep = (cf + target) / wamdc

        # calcolo il margine di sicurezza
        self.mds = sum(revenue) - self.rbep

        # memorizzo i risultati
        self._ris1 = (name_prod, qty, revenue, mixx)

    def get_ris1(self):
        """ Restituisce i risultati calcolati """
        return self._ris1

    def ricorsione2(self, qty, rr, mdc, totq, totr, index=0, wamdc=0, mix=None):
        """ Funzione ricorsiva per calcolare variabili relative a vendite e margini per ogni prodotto """

        if mix is None:
            mix = []

        # Condizione di uscita dalla ricorsione
        if index >= len(qty):
            return wamdc, mix

        # Calcolo il MDC unitario
        u = mdc[index] / qty[index]
        mixu = qty[index] / totq  # <-- sales mix in % unit
        wamdc += mixu * u

        # per ottenere il ricavo da ottenere per ogni prodotto
        mixr = rr[index] / totr
        rbepi = mixr * self.rbep
        mix.append(rbepi)

        return self.ricorsione2(qty, rr, mdc, totq, totr, index + 1, wamdc=wamdc, mix=mix)

    def get_bep_e_mds(self):
        """ restituisce il punto di pareggio, margine di sicurezza e il reddito operativo """
        return self.qbep, self.rbep, self.mds, self.ro

    def get_retta(self, cf):
        """ Calcolo la retta per rappresentare graficamente i risultati in base ai costi fissi """

        # Calcolo la quantita totale venduta
        q = sum(self.get_ris1()[1])

        # Ricavo i valori necessari per la retta
        qbep, rbep, mds, ro = self.get_bep_e_mds()

        # Creo i valori per l'asse x
        x1 = np.linspace(0, q + qbep)

        # Definisco i punti per la retta
        pt = [(0, 0), (qbep, rbep), (0, cf)]

        return self.ricorsione3(pt, x1)

    def ricorsione3(self, punti, x1, index=0):
        """ Funzione ricorsiva per calcolare le rette tra punti dati
            e restituire una lista di rette """

        # Condizione di uscita dalla ricorsione
        if index >= len(punti)-1:
            return []  # se non ci sono più punti da elaborare, restituisce una lista vuota

        a = punti[index]
        b = punti[index + 1]

        # Ricavo equazione della retta passante tra i due punti dati
        retta = self.creazione_retta(a, b, x1)

        # Restituisce la retta e continua la ricorsione
        return [retta] + self.ricorsione3(punti, x1, index + 1)

    @staticmethod
    def creazione_retta(a, b, x1):
        """ Calcola l'equazione della retta passante per i punti a e b
            e restituisce i valori y corrispondenti a x1 """

        # Calcolo il coefficiente angolare m
        m = (b[1] - a[1]) / (b[0] - a[0])
        # Calcolo q
        q = (-m * a[0]) + a[1]

        return (m * x1) + q

    # calcolo variazione variabili
    def simulazione(self, cf, vqty, vpr, vcf):
        """ Esegue una simulazione basata sui parametri forniti """

        # ricavo i parametri che devono essere passati:
        nameprod, qty, rr, mixx = self.get_ris1()
        mdc = self.ro+cf  # Calcolo il MDC attuale
        prod = {}   # lista che contiene informazioni riguardanti ai prodotti (Pname, Pr, cv, qty)
        for i in range(len(nameprod)):
            prod.update({nameprod[i]: (self.get_prodotti(nameprod[i]).product_price, self.get_prodotti(nameprod[i]).product_cost, qty[i])})

        # Passo i parametri al simulatore:
        sim = Simulatore(prod, mdc)
        sim.init(vqty, vpr, vcf)  # passo i parametri che vengono dal controller
        # avvio la simulazione
        sim.run()
        # memorizzo i risultati della simulazione
        result = sim.get_result()
        self._ris2 = dict(sorted(result.items(), key=lambda item: item[1]))  # ordino il dizionario in base a ro

    def get_ris2(self):
        """ Restituisce i risultati della simulazione """
        return self._ris2
