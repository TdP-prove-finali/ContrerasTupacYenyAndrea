import flet as ft


class Page1(ft.View):
    def __init__(self, page: ft.Page):
        super(Page1, self).__init__(
            route="/page1",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor="indigo"

        )
        self.page = page

        titolo = ft.Text("WELCOME",
                         style=ft.TextStyle(size=44,
                                            color="white",
                                            weight=ft.FontWeight.BOLD,
                                            word_spacing=4,
                                            letter_spacing=4
                                            )
                         )

        sottoTitolo = ft.Text("which operation would you like to execute?\nPlease select one of the buttons shown below:",
                                    style=ft.TextStyle(size=19,
                                                       color="white",
                                                       letter_spacing=1,
                                                       word_spacing=3
                                                       ),
                              )
        bt1 = ft.ElevatedButton("DATE ANALYSIS",
                               style=ft.ButtonStyle(
                                   shape=ft.RoundedRectangleBorder(radius=10),
                                   bgcolor={ft.ControlState.DEFAULT: "white",
                                            ft.ControlState.PRESSED: "blue100"},
                                   text_style=ft.TextStyle(size=17,
                                                           weight=ft.FontWeight.BOLD,
                                                           ),
                               ),
                                color="black",
                                width=220,
                                height=50,
                                on_click=lambda _: self.page.go("/page2"),
                               )

        bt2 = ft.ElevatedButton("CVP ANALYSIS",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    bgcolor={ft.ControlState.DEFAULT: "white",
                                             ft.ControlState.PRESSED: "blue100"},
                                    text_style=ft.TextStyle(size=17,
                                                            weight=ft.FontWeight.BOLD,
                                                            #color="black"
                                                          ),
                                ),
                                color="black",
                                width=220,
                                height=50,
                                on_click=lambda _: self.page.go("/page3"),
                               )

        bt3 = ft.ElevatedButton("LOGOUT",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    bgcolor={ft.ControlState.DEFAULT: "red",
                                             ft.ControlState.PRESSED: "red900"},
                                    text_style=ft.TextStyle(size=18,
                                                            weight=ft.FontWeight.BOLD,
                                                            #color="white"
                                                            ),
                                ),
                                color="white",
                               width=220,
                               height=50,
                               on_click=lambda _: self.page.go("/"),
                               )


        self.controls = [
            titolo,
            sottoTitolo,
            ft.Container(height=4),
            bt1,
            bt2,
            bt3
        ]


