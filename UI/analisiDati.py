import flet as ft

from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class Page2(ft.View):
    def __init__(self, page: ft.Page, controller, buttons):
        super(Page2, self).__init__(
            route="/page2",
            bgcolor="indigo500"
        )
        self.page = page
        self._controller = controller
        self.buttons = buttons

        # Creazione pulsanti
        bt1 = self.create_icon_button(ft.icons.UPDATE, "UPDATE PAGE", self._controller.update_page2, "green", "white")
        bt2 = self.create_button("UPDATE CHART", self._controller.aggiorna_grafico1)
        bt3 = self.create_button("UPDATE CHART", self._controller.aggiorna_grafico2)
        bt4 = self.create_button("STOCK 09/2023\nOF THE STORE SELECTED", self._controller.aggiorna_button_stock)

        # Creazione grafici:
        # 1. GRAFICO SULL'ANDAMENTO DEL PROFITTO
        self.fig2a, self.axs2a = plt.subplots(1, 1, figsize=(6, 3))
        box = self.axs2a.get_position()
        self.axs2a.set_position([box.x0, box.y0, box.width * 0.90, box.height])
        self.chart2a = MatplotlibChart(self.fig2a, expand=True)

        # 2.GRAFICO A BARRA PER LE CATEGORIE
        self.fig2b, self.axs2b = plt.subplots(2, 1, figsize=(5.5, 4.4))
        self.chart2b = MatplotlibChart(self.fig2b, expand=True)

        # 3.GRAFICO ANDAMENTO DEL PRODOTTO X
        self.fig2c, self.axs2c = plt.subplots(1, 1, figsize=(7, 1.8))
        box = self.axs2c.get_position()
        self.axs2c.set_position([box.x0, box.y0, box.width * 0.9, box.height])
        self.chart2c = MatplotlibChart(self.fig2c, expand=True)

        # 4.GRAFICO ANDAMENTO DEL NEGOZIO X
        self.fig2d, self.axs2d = plt.subplots(1, 1, figsize=(7, 1.8))
        pos = self.axs2d.get_position()
        self.axs2d.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
        self.chart2d = MatplotlibChart(self.fig2d, expand=True)

        # Creazione tabelle
        # 1.Tabella Prodotti
        self.tabella21a = self.create_table("PRODUCT", n_column=2)
        # 2. Tabella Negozi
        self.tabella21b = self.create_table("STORE ")

        # Creazione titolo box
        self.t1 = self.create_text2("")
        t2 = self.create_text2("STORE WITH THE MOST PROFITABLE PRODUCT")
        t3 = self.create_text2("PRODUCTS BY CATEGORY")
        t4 = self.create_text2("LIST OF ALL PRODUCTS")
        t5 = self.create_text2("LIST OF ALL STORES")

        # contenitori x i risultati ottenuti
        c1 = self.create_column(['PROFIT', 'REVENUE', 'UNITS SOLD'])
        self.c2 = ft.Row([], spacing=2)  # riga contenente la qty totale, il ricavo totale e il profitto totale ottenuto
        rw1 = ft.Row([c1, self.c2], alignment=ft.MainAxisAlignment.CENTER)  # <-- per centrare i contenutI all'interno delle righe

        self.c3 = ft.Row([], alignment=ft.MainAxisAlignment.CENTER)  # riga contenente il negozio con il prodotto più redittizio

        c4 = self.create_container1(self.scroll_y([self.tabella21a]), 150)
        c5 = self.create_container1(self.chart2c, 228)

        c6 = self.create_container1(self.scroll_y([self.tabella21b]), 150)
        c7 = self.create_container1(self.chart2d, 228)

        self.ris = ft.ListView([], expand=True, padding=0)  # lista contenente lo stock
        r = self.create_container1(self.scroll_y([self.ris]), 420)

        # Creazione dei box
        # OVERVIEW
        cl1 = self.box(self.scroll_y([self.chart2a]), 680, 500)  # <-- 1box=1col
        bx2 = self.box(self.scroll_y([self.t1, rw1]), 480, 200)  # <-- 2box
        bx3 = self.box(self.scroll_y([t2, self.c3]), 480, 290)  # <-- 3box
        cl2 = ft.Container(self.scroll_y([bx2, bx3]), height=500)  # <-- 2col
        # PRODUCT ----------------------------------------------------------------------------------------------
        cl3 = self.box(self.scroll_y([t3, self.chart2b]), 510, 500)  # <-- 1col
        cl4 = self.box(self.scroll_y([t4, c4, bt2, c5]), 960, 500)  # <-- 2col
        # NEGOZI
        cl5 = self.box(self.scroll_y([t5, c6, bt3, c7]), 960, 500)  # <-- 1col
        cl6 = self.box(ft.Column([bt4, r]), 330, 500)  # <-- 2col

        # --------------------------------------------------------------------------
        # Creazione delle schede
        result = ft.Tabs(selected_index=0,
                         animation_duration=300,
                         label_color="white",
                         label_text_style=ft.TextStyle(size=17,
                                                       weight=ft.FontWeight.BOLD),
                         tabs=[
                             ft.Tab(text="OVERVIEW",
                                    content=self.container_body([cl1, cl2])
                                    ),
                             ft.Tab(text="PRODUCTS",
                                    content=self.container_body([cl3, cl4])
                                    ),
                             ft.Tab(text="STORES",
                                    content=self.container_body([cl5, cl6])
                                    ),
                         ],
                         tab_alignment=ft.TabAlignment.CENTER,
                         expand=True
                         )

        self.controls = [
            self.header(),
            self.info_container(self.create_text1("Please select the location and the year\nfor which you would like to view the performance", 18)),
            self.container_input(self.buttons, bt1),
            self.info_container(self.create_text1("RESULT", 27)),
            result
        ]

    def header(self):
        return ft.AppBar(leading=self.create_icon_button(ft.icons.NAVIGATE_BEFORE,
                                                         "BACK TO HOME",
                                                         lambda _: self.page.go("/page1"),
                                                         "white",
                                                         "indigo"
                                                         ),
                         title=self.create_text1("DATA ANALYSIS", 40),
                         bgcolor=ft.colors.INDIGO,
                         center_title=True,
                         actions=[self.create_icon_button(ft.icons.NAVIGATE_NEXT,
                                                          "GO TO THE NEXT PAGE\n ( analysis CVP )",
                                                          lambda _: self.page.go("/page3"),
                                                          "white",
                                                          "indigo"
                                                          )
                                  ]
                         )

    def container_input(self, buttons, aggiorna):

        return ft.Container(self.scroll_x([buttons, aggiorna]),
                            alignment=ft.Alignment(0, 0),
                            margin=ft.Margin(top=10, left=0, right=0, bottom=0),
                            padding=0
                            )

    def scroll_y(self, controls):
        """ metodo per poter scorrere verticalmente """
        return ft.Column(controls,
                         scroll=ft.ScrollMode.ALWAYS,
                         alignment=ft.MainAxisAlignment.CENTER,
                         horizontal_alignment=ft.CrossAxisAlignment.CENTER  # <-- per alineare orizzontalmente
                         )

    def box(self, content, width, height):
        """ Crea i box presenti ad ogni tab"""
        return ft.Container(content,
                            alignment=ft.Alignment(0, 0),
                            bgcolor="white",
                            width=width,
                            height=height,
                            margin=0,
                            padding=4,
                            border_radius=10
                            )  # <-- mettendo una virgola mi avrebbe restituito una tupla

    def create_table(self, testo, n_column=1):
        """ Crea Tabelle """
        # Definizione delle colonne in base al numero richiesto
        columns = [ft.DataColumn(self.create_text3(testo, 82),
                                 on_sort=lambda e: self._controller.ordine(e, tabella))]

        # Aggiungi una colonna aggiuntiva se richiesto
        if n_column > 1:
            columns.append(ft.DataColumn(self.create_text3("CATEGORY", 89),
                                         on_sort=lambda e: self._controller.ordine(e, tabella)))
        tabella = ft.DataTable(
            sort_column_index=0,
            sort_ascending=True,
            show_checkbox_column=True,
            border=ft.border.all(2, "indigo"),
            columns=columns,
            horizontal_lines=ft.BorderSide(color="INDIGO", width=2),
            vertical_lines=ft.BorderSide(color="INDIGO", width=2),
            heading_row_color="white",
            expand=True
        )

        return tabella

    def create_button(self, testo, comando):
        """ Crea contenitore per i pulsanti """
        return ft.Container(ft.ElevatedButton(testo,
                                              style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "indigo500",
                                                                            ft.ControlState.PRESSED: "indigo900"},
                                                                   shape=ft.RoundedRectangleBorder(radius=10),
                                                                   color={ft.ControlState.DEFAULT: "white",
                                                                          ft.ControlState.PRESSED: "white"},
                                                                   padding=15,
                                                                   text_style=ft.TextStyle(size=16,
                                                                                           weight=ft.FontWeight.BOLD),
                                                                   side=ft.BorderSide(color="indigo", width=2)
                                                                   ),
                                              on_click=comando
                                              ),
                            alignment=ft.Alignment(0, 0),
                            margin=0,
                            padding=0
                            )

    def scroll_x(self, controls):
        """ metodo per scorrere orizzontalemente """
        return ft.Row(controls,
                      alignment=ft.MainAxisAlignment.CENTER,
                      scroll=ft.ScrollMode.ALWAYS
                      )

    def container_body(self, content):
        """ Crea contenitore per il body del tab"""
        return ft.Container(self.scroll_x(content),
                            alignment=ft.Alignment(0, 0),
                            margin=4
                            )

    def create_column(self, valori):
        c = ft.Column([], spacing=6)
        for i in valori:
            c.controls.append(
                ft.Container(self.create_text3(f"{i}", None),
                             bgcolor=ft.colors.BLUE_100,
                             width=145,
                             height=45,
                             alignment=ft.alignment.center,
                             border_radius=10,
                             )
            )
        return c

    def create_icon_button(self, icon, tooltip, on_click, color1, color2):
        """ Crea un pulsante con icona """
        return ft.IconButton(icon,
                             tooltip=tooltip,
                             style=ft.ButtonStyle(
                                 bgcolor={ft.ControlState.DEFAULT: color2, ft.ControlState.PRESSED: color1},
                                 color={ft.ControlState.DEFAULT: color1, ft.ControlState.PRESSED: color2}
                             ),
                             icon_size=30,
                             on_click=on_click
                             )

    def create_container1(self, control, height):
        return ft.Container(control, height=height)

    def create_text1(self, testo, size):
        """ Crea l'informazione per l'utente """
        return ft.Text(testo,
                       style=ft.TextStyle(size=size,
                                          weight=ft.FontWeight.BOLD,
                                          color="white",
                                          letter_spacing=1,
                                          word_spacing=2
                                          ),
                       text_align=ft.TextAlign.CENTER,
                       )

    def create_text2(self, testo):
        """ Crea titolo box """
        txt = ft.Text(testo,
                      style=ft.TextStyle(size=20,
                                         weight=ft.FontWeight.BOLD,
                                         color="INDIGO900",
                                         ),
                      text_align=ft.TextAlign.CENTER
                      )
        return txt

    def create_text3(self, testo, width):
        """ Crea text heading tabelle """
        txt = ft.Text(testo,
                      style=ft.TextStyle(size=17,
                                         weight=ft.FontWeight.BOLD,
                                         color="black"
                                         ),
                      width=width
                      )
        return txt

    def info_container(self, info):
        """ Crea un contenitore con informazioni per l'utente """
        return ft.Container(info,
                            alignment=ft.Alignment(0, 0)
                            )
