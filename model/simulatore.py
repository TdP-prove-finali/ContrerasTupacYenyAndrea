import heapq
import random
import time


class Simulatore:
    def __init__(self, p, mdc):
        """ Inizializza un'istanza della classe Simulatore """

        self.prod = p  # Dizionario contenente informazioni sui prodotti(Pname, Pr, cv, qtySold)
        self.mdc_attuale = mdc  # MDC realizzato nel mese in esame

        self.ti = time.perf_counter()  # tempo inizio contatore

        self.list_vpr = [-50, -40, -30, -25, -20, -15, -10, -5, 5, 10, 15, 20, 25, 30, 40, 50]   # variazioni possibili per pr
        self.list_vcf = list(range(-1400, -49, 50)) + list(range(50, 1401, 50))  # variazioni possibili per cf
        self.tot_soluzioni = 10  # Numero totale di soluzioni alternative da trovare
        self.num_combinazioni = len(self.list_vpr)*len(self.list_vcf) # numero di combinazioni possibili

        # Creo una coda per gestire gli eventi
        self.queue = []

    def init(self, vqty, vpr, vcf):
        """ Inizializza le variabili che subiscono variazioni e carica la coda """

        self.vQty = vqty
        self.vPr = vpr
        self.vCF = vcf

        # Inizializzo i risultati della simulazione
        self.ro = {}
        self.ris = 0
        self.combinazioni = [(self.vPr, self.vCF)]  # memorizzo le combinazioni già provate

        # carico la coda con l'evento iniziale
        heapq.heappush(self.queue, (0, "inizio", self.tot_soluzioni))

    def run(self):
        """ Eseguo la simulazione fino all'esaurimento della coda degli eventi """

        # condizione di fine è l'esaurimento della coda
        while self.queue:
            # restituisce il piccolo elemento della coda
            e = heapq.heappop(self.queue)

            self.process_events(e)

    def process_events(self, e):
        """ Processa gli eventi nella coda """

        t = e[0]    # tempo dell'evento
        tipo = e[1]  # tipo di evento
        n = e[2]    # Numero di soluzioni rimanenti

        if tipo == 'inizio':
            # Calcolo la variazione del RO atteso
            self.ris = self.calcolo_mdc_atteso() - self.mdc_attuale - self.vCF

            # Calcolo il tempo richiesto per eseguire questa procedura
            tf = time.perf_counter()
            te = tf-self.ti

            # Aggiunge un nuovo evento alla coda
            heapq.heappush(self.queue, (te, 'fine', n))

        if tipo == 'fine':
            # controllo che le soluzioni alternative non  siano state già trovate
            # e che il tempo di esecuzione non sia superiore a 2 secondi
            if n > 0 and t < 2:
                # carico la coda
                if self.ris > 0:
                    # memorizzo le soluzioni trovate
                    self.ro.update({(self.vQty, self.vPr, self.vCF): self.ris})

                # cerco nuove soluzioni alternative:
                heapq.heappush(self.queue, (t, 'nuovo', n))

        if tipo == 'nuovo':
            # Genero nuove percentuali per le variabili
            trovato = self.genero_percentuali()

            # calcolo il tempo richiesto per la procedura precedente
            tf = time.perf_counter()
            te = tf-self.ti

            # controllo che tutte le combinazioni possibili siano state provate
            # e che il tempo di esecuzione non sia superiore a 2 secondi
            if te < 2 and self.num_combinazioni > 0:
                self.num_combinazioni -= 1  # decremento il numero di cobinazioni possibili
                if trovato is True:
                    # Aggiungo un evento alla coda aggiornando il numero di soluzioni trovate
                    heapq.heappush(self.queue, (te, 'inizio', n-1))
                else:
                    heapq.heappush(self.queue, (te, 'nuovo', n))

    def calcolo_mdc_atteso(self):
        """ calcolo il MDC atteso basato sulle varizioni delle variabili"""

        mdc_atteso = 0
        for k, i in self.prod.items():
            # calcolo le variazioni:
            var_qty = i[2] + (i[2] * (self.vQty/100))
            pr = i[0]
            var_pr = pr + (pr * (self.vPr/100))
            cvu = i[1]
            mdcu = var_pr - cvu
            mdc_atteso = mdc_atteso + var_qty * mdcu  # aggiorno il MDC atteso
        return mdc_atteso

    def genero_percentuali(self):
        """ Genera nuove percentuali per le variabili """
        # controllo che non vengano scelte le stesse combinazioni
        if self.vPr != 0:
            # scelgo casualmente una variazione percentuale per il prezzo
            self.vPr = random.choice(self.list_vpr)
        if self.vCF != 0:
            # scelgo casualmente una variazione percentuale per il costoFisso
            self.vCF = random.choice(self.list_vcf)

        # Aggiungo la nuova combinazione se non è già presente
        if (self.vPr, self.vCF) not in self.combinazioni:
            self.combinazioni.append((self.vPr, self.vCF))
            return True
        return False

    def get_result(self):
        """ Restituisce i risultati ottenuti dalla simulazione """
        return self.ro
