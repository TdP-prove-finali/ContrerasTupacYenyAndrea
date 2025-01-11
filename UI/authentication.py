import flet as ft

class Page0(ft.View):
    def __init__(self, page: ft.Page, controller):
        super(Page0, self).__init__(
            route="/",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor="indigo"
        )
        self.page = page

        titolo = ft.Text("TOY STORE ",
                         style=ft.TextStyle(size=44,
                                            color="white",
                                            weight=ft.FontWeight.BOLD,
                                            word_spacing=4,
                                            letter_spacing=4
                                            )
                         )

        sottoTitolo = ft.Text(
            "Please enter your username and password\nto access the application",
            style=ft.TextStyle(size=19,
                               color="white",
                               letter_spacing=1,
                               word_spacing=3
                               ),
            text_align=ft.TextAlign.CENTER
            )

        t1 = ft.Text("AUTHENTICATION",
                               style=ft.TextStyle(size=25,
                                                  color="black",
                                                  weight=ft.FontWeight.BOLD,
                                                  ),
                                    )

        self._username = ft.TextField(label="USERNAME",
                                      width=220,
                                      )
        self._password = ft.TextField(label="PASSWORD",
                                      password=True,
                                      width=220,
                                      )

        login = ft.ElevatedButton("SIGN UP",
                                        style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "greenaccent700",
                                                                      ft.ControlState.PRESSED: "green800",
                                                                      },
                                                             text_style=ft.TextStyle(size=20,
                                                                                     weight=ft.FontWeight.BOLD,
                                                                                     ),
                                                             shape=ft.RoundedRectangleBorder(radius=10)
                                                             ),
                                        color="black",
                                        width=220,
                                        height=50,
                                        on_click=controller.login
                                        )

        self.controls = [
            ft.Row([
                    titolo,
                    ft.Icon(name=ft.icons.SMART_TOY_OUTLINED,
                            color=ft.colors.WHITE,
                            size=44
                            )
            ],alignment=ft.MainAxisAlignment.CENTER # <-- per centrare il titolo
            ),
            sottoTitolo,
            ft.Container(height=4),
            self.boxAutenticazione(t1, self._username, self._password, login)

        ]

    def boxAutenticazione(self, t1, username, password, login):
        r1 = ft.Container(
            ft.Row(
                [
                    ft.Column([t1,
                               username,
                               password,
                               ft.Container(ft.Divider(color="black"),
                                     width=220,
                                      ),
                               login
                               ], alignment=ft.MainAxisAlignment.CENTER # <-- per centrare il contenuto dentro la box
                    )
                ], alignment=ft.MainAxisAlignment.CENTER # <-- per centrare il contenuto dentro la box
            ),
            bgcolor="white",
            width=270,
            height=280,
            border_radius=10,
        )

        return r1