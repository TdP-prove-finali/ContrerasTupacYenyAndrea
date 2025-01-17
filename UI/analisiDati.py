import flet as ft

from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt

class Page2(ft.View):
    def __init__(self, page: ft.Page, controller, buttons):
        super(Page2, self).__init__(
            route="/page2",
            bgcolor="indigo500"
        )
        self._page = page
        self._controller=controller

        aggiorna = ft.IconButton(ft.icons.UPDATE,
                                 tooltip="UPDATE PAGE",
                                 style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "white",
                                                               ft.ControlState.PRESSED: "green",
                                                               },
                                                      color={ft.ControlState.DEFAULT: "green",
                                                             ft.ControlState.PRESSED: "white"}),
                                 icon_size=30,
                                 on_click=self._controller.update
                                 )

        #OVERVIEW
        # 1.GRAFICO SULL'ANDAMENTO DEL PROFITTO
        self._fig2a, self._axs2a = plt.subplots(1, 1, figsize=(6, 3))
        box = self._axs2a.get_position()
        self._axs2a.set_position([box.x0, box.y0, box.width * 0.90, box.height])
        self._chart2a = MatplotlibChart(self._fig2a, expand=True)

        cl1 = self.box(self.scrollY([self._chart2a]), 680, 500) # <-- 1box=1col

        # 2.RISULTATO TOTALE DI TUTTI I NEGOZI PRESENTI NELLA LOCALITA SELEZIONATA
        c = ft.Column([], spacing=6)
        for i in ['PROFIT', 'REVENUE', 'UNITS SOLD']:
            c.controls.append(
                ft.Container(
                    ft.Text(f"{i}",
                            style=ft.TextStyle(color="BLACK",
                                               size=17,
                                               weight=ft.FontWeight.BOLD
                                               ),
                            text_align=ft.TextAlign.CENTER
                            ),
                    bgcolor=ft.colors.BLUE_ACCENT_100,
                    width=145,
                    height=45,
                    alignment=ft.alignment.center,
                    border_radius=10
                )
            )

        self._r21b = ft.Row([], spacing=2)

        rw21a = ft.Row([c, self._r21b],
                       alignment=ft.MainAxisAlignment.CENTER # <-- per centrare i contenutI all'interno delle righe
                       )

        self._txt0 = ft.Container(alignment=ft.Alignment(0,0))

        c1 = self.box(self.scrollY([self._txt0, rw21a]),480, 200) # <-- 2box

        # 3.NEGOZIO AVENTE IL PRODOTTO PIU PROFICUO
        txt1 = self.createText2("STORE WITH THE MOST PROFITABLE PRODUCT")
        self._r21c = ft.Row([],
                            alignment=ft.MainAxisAlignment.CENTER
                            )

        c2= self.box(self.scrollY([txt1, self._r21c]), 480, 290)  # <-- 3box

        cl2=ft.Container(self.scrollY([c1,c2]), height=500)  # <-- 2col


        #PRODUCT ----------------------------------------------------------------------------------------------
        # 1.GRAFICO A BARRA PER LE CATEGORIE

        t1 = self.createText2("PRODUCTS BY CATEGORY")
        self._fig2b, self._axs2b = plt.subplots(2, 1, figsize=(5.5, 4.4))
        self._chart2b = MatplotlibChart(self._fig2b, expand=True)
        cl3=self.box(self.scrollY([t1, self._chart2b]), 550, 500) # <-- 1col

        # 2.TABELLA PRODOTTI
        t2=self.createText2("LIST OF ALL PRODUCTS")
        self._tabella21a = self.createTable("PRODUCT", self._controller.ordine1)
        l21a = ft.Container(self.scrollY([self._tabella21a]), height=150, padding=4)

        bt1=self.createButton("UPDATE CHART", self._controller.aggiornaGrafico1)

        # 3.GRAFICO ANDAMENTO DEL PRODOTTO X
        self._fig2c, self._axs2c = plt.subplots(1, 1, figsize=(7, 1.8))
        box = self._axs2c.get_position()
        self._axs2c.set_position([box.x0, box.y0, box.width * 0.9, box.height])
        self._chart2c = MatplotlibChart(self._fig2c, expand=True)
        d=ft.Container(self._chart2c, height=228)

        cl4=self.box(self.scrollY([t2, l21a, bt1, d]),870, 500) # <-- 2col

        #NEGOZI
        # 1.TABELLA NEGOZI
        t3 = self.createText2("LIST OF ALL STORES")
        self._tabella21b = self.createTable("STORE ", self._controller.ordine2)
        l21b = ft.Container(self.scrollY([self._tabella21b]), height=150, padding=5)

        bt2 = self.createButton("UPDATE CHART", self._controller.aggiornaGrafico2)

        # 2. GRAFICO ANDAMENTO DEL NEGOZIO X
        self._fig2d, self._axs2d = plt.subplots(1, 1, figsize=(7, 1.8))
        pos = self._axs2d.get_position()
        self._axs2d.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
        self._chart2d = MatplotlibChart(self._fig2d, expand=True)
        e=ft.Container(self._chart2d, height=228)

        cl5=self.box(self.scrollY([t3,l21b,bt2,e]), 930, 500) # <-- 1col
        # 3. STOCK
        stock = self.createButton("STOCK 09/2023\nOF THE STORE SELECTED", self._controller.aggiornaButtonStock)
        self._ris = ft.ListView([], expand=True, padding=0)
        r=ft.Container(self.scrollY([self._ris]), height=430)
        cl6=self.box(ft.Column([stock, r]), 330,500) # <-- 2col
        #--------------------------------------------------------------------------
        #TAB
        result = ft.Tabs(selected_index=0,
                      animation_duration=300,
                      label_color="white",
                      label_text_style=ft.TextStyle(size=17,
                                                    weight=ft.FontWeight.BOLD),
                      tabs=[
                          ft.Tab(
                              text="OVERVIEW",
                              content=self.createcontainerBody(self.scrollX([cl1, cl2]))
                          ),
                          ft.Tab(
                              text="PRODUCTS",
                              content=self.createcontainerBody(self.scrollX([cl3, cl4]))
                          ),
                          ft.Tab(
                              text="STORES",
                              content= self.createcontainerBody(self.scrollX([cl5, cl6]))
                          ),
                      ],
                      tab_alignment=ft.TabAlignment.CENTER,
                      expand=True
                      )

        self.controls = [
            self.header(),
            ft.Container(ft.Text("Please select the location and the year\nfor which you would like to start the analysis",
                                 text_align=ft.TextAlign.CENTER,
                                 style=ft.TextStyle(color="white", size=17,letter_spacing=2, word_spacing=3)
                                 ),
                         alignment=ft.Alignment(0,0),
                         margin=ft.Margin(top=0, left=0, right=0, bottom=10),
                         padding=0
                         ),
            self.row1(buttons, aggiorna),
            ft.Container(
                ft.Text("RESULT",
                        text_align=ft.TextAlign.CENTER,
                        style = ft.TextStyle(size=27, weight=ft.FontWeight.BOLD, color="white", letter_spacing=2)
                        ),
                alignment=ft.Alignment(0, 0),
                margin=0,
                padding=0
            ),

            result
        ]

    def header(self):
        return ft.AppBar(leading=ft.Container(ft.IconButton(ft.icons.NAVIGATE_BEFORE,
                                                            tooltip="BACK TO HOME",
                                                            icon_size=34,
                                                            icon_color="WHITE",
                                                            on_click=lambda _: self.page.go("/page1")
                                                           )
                                              ),
                        title=ft.Text("DATA ANALYSIS",
                                      style=ft.TextStyle(size=40,
                                                         weight=ft.FontWeight.BOLD,
                                                         color="white",
                                                         letter_spacing=5,
                                                         word_spacing=5,
                                                         )
                                      ),
                        bgcolor=ft.colors.INDIGO,
                        center_title=True,
                        actions=[ft.IconButton(ft.icons.NAVIGATE_NEXT,
                                               tooltip="GO TO THE NEXT PAGE\n ( CVP analysis )",
                                               icon_size=34,
                                               icon_color="WHITE",
                                               on_click=lambda _: self.page.go("/page3")
                                          )
                                 ]
                        )
    def row1(self, buttons, aggiorna):

        return ft.Container(ft.Row([buttons, aggiorna],
                                   alignment=ft.MainAxisAlignment.CENTER,
                                   scroll=ft.ScrollMode.ALWAYS
                                   ),
                            alignment=ft.Alignment(0, 0),
                            margin=0,
                            padding=0
                            )

    def scrollY(self, controls):
        scroll= ft.Column(controls,
                          scroll=ft.ScrollMode.ALWAYS,
                          alignment=ft.MainAxisAlignment.CENTER,
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER # <-- per alineare orizzontalmente
                         )
        return scroll
    def box(self, content, width, height):
         t = ft.Container(content,
                            alignment=ft.Alignment(0, 0),
                            bgcolor="white",
                            width=width,
                            height=height,
                            margin=0,
                            padding=4,
                            border_radius=10
                            ) # <-- mettedno una virgola mi avrebbe restituito una tupla
         return t

    def createTable(self, testo, comando):
        tabella=ft.DataTable(sort_column_index=0,
                     sort_ascending=True,
                     show_checkbox_column=True,
                     border=ft.border.all(2, "indigo"),
                     columns=[ft.DataColumn(ft.Text(testo,
                                                    color="indigo"
                                                    ),
                                            on_sort=comando,

                                            ),
                              ],
                     horizontal_lines=ft.BorderSide(color="INDIGO",
                                                    width=2
                                                    ),
                     vertical_lines=ft.BorderSide(color="INDIGO",
                                                  width=2
                                                  ),
                     heading_row_color="white",
                     heading_text_style=ft.TextStyle(italic=True,
                                                     size=18,
                                                     color=ft.colors.BLACK,
                                                     weight=ft.FontWeight.BOLD
                                                     ),
                     expand=True
                     )

        return tabella

    def createButton(self, testo, comando):
        bottone = ft.Container(ft.ElevatedButton(testo,
                                       style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "indigo500",
                                                                     ft.ControlState.PRESSED: "indigo900"},
                                                            shape=ft.RoundedRectangleBorder(radius=10),
                                                            color={ft.ControlState.DEFAULT: "white",
                                                                   ft.ControlState.PRESSED: "white"},
                                                            padding=15,
                                                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                                                            side=ft.BorderSide(color="indigo", width=2)
                                                            ),
                                       on_click=comando
                                       ),
                     alignment=ft.Alignment(0, 0),
                     margin=0,
                     padding=0
                     )

        return bottone

    def createText2(self, testo):
        txt= ft.Text(testo,
                style=ft.TextStyle(size=20,
                                   weight=ft.FontWeight.BOLD,
                                   color="INDIGO900"
                                   ),
                text_align=ft.TextAlign.CENTER
                )
        return txt

    def scrollX(self, controls):
        return ft.Row(controls,
                   alignment=ft.MainAxisAlignment.CENTER,
                   scroll=ft.ScrollMode.ALWAYS
                   )
    def createcontainerBody(self, content):
        return ft.Container(
            content,
            alignment=ft.Alignment(0, 0),
            margin=4
        )




