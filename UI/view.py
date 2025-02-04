import flet as ft

from UI.authentication import Page0
from UI.home import Page1
from UI.analisiDati import Page2
from UI.analisiCVP import Page3


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.title = "TESI: Sotware a supporto del processo decisionale"
        self.page.window_min_width = 400
        self.page.window_min_height = 500

        self._controller = None

        self.page0, self.page1, self.page2, self.page3 = None, None, None, None

    def load_interface(self):
        """ Carica l'interfaccia e imposta le funzioni per il cambio pagina"""

        # creazione pulsanti
        self.ddLoc = self.create_dd(" LOCATION ", 155, click=self._controller.update_store)
        self.ddShop = self.create_dd(" STORE ", 260)
        self.ddAnno = self.create_dd(" YEAR ", 90, click=self._controller.update_mese)
        self.ddMese = self.create_dd(" MONTH ", 120)

        # creazione contenitore pulsanti
        self.pulsanti1 = self.create_container([self.ddLoc, self.ddAnno], 260)
        self.pulsanti2 = self.create_container([self.ddLoc, self.ddShop, self.ddAnno, self.ddMese], 660)

        self._controller.fill_dd()

        def route_change(route):

            self.page.views.clear()

            # Creo le pagine necessarie per l'applicazione
            if route.route == '/':
                self.pag0 = Page0(self.page, self._controller)
            if route.route == '/page1':
                self.pag1 = Page1(self.page)
            if route.route == '/page2':
                self.pag2 = Page2(self.page, self._controller, self.pulsanti1)
            if route.route == '/page3':
                self.pag3 = Page3(self.page, self._controller, self.pulsanti2)


            # Richiamo la funzione per cambiare la pagina
            self._controller.change_page()

            self.page.update()

        self.page.on_route_change = route_change
        self.page.go(self.page.route)

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self.page.update()

    def create_dd(self, testo, width, click=None):
        return ft.Dropdown(label=testo,
                           border_color="black",
                           text_style=ft.TextStyle(italic=True,
                                                   size=15,
                                                   color=ft.colors.BLACK,
                                                   weight=ft.FontWeight.BOLD),
                           border_radius=9,
                           bgcolor="white",
                           label_style=ft.TextStyle(italic=True,
                                                    size=15,
                                                    bgcolor="white",
                                                    letter_spacing=3,
                                                    color=ft.colors.BLACK,
                                                    weight=ft.FontWeight.BOLD),
                           on_change=click,
                           width=width,
                           )

    def create_container(self, control, width):
        return ft.Container(ft.Row(control, alignment=ft.MainAxisAlignment.CENTER),
                            width=width,
                            )

