import flet as ft

import numpy as np
from model.stampa import print_file


class Controller:
    def __init__(self, view, model):
        self._model = model
        self._view = view
        # variabile per memorizzare la pagina attualmente chiamata
        self.view_active = None

        # variabili per memorizzare le credenziali di accesso
        self.un = None
        self.pw = None

    def initialization(self):
        """ Inizzializazione delle variabili """

        # variabili per memorizzare i mesi di ogni relativo anno
        self.mese1 = []
        self.mese2 = []

        # variabile per memorizzare la località e l'anno selezionato
        self.loc = None
        self.yy = []

        # variabili per memorizzare i risultati precedentemente ottenuti
        self.ppp = {}
        self.p = None
        self.a1 = []

        self.sp = {}
        self.n = None
        self.a2 = []

        # variabili per memorizzare il costo fisso e l'obiettivo di reddito forniti
        self.cf = None
        self.target = None

        # dizionario per memorizzare il risultato della simulazione
        self._ris = {}

    # ---------- PAGINA AUTENTICAZIONE ----------
    def login(self, e):
        """ metodo per verificare le credenziali di accesso """

        # memorizzo i dati inseriti dall'utente
        password = self.view_active.password.value
        username = self.view_active.username.value

        # Controllo che i codici di accesso siano stati già memorizzati
        if self.un is None or self.pw is None:
            # estraggo i codici d'accesso dal file txt
            self.load_credenziali()

        # 1.controllo: password sbagliata
        if username == self.un and password != self.pw:
            # visualizzero eventuali messaggi di errore
            self.msg_error("LOGIN FAILED\nincorrect password")
            return

        # 2. controllo: username sbagliata
        elif username != self.un and password == self.pw:
            # visualizzero eventuali messaggi di errore
            self.msg_error("LOGIN FAILED\nincorrect username")
            return

        # 3. controllo: username e password sbagliati
        elif username != self.un and password != self.pw:
            # visualizzero eventuali messaggi di errore
            self.msg_error("LOGIN FAILED\nplease verify your credentials")
            return

        # superato i vari controlli, posso procedere alla pagina seguente
        # inizializzo le variabili:
        self.initialization()
        self._model.initialization()
        self.fill_dd()
        self._view.page.go("/page1")

        self._view.page.update()

    def get_valore(self, line):
        """ Rimuove eventuali spazi bianchi dal valore estratto """
        line = line.rstrip('\n')           # rimuovo il carattere di nuovo linea
        word = line[line.index(':') + 1:]  # estrai la sottostringa dopo il carattere ':'
        word = word.replace(" ", "")       # rimuovo eventuali spazi bianchi
        return word

    def load_credenziali(self):
        """ estrai le credenziali da un file di testo e memorizza i valori """
        with open("UI/codici.txt", "r") as file:
            for line in file:
                if line.startswith('USERNAME'):   # controlla se la riga inizia con username
                    self.un = self.get_valore(line)
                elif line.startswith('PASSWORD'):
                    self.pw = self.get_valore(line)

    def msg_error(self, text):
        """ mostra un messaggio di errore in un dialogo di avviso"""
        self._view.page.open(ft.AlertDialog(
            content=self.create_text1(text, "black"),
            bgcolor="red300",
        ))

    def create_text1(self, testo, color, weight=None):
        return ft.Text(testo,
                       text_align=ft.TextAlign.CENTER,
                       style=ft.TextStyle(color=color,
                                          size=17,
                                          weight=weight
                                          ),
                       width=65
                       )

    def create_text2(self, testo, align=None):
        return ft.Text(testo,
                       text_align=align,
                       size=16
                       )

# ---------- PAGINA HOME ----------

    def change_page(self, page):
        """ Metodo per cambiare la pagina """

        self._view.page.views.append(page)  # aggiungo alla vista la pagina
        self.view_active = self._view.page.views[-1]  # memorizzo la pagina attuale

        if page.route == '/page2':
            self.load_page2()
        elif page.route == '/page3':
            self.load_page3()

    def load_page2(self):
        """ Inizializza la pagina 2 con i valori e le funzioni necessarie """

        # Controllo se viene selezionata una località diversa
        if self._view.ddLoc.value != self.loc:
            self.loc = self._view.ddLoc.value
            self.yy = []
            self.clear_chart(self.view_active.axs2a)
            self.clear_chart(self.view_active.axs2b[0])
            self.clear_chart(self.view_active.axs2b[1])
            self.view_active.c2.controls.clear()
            self.view_active.c3.controls.clear()

        # Aggiungi l'anno se non è già presente
        if int(self._view.ddAnno.value) not in self.yy:
            # memorizzo l'anno selezionato
            self.yy.append(int(self._view.ddAnno.value))
            self.a1 = [int(self._view.ddAnno.value)]  # inizializzo l'anno selezionato per l'andamento prodotto X
            self.a2 = [int(self._view.ddAnno.value)]  # inizializzo l'anno selezionato per l'andamento negozio X
            self.clear_chart(self.view_active.axs2c)
            self.clear_chart(self.view_active.axs2d)

            # avvio i metodi
            self.c1()
            self.c2()
            self.c3()
            self.c4()
            self.c5()
            self.c6()
            self.c7()
            self.c8()
            self.stock()

    def load_page3(self):
        """ Inizializza la pagina 3 con i valori e le funzioni necessarie """

        # pulisco la lista risultati e alcune variabili
        self.view_active.l3a.controls.clear()
        self.view_active.l4a.controls.clear()
        self.clear_chart(self.view_active.axs3a)
        self.view_active.vQty.value = ""
        self.view_active.vCF.value = ""
        self.view_active.vPr.value = ""

        # chiamo le funzioni
        self.c9()
        self.c10()

    def logout(self, e):
        # pulisco tutto come se stessi chiudendo l'applicazione e iniziando una nuova sessione
        self._view.pages = {}  # cancello tutte le pagine create
        # riporto le variabili inizializzate come in principio
        self.initialization()
        self._model.initialization()

        self._view.ddAnno.options.clear()
        self._view.ddLoc.options.clear()
        self._view.page.go("/")

    def fill_dd(self):
        """ metodo per riempire i menu a tendina"""

        # viene richiamato il model
        loc, date = self._model.get_loc_e_date()

        # popolo menu "location"
        for i in loc:
            self._view.ddLoc.options.append(ft.dropdown.Option(i))

        # popolo menu "anno"
        self._view.ddAnno.options = [ft.dropdown.Option(key) for key in date]

        # memorizzo i mesi di ogni anno
        self.mese1 = [ft.dropdown.Option(value) for value in date.get(self._view.ddAnno.options[0].key)]
        self.mese2 = [ft.dropdown.Option(value) for value in date.get(self._view.ddAnno.options[1].key)]

        # imposto che il primo valore inserito sia selezionato
        self._view.ddLoc.value = self._view.ddLoc.options[0].key
        self._view.ddAnno.value = str(self._view.ddAnno.options[0].key)

        # riempio gli altri menu a tendina in base alla location e l'anno selezionato
        self.fill_mese()
        self.fill_store()

    def fill_mese(self):
        """ metodo per riempire il menu "month" in base all'anno selezionato"""
        if self._view.ddAnno.value == str(self._view.ddAnno.options[0].key):
            self._view.ddMese.options = self.mese1
        if self._view.ddAnno.value == str(self._view.ddAnno.options[1].key):
            self._view.ddMese.options = self.mese2

        # imposto che il primo valore inserito sia selezionato
        self._view.ddMese.value = str(self._view.ddMese.options[0].key)

    def update_mese(self, e):
        """ metodo per aggiornare il menu "month" in base all'anno selezionato"""
        self.fill_mese()
        self._view.page.update()

    def fill_store(self):
        """ metodo per riempire il menu "Store" in base alla località selezionata"""
        # popolo il menu a tendina "store"
        store_dd = []
        n = self._model.get_negozi(self._view.ddLoc.value)
        for i in n:
            store_dd.append(ft.dropdown.Option(i))
        self._view.ddShop.options = store_dd

        # imposto che il primo valore inserito sia selezionato
        self._view.ddShop.value = self._view.ddShop.options[0].key

    def update_store(self, e):
        """ metodo per aggiornare il menu Store in base alla location selezionata """
        self.fill_store()
        self._view.page.update()

# ---------- PAGINA 1 ----------

    # 1TAB: ------------------------------------------------------------------------------------------
    def c1(self):
        """ metodo per generare il grafico 'monthly profit' """

        # viene richiamato il model
        m1 = self._model.get_andamento_profitto(self.loc, self.yy[-1])

        # proietto nel grafico l'andamento del profitto mensile ottenuto nell'anno selezionato
        y = np.arange(1, len(m1) + 1)
        self.view_active.axs2a.plot(y, m1, marker=".", label=f"{self.yy[-1]}")
        self.view_active.axs2a.set_title(f"MONTHLY PROFIT", fontdict={'size': 15, 'color': "indigo"})
        self.view_active.axs2a.legend(
            loc='upper left',  # <-- dove posizionare la legenda
            bbox_to_anchor=(1, 1),
            ncol=1,
            borderpad=1,  # <-- spazio nel contorno degli anni
            fontsize='x-small',
            borderaxespad=1,
            shadow=True
        )

    def c2(self):
        """ Metodo per ottenere alcuni indicatori"""

        # richiamo il model per ricavare il tot di negozi presenti nella location selezionata:
        n_store = len(self._model.get_negozi(self.loc))
        self.view_active.t1.value = f"TOTAL OF ALL {n_store} STORES"

        # proietto il risultato totale delle quantita vendute, dei ricavi e del profitto avuto nell'anno selezionato
        q, r, m = self._model.get_indicatori(self.loc, self.yy[-1])
        colonna = ft.Column([], spacing=6, alignment=ft.MainAxisAlignment.CENTER)
        for i in [f"${m:1.2f}", f"${r:1.2f}", f"{q} unit"]:
            colonna.controls.append(
                ft.Container(self.create_text2(f"{i}"),
                             bgcolor=ft.colors.WHITE,
                             width=145,
                             height=45,
                             alignment=ft.alignment.center,
                             border_radius=10,
                             border=ft.border.all(1, "black"),
                             ))
        self.view_active.c2.controls.append(colonna)

    def c3(self):
        """ metodo per ottenere il negozio che presenta il prodotto più redditizio"""

        ris = ft.Column([], alignment=ft.MainAxisAlignment.CENTER)
        # richiamo il model
        m2 = self._model.get_prodotto_most_redditizio(self.loc, self.yy[-1])

        # proietto il prodotto più venduto nel negozio X
        # con la sua relativa categoria di appartenenza e il valore del profitto ottenuto
        for k in m2:
            ris.controls.append(ft.Container(self.create_text2(f"{k}", align=ft.TextAlign.CENTER),
                                             width=120,
                                             alignment=ft.Alignment(0, 0)
                                             )
                                )

        self.view_active.c3.controls.append(ft.Container(ris, bgcolor="white",
                                                         width=190,
                                                         height=225,
                                                         alignment=ft.Alignment(0, 0),
                                                         border_radius=9,
                                                         border=ft.border.all(2, "blue800"),
                                                         )
                                            )

    # 2TAB ------------------------------------------------------------------------------------
    def c4(self):
        """ metodo per generare il grafico a barre 'categorie prodotti'"""

        q = []
        m = []
        # richiamo il model
        m3 = self._model.get_category(self.loc, self.yy[-1])
        # ricavo le quantità vendute e il profitto ottenuto per ogni categoria di prodotti
        for t, i in m3.items():
            q.append(i[0])
            m.append(i[1])

        x = np.arange(len(m3.keys()))
        width = 0.30  # larghezza delle barre
        multiplier = 0
        if len(self.yy) == 2:  # <-- nel caso viene selezionato un anno diverso per la stessa location allora le barre del grafico saranno sposate di 1
            multiplier = 1

        offset = width * multiplier

        # proietto nel grafico a barra il profitto annuale e le quantita vendute per ogni categoria di prodotti
        self.view_active.axs2b[0].bar(x + offset, q, width)
        self.view_active.axs2b[0].set_title('QTY SOLD', fontdict={'size': 14, 'color': "INDIGO"})
        self.view_active.axs2b[0].set_xticks(x + offset, m3.keys())
        self.view_active.axs2b[0].set_xlabel('category', fontdict={'size': 18,
                                                                   'color': "white"})  # <-- per aumentare lo spazio tra i due grafici

        self.view_active.axs2b[1].bar(x + offset, m, width)
        self.view_active.axs2b[1].set_title('TOT PROFIT', fontdict={'size': 14, 'color': "INDIGO"})
        self.view_active.axs2b[1].set_xticks(x + offset, m3.keys())

        self.view_active.fig2b.tight_layout()

    def c5(self):
        """ Metodo per generare la tabella 'prodotti' """

        # Imposto che inizialmente l'ordinamento si faccia in base alla prima colonna
        self.view_active.tabella21a.sort_column_index = 0
        # Richiamo il model
        m4 = self._model.get_lista_prodotti(self.loc, self.yy[-1])

        # Controllo se viene selezionato un anno diverso per la stessa location
        if len(self.yy) < 2:
            if len(self.view_active.tabella21a.columns) > 2:
                self.view_active.tabella21a.rows.clear()
                self.clear_table_columns(self.view_active.tabella21a)

            self.ppp = {}
            self.ppp = {t: (i[0], i[1], i[2]) for t, i in
                        m4.items()}  # Necessario per la stessa location con anno diverso
            self.aggiungi_colonne(self.view_active.tabella21a, self.yy[0])
            self.aggiungi_righe(m4, self.view_active.tabella21a, self.ppp, n_columns=2)
        elif len(self.yy) == 2:
            # Pulisco le righe della tabella
            self.view_active.tabella21a.rows.clear()
            self.aggiungi_colonne(self.view_active.tabella21a, self.yy[1])
            self.aggiungi_righe(m4, self.view_active.tabella21a, self.ppp, n_columns=2, anno=self.yy[0])

        # Imposto che la prima riga della colonna sia selezionata
        if self.view_active.tabella21a.rows:
            self.view_active.tabella21a.rows[0].selected = True

    def aggiungi_colonne(self, tabella, anno):
        """ Aggiunge le colonne per l'anno specificato """
        for tipo in ["QTY", "PROFIT"]:
            tabella.columns.append(
                ft.DataColumn(self.create_text1(f"{tipo} {anno}", "BLACK", weight=ft.FontWeight.BOLD),
                              on_sort=lambda e: self.ordine(e, tabella)
                              ))

    def aggiungi_righe(self, dati, tabella, dati_precedenti, n_columns=1, anno=None):
        """ Aggiunge righe alla tabella, con dati opzionali per l'anno precedente """
        for t, i in dati.items():
            # controllo se la tabella contiene inizialmente più di una colonna
            if n_columns > 1:
                celle = [
                    ft.DataCell(self.create_text2(f"{t}")),
                    ft.DataCell(self.create_text2(f"{i[0]}")),
                    ft.DataCell(self.create_text2(f"{int(i[1])}")),
                    ft.DataCell(self.create_text2(f"{float(i[2]):1.2f}")),
                ]
            else:
                celle = [
                    ft.DataCell(self.create_text2(f"{t}")),
                    ft.DataCell(self.create_text2(f"{int(i[0])}")),
                    ft.DataCell(self.create_text2(f"{float(i[1]):1.2f}")),
                ]

            if anno:
                # controllo se la tabella inizilmente conteneva una colonna
                if n_columns > 1:
                    celle.extend([
                        ft.DataCell(self.create_text2(f"{int(dati_precedenti.get(t)[1])}")),
                        ft.DataCell(self.create_text2(f"{float(dati_precedenti.get(t)[2]):1.2f}")),
                    ])
                else:
                    celle.extend([
                        ft.DataCell(self.create_text2(f"{int(dati_precedenti.get(t)[0])}")),
                        ft.DataCell(self.create_text2(f"{float(dati_precedenti.get(t)[1]):1.2f}")),
                    ])

            tabella.rows.append(
                ft.DataRow(cells=celle, selected=False, on_select_changed=lambda e: self.chkselect(e, tabella)))

    def chkselect(self, e, tabella):
        """ Metodo per selezionare una riga alla volta in una tabella specificata """

        # Imposto che nella tabella sia possibile selezionare solo una riga alla volta
        for row in tabella.rows:
            row.selected = False
        e.control.selected = not e.control.selected

        self._view.page.update()

    def ordine(self, e, tabella):
        """ Metodo per ordinare le tabelle in base alla colonna selezionata """

        # Aggiorno l'indice della colonna di ordinamento nel controllo genitore
        tabella.sort_column_index = e.column_index
        # Controllo se l'ordinamento è attualmente ascendente
        tabella.sort_ascending = not tabella.sort_ascending
        # Ordino le righe della tabella in base all'indice della colonna selezionata
        if e.column_index == 0:
            tabella.rows.sort(key=lambda x: x.cells[e.column_index].content.value, reverse=tabella.sort_ascending)

        # controllo quante colonne abbia la tabella
        # in base a ciò la seconda colonna subirà un ordinamento diverso
        if len(tabella.columns) == 4 or len(tabella.columns) == 6:
            if e.column_index == 0 or e.column_index == 1:
                tabella.rows.sort(key=lambda x: x.cells[e.column_index].content.value, reverse=tabella.sort_ascending)
            else:
                tabella.rows.sort(key=lambda x: float(x.cells[e.column_index].content.value),
                                  reverse=tabella.sort_ascending)
        elif len(tabella.columns) == 3 or len(tabella.columns) == 5:
            if e.column_index == 0 or e.column_index == 1:
                tabella.rows.sort(key=lambda x: x.cells[e.column_index].content.value, reverse=tabella.sort_ascending)
            else:
                tabella.rows.sort(key=lambda x: float(x.cells[e.column_index].content.value),
                                  reverse=tabella.sort_ascending)

        # Aggiorno la tabella
        tabella.update()
        self._view.page.update()

    def c6(self):
        """ metodo per generare il grafico 'andamento prodotto x' """

        # ricavo i valori della cella selezionata
        if self.p is None:
            for i in range(len(self.view_active.tabella21a.rows)):
                if self.view_active.tabella21a.rows[i].selected is True:
                    # inizializzo la variabile con il nominativo del prodotto selezionato
                    self.p = self.view_active.tabella21a.rows[i].cells[0].content.value
                    break  # aggiunto break per uscire dal for non appena viene trovato il valore true

        # richiamo il model:
        m5 = self._model.get_andamento_prodotto(self.loc, self.a1[-1], self.p)
        #  proietto nel grafico l'andamento del profitto mensile avuto nell'anno selezionato per il prodotto X
        y = np.arange(1, len(m5) + 1)
        self.view_active.axs2c.plot(y, m5, marker=".", label=f"{self.a1[-1]}")
        self.view_active.axs2c.set_title(f"TRENDS OF PRODUCT '{self.p}'", fontdict={'size': 11, 'color': "indigo"})
        self.view_active.axs2c.legend(
            loc='upper left',
            bbox_to_anchor=(1, 1),
            ncol=1,
            borderpad=1,
            fontsize='xx-small',
            borderaxespad=1,
            shadow=True
        )

    def aggiorna_grafico1(self, e):
        """ metodo per aggiornare il grafico 'andamento prodotto X' """
        t = None
        for i in range(len(self.view_active.tabella21a.rows)):
            if self.view_active.tabella21a.rows[i].selected is True:
                t = self.view_active.tabella21a.rows[i].cells[0].content.value
                break

        # controllo se il prodotto selezionato è diverso
        if t != self.p:
            # pulisco le variabili
            self.a1 = [int(self._view.ddAnno.value)]
            self.p = t
            self.clear_chart(self.view_active.axs2c)
            # avvio la funzione
            self.c6()
        else:
            # controllo se per lo stesso prodotto è stato selezionato un anno diverso
            if int(self._view.ddAnno.value) not in self.a1:
                self.a1.append(int(self._view.ddAnno.value))
                self.c6()
        self._view.page.update()

    # 3TAB -------------------------------------------------------------------------------

    def c7(self):
        """ Metodo per generare la tabella 'negozi' """

        # Imposto che inizialmente l'ordinamento si faccia in base alla prima colonna
        self.view_active.tabella21b.sort_column_index = 0
        # Richiamo il model
        m6 = self._model.get_lista_negozi(self.loc, self.yy[-1])

        # Controllo se viene selezionato un anno diverso per la stessa location
        if len(self.yy) < 2:
            if len(self.view_active.tabella21b.columns) > 2:
                self.view_active.tabella21b.rows.clear()
                self.clear_table_columns(self.view_active.tabella21b)
            self.sp = {}
            self.sp = {t: (i[0], i[1]) for t, i in m6.items()}  # Necessario per la stessa location con anno diverso
            self.aggiungi_colonne(self.view_active.tabella21b, self.yy[0])
            self.aggiungi_righe(m6, self.view_active.tabella21b, self.sp)
        elif len(self.yy) == 2:
            # Pulisco le righe della tabella
            self.view_active.tabella21b.rows.clear()
            self.aggiungi_colonne(self.view_active.tabella21b, self.yy[1])
            self.aggiungi_righe(m6, self.view_active.tabella21b, self.sp, anno=self.yy[0])

        # Imposto che la prima riga della colonna sia selezionata
        if self.view_active.tabella21b.rows:
            self.view_active.tabella21b.rows[0].selected = True

    def c8(self):
        """ metodo per generare il grafico 'andamento negozio x' """
        # ricavo i valori della cella selezionata
        if self.n is None:
            for i in range(len(self.view_active.tabella21b.rows)):
                if self.view_active.tabella21b.rows[i].selected is True:
                    # inizializzo la variabile con il nominativo del prodotto selezionato
                    self.n = self.view_active.tabella21b.rows[i].cells[0].content.value
                    break
        # richiamo il model
        m7 = self._model.get_andamento_negozio(self.n, self.a2[-1])
        #  proietto nel grafico l'andamento del profitto mensile avuto nell'anno selezionato per il negozio X
        y = np.arange(1, len(m7) + 1)
        self.view_active.axs2d.plot(y, m7, marker=".", label=f"{self.a2[-1]}")
        self.view_active.axs2d.set_title(f"TRENDS OF SHOP '{self.n}'", fontdict={'size': 11, 'color': "indigo"})
        self.view_active.axs2d.legend(
            loc='upper left',
            bbox_to_anchor=(1, 1),
            ncol=1,
            borderpad=1,  # <--spazio nel contorno degli anni
            fontsize='xx-small',
            borderaxespad=1,
            shadow=True
        )

    def aggiorna_grafico2(self, e):
        """ metodo per aggiornare il grafico 'andamento negozio X' """
        t = None
        for i in range(len(self.view_active.tabella21b.rows)):
            if self.view_active.tabella21b.rows[i].selected is True:
                t = self.view_active.tabella21b.rows[i].cells[0].content.value
                break
        # controllo se il negozio selezionato è diverso
        if t != self.n:
            # pulisco le variabili
            self.a2 = [int(self._view.ddAnno.value)]
            self.n = t
            self.clear_chart(self.view_active.axs2d)
            # avvio le funzioni
            self.c8()
        else:
            # controllo se per lo stesso negozio è stato selezionato un anno diverso
            if int(self._view.ddAnno.value) not in self.a2:
                self.a2.append(int(self._view.ddAnno.value))
                self.c8()

        self._view.page.update()

    def stock(self):
        """ metodo per ricavare lo stock di ogni prodotto nel negozio selezionato"""

        self.view_active.ris.controls.clear()
        # ricavo i valori della cella selezionata
        t = None
        for i in range(len(self.view_active.tabella21b.rows)):
            if self.view_active.tabella21b.rows[i].selected is True:
                t = self.view_active.tabella21b.rows[i].cells[0].content.value
                break

        # ricavo la quantità presente a fine luglio 2023 di ogni prodotto del negozio X
        s, q = self._model.get_rimanenze(self.loc, self.yy[-1], t)
        self.view_active.ris.controls.append(
            self.create_text1(f"{t} \n TOT STOCK = {int(sum(q))} unit:", "black", weight=ft.FontWeight.BOLD))
        for i in range(len(q)):
            self.view_active.ris.controls.append(
                self.create_text2(f"{s[i]} = {int(q[i])} unit", align=ft.TextAlign.CENTER))

    def aggiorna_button_stock(self, e):
        """ Pulsante per aggiornare lo stock relativo al negozio selezioanto nella tabella """
        self.stock()
        self._view.page.update()

    def update_page2(self, e):
        """ Aggiorna i dati della pagina 2 """
        self.load_page2()
        self._view.page.update()

    def clear_chart(self, chart):
        """ Pulisce un grafico specificato """
        chart.clear()

    def clear_table_columns(self, table):
        """ Pulisce le righe e le colonne della tabella """
        table.rows.clear()

        # calcolo il numero di colonne da non cancellare
        max_column_keep = 0
        if len(table.columns) == 5 or len(table.columns) == 3:
            max_column_keep = 1
        elif len(table.columns) == 6 or len(table.columns) == 4:
            max_column_keep = 2

        column_remove = len(table.columns) - max_column_keep
        # cancello n colonne
        for _ in range(column_remove):
            table.columns.pop()

    # ---------- PAGINA 2 ----------
    def controllo_input1(self):
        """ Metodo per controllora che siano stati inseriti valori accettabili """

        if not self.controlla_number(self.view_active.cf.value):
            self.msg_error("ERROR\nplease, enter a number\nfor CF")
        else:
            # memorizzo il valore inserito
            self.cf = float(self.view_active.cf.value)

        if not self.controlla_number(self.view_active.target.value):
            self.msg_error("ERROR\nplease, enter a number\nfor TARGET")
        else:
            self.target = float(self.view_active.target.value)

    def controlla_number(self, valore):
        """ metodo per valutare se è stato inserito un numero """
        try:
            float(valore)  # Prova a convertire in float
            return True
        except ValueError:
            return False  # Ritorna False se la conversione fallisce

    def c9(self):
        """ metodo per proiettare i risultati in forma grafica"""

        self.view_active.l3a.controls.append(
            ft.Text(f"--------------", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER))

        # controllo input:
        self.controllo_input1()

        # avvio calcolo MDC
        self._model.calcolo_mdc(self._view.ddShop.value, int(self._view.ddAnno.value), int(self._view.ddMese.value),
                                self.cf, self.target)

        # estrazione dei risultati
        name_prod, q, r, mixx = self._model.get_ris1()
        qbep, rbep, mds, ro = self._model.get_bep_e_mds()

        mdsq = sum(q) - qbep

        x1 = np.linspace(0, sum(q) + qbep)
        y = self._model.get_retta(self.cf)

        # proietto il risultato nel grafico
        self.view_active.axs3a.plot(x1, y[0], ls="-", linewidth=1, label='REVENUE')
        self.view_active.axs3a.plot(x1, y[1], ls="-", linewidth=1, label='CT')

        # imposto il colore tra due rette che si intersecano
        # questo permetterà di indetificare la zona di perdita e la zona di guadagno
        self.view_active.axs3a.fill_between(x1, y[0], y[1], where=(y[0] > y[1]), interpolate=True,
                                            color="g", alpha=0.3
                                            )
        self.view_active.axs3a.fill_between(x1, y[0], y[1], where=(y[0] <= y[1]), interpolate=True,
                                            color="r", alpha=0.3
                                            )
        # asse verticale che indica i costi fissi sostenuti
        self.view_active.axs3a.axhline(y=self.cf, ls='-', linewidth=1, label='CF', color='red')
        # il punto di intersezione
        self.view_active.axs3a.plot(qbep, rbep, marker="o", lw=3, label="BEP", color="r")

        # indicazioni aggiuntive se target è zero
        if self.target == 0:
            self.view_active.axs3a.plot([sum(q), sum(q)], [(sum(r) - ro), sum(r)], ls="--", linewidth=2, color="g",
                                        label=f'RO')
            self.view_active.l3a.controls.append(
                self.create_text2(f"the OPERATING INCOME is $ {ro:1.2f}", align=ft.TextAlign.CENTER))
            if ro > 0:
                self.view_active.axs3a.plot([sum(q), qbep], [0, 0], ls="--", linewidth=2, color="m", label=f'MDS')
                self.view_active.axs3a.plot([0, 0], [sum(r), rbep], ls="--", linewidth=2, color="m")
                self.view_active.l3a.controls.append(
                    self.create_text2(f"the MARGIN OF SAFETY is:\n{mds:1.2f} in sales e {int(mdsq)} in unit",
                                      align=ft.TextAlign.CENTER))

            self.view_active.l3a.controls.append(
                ft.Text(f"--------------", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER))

        # Impostazione del titolo e della leggenda
        self.view_active.axs3a.set_title(f"BREAK-EVEN CHART", fontdict={'size': 16, 'color': "INDIGO"})
        self.view_active.axs3a.legend(
            loc='upper left',
            bbox_to_anchor=(1, 1),
            ncol=1,
            borderpad=1,  # <--spazio nel contorno degli anni
            fontsize='x-small',
            borderaxespad=1,
            shadow=True
        )

        # Linee orizzontali e verticali per il BEP
        self.view_active.axs3a.hlines(y=[rbep, sum(r)], xmin=[0, 0], xmax=[qbep, sum(q)],
                                      color='lightgrey', linestyle='--', linewidth=0.5)
        self.view_active.axs3a.vlines(x=[qbep, sum(q)], ymin=[0, 0], ymax=[rbep, sum(r)],
                                      color='lightgrey', linestyle='--', linewidth=0.5)

        # impostazione dei valori sugli assi
        n1 = [0, int(sum(q))]
        n2 = [0, sum(r), self.cf]
        self.view_active.axs3a.set_xticks(n1)
        self.view_active.axs3a.set_yticks(n2, labels=[f"{i:1.2f}" for i in n2])
        self.view_active.axs3a.annotate('unit', xy=(1, 0), ha='left', va='top', xycoords='axes fraction', fontsize=13)
        self.view_active.axs3a.annotate('$', xy=(0, 1), xytext=(-15, 2), ha='left', va='top', xycoords='axes fraction',
                                        textcoords='offset points', fontsize=13)

    def c10(self):
        """ metodo per proiettare il mix(ideale) dei ricavi per ogni prodotto"""

        # richiamo il model
        name_prod, q, r, mixx = self._model.get_ris1()
        qbep, rbep, mds, ro = self._model.get_bep_e_mds()

        # controllo se il target sia diverso da zero
        if self.target == 0:
            # 1. viene mostrato il BEP
            self.view_active.l3a.controls.append(
                self.create_text2(f"SALES ${rbep:1.2f} are required to BREAK EVEN", align=ft.TextAlign.CENTER))
            self.view_active.l3a.controls.append(
                self.create_text2(f"The SALES of EACH TOYS must be:", align=ft.TextAlign.CENTER))
            for i in range(len(mixx)):
                self.view_active.l3a.controls.append(
                    self.create_text2(f"{name_prod[i]}: ${r[i]:1.2f} --> ${mixx[i]:1.2f}", align=ft.TextAlign.CENTER))

        elif self.target > 0:
            # 2. viene mostrato il profit target
            self.view_active.l3a.controls.clear()
            self.view_active.l3a.controls.append(
                self.create_text2(f"SALES ${rbep:1.2f} are required\nto make an OPERATING INCOME of ${self.target}",
                                  align=ft.TextAlign.CENTER))
            self.view_active.l3a.controls.append(
                self.create_text2("the SALES of EACH TOYS must be:", align=ft.TextAlign.CENTER))
            for i in range(len(mixx)):
                self.view_active.l3a.controls.append(
                    self.create_text2(f"{name_prod[i]}: ${r[i]:1.2f} --> ${mixx[i]:1.2f}", align=ft.TextAlign.CENTER))

    def update_page3(self, e):
        """ Aggiorna i dati della pagina 3 """
        self.load_page3()
        self._view.page.update()

    def controllo_input2(self):
        """ Metodo per controllare gli input inseriti """
        # Inizializza le variabili
        vqty, vpr, vcf = None, None, None

        if not self.controlla_number(self.view_active.vQty.value):  # controllo che venga inserito un numero
            self.msg_error("ERROR\nplease, enter a number between 0-100 for ΔQty")
            return None, None, None

        vqty = int(self.view_active.vQty.value)
        if not (0 <= vqty <= 100):  # controllo che il numero sia compreso tra 0 e 100
            self.msg_error("ERROR\nPlease, enter a number between 0-100 for Δqty")
            return None, None, None

        if not self.controlla_number(self.view_active.vPr.value):
            self.msg_error("ERROR\nplease, enter a number between 0-100 for ΔPr")
            return None, None, None
        vpr = int(self.view_active.vPr.value)
        if not (0 <= vpr <= 100):
            self.msg_error("ERROR\nPlease, enter a number between 0-100 for Δpr")
            return None, None, None

        if not self.controlla_number(self.view_active.vCF.value):
            self.msg_error("ERROR\nplease, enter a number\nfor ΔCF")
            return None, None, None
        vcf = int(self.view_active.vCF.value)

        return vqty, vpr, vcf

    def variazioni2(self, e):
        """ calcolo le variazioni apportate ad alcune variabili"""

        # pulisco la lista dove verrà visualizzato il risultato della simulazione
        self.view_active.l4a.controls.clear()

        # controllo i valori inseriti
        vqty, vpr, vcf = self.controllo_input2()
        if vqty is None and vpr is None and vcf is None:
            return
        # nel caso i valori non subiscono variazioni allora non viene avviato la simulazione
        if vqty == 0 and vpr == 0 and vcf == 0:
            return

        # avvio la simulazione
        self._model.simulazione(self.cf, vqty, vpr, vcf)

        # ricavo il risultato della simulazione
        self.ris = self._model.get_ris2()

        # controllo se la tupla di variazioni è contenuta nei risultati ottenuti
        if (vqty, vpr, vcf) not in self.ris.keys():
            self.view_active.l4a.controls.append(self.create_text2("RO decrease", align=ft.TextAlign.CENTER))
        else:
            self.view_active.l4a.controls.append(
                self.create_text2(f"RO increase of ${self.ris.get((vqty, vpr, vcf)):1.2f}", align=ft.TextAlign.CENTER))

        # proietto le soluzioni alternative trovate:
        self.view_active.l4a.controls.append(
            self.create_text2("other possible solutions are:", align=ft.TextAlign.CENTER))
        for t, i in self.ris.items():
            if (vqty, vpr, vcf) != t:
                self.view_active.l4a.controls.append(
                    self.create_text2(f"vqty={int(t[0])}%, vpr={int(t[1])}%, vcf={int(t[2])}\nro={i:1.2f}",
                                      align=ft.TextAlign.CENTER))

        self._view.page.update()

    def stampa(self, e):
        """ metodo per confermare di voler stampare il risultato della simulazione"""

        self.msg_print = ft.AlertDialog(title=self.create_text1("Please indicate the name\nyou wish to give to the file", "black"),
                                        content=ft.TextField(bgcolor="white"),
                                        actions=[ft.TextButton("CONFIRM",
                                                               style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: "indigo",
                                                                                           ft.ControlState.PRESSED: "indigo900"}
                                                                                    ),
                                                               on_click=self.action),
                                                 ft.TextButton("DELETE",
                                                               style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: "red",
                                                                                           ft.ControlState.PRESSED: "red900"}
                                                                                    ),
                                                               on_click=lambda e: self._view.page.close(self.msg_print)),
                                                 ],
                                        bgcolor="bluegrey300"
                                        )

        self._view.page.open(self.msg_print)

        self._view.page.update()

    def action(self, e):
        """ Metodo per avviare la stampa """

        self._view.page.close(self.msg_print)

        # estraggo i valori che devono essere stampati
        name_prod, q, r, mixx = self._model.get_ris1()
        qbep, rbep, mds, ro = self._model.get_bep_e_mds()

        # prendo il nome con cui l'utente vuole salvare il file
        name_file = self.msg_print.content.value

        # passo i valori da stampare e avvio la generazione del file PDF
        stampa = print_file(self.cf, self.target, name_file)
        stampa.generazione_pdf(name_prod, q, r, mixx, qbep, rbep, mds, ro, self.ris)

        # viene confermato il successo dell'operazione
        msg_conferma = ft.SnackBar(self.create_text1("The document has been saved successfully",
                                                     "white",
                                                     weight=ft.FontWeight.BOLD
                                                     ),
                                   bgcolor="blueblack"
                                   )
        self._view.page.open(msg_conferma)

        self._view.page.update()
