import flet as ft
from psycopg2.errors import InvalidTextRepresentation

from src.core import AppConfig, AuthTableConfig, PostgresAuthenticator, PostgresConfig, verify_argon2
from src.ui.tela_login import show_login


class MecanicaExpress:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = AppConfig()
        self._snack_bar: ft.SnackBar | None = None


    def initialize(self) -> None:
        self._configure_page()
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
        print(f"Tentativa de login: {login_value}")
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

        authenticator = self._build_authenticator()
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
        except Exception:
            self._show_message("Falha ao conectar no banco.", ft.Colors.RED_600, kind="error")
            return

        if ok:
            self._show_message("Login autorizado.", ft.Colors.GREEN_600, kind="success")
        else:
            self._show_message("Senha invalida.", ft.Colors.RED_600, kind="error")

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
