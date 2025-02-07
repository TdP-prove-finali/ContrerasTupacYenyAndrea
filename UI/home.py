import flet as ft


class Page1(ft.View):
    def __init__(self, page: ft.Page, controller):
        super(Page1, self).__init__(
            route="/page1",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor="indigo"

        )
        self.page = page

        # creazione testo
        titolo = self.create_text("WELCOME\nTO MAVEN TOY STORE ANALYTICS", 40)
        info = self.create_text("which operation would you like to execute?\nPlease select one of the buttons shown below:", 18)

        # creazione pulsanti
        bt1 = self.create_button("DATE ANALYSIS", lambda _: self.page.go("/page2"), "black", "white", "blue100")
        bt2 = self.create_button("CVP ANALYSIS", lambda _: self.page.go("/page3"), "black", "white", "blue100")
        bt3 = self.create_button("LOGOUT", controller.logout, "white", "red", "red900")

        self.controls = [
            titolo,
            info,
            ft.Container(height=4),
            bt1,
            bt2,
            bt3
        ]

    def create_button(self, testo, comando, color1, color2, color3):
        """ Crea il pulsante """
        bottone = ft.ElevatedButton(testo,
                                    style=ft.ButtonStyle(bgcolor={ft.ControlState.DEFAULT: color2,
                                                                  ft.ControlState.PRESSED: color3},
                                                         shape=ft.RoundedRectangleBorder(radius=10),
                                                         text_style=ft.TextStyle(size=17, weight=ft.FontWeight.BOLD),
                                                         ),
                                    color=color1,
                                    width=220,
                                    height=50,
                                    on_click=comando
                                    )

        return bottone

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
