import flet as ft
from theme import *

__img__ = "assets/logo/Logo_MecanicaExpress_Azul.png"

class LoginScreen(ft.Container):
    def __init__(self, on_login=None):
        super().__init__(expand=True)
        self.on_login = on_login
        self.email = ft.TextField(
            label="Usuário ou e-mail",
            border_radius=12,
            bgcolor="#FFFFFF",
            color="#101828",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
        )
        self.password = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            border_radius=12,
            bgcolor="#FFFFFF",
            color="#101828",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
        )
        self.message = ft.Text(color="#FFB4A8", size=12)

        self.content = ft.Row(
            expand=True,
            controls=[
                self._build_brand_panel(),
                self._build_form_panel(),
            ],
        )

    def _build_brand_panel(self):
        return ft.Container(
            expand=6,
            padding=40,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_PRIMARY_DARK, COLOR_PRIMARY, COLOR_PRIMARY_LIGHT],
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src=__img__, width=320),
                    ft.Text("Mecânica Express 2.0", size=34, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
                    ft.Text(
                        "Gestão inteligente para oficinas mecânicas.",
                        size=16,
                        color="#DCE6FF",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    def _build_form_panel(self):
        return ft.Container(
            expand=4,
            bgcolor="#F4F7FC",
            padding=50,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=420,
                        padding=30,
                        border_radius=24,
                        bgcolor="#FFFFFF",
                        shadow=ft.BoxShadow(blur_radius=24, color="#1A2A4A22", offset=ft.Offset(0, 10)),
                        content=ft.Column(
                            spacing=18,
                            controls=[
                                ft.Text("Acessar sistema", size=28, weight=ft.FontWeight.BOLD, color="#14213D"),
                                ft.Text("Entre com suas credenciais para continuar.", color="#667085"),
                                self.email,
                                self.password,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Checkbox(label="Lembrar-me", value=True),
                                        ft.TextButton("Esqueci minha senha")
                                    ],
                                ),
                                ft.ElevatedButton(
                                    text="Entrar",
                                    width=360,
                                    height=48,
                                    style=ft.ButtonStyle(
                                        bgcolor=COLOR_ACCENT,
                                        color="#FFFFFF",
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                    ),
                                    on_click=self._handle_login,
                                ),
                                self.message,
                            ],
                        ),
                    )
                ],
            ),
        )

    def _handle_login(self, e):
        if not self.email.value or not self.password.value:
            self.message.value = "Informe usuário e senha."
            self.update()
            return
        self.message.value = ""
        if self.on_login:
            self.on_login(self.email.value)
