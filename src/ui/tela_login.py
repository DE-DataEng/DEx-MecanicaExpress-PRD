import flet as ft

from DEx_Framework.foundations.components import DS_Login_Screen
from src.core.config.app_config import AppConfig



def show_login(page: ft.Page, on_login=None) -> None:
    cfg = AppConfig()
    login_screen = DS_Login_Screen(
        logo_src=getattr(cfg, "LOGO_SRC", None),
        system_name=getattr(cfg, "SYSTEM_NAME", "Sistema"),
        welcome_message=getattr(cfg, "WELCOME_MESSAGE", "Bem-vindo"),
        login_label="Usuario ou e-mail",
        login_hint="Digite seu usuario ou e-mail",
        password_label="Senha",
        enter_label="Entrar",
        forgot_password_text="Esqueci minha senha",
        client_logo_src=getattr(cfg, "CLIENT_LOGO_SRC", None),
        right_title="Bem-vindo de volta",
        right_subtitle="Acesse com sua conta para continuar.",
        right_button_label="Solicitar acesso",
        on_enter=on_login,
    )

    page.controls.clear()
    page.add(login_screen)
    page.update()
