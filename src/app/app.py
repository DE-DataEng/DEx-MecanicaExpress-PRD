import flet as ft

from src.core import AppConfig
from src.ui.tela_login import show_login

class MecanicaExpress:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = AppConfig()


    def initialize(self) -> None:
        self._configure_page()
        show_login(self.page)

    def _configure_page(self) -> None:
        self.page.title = self.config.APP_TITLE
        self.page.window_width = self.config.WINDOW_WIDTH
        self.page.window_height = self.config.WINDOW_HEIGHT
        self.page.window_min_width = 1200
        self.page.window_min_height = 760
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = self.config.THEME_MANAGER.theme.page_bgcolor
        self.page.theme_mode = ft.ThemeMode.LIGHT


def create_app(page: ft.Page) -> MecanicaExpress:
    return MecanicaExpress(page)
