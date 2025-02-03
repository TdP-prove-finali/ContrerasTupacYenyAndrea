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

        # creazione testo
        info = self.create_text("Please enter your username and password\nto access the application", 18)
        t1 = ft.Text("AUTHENTICATION",
                     style=ft.TextStyle(size=25, color="black", weight=ft.FontWeight.BOLD),
                     )
        # creazione campi di testo
        self.username = ft.TextField(label="USERNAME", width=220)
        self.password = ft.TextField(label="PASSWORD", width=220, password=True)

        # Creazione pulsante di accesso
        login = ft.ElevatedButton("SIGN UP",
                                  style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: "greenaccent700",
                                                                ft.ControlState.PRESSED: "green800",
                                                                },
                                                       shape=ft.RoundedRectangleBorder(radius=10),
                                                       text_style=ft.TextStyle(size=17, weight=ft.FontWeight.BOLD),
                                                       ),
                                  color="black",
                                  width=220,
                                  height=50,
                                  on_click=controller.login
                                  )

        # controlli da visualizzare nella vista
        self.controls = [
            self.header(),
            info,
            ft.Container(height=4),
            self.box_autenticazione(t1, self.username, self.password, login)

        ]

    def header(self):
        """ Crea l'intestazione della pagina """
        return ft.Row([
                self.create_text("MAVEN TOY STORE ANALYTICS ", 40),
            ], alignment=ft.MainAxisAlignment.CENTER  # <-- per centrare il titolo
            )

    def box_autenticazione(self, t1, username, password, login):
        """ Crea contenitore per i campi di autenticazioni """
        r1 = ft.Container(ft.Row([ft.Column([t1,
                                             username,
                                             password,
                                             ft.Container(ft.Divider(color="black"), width=220),
                                             login
                                             ], alignment=ft.MainAxisAlignment.CENTER
                                            )
                                  ], alignment=ft.MainAxisAlignment.CENTER
                                 ),
                          bgcolor="white",
                          width=270,
                          height=280,
                          border_radius=10
                          )

        return r1

    def create_text(self, testo, size):
        return ft.Text(testo,
                       style=ft.TextStyle(size=size,
                                          color="white",
                                          weight=ft.FontWeight.BOLD,
                                          word_spacing=2,
                                          letter_spacing=1
                                          ),
                       text_align=ft.TextAlign.CENTER
                       )
