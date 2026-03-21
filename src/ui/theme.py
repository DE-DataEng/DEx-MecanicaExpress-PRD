import flet as ft

COLOR_PRIMARY = "#0A2A6B"
COLOR_PRIMARY_LIGHT = "#184FD1"
COLOR_PRIMARY_DARK = "#081F4A"
COLOR_ACCENT = "#FF8A00"
COLOR_ACCENT_DARK = "#D96A00"
COLOR_BG = "#0B1020"
COLOR_SURFACE = "#111A33"
COLOR_SURFACE_2 = "#162349"
COLOR_TEXT = "#F5F7FB"
COLOR_TEXT_MUTED = "#B8C2D6"


def app_theme() -> ft.Theme:
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=COLOR_PRIMARY,
            secondary=COLOR_ACCENT,
            surface=COLOR_SURFACE,
            background=COLOR_BG,
            on_primary="#FFFFFF",
            on_secondary="#0B1020",
            on_surface=COLOR_TEXT,
            on_background=COLOR_TEXT,
        )
    )
