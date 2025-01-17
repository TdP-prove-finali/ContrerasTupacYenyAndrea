import flet as ft

import numpy as np
from model.stampa import printF

class Controller:
    def __init__(self, view, model):
        self._model = model
        self._view = view

        self._un = None
        self._pw = None

        self._mese1 = []
        self._mese2 = []

        self._loc=None
        self._yy=[]

        self.ppp={}
        self._p=None
        self._a1=[]

        self.sp={}
        self._n=None
        self._a2=[]

        self.cf=None
        self.target=None

    def getValore(self, line):
        line = line.rstrip('\n')
        word = line[line.index(':') + 1:]
        word = word.replace(" ", "")
        return word

    def login(self, e):
        """ metodo per verificare le credenziali di accesso """

        password = self._view._pag0._password.value
        username = self._view._pag0._username.value

        # estraggo i codici d'accesso dal file txt
        if self._un==None or self._pw==None:
            file = open("UI/codici.txt", "r")
            lines = file.readlines()
            for line in lines:
                if line.startswith('USERNAME'):
                    self._un = self.getValore(line)
                if line.startswith('PASSWORD'):
                    self._pw = self.getValore(line)
            file.close()

        # 1.controllo: password sbagliata
        if username == self._un and password != self._pw:
            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("LOGIN FAILED\nincorrect password", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",
            ))
            return

        # 2. controllo: username sbagliato
        elif username != self._un and password == self._pw:
            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("LOGIN FAILED\nincorrect username", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",

            ))
            return

        # 3. controllo: username e password sbagliati
        elif username != self._un and password != self._pw:
            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("LOGIN FAILED\nplease verify your credentials", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",
            ))
            return

        self._view._page.go("/page1")

        self._view._page.update()

    def changePage(self):
        """ metodo per cambiare la pagina """

        # utente viene indirizzato alla pagina HOME
        if self._view._page.route == "/page1":
            self._view._page.views.append(self._view._pag1)

        # utente indirizzato alla pagina ANALISI DATI
        if self._view._page.route == "/page2":
            self._view._page.views.append(self._view._pag2)

            # vengono inizializzati due variabili in base a quello selezionato nei menu a tendina
            self._yy=[int(self._view._ddAnno.value)]
            self._loc = self._view._ddLoc.value
            # le tabelle presenteranno inizialmente 3 colonne
            # per cui eventuali colonne aggiuntive verranno eliminate
            self._view._pag2._tabella21a.rows.clear()
            self._view._pag2._tabella21b.rows.clear()
            if len(self._yy) == 2:
                self._view._pag2._tabella21a.columns.pop(4)
                self._view._pag2._tabella21a.columns.pop(3)
                self._view._pag2._tabella21b.columns.pop(4)
                self._view._pag2._tabella21b.columns.pop(3)

            #viene inizializzato la variabile per il prodotto selezionato nella tabella prodotti
            self._a1=[]
            self._a2=[]

            self.c1()
            self.c2()
            self.c3()
            self.c4()
            self.c5()
            self.c6()
            self.c7()
            self.stock()

        # utente viene indirizzato alla pagina ANALISI CVP
        if self._view._page.route == "/page3":
            self._view._page.views.append(self._view._pag3)

            self.c8()
            self.c9()

        self._view._page.update()

    def fillDD(self):
        """ metodo per riempire i menu a tendina"""

        locDD=[]
        yyDD=[]
        mm = []

        # viene richiamato il model
        loc, date =self._model.getLOCeDATE()

        # si riempie il menu "location"
        for i in loc:
            locDD.append(ft.dropdown.Option(i))
        self._view._ddLoc.options = locDD

        # si riempie il menu "anno"
        for t, i in date.items():
            yyDD.append(ft.dropdown.Option(t))
            # per riempire il menu "mese" in base all'anno selezionato
            for k in range(len(i)):
                if i[k] not in mm:
                    mm.append(i[k])
                    self._mese1.append(ft.dropdown.Option(i[k]))
                else:
                    self._mese2.append(ft.dropdown.Option(i[k]))
        self._view._ddAnno.options = yyDD

    #1TAB: ------------------------------------------------------------------------------------------
    def c1(self):
        """ metodo per generare il grafico 'monthly profit' e ottenere alcuni indicatori"""

        # viene richiamato il model
        m1 = self._model.getAndamentoProfitto(self._loc, self._yy[-1])

        # proietto nel grafico l'andamento del profitto mensile avuto nell'anno selezionato
        y = np.arange(1, len(m1) + 1)
        self._view._pag2._axs2a.plot(y, m1, marker=".", label=f"{self._yy[-1]}")
        self._view._pag2._axs2a.set_title(f"MONTHLY PROFIT", fontdict={'size': 15, 'color': "indigo"})
        self._view._pag2._axs2a.legend(
            loc='upper left',       # <-- dove posizionare la legenda
            bbox_to_anchor=(1, 1),
            ncol=1,
            borderpad=1,  # <-- spazio nel contorno degli anni
            fontsize='x-small',
            borderaxespad=1,
            shadow=True
        )

        #richiamo il model per ricavare il tot di negozi presenti nella location selezionata:
        nStore=len(self._model.getNegozi(self._loc))
        self._view._pag2._txt0.content = ft.Text(f"TOTAL OF ALL {nStore} STORES",
                                  style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD, color="indigo900"),
                                  #text_align=ft.TextAlign.CENTER
                                  )

        #proietto il risultato totale delle quantita vendute, dei ricavi e del profitto avuto nell'anno selezionato
        q, r, m =self._model.getIndicatori(self._loc, self._yy[-1])
        colonna=ft.Column([],spacing=6, alignment=ft.MainAxisAlignment.CENTER)
        for i in [f"${m:1.2f}", f"${r:1.2f}", f"{q} unit"]:
            colonna.controls.append(
                ft.Container(
                    ft.Text(f"{i}", style=ft.TextStyle(color="BLACK", size=15, weight=ft.FontWeight.BOLD)),
                    bgcolor=ft.colors.WHITE,
                    width=145,
                    #height=45,
                    height=45,
                    alignment=ft.alignment.center,
                    border_radius=10,
                    border=ft.border.all(1, "black"),
                ))
        self._view._pag2._r21b.controls.append(colonna)


    def c2(self):
        """ metodo per ottenere il negozio che presenta il prodotto più redditizio"""

        ris = ft.Column([],alignment=ft.MainAxisAlignment.CENTER)
        # richiamo il model
        m2 = self._model.getProdottoMostRedditizio(self._loc, self._yy[-1])
        # proietto il prodotto più venduto nel negozio X con la sua relativa categoria di appartenenza e il valore del profitto ricevuto
        for k in m2:
            ris.controls.append(ft.Container(ft.Text(f"{k}", text_align=ft.TextAlign.CENTER, size=16), width=120, alignment=ft.Alignment(0,0)))
        self._view._pag2._r21c.controls.append(ft.Container(ris, bgcolor="white",
                                                                    width=190,
                                                                    height=225,
                                                                    alignment=ft.Alignment(0,0),
                                                                    border_radius=9,
                                                                    border=ft.border.all(2, "blue800"),
                                                                    ))

    #2TAB ------------------------------------------------------------------------------------
    def c3(self):
        """ metodo per generare il grafico a barre 'categorie prodotti'"""

        q=[]
        m=[]
        # richiamo il model
        m3 = self._model.getCategory1(self._loc, self._yy[-1])
        # ricavo le quantità vendute e il profitto ottenuto per ogni categoria di prodotti
        for t, i in m3.items():
            q.append(i[0])
            m.append(i[1])

        # proietto nel grafico a barra il profitto annuale per ogni categoria di prodotti
        x = np.arange(len(m3.keys()))
        width = 0.30  # the width of the bars
        multiplier = 0
        if len(self._yy) == 2: # <-- nel caso viene selezionato un anno diverso per la stessa location allora le barre del grafico saranno sposate di 1
            multiplier = 1

        offset = width * multiplier
        self._view._pag2._axs2b[0].bar(x + offset, q, width)
        self._view._pag2._axs2b[0].set_title('QTY SOLD',fontdict={'size': 14, 'color': "INDIGO"})
        self._view._pag2._axs2b[0].set_xticks(x + offset, m3.keys())
        self._view._pag2._axs2b[0].set_xlabel('category',fontdict={'size': 18, 'color': "white"}) # <-- per poter dare più spazio tra i due grafici

        self._view._pag2._axs2b[1].bar(x + offset, m, width)
        self._view._pag2._axs2b[1].set_title('TOT PROFIT',fontdict={'size': 14, 'color': "INDIGO"})
        self._view._pag2._axs2b[1].set_xticks(x + offset, m3.keys())

        self._view._pag2._fig2b.tight_layout()

    def c4(self):
        """ metodo per generare la tabella 'prodotti' """

        # imposto che inizialmente l'ordinamento si faccia in base alla prima colonna
        self._view._pag2._tabella21a.sort_column_index=0
        # richiamo il model
        m4 = self._model.getListaProdotti(self._loc, self._yy[-1])

        # controllo se viene selezionato un anno diverso per la stessa location
        # 1. viene selezionato location e anno diversi da quelli precedentemente registrati
        if len(self._yy) < 2:
            self.ppp={} # <--- mi serve nel caso in cui venga selezionato un anno diverso per la stessa location
            # aggiungo due colonne alla tabella per l'anno selezionato
            self._view._pag2._tabella21a.columns.append(
                ft.DataColumn(ft.Text(f"QTY {self._yy[0]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine1))
            self._view._pag2._tabella21a.columns.append(
                ft.DataColumn(ft.Text(f"PROFIT {self._yy[0]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine1))

            # popolo la tabella
            for t, i in m4.items():
                self.ppp.update({t:(i[0],i[1])})
                self._view._pag2._tabella21a.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{t}", size=16)),
                        ft.DataCell(ft.Text(f"{int(i[0])}", size=16)),
                        ft.DataCell(ft.Text(f"{float(i[1]):1.2f}", size=16)),
                    ],
                    selected=False,
                    on_select_changed=self.chkselect1
                ))
        # 2. viene selezionato per la stessa location un anno diverso
        elif len(self._yy) == 2:
            # pulisco le righe della tabella per aggiungere altre colonne alla tabella
            self._view._pag2._tabella21a.rows.clear()
            # aggiungo due colonne alla tabella per l'anno selezionato
            self._view._pag2._tabella21a.columns.append(
                ft.DataColumn(ft.Text(f"QTY {self._yy[1]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine1))
            self._view._pag2._tabella21a.columns.append(
                ft.DataColumn(ft.Text(f"PROFIT {self._yy[1]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine1))

            # popolo la nuova tabella
            for t, i in m4.items():
                self._view._pag2._tabella21a.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{t}", size=16)),
                        ft.DataCell(ft.Text(f"{int(self.ppp.get(t)[0])}", size=16)),
                        ft.DataCell(ft.Text(f"{float(self.ppp.get(t)[1]):1.2f}", size=16)),
                        ft.DataCell(ft.Text(f"{int(i[0])}", size=16)),
                        ft.DataCell(ft.Text(f"{float(i[1]):1.2f}", size=16)),
                    ],
                    selected=False,
                    on_select_changed=self.chkselect1
                ))

        # imposto che la prima riga della colonna sia selezionata
        for i in range(len(self._view._pag2._tabella21a.rows)):
            self._view._pag2._tabella21a.rows[0].selected = True


    def c5(self):
        """ metodo per generare il grafico 'andamento prodotto x' """
        self._a1.append(int(self._view._ddAnno.value))

        # ricavo i valori della cella selezionata
        for i in range(len(self._view._pag2._tabella21a.rows)):
            if self._view._pag2._tabella21a.rows[i].selected == True:
                # inizializzo la variabile con il nominativo del prodotto selezionato
                self._p = self._view._pag2._tabella21a.rows[i].cells[0].content.value

                #richiamo il model:
                m5=self._model.getAndamentoProdotto(self._loc, self._a1[-1], self._p)
                #  proietto nel grafico l'andamento del profitto mensile avuto nell'anno selezionato per il prodotto X
                y = np.arange(1, len(m5) + 1)
                self._view._pag2._axs2c.plot(y, m5, marker=".", label=f"{self._a1[-1]}")
                self._view._pag2._axs2c.set_title(f"TRENDS OF PRODUCT '{self._p}'", fontdict={'size': 11, 'color': "indigo"})
                self._view._pag2._axs2c.legend(
                    loc='upper left',
                    bbox_to_anchor=(1, 1),
                    ncol=1,
                    borderpad=1,
                    fontsize='xx-small',
                    borderaxespad=1,
                    shadow=True
                )

    def aggiornaGrafico1(self, e):
        """ metodo per aggiornare il grafico 'andamento prodotto X' """

        for i in range(len(self._view._pag2._tabella21a.rows)):
            if self._view._pag2._tabella21a.rows[i].selected == True:
                t = self._view._pag2._tabella21a.rows[i].cells[0].content.value

                # controllo se il prodotto selezionato è diverso
                if t != self._p:
                    self._a1=[]
                    self._view._pag2._axs2c.clear()
                    self.c5()
                    self._view._pag2._chart2c.update()
                elif t==self._p:
                    # controllo se per lo stesso prodotto è stato selezionato un anno diverso
                    if int(self._view._ddAnno.value) not in self._a1:
                        self.c5()
                        self._view._pag2._chart2c.update()

        self._view._page.update()


    def chkselect1(self, e):
        """ metodo per selezionare una riga alla volta"""

        # imposto che nella tabella sia possibile selezionare solo un prodotto alla volta
        for i in range(len(self._view._pag2._tabella21a.rows)):
            self._view._pag2._tabella21a.rows[i].__setattr__("selected", False)
        e.control.selected = not e.control.selected

        self._view._page.update()


    def ordine1(self, e):
        """ metodo per ordinare le tabelle dei prodotti e dei negozi in base alla colonna selezionata"""

        e.control.parent.__setattr__("sort_column_index", e.column_index)

        # Toggle the sort (ascending / descending)
        if e.control.parent.sort_ascending:
            e.control.parent.__setattr__("sort_ascending", False)
        else:
            e.control.parent.__setattr__("sort_ascending", True)

        # Sort the table rows according above

        if e.column_index==0:
            e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value, reverse=e.control.parent.sort_ascending)
        else:
            e.control.parent.rows.sort(key=lambda x: float(x.cells[e.column_index].content.value), reverse=e.control.parent.sort_ascending)


        # aggiornare la tabella
        e.control.parent.update()

        self._view._page.update()

    # 3TAB -------------------------------------------------------------------------------
    def c6(self):
        """ metodo per generare la tabella 'negozi' """

        # imposto che inizialmente l'ordinamento si faccia in base alla prima colonna
        self._view._pag2._tabella21b.sort_column_index=0

        # richiamo il model
        m6=self._model.getListaNegozi(self._loc, self._yy[-1])
        # controllo se viene selezionato un anno diverso per la stessa location
        # 1. viene selezionato location e anno diversi da quelli precedentemente registrati
        if len(self._yy) < 2:
            self.sp={} # <--- mi serve nel caso in cui venga selezionato un anno diverso per la stessa location
            # aggiungo due colonne alla tabella per l'anno selezionato
            self._view._pag2._tabella21b.columns.append(
                ft.DataColumn(ft.Text(f"QTY {self._yy[0]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine2))
            self._view._pag2._tabella21b.columns.append(
                ft.DataColumn(ft.Text(f"PROFIT {self._yy[0]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine2))
            # ricavo le quantità vendute e il profitto ottenuto per ogni categoria di prodotti
            for t, i in m6.items():
                self.sp.update({t: (i[0], i[1])})
                # popolo la tabella
                self._view._pag2._tabella21b.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{t}", size=16)),
                        ft.DataCell(ft.Text(f"{int(i[0])}", size=16)),
                        ft.DataCell(ft.Text(f"{float(i[1]):1.2f}", size=16)),
                    ],
                    selected=False,
                    on_select_changed=self.chkselect2
                ))

        # 2. viene selezionato per la stessa location un anno diverso
        elif len(self._yy) == 2:
            # pulisco le righe della tabella per aggiungere altre colonne alla tabella
            self._view._pag2._tabella21b.rows.clear()
            # aggiungo due colonne alla tabella per l'anno selezionato
            self._view._pag2._tabella21b.columns.append(
                ft.DataColumn(ft.Text(f"QTY {self._yy[1]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine2))
            self._view._pag2._tabella21b.columns.append(
                ft.DataColumn(ft.Text(f"PROFIT {self._yy[1]}", color="indigo", size=18, text_align=ft.TextAlign.CENTER),on_sort=self.ordine2))

            # popolo la nuova tabella
            for t, i in m6.items():
                self._view._pag2._tabella21b.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{t}", size=16)),
                        ft.DataCell(ft.Text(f"{int(self.sp.get(t)[0])}", size=16)),
                        ft.DataCell(ft.Text(f"{float(self.sp.get(t)[1])}", size=16)),
                        ft.DataCell(ft.Text(f"{int(i[0])}", size=16)),
                        ft.DataCell(ft.Text(f"{float(i[1]):1.2f}", size=16)),
                    ],
                    selected=False,
                    on_select_changed=self.chkselect2
                ))

        # imposto che la prima riga della colonna sia selezionata
        for i in range(len(self._view._pag2._tabella21b.rows)):
            self._view._pag2._tabella21b.rows[0].selected=True


    def c7(self):
        """ metodo per generare il grafico 'andamento negozio x' """
        # ricavo i valori della cella selezionata
        self._a2.append(int(self._view._ddAnno.value))
        for i in range(len(self._view._pag2._tabella21b.rows)):
            if self._view._pag2._tabella21b.rows[i].selected == True:
                # inizializzo la variabile con il nominativo del prodotto selezionato
                self._n = self._view._pag2._tabella21b.rows[i].cells[0].content.value
                # richiamo il model
                m7 = self._model.getAndamentoNegozio(self._n, self._a2[-1])
                #  proietto nel grafico l'andamento del profitto mensile avuto nell'anno selezionato per il negozio X
                y = np.arange(1, len(m7) + 1)
                self._view._pag2._axs2d.plot(y, m7, marker=".", label=f"{self._a2[-1]}")
                self._view._pag2._axs2d.set_title(f"TRENDS OF SHOP '{self._n}'", fontdict={'size': 11, 'color': "indigo"})
                self._view._pag2._axs2d.legend(
                    loc='upper left',
                    bbox_to_anchor=(1, 1),
                    ncol=1,
                    borderpad=1,  # <--spazio nel contorno degli anni
                    fontsize='xx-small',
                    borderaxespad=1,
                    shadow=True
                )

    def aggiornaGrafico2(self, e):
        """ metodo per aggiornare il grafico 'andamento negozio X' """
        for i in range(len(self._view._pag2._tabella21b.rows)):
            if self._view._pag2._tabella21b.rows[i].selected == True:
                t = self._view._pag2._tabella21b.rows[i].cells[0].content.value
                # controllo se il negozio selezionato è diverso
                if t != self._n:
                    self._a2 = []
                    self._view._pag2._axs2d.clear()
                    self.c7()
                    self._view._pag2._chart2d.update()
                elif t == self._n:
                    # controllo se per lo stesso negozio è stato selezionato un anno diverso
                    if int(self._view._ddAnno.value) not in self._a2:
                        self.c7()
                        self._view._pag2._chart2d.update()

        self._view._page.update()

    def chkselect2(self, e):
        """ metodo per selezionare una riga alla volta"""

        # imposto che nella tabella sia possibile selezionare solo un negozio alla volta
        for i in range(len(self._view._pag2._tabella21b.rows)):
            self._view._pag2._tabella21b.rows[i].__setattr__("selected", False)

        e.control.selected = not e.control.selected

        self._view._page.update()

    def stock(self):
        """ metodo per ricavare lo stock di ogni prodotto nel negozio selezionato"""

        self._view._pag2._ris.controls.clear()
        # ricavo i valori della cella selezionata
        for i in range(len(self._view._pag2._tabella21b.rows)):
            if self._view._pag2._tabella21b.rows[i].selected == True:
                t = self._view._pag2._tabella21b.rows[i].cells[0].content.value
                # ricavo la quantità presente a fine luglio 2023 di ogni prodotto del negozio X
                s, q = self._model.getRimanenze(self._loc, self._yy[-1], t)
                self._view._pag2._ris.controls.append(ft.Text(f"{t} \n TOT STOCK = {int(sum(q))} unit:", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=17, weight=ft.FontWeight.BOLD)))
                for i in range(len(q)):
                    self._view._pag2._ris.controls.append(ft.Text(f"{s[i]} = {int(q[i])} unit", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=16)))

    def aggiornaButtonStock(self, e):
        self.stock()
        self._view._page.update()


    def ordine2(self, e):
        """ metodo per ordinare le tabelle dei prodotti e dei negozi in base alla colonna selezionata"""

        e.control.parent.__setattr__("sort_column_index", e.column_index)

        # Toggle the sort (ascending / descending)
        if e.control.parent.sort_ascending:
            e.control.parent.__setattr__("sort_ascending", False)
        else:
            e.control.parent.__setattr__("sort_ascending", True)

        # Sort the table rows according above
        if e.column_index == 0:
            e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value,
                                       reverse=e.control.parent.sort_ascending)
        else:
            e.control.parent.rows.sort(key=lambda x: float(x.cells[e.column_index].content.value),
                                       reverse=e.control.parent.sort_ascending)



        # aggiornare la tabella
        e.control.parent.update()
        self._view._page.update()


    def update(self, e):
        """ metodo per aggiornare la pagina """

        if self._view._page.route == "/page2":

            # controllo se viene selezionato una località diversa dalla precedente
            if self._view._ddLoc.value != self._loc:
                # inizializzo la variabile con la nuova località
                self._loc = self._view._ddLoc.value
                # pulisco la prima TAB
                self._view._pag2._axs2a.clear()
                self._view._pag2._r21b.controls.clear()
                self._view._pag2._r21c.controls.clear()
                # pulisco la seconda TAB
                self._view._pag2._axs2b[0].clear()
                self._view._pag2._axs2b[1].clear()
                self._view._pag2._tabella21a.rows.clear()
                self._p=None

                #pulisco la terza TAB
                self._view._pag2._tabella21b.rows.clear()
                self._n=None

                # cancello eventuali colonne aggiuntive
                if len(self._yy) == 2:
                    self._view._pag2._tabella21a.columns.pop(4)
                    self._view._pag2._tabella21a.columns.pop(3)
                    self._view._pag2._tabella21b.columns.pop(4)
                    self._view._pag2._tabella21b.columns.pop(3)

                self._view._pag2._tabella21a.columns.pop(2)
                self._view._pag2._tabella21a.columns.pop(1)
                self._view._pag2._tabella21b.columns.pop(2)
                self._view._pag2._tabella21b.columns.pop(1)

                self._yy=[]

            if int(self._view._ddAnno.value) not in self._yy:
                self._yy.append(int(self._view._ddAnno.value))
                self._a1 = []
                self._a2 = []

                self.c1()
                self._view._pag2._chart2a.update()
                self.c2()
                self.c3()
                self._view._pag2._chart2b.update()
                self.c4()
                # pulisco il grafico andamento prodotto X
                self._view._pag2._axs2c.clear()
                self.c5()
                self._view._pag2._chart2c.update()

                self.c6()

                # pulisco il grafico andamento negozio X
                self._view._pag2._axs2d.clear()
                self.c7()
                self._view._pag2._chart2d.update()

                self.stock()

        if self._view._page.route == "/page3":
            self._view._pag3._l3a.controls.clear()

            self._view._pag3._axs3a.clear()
            self.c8()
            self._view._pag3._chart3a.update()
            self.c9()

        self._view._page.update()


    def fillMese(self, e):
        """ metodo per riempire il menu "month" in base all'anno selezionato"""
        if self._view._ddAnno.value == '2022':
            self._view._ddMese.options = self._mese1
        if self._view._ddAnno.value == '2023':
            self._view._ddMese.options = self._mese2

        self._view._page.update()

    def fillShop(self, e):
        """ metodo per riempire il menu "shop" in base alla località selezionata"""
        negDD=[]
        loc=self._view._ddLoc.value
        n=self._model.getNegozi(loc)
        for i in n:
            negDD.append(ft.dropdown.Option(i))
        self._view._ddShop.options = negDD

        self._view._page.update()

    def controlloInput(self):
        try:
            self.cf = float(self._view._pag3._cf.value)
        except ValueError as e:  # <--- se inserisco un carattere

            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("ERROR\nplease, enter a number", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",
            ))
        except Exception as err:  # <--- se non inserisco nulla
            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("ERROR\nplease, enter a number", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",
            ))

        try:
            self.target = float(self._view._pag3._target.value)
        except ValueError as e:
            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("ERROR\nplease, enter a number", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",
            ))
        except Exception as err:
            # visualizzero eventuali messaggi di errore
            self._view._page.open(ft.AlertDialog(
                content=ft.Text("ERROR\nplease, enter a number", text_align=ft.TextAlign.CENTER),
                content_text_style=ft.TextStyle(color="white",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                letter_spacing=1
                                                ),
                bgcolor="deeporange400",
            ))

    def c8(self):
        """ metodo per proiettare i risultati nell'analisi CVP in forma grafica"""

        self._view._pag3._l3a.controls.append(
            ft.Text(f"--------------", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER))

        #controllo input:
        self.controlloInput()

        # avvio la simulazione
        self._model.simula(self._view._ddShop.value, int(self._view._ddAnno.value), int(self._view._ddMese.value), self.cf, self.target)

        Pname, q, r, mixx = self._model.getRis()
        qbep, rbep, mds, ro = self._model.getBEPeMDS()

        mdsq = sum(q)-qbep

        x1 = np.linspace(0, sum(q) + qbep)
        y = self._model.getRetta()
        # proietto il risultato nel grafico
        self._view._pag3._axs3a.plot(x1, y[0], ls="-", linewidth=1, label='REVENUE')
        self._view._pag3._axs3a.plot(x1, y[1], ls="-", linewidth=1, label='CT')

        # imposto il colore tra due rette che si intersecano
        # questo permetterà di indetificare la zona di perdita e la zona di guadagno
        self._view._pag3._axs3a.fill_between(x1, y[0], y[1],
                                             where=(y[0] > y[1]),
                                             interpolate=True,
                                             color="g",
                                             alpha=0.3
                                             )
        self._view._pag3._axs3a.fill_between(x1, y[0], y[1],
                                             where=(y[0] <= y[1]),
                                             interpolate=True,
                                             color="r",
                                             alpha=0.3
                                             )
        # asse verticale che indica i costi fissi sostenuti
        self._view._pag3._axs3a.axhline(y=self.cf, ls='-', linewidth=1, label='CF', color='red')
        # il punto di intersezione
        self._view._pag3._axs3a.plot(qbep, rbep, marker="o", lw=3, label="BEP", color="r")

        # se target è uguale a zero allora si aggiungeranno altre indicazioni
        if self.target == 0:
            self._view._pag3._axs3a.plot([sum(q), sum(q)], [(sum(r)-ro), sum(r)], ls="--", linewidth=2, color="g", label=f'RO')
            self._view._pag3._l3a.controls.append(ft.Text(f"the PROFIT is {ro:1.2f} in sales", size=17, text_align=ft.TextAlign.CENTER))
            if ro > 0:
                self._view._pag3._axs3a.plot([sum(q), qbep], [0, 0], ls="--", linewidth=2, color="m", label=f'MDS')
                self._view._pag3._axs3a.plot([0, 0], [sum(r), rbep], ls="--", linewidth=2, color="m")
                self._view._pag3._l3a.controls.append(ft.Text(f"the MARGIN OF SAFETY is:\n{mds:1.2f} in sales e {int(mdsq)} in unit", size=17, text_align=ft.TextAlign.CENTER))

            self._view._pag3._l3a.controls.append(
                ft.Text(f"--------------", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER))

        self._view._pag3._axs3a.set_title(f"BREAK-EVEN CHART", fontdict={'size': 15, 'color': "INDIGO"})
        self._view._pag3._axs3a.legend(
            loc='upper left',
            bbox_to_anchor=(1, 1),
            ncol=1,
            borderpad=1,  # <--spazio nel contorno degli anni
            fontsize='x-small',
            borderaxespad=1,
            shadow=True
        )

        self._view._pag3._axs3a.hlines(y=[rbep, sum(r)], xmin=[0, 0],
                                        xmax=[qbep, sum(q)], color='lightgrey',
                                        linestyle='--', linewidth=0.5)
        self._view._pag3._axs3a.vlines(x=[qbep, sum(q)], ymin=[0, 0], ymax=[rbep, sum(r)], color='lightgrey', linestyle='--',
                                           linewidth=0.5)

        # imposto i valori che si visualizzeranno negli assi
        n1 = [0, int(sum(q))]
        n2 = [0, sum(r), self.cf]
        self._view._pag3._axs3a.set_xticks(n1)
        self._view._pag3._axs3a.set_yticks(n2, labels=[f"{i:1.2f}" for i in n2])
        self._view._pag3._axs3a.annotate('unit', xy=(1, 0), ha='left', va='top', xycoords='axes fraction', fontsize=14)
        self._view._pag3._axs3a.annotate('$', xy=(0, 1), xytext=(-15,2), ha='left', va='top', xycoords='axes fraction',
                     textcoords='offset points', fontsize=14)

    def c9(self):
        """ metodo per proiettare il mix(ideale) dei ricavi per ogni prodotto"""

        #richiamo il model
        Pname, q, r, mixx = self._model.getRis()
        qbep, rbep, mds, ro = self._model.getBEPeMDS()

        # controllo se il target sia diverso da zero
        # 1. viene mostrato il BEP
        if self.target==0:
            self._view._pag3._l3a.controls.append(ft.Text(f"SALES ${rbep:1.2f} are required to BREAK EVEN", size=16, text_align=ft.TextAlign.CENTER))
            self._view._pag3._l3a.controls.append(ft.Text(
                f"The SALES of EACH TOYS must be:", size=16, text_align=ft.TextAlign.CENTER))
            for i in range(len(mixx)):
                self._view._pag3._l3a.controls.append(ft.Text(f"{Pname[i]}: ${r[i]:1.2f} --> ${mixx[i]:1.2f}", size=16, text_align=ft.TextAlign.CENTER))
        # 2. viene mostrato il profit target
        elif self.target > 0:
            self._view._pag3._l3a.controls.clear()
            self._view._pag3._l3a.controls.append(
                ft.Text(f"--------------", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="transparent"))
            self._view._pag3._l3a.controls.append(ft.Text(
                f"SALES ${rbep:1.2f} are required\nto make a PROFIT of ${self.target}", size=16, text_align=ft.TextAlign.CENTER))
            self._view._pag3._l3a.controls.append(ft.Text(
                f"the SALES of EACH TOYS must be:", size=16, text_align=ft.TextAlign.CENTER))
            for i in range(len(mixx)):
                self._view._pag3._l3a.controls.append(ft.Text(f"{Pname[i]}: ${r[i]:1.2f} --> ${mixx[i]:1.2f} ", size=16, text_align=ft.TextAlign.CENTER))

        self._view._pag3._l3a.controls.append(
            ft.Text(f"--------------", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER,
                    color="transparent"))


    def stampa(self, e):
        """ metodo per confermare di voler stampare il risultato della simulazione in forma tabellare"""

        self.alertDialog=ft.AlertDialog(title=ft.Text("Please indicate the name\nyou wish to give to the file", text_align=ft.TextAlign.CENTER),
                                             content=ft.TextField(bgcolor="white"),
                                             actions=[
                                                 ft.TextButton("CONFIRM",
                                                               style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: "indigo",
                                                                                           ft.ControlState.PRESSED: "indigo900"}
                                                                                    ),
                                                               on_click=self.action),
                                                 ft.TextButton("DELETE",style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: "red",
                                                                                           ft.ControlState.PRESSED: "red900"}), on_click=self.action),
                                             ],
                                        bgcolor="bluegrey300"
                                        )
        self._view._page.open(self.alertDialog)


        self._view._page.update()

    def action(self, e):
        self._view._page.close(self.alertDialog)

        if e.control.text=="CONFIRM":
            Pname, q, r, mixx = self._model.getRis()
            qbep, rbep, mds, ro = self._model.getBEPeMDS()

            #prendo il nome con cui l'utente vuole salvare il file
            nameFile=self.alertDialog.content.value
            self._view._page.snack_bar = ft.SnackBar(ft.Text("The document has been saved successfully", style=ft.TextStyle(size=17, color="white", weight=ft.FontWeight.BOLD), text_align=ft.TextAlign.CENTER), bgcolor="blueblack")
            self._view._page.snack_bar.open = True

            printF(self.cf, self.target, Pname, q, r, mixx, qbep, rbep, mds, ro, nameFile)

        self._view._page.update()

