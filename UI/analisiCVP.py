import flet as ft

from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class Page3(ft.View):
    def __init__(self, page: ft.Page, controller, buttons):
        super(Page3, self).__init__(
            route="/page3",
            bgcolor="indigo"
        )
        self.page = page
        self.controller3 = controller

        self.buttons = buttons

        # Creazione campi di testo
        self.cf = self.create_text_field(' CF ', '4000')
        self.target = self.create_text_field(" TARGET ", '0')
        self.vQty = self.create_text_field(" ΔQty(%) ", None)
        self.vPr = self.create_text_field(" ΔPrice(%) ", None)
        self.vCF = self.create_text_field(" ΔCF ", None)

        # Creazione pulsanti
        aggiorna = self.create_icon_button(ft.icons.UPDATE, "UPDATE PAGE", self.controller3.update_page3, "green", "white")
        stampa = self.create_icon_button(ft.icons.PRINT, "PRINT RESULT", self.controller3.stampa, "bluegrey700", "white")
        self.calcolaVar = self.create_button("CALCULATE", self.controller3.variazioni2)

        # Creazione grafico
        self.fig3a, self.axs3a = plt.subplots(1, 1, figsize=(6, 3))
        plt.rc('xtick', labelsize=8)  # <-- per aggiustare la dimensione dei valori nelle ascisse e nelle ordinate
        plt.rc('ytick', labelsize=8)
        box = self.axs3a.get_position()
        self.axs3a.set_position([box.x0, box.y0, box.width * 0.90, box.height])
        self.chart3a = MatplotlibChart(self.fig3a, expand=True)
        plt.close(self.fig3a)

        # Creazione delle liste
        self.l3a = ft.ListView(expand=True, spacing=4, padding=0)
        self.l4a = ft.ListView(expand=True, spacing=4, padding=0)

        # Controlli della pagina
        self.controls = [
            self.header(),
            self.info_container(self.create_text("Please select the four dropdown menus below to extract the sold quantities for each product\nassumed to occur as an average in the month in question.\nIn the 'CF' field, enter the fixed costs that are expected to be incurred,\nIn the 'Target' field, indicate any profit goal you wish to achieve", 18, "white")),
            self.input_insert(self.buttons, aggiorna, stampa),
            self.info_container(self.create_text("RESULT", 27, "WHITE")),
            self.result()
        ]

    def header(self):
        return ft.AppBar(leading=self.create_icon_button(ft.icons.NAVIGATE_BEFORE,
                                                         "BACK TO HOME",
                                                         lambda _: self.page.go("/page1"),
                                                         "white", "indigo"),
                         title=self.create_text("CVP ANALYSIS", 40, "white"),
                         bgcolor=ft.colors.INDIGO,
                         center_title=True,
                         actions=[self.create_icon_button(ft.icons.NAVIGATE_NEXT,
                                                          "GO TO THE NEXT PAGE\n ( date analysis )",
                                                          lambda _: self.page.go("/page2"),
                                                          "white", "indigo")]
                         )

    def create_text_field(self, testo, valore):
        """ Crea i campi di testo """
        return ft.TextField(label=testo,
                            value=valore,
                            text_style=ft.TextStyle(size=15,
                                                    color=ft.colors.BLACK,
                                                    weight=ft.FontWeight.BOLD,
                                                    italic=True,
                                                    ),
                            label_style=ft.TextStyle(size=15,
                                                     color=ft.colors.BLACK,
                                                     bgcolor="white",
                                                     weight=ft.FontWeight.BOLD,
                                                     italic=True,
                                                     letter_spacing=1,
                                                     ),
                            bgcolor="white",
                            border_radius=10,
                            width=135,
                            )

    def input_insert(self, buttons, aggiorna, stampa):
        """ Crea contenitore per i campi di input """
        return ft.Container(ft.Row([buttons,
                                    ft.Container(self.cf, width=100),
                                    ft.Container(width=30),
                                    ft.Container(self.target, width=100),
                                    aggiorna, stampa
                                    ],
                                   scroll=ft.ScrollMode.ALWAYS,
                                   alignment=ft.MainAxisAlignment.CENTER,
                                   ),
                            alignment=ft.Alignment(0, 0),
                            margin=ft.Margin(top=10, left=0, right=0, bottom=0),
                            padding=0
                            )

    def container_chart(self):
        """ Crea contenitore per il grafico """
        return ft.Container(self.chart3a,
                            alignment=ft.Alignment(0, 0),
                            bgcolor="white",
                            width=710,
                            height=480,
                            padding=0,
                            margin=0,
                            border_radius=10,
                            )

    def container_list(self, control, width):
        """ Crea contenitore di ogni box"""
        return ft.Container(ft.Column(control,
                                      scroll=ft.ScrollMode.ALWAYS,
                                      alignment=ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                      ),
                            bgcolor="white",
                            width=width,
                            height=480,
                            padding=10,
                            margin=0,
                            border_radius=10,
                            )

    def result(self):
        """ Crea contenitore per il body"""
        return ft.Container(ft.Column([ft.Row([self.container_chart(),
                                               self.container_list([self.l3a], 430),
                                               self.container_list([self.create_text("Please provide the variations of the variables\nto analyze their impact on operating income", 16, "black"), ft.Container(height=2), self.vQty, self.vPr, self.vCF, self.calcolaVar, self.l4a], 280)
                                               ],
                                              scroll=ft.ScrollMode.ALWAYS,
                                              )
                                       ],
                                      scroll=ft.ScrollMode.ALWAYS,
                                      ),
                            alignment=ft.Alignment(0, 0),
                            expand=True,
                            margin=5
                            )

    def create_button(self, testo, comando):
        """ Crea il pulsante di calcolo variazione"""
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
                            margin=10,
                            padding=0
                            )

    def create_icon_button(self, icon, tooltip, on_click, color1, color2):
        """ Crea un pulsante con icona """
        return ft.IconButton(
            icon,
            tooltip=tooltip,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: color2, ft.ControlState.PRESSED: color1},
                color={ft.ControlState.DEFAULT: color1, ft.ControlState.PRESSED: color2}
            ),
            icon_size=30,
            on_click=on_click
        )

    def create_text(self, testo, size, color):
        """ Crea l'informazione per l'utente """
        return ft.Text(testo,
                       style=ft.TextStyle(size=size,
                                          color=color,
                                          weight=ft.FontWeight.BOLD,
                                          letter_spacing=1,
                                          word_spacing=2
                                          ),
                       text_align=ft.TextAlign.CENTER,
                       )

    def info_container(self, info):
        """ Crea un contenitore con informazioni per l'utente """
        return ft.Container(info,
                            alignment=ft.Alignment(0, 0),
                            padding=0
                            )
