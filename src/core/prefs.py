from __future__ import annotations

from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _prefs_path() -> Path:
    return _project_root() / "prefs.ini"


@dataclass
class UserPrefs:
    theme: str = "default"
    window_x: int | None = None
    window_y: int | None = None
    window_width: int | None = None
    window_height: int | None = None
    username: str = ""

    @classmethod
    def load(cls) -> "UserPrefs":
        path = _prefs_path()
        if not path.exists():
            return cls()
        parser = ConfigParser()
        parser.read(path, encoding="utf-8")

        theme = parser.get("tema", "nome", fallback="default")
        username = parser.get("usuario", "nome", fallback="")

        def _get_int(section: str, key: str) -> int | None:
            if not parser.has_option(section, key):
                return None
            value = parser.get(section, key, fallback="").strip()
            if value == "":
                return None
            try:
                return int(value)
            except ValueError:
                return None

        return cls(
            theme=theme,
            window_x=_get_int("janela", "x"),
            window_y=_get_int("janela", "y"),
            window_width=_get_int("janela", "largura"),
            window_height=_get_int("janela", "altura"),
            username=username,
        )

    def save(self) -> None:
        parser = ConfigParser()
        parser["tema"] = {"nome": self.theme}
        parser["usuario"] = {"nome": self.username}
        parser["janela"] = {
            "x": "" if self.window_x is None else str(self.window_x),
            "y": "" if self.window_y is None else str(self.window_y),
            "largura": "" if self.window_width is None else str(self.window_width),
            "altura": "" if self.window_height is None else str(self.window_height),
        }
        path = _prefs_path()
        path.write_text(_to_ini_text(parser), encoding="utf-8")


def _to_ini_text(parser: ConfigParser) -> str:
    lines: list[str] = []
    for section in parser.sections():
        lines.append(f"[{section}]")
        for key, value in parser[section].items():
            lines.append(f"{key} = {value}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
