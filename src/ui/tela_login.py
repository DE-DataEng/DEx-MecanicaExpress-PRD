import flet as ft

from DEx_Framework.foundations.components import DS_Login_Screen
from src.core.config.app_config import AppConfig


def show_login(page: ft.Page, on_login=None) -> None:
    cfg = AppConfig()
    login_screen = None

    def _handle_enter(e: ft.ControlEvent):
        if login_screen is None:
            return
        login_value = (login_screen._login_field.value or "").strip()
        password_value = login_screen._password_field.value or ""
        if on_login:
            on_login(login_value, password_value)

    login_screen = DS_Login_Screen(
        logo_src=getattr(cfg, "LOGO_SRC", None),
        system_name=getattr(cfg, "SYSTEM_NAME", "Sistema"),
        welcome_message=getattr(cfg, "WELCOME_MESSAGE", "Bem-vindo"),
        login_label="Usuario",
        login_hint="Digite seu usuario (e-mail, cpf, login)",
        password_label="Senha",
        enter_label="Entrar",
        forgot_password_text="Esqueci minha senha",
        client_logo_src=getattr(cfg, "CLIENT_LOGO_SRC", None),
        right_title="Bem-vindo de volta",
        right_subtitle="Acesse com sua conta para continuar.",
        right_button_label=getattr(cfg, "RIGHT_BUTTON_LABEL", "Solicitar acesso"),
        on_enter=_handle_enter,
    )

    page.controls.clear()
    page.add(login_screen)
    page.update()
