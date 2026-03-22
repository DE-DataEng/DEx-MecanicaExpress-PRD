from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

from DEx_Framework.foundations.components import DS_ThemeManager

@dataclass(frozen=True)
class AppConfig:

    # definição do tema
    THEME_MANAGER = DS_ThemeManager()
    # definicao do painel da esquerda da tela de login
    LOGO_SRC = "logo/Logo_MecanicaExpress_Azul.png"
    SYSTEM_NAME = "Mecânica Express 2.0"
    WELCOME_MESSAGE = 'Bem-vindo ao mais moderno sistema de gestão para a sua oficina mecânica!'

    # definição do painel da direita da tela de login
    CLIENT_LOGO_SRC = "logo/logo_cliente.png"
    RIGHT_TITLE = "Bem vindo de volta"
    RIGHT_SUBTITLE = 'Acesse com sua conta para continuar...'
    RIGHT_BUTTON_LABEL = "Clique aqui para solicitar acesso!"

    # Definindo janela
    APP_TITLE: str = SYSTEM_NAME
    WINDOW_WIDTH: int = 1440
    WINDOW_HEIGHT: int = 920

    # variaveis para conexao com o banco de dados
    DB_HOST: str = os.getenv("DB_HOST", os.getenv("MECEXP_DB_HOST", "localhost"))
    DB_PORT: int = int(os.getenv("DB_PORT", os.getenv("MECEXP_DB_PORT", "5432")))
    DB_NAME: str = os.getenv("DB_NAME", os.getenv("MECEXP_DB_NAME", "mecanica_express"))
    DB_USER: str = os.getenv("DB_USER", os.getenv("MECEXP_DB_USER", "postgres"))
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", os.getenv("MECEXP_DB_PASSWORD", "postgres"))
    DB_SSLMODE: str = os.getenv("DB_SSLMODE", "prefer")

    # variaveis para conexao do usuario
    AUTH_SCHEMA: str = os.getenv("AUTH_SCHEMA", "oficina")
    AUTH_TABLE: str = os.getenv("AUTH_TABLE", "usuarios")
    AUTH_PASSWORD_COLUMN: str = os.getenv("AUTH_PASSWORD_COLUMN", "senha_hash")
    AUTH_SEARCH_COLUMN: str = os.getenv("AUTH_SEARCH_COLUMN", "login")
    AUTH_PASSWORD_ALGO: str = os.getenv("AUTH_PASSWORD_ALGO", "argon2")

    # Snackbar
    SNACKBAR_DURATION_MS: int = int(os.getenv("SNACKBAR_DURATION_MS", "5000"))
    SNACKBAR_SUCCESS_MS: int = int(os.getenv("SNACKBAR_SUCCESS_MS", "3000"))
    SNACKBAR_ERROR_MS: int = int(os.getenv("SNACKBAR_ERROR_MS", "5000"))
