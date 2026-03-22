import os
import flet as ft

from src.app.app import create_app


def main(page: ft.Page) -> None:
    app = create_app(page)
    app.initialize()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    ft.app(
        target=main,
        host="0.0.0.0",
        port=port,
    )