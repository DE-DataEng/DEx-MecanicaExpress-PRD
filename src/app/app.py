import os
import logging
import flet as ft
from psycopg2.errors import InvalidTextRepresentation

from src.core import AppConfig, AuthTableConfig, PostgresAuthenticator, PostgresConfig, verify_argon2
from src.core.prefs import UserPrefs
from src.ui.tela_login import show_login
from src.ui.main_menu import show_main_menu


class MecanicaExpress:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = AppConfig()
        self._snack_bar: ft.SnackBar | None = None
        self._prefs = UserPrefs.load()


    def initialize(self) -> None:
        self._configure_page()
        self._apply_prefs()
        self._register_events()
        self._save_prefs()
        self._show_login()

    def _show_login(self) -> None:
        show_login(self.page, on_login=self._handle_login)

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

    def _apply_prefs(self) -> None:
        try:
            if self._prefs.window_width:
                self.page.window_width = self._prefs.window_width
            if self._prefs.window_height:
                self.page.window_height = self._prefs.window_height
            if self._prefs.window_x is not None:
                self.page.window_left = self._prefs.window_x
            if self._prefs.window_y is not None:
                self.page.window_top = self._prefs.window_y
        except Exception:
            pass

        try:
            if self._prefs.theme:
                self.config.THEME_MANAGER.apply(self.page, self._prefs.theme)
        except Exception:
            pass

    def _register_events(self) -> None:
        self.page.on_window_event = self._handle_window_event
        self.config.THEME_MANAGER.subscribe(self._handle_theme_change)

    def _build_authenticator(self) -> PostgresAuthenticator:
        db_cfg = PostgresConfig()
        table_cfg = AuthTableConfig(
            schema=self.config.AUTH_SCHEMA,
            table=self.config.AUTH_TABLE,
            password_column=self.config.AUTH_PASSWORD_COLUMN,
            search_column=self.config.AUTH_SEARCH_COLUMN,
        )
        verify_func = None
        if self.config.AUTH_PASSWORD_ALGO.lower() == "argon2":
            verify_func = verify_argon2
        return PostgresAuthenticator(db_cfg, table_cfg, verify_func=verify_func)

    def _handle_login(self, login_value: str, password_value: str) -> None:
        # print(f"Tentativa de login: {login_value}")
        if not login_value or not password_value:
            self._show_message("Preencha login e senha.", ft.Colors.RED_600, kind="error")
            return
        if self.config.AUTH_SEARCH_COLUMN.lower() == "id_usuario":
            if not login_value.isdigit():
                self._show_message(
                    "Informe um login/senha válidos!",
                    ft.Colors.RED_600,
                    kind="error",
                )
                return

        db_cfg = PostgresConfig()
        if db_cfg.host in ("localhost", "127.0.0.1") and (
            os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or os.getenv("RENDER_SERVICE_NAME")
        ):
            self._show_message(
                "Banco em localhost. Configure DATABASE_URL ou DB_HOST no Render.",
                ft.Colors.AMBER_600,
                kind="error",
            )
            logging.getLogger(__name__).warning(
                "Banco em localhost no Render. Configure DATABASE_URL ou DB_HOST."
            )
        authenticator = PostgresAuthenticator(db_cfg, AuthTableConfig(
            schema=self.config.AUTH_SCHEMA,
            table=self.config.AUTH_TABLE,
            password_column=self.config.AUTH_PASSWORD_COLUMN,
            search_column=self.config.AUTH_SEARCH_COLUMN,
        ), verify_func=verify_argon2 if self.config.AUTH_PASSWORD_ALGO.lower() == "argon2" else None)
        try:
            ok = authenticator.authenticate(login_value, password_value)
        except InvalidTextRepresentation:
            self._show_message(
                "Coluna de pesquisa incompatível com o valor informado. "
                "Ajuste AUTH_SEARCH_COLUMN.",
                ft.Colors.RED_600,
                kind="error",
            )
            return
        except Exception as error:
            self._show_message(f"Falha ao conectar no banco.\ntraceback:{error}", ft.Colors.RED_600, kind="error")
            return

        if ok:
            self._show_message("Login autorizado.", ft.Colors.GREEN_600, kind="success")
            self._prefs.username = login_value
            self._save_prefs()
            show_main_menu(self.page, on_logout=self._show_login)
        else:
            self._show_message("Senha invalida.", ft.Colors.RED_600, kind="error")

    def _handle_window_event(self, e: ft.ControlEvent) -> None:
        if str(e.data).lower() == "close":
            self._capture_window_state()
            self._save_prefs()

    def _handle_theme_change(self, theme) -> None:
        try:
            self._prefs.theme = getattr(theme, "name", self._prefs.theme)
            self._save_prefs()
        except Exception:
            pass

    def _capture_window_state(self) -> None:
        try:
            self._prefs.window_width = int(self.page.window_width or 0) or None
            self._prefs.window_height = int(self.page.window_height or 0) or None
            self._prefs.window_x = int(self.page.window_left or 0) if self.page.window_left is not None else None
            self._prefs.window_y = int(self.page.window_top or 0) if self.page.window_top is not None else None
        except Exception:
            pass

    def _save_prefs(self) -> None:
        try:
            self._prefs.save()
        except Exception:
            pass

    def _show_message(
        self,
        text: str,
        color: str,
        duration_ms: int | None = None,
        kind: str | None = None,
    ) -> None:
        if duration_ms is None:
            if kind == "success":
                duration_ms = self.config.SNACKBAR_SUCCESS_MS
            elif kind == "error":
                duration_ms = self.config.SNACKBAR_ERROR_MS
            else:
                duration_ms = self.config.SNACKBAR_DURATION_MS
        if self._snack_bar is None:
            self._snack_bar = ft.SnackBar(
                content=ft.Text(text),
                bgcolor=color,
                duration=duration_ms,
            )
        else:
            self._snack_bar.content = ft.Text(text)
            self._snack_bar.bgcolor = color
            self._snack_bar.duration = duration_ms
        self.page.open(self._snack_bar)


def create_app(page: ft.Page) -> MecanicaExpress:
    return MecanicaExpress(page)
