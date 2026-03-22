import flet as ft

from DEx_Framework.foundations.components import (
    DS_AppShell,
    DS_Theme_Action,
    HeaderAction,
    DS_Modal,
    ModalAction,
    SidebarItem,
)
from src.core.config.app_config import AppConfig
from src.ui.clientes_screen import build_clientes_screen


def show_main_menu(page: ft.Page, on_logout=None) -> None:
    cfg = AppConfig()

    def _build_placeholder(title: str) -> ft.Control:
        return ft.Text(value=title, size=28, weight="w700")

    theme_manager = cfg.THEME_MANAGER
    header_token = theme_manager.theme.app_shell.header_token

    current_label = "Atendimento"
    pending_label: str | None = None

    content_area = ft.Container(
        expand=True,
        padding=24,
        content=_build_placeholder("Atendimento"),
    )

    menu_items = [
        SidebarItem(
            label="Atendimento",
            icon=ft.Icons.DASHBOARD_OUTLINED,
            selected_icon=ft.Icons.DASHBOARD,
        ),
        SidebarItem(
            label="Clientes",
            icon=ft.Icons.PEOPLE_OUTLINE,
            selected_icon=ft.Icons.PEOPLE,
        ),
        SidebarItem(
            label="Orcamentos",
            icon=ft.Icons.REQUEST_PAGE_OUTLINED,
            selected_icon=ft.Icons.REQUEST_PAGE,
        ),
        SidebarItem(
            label="Ordem de Servicos",
            icon=ft.Icons.BUILD_OUTLINED,
            selected_icon=ft.Icons.BUILD,
        ),
        SidebarItem(
            label="Pecas",
            icon=ft.Icons.INVENTORY_2_OUTLINED,
            selected_icon=ft.Icons.INVENTORY_2,
        ),
        SidebarItem(
            label="Funcionarios",
            icon=ft.Icons.BADGE_OUTLINED,
            selected_icon=ft.Icons.BADGE,
        ),
        SidebarItem(
            label="Usuarios",
            icon=ft.Icons.MANAGE_ACCOUNTS_OUTLINED,
            selected_icon=ft.Icons.MANAGE_ACCOUNTS,
        ),
    ]

    def _proceed_to(label: str) -> None:
        nonlocal current_label
        if label == "Clientes":
            content_area.content = build_clientes_screen(page)
        else:
            content_area.content = _build_placeholder(label)
        current_label = label
        page.update()

    def _confirm_leave(e: ft.ControlEvent) -> None:
        nonlocal pending_label
        leave_modal.close_modal(page)
        if pending_label is not None:
            _proceed_to(pending_label)
        pending_label = None

    def _cancel_leave(e: ft.ControlEvent) -> None:
        nonlocal pending_label
        leave_modal.close_modal(page)
        pending_label = None

    leave_modal = DS_Modal(
        title="Alteracoes nao salvas",
        subtitle="Voce perdera as alteracoes efetuadas.",
        icon=ft.Icons.WARNING_AMBER,
        actions=[
            ModalAction(label="Cancelar", on_click=_cancel_leave, icon=ft.Icons.CLOSE),
            ModalAction(label="Sair", on_click=_confirm_leave, icon=ft.Icons.CHECK, primary=True),
        ],
        theme_manager=theme_manager,
    )

    def _handle_menu_click(idx: int) -> None:
        nonlocal pending_label
        if 0 <= idx < len(menu_items):
            label = menu_items[idx].label
            if label == current_label:
                return
            if current_label == "Clientes":
                guard = getattr(page, "_clientes_guard", None)
                if guard and guard.get("is_dirty", lambda: False)():
                    pending_label = label
                    leave_modal.open_modal(page)
                    return
            _proceed_to(label)

    def _handle_exit(e: ft.ControlEvent) -> None:
        if on_logout:
            on_logout()
            return
        page.controls.clear()
        page.update()

    def _disabled_action(icon_name: str, tooltip: str) -> ft.IconButton:
        return ft.IconButton(
            icon=icon_name,
            icon_color=header_token.action_btn_icon_color,
            icon_size=header_token.action_btn_icon_size,
            tooltip=tooltip,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=header_token.action_btn_bgcolor,
                overlay_color=header_token.action_btn_hover_color,
                shape=ft.CircleBorder(),
                padding=ft.padding.all(8),
            ),
            width=header_token.action_btn_size,
            height=header_token.action_btn_size,
        )

    theme_action = DS_Theme_Action(
        page=page,
        theme_manager=theme_manager,
        auto_apply_theme=True,
        tooltip="Tema",
    )

    header_actions = [
        _disabled_action(ft.Icons.SEARCH, "Pesquisar"),
        _disabled_action(ft.Icons.NOTIFICATIONS, "Notificacoes"),
        _disabled_action(ft.Icons.SETTINGS, "Configuracoes"),
        _disabled_action(ft.Icons.HELP_OUTLINE, "Ajuda"),
        theme_action,
        _disabled_action(ft.Icons.PERSON, "Perfil do usuario"),
        HeaderAction(
            icon=ft.Icons.LOGOUT,
            tooltip="Sair do sistema",
            on_click=_handle_exit,
            visible=True,
        ),
    ]

    app_shell = DS_AppShell(
        title="Gestao da oficina",
        subtitle="Menu principal - Standart",
        items=menu_items,
        logo_path=cfg.LOGO_SRC,
        content=content_area,
        page=page,
        theme_manager=theme_manager,
        on_item_click=_handle_menu_click,
        header_actions=header_actions,
    )

    page.controls.clear()
    page.add(app_shell)
    page.update()
