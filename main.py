import os
import flet as ft

from src.app.app import create_app

try:
    from DEx_Framework.foundations.components.layout_structure.ds_container import DS_Container

    if not hasattr(DS_Container, "_DEFAULT_BORDER_COLOR"):
        transparent = ft.Colors.TRANSPARENT if hasattr(ft, "Colors") else "transparent"
        DS_Container._DEFAULT_BGCOLOR = None
        DS_Container._DEFAULT_BORDER_RADIUS = 0
        DS_Container._DEFAULT_BORDER_WIDTH = 0
        DS_Container._DEFAULT_BORDER_COLOR = transparent
        DS_Container._DEFAULT_PADDING = 0
except Exception:
    pass


def main(page: ft.Page) -> None:
    app = create_app(page)
    app.initialize()


if __name__ == "__main__":
    env_port = os.getenv("PORT", "8000")
    port = int(env_port) if env_port.isdigit() else 8000
    ft.app(
        target=main,
        host="0.0.0.0",
        port=port,
        assets_dir="src/assets",
    )
