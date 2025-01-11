import flet as ft

from UI.authentication import Page0
from UI.home import Page1
from UI.analisiDati import Page2
from UI.analisiCVP import Page3

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "TESI: Sotware a supporto del processo decisionale"
        self._page.window_min_width=500
        self._page.window_min_height=700

        self._controller = None


    def load_interface(self):
        self._ddLoc = ft.Dropdown(label=" LOCATION ",
                                     value="Airport",
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
                                                              color=ft.colors.BLACK,  # colore del testo sopra il box
                                                              weight=ft.FontWeight.BOLD),

                                     on_change=self._controller.fillShop,
                                     width=155,

                                     )

        self._ddShop = ft.Dropdown(label=" STORE ",
                                  value="Maven Toys Ciudad de Mexico 2",
                                  border_color="black",
                                  text_style=ft.TextStyle(italic=True,
                                                          size=15,
                                                          color=ft.colors.BLACK,
                                                          weight=ft.FontWeight.BOLD),
                                  width=260,
                                  border_radius=9,
                                  bgcolor="white",
                                  label_style=ft.TextStyle(italic=True,
                                                           size=15,
                                                           bgcolor="white",
                                                           letter_spacing=3,
                                                           color=ft.colors.BLACK,  # colore del testo sopra il box
                                                           weight=ft.FontWeight.BOLD
                                                           ),
                                  )

        self._ddAnno = ft.Dropdown(label=" YEAR ",
                                   value="2022",
                                   border_color="black",
                                   text_style=ft.TextStyle(italic=True,
                                                           size=15,
                                                           color=ft.colors.BLACK,
                                                           weight=ft.FontWeight.BOLD),
                                   width=90,
                                   border_radius=9,
                                   bgcolor="white",
                                   label_style=ft.TextStyle(italic=True,
                                                            size=15,
                                                            bgcolor="white",
                                                            letter_spacing=3,
                                                            color=ft.colors.BLACK,
                                                            weight=ft.FontWeight.BOLD),
                                   on_change=self._controller.fillMese
                                   )

        self._ddMese = ft.Dropdown(label=" MONTH ",
                                   value="1",
                                   border_color="black",
                                   text_style=ft.TextStyle(italic=True,
                                                           size=15,
                                                           color=ft.colors.BLACK,
                                                           weight=ft.FontWeight.BOLD),
                                   width=120,

                                   border_radius=9,
                                   bgcolor="white",
                                   label_style=ft.TextStyle(italic=True,
                                                            size=15,
                                                            bgcolor="white",
                                                            letter_spacing=2,
                                                            color=ft.colors.BLACK,
                                                            weight=ft.FontWeight.BOLD),

                                   )


        self.pulsanti1 = ft.Container(ft.Row([self._ddLoc,self._ddAnno],
                                             alignment=ft.MainAxisAlignment.CENTER),
                                      width=260,
                                      )
        self.pulsanti2 = ft.Container(ft.Row([self._ddLoc, self._ddShop, self._ddAnno, self._ddMese],
                                             alignment=ft.MainAxisAlignment.CENTER),
                                      width=660)
        self._controller.fillDD()
        def route_change(route): #<--- funzione per cambiare pagina
            self._page.views.clear()

            self._pag0 = Page0(self._page, self._controller)
            self._pag1 = Page1(self._page)
            self._pag2 = Page2(self._page, self._controller, self.pulsanti1)
            self._pag3 = Page3(self._page, self._controller, self.pulsanti2)

            self._page.views.append(self._pag0)

            self._controller.changePage()
            self._page.update()

        def view_pop(view): #<--- funzione per cancellare la pagina precedente
            self._page.views.pop()
            top_view = self._page.views[-1]
            self._page.go(top_view.route)


        self._page.on_route_change = route_change
        self._page.on_view_pop = view_pop
        self._page.go(self._page.route)



    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()