from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

from DEx_Framework.foundations.components import DS_ThemeManager

@dataclass(frozen=True)
class AppConfig:

    THEME_MANAGER = DS_ThemeManager()
    LOGO_SRC = "./src/assets/logo/Logo_MecanicaExpress_Azul.png"
    CLIENT_LOGO_SRC = "./src/assets/logo/logo_cliente.png"
    SYSTEM_NAME = "Mecanica Express"
    WELCOME_MESSAGE = 'Bem-vindo ao mais moderno sistema para gestão de sua mecânica!'
    RIGHT_TITLE = "Bem vindo de volta"
    RIGHT_SUBTITLE = 'Acesse com sua conta para continuar...'
    RIGHT_BUTTON_LABEL = "Clique aqui para solicitar acesso!"


    APP_TITLE: str = SYSTEM_NAME
    WINDOW_WIDTH: int = 1440
    WINDOW_HEIGHT: int = 920

    # BACKGROUND_COLOR: str = "#F4F7FB"
    # SIDEBAR_COLOR: str = "#0A2E6F"
    # SIDEBAR_ACCENT: str = "#FFB000"
    # CARD_COLOR: str = "#FFFFFF"
    # TEXT_PRIMARY: str = "#132238"
    # TEXT_SECONDARY: str = "#5B6678"
    # BORDER_COLOR: str = "#D9E2F0"
    # SUCCESS_COLOR: str = "#1E8E3E"
    # DANGER_COLOR: str = "#C62828"

    DB_HOST: str = os.getenv("MECEXP_DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("MECEXP_DB_PORT", "5432"))
    DB_NAME: str = os.getenv("MECEXP_DB_NAME", "mecanica_express")
    DB_USER: str = os.getenv("MECEXP_DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("MECEXP_DB_PASSWORD", "postgres")
