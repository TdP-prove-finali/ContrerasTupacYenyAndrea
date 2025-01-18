import flet as ft

from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt

class Page3(ft.View):
    def __init__(self, page: ft.Page, controller, buttons):
        super(Page3, self).__init__(
            route="/page3",
            bgcolor="indigo"
        )
        self.page = page
        self.controller3=controller

        self._cf = self.createTextField(' CF ', '4000')
        self._target = self.createTextField(" TARGET ",'0')

        aggiorna = ft.IconButton(ft.icons.UPDATE,
                                 tooltip="UPDATE PAGE",
                                 style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "white",
                                                               ft.ControlState.PRESSED: "green",
                                                               },
                                                      color={ft.ControlState.DEFAULT: "green",
                                                             ft.ControlState.PRESSED: "white"}),
                                 icon_size=30,
                                 on_click=self.controller3.update
                                 )

        stampa = ft.IconButton(ft.icons.PRINT,
                               tooltip="PRINT RESULT",
                               style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "white",
                                                             ft.ControlState.PRESSED: "bluegrey700",
                                                             },
                                                    color={ft.ControlState.DEFAULT: "bluegrey700",
                                                           ft.ControlState.PRESSED: "white"}),
                               icon_size=30,
                               on_click=self.controller3.stampa
                               )


        self._fig3a, self._axs3a = plt.subplots(1, 1, figsize=(6, 3))
        plt.rc('xtick', labelsize=8) # <-- per aggiustare la dimensione dei valori nelle ascisse e nelle ordinate
        plt.rc('ytick', labelsize=8)
        box = self._axs3a.get_position()
        self._axs3a.set_position([box.x0, box.y0, box.width * 0.90, box.height])
        self._chart3a = MatplotlibChart(self._fig3a, expand=True)

        self._l3a = ft.ListView(expand=True, spacing=4, padding=0)

        self.controls = [
            self.header(),
            ft.Container(ft.Text("Please select the store and the month to indicate the sales quantities for each product\n(it is assumed that these quantities may occur as an average for the month in question).\nIn the 'CF' field, please enter the fixed costs that are expected to be incurred,\nand in the 'Target' field, please indicate any profit goal you wish to achieve",
                                 style=ft.TextStyle(size=17,
                                                    color="white",
                                                    letter_spacing=2,
                                                    word_spacing=3
                                                    ),
                                 text_align=ft.TextAlign.CENTER,
                                 ),
                         alignment=ft.Alignment(0, 0),
                         margin=ft.Margin(top=0, left=0, right=0, bottom=10),
                         padding=0
                         ),
            self.row1(buttons, aggiorna, stampa),
            ft.Container(
                ft.Text("RESULT",
                        style=ft.TextStyle(size=27,
                                           weight=ft.FontWeight.BOLD,
                                           color="white",
                                           letter_spacing=2
                                           ),
                        text_align=ft.TextAlign.CENTER,
                        ),
                alignment=ft.Alignment(0, 0),
                margin=0,
                padding=0
            ),
            self.row2()

        ]

    def header(self):
        return ft.AppBar(leading=ft.Container(ft.IconButton(ft.icons.NAVIGATE_BEFORE,
                                                           tooltip="BACK TO HOME",
                                                           icon_size=34,
                                                           icon_color="WHITE",
                                                           on_click=lambda _: self.page.go("/page1")
                                                           ),
                                             ),
                        title=ft.Text("CVP ANALYSIS",
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
                                               tooltip="GO TO THE NEXT PAGE\n ( date analysis )",
                                               icon_size=34,
                                               icon_color="WHITE",
                                               on_click=lambda _: self.page.go("/page2")
                                               )
                                 ]
                        )


    def createTextField(self, testo, valore):
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
                                              letter_spacing=3,
                                              ),

                        bgcolor="white",
                        border_radius=10,
                        )


    def row1(self, buttons, aggiorna, stampa):
        return ft.Container(ft.Row([buttons,
                                    ft.Container(self._cf, width=100),
                                    ft.Container(width=30),
                                    ft.Container(self._target, width=100),
                                    aggiorna, stampa
                                    ],
                                   scroll=ft.ScrollMode.ALWAYS,
                                   alignment=ft.MainAxisAlignment.CENTER,
                                   ),
                            alignment=ft.Alignment(0, 0),
                            margin=0,
                            padding=0
                            )

    def containerChart(self):
        return ft.Container(self._chart3a,
                            alignment=ft.Alignment(0, 0),
                            bgcolor="white",
                            width=720,
                            height=490,
                            padding=0,
                            margin=0,
                            border_radius=10,
        )

    def containerList(self):
        return ft.Container(ft.Column([self._l3a],
                                      scroll=ft.ScrollMode.ALWAYS,
                                      alignment=ft.MainAxisAlignment.CENTER
                                      ),
                            bgcolor="white",
                            width=450,
                            height=490,
                            padding=0,
                            margin=0,
                            border_radius=10,
        )

    def row2(self):
        return ft.Container(ft.Column([ft.Row([self.containerChart(),
                                                               ft.Container(width=2),
                                                               self.containerList()
                                               ],
                                              scroll=ft.ScrollMode.ALWAYS,
                                              )
                                       ],
                                      scroll=ft.ScrollMode.ALWAYS,
                                      ),
                            alignment=ft.Alignment(0,0),
                            expand=True,
                            margin=5
                            )
