import flet as ft
from login_screen import LoginScreen
from theme import *


def dashboard_view(page: ft.Page, user_name: str):
    cards = [
        ("Clientes", "1.248", ft.Icons.PEOPLE_OUTLINE),
        ("Ordens de Serviço", "312", ft.Icons.DESCRIPTION_OUTLINED),
        ("Veículos", "842", ft.Icons.DIRECTIONS_CAR_OUTLINED),
        ("Financeiro", "R$ 184 mil", ft.Icons.ATTACH_MONEY_OUTLINED),
    ]

    def metric_card(title: str, value: str, icon):
        return ft.Container(
            width=250,
            padding=20,
            border_radius=18,
            bgcolor=COLOR_SURFACE,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Icon(icon, size=34, color=COLOR_ACCENT),
                    ft.Text(title, color=COLOR_TEXT_MUTED, size=14),
                    ft.Text(value, color=COLOR_TEXT, size=28, weight=ft.FontWeight.BOLD),
                ],
            ),
        )

    return ft.Container(
        expand=True,
        bgcolor=COLOR_BG,
        padding=24,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Image(src="../assets/logo/mecanica_express_flat.svg", width=240),
                            ]
                        ),
                        ft.Text(f"Olá, {user_name}", color=COLOR_TEXT, size=16),
                    ],
                ),
                ft.Container(height=12),
                ft.Text("Painel inicial", color=COLOR_TEXT, size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Visão rápida da operação da oficina.", color=COLOR_TEXT_MUTED),
                ft.Container(height=12),
                ft.Row(wrap=True, spacing=16, run_spacing=16, controls=[metric_card(*c) for c in cards]),
                ft.Container(height=22),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=7,
                            padding=20,
                            border_radius=18,
                            bgcolor=COLOR_SURFACE,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Agenda de hoje", color=COLOR_TEXT, size=20, weight=ft.FontWeight.BOLD),
                                    ft.ListView(
                                        expand=True,
                                        spacing=10,
                                        controls=[
                                            ft.ListTile(title=ft.Text("08:00 - Revisão completa | HB20", color=COLOR_TEXT)),
                                            ft.ListTile(title=ft.Text("10:30 - Troca de óleo | Onix", color=COLOR_TEXT)),
                                            ft.ListTile(title=ft.Text("14:00 - Freios | Corolla", color=COLOR_TEXT)),
                                            ft.ListTile(title=ft.Text("16:00 - Alinhamento | Compass", color=COLOR_TEXT)),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        ft.Container(
                            expand=5,
                            padding=20,
                            border_radius=18,
                            bgcolor=COLOR_SURFACE_2,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Módulos", color=COLOR_TEXT, size=20, weight=ft.FontWeight.BOLD),
                                    ft.FilledButton("Clientes", icon=ft.Icons.PEOPLE_ALT_OUTLINED),
                                    ft.FilledButton("Orçamentos", icon=ft.Icons.REQUEST_QUOTE_OUTLINED),
                                    ft.FilledButton("Ordens de Serviço", icon=ft.Icons.BUILD_CIRCLE_OUTLINED),
                                    ft.FilledButton("Veículos", icon=ft.Icons.DIRECTIONS_CAR_FILLED_OUTLINED),
                                    ft.FilledButton("Financeiro", icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED),
                                ],
                            ),
                        ),
                    ],
                )
            ],
        ),
    )


def main(page: ft.Page):
    page.title = "Mecânica Express 2.0"
    page.window.icon = "D:/cloud/OneDrive/Projetos/DataEng/DEx-CarExpress/src/assets/icon/mecanica_express_v2.ico"
    page.theme = app_theme()
    page.bgcolor = COLOR_BG
    page.window_width = 1440
    page.window_height = 900
    page.padding = 0

    def go_dashboard(user_name: str):
        page.clean()
        page.add(dashboard_view(page, user_name))
        page.update()

    page.add(LoginScreen(on_login=go_dashboard))


if __name__ == "__main__":
    ft.app(target=main, assets_dir="../assets")
