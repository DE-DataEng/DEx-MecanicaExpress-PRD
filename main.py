import flet as ft

from src.app.app import create_app

def main(page: ft.Page) -> None:
    # print("Hello world!")
    app = create_app(page)
    app.initialize()


if __name__ == "__main__":
    _view = {
        "desktop": ft.FLET_APP,
        "webbrowser": ft.WEB_BROWSER,
        "mobile": ft.FLET_APP
    }
    ft.app(target=main, view=_view["webbrowser"])
