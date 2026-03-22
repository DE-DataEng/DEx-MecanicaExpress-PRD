import re
from datetime import datetime

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import flet as ft
import requests

from DEx_Framework.foundations.components import (
    DS_Card,
    DS_Checkbox,
    DS_Dropdown,
    DS_Button,
    DS_Table,
    DS_TextField,
    DS_Modal,
    DS_Tabs,
    DS_Search,
    TabItem,
    ModalAction,
    DropdownOption,
    TableColumn,
    TableRow,
)
from src.core.config.app_config import AppConfig
from src.core.config import PostgresConfig
from DEx_Framework.foundations.tokens.tk_table import TK_TableToken


def build_clientes_screen(page: ft.Page) -> ft.Control:
    cfg = AppConfig()
    theme_manager = cfg.THEME_MANAGER

    snack = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.RED_600)

    def _show_snack(text: str, color: str = ft.Colors.RED_600) -> None:
        snack.content = ft.Text(text)
        snack.bgcolor = color
        page.open(snack)

    def _digits_only(value: str) -> str:
        return re.sub(r"\D+", "", value or "")

    def _format_cpf(digits: str) -> str:
        return f"{digits[0:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"

    def _format_cnpj(digits: str) -> str:
        return f"{digits[0:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:14]}"

    def _format_phone(digits: str) -> str:
        if len(digits) == 10:
            return f"({digits[0:2]}) {digits[2:6]}-{digits[6:10]}"
        if len(digits) == 11:
            return f"({digits[0:2]}) {digits[2:7]}-{digits[7:11]}"
        return digits

    def _format_cep(digits: str) -> str:
        if len(digits) == 8:
            return f"{digits[0:5]}-{digits[5:8]}"
        return digits

    def _validate_cpf(digits: str) -> bool:
        if len(digits) != 11 or digits == digits[0] * 11:
            return False
        nums = [int(d) for d in digits]
        soma = sum(nums[i] * (10 - i) for i in range(9))
        resto = soma % 11
        dig1 = 0 if resto < 2 else 11 - resto
        if dig1 != nums[9]:
            return False
        soma = sum(nums[i] * (11 - i) for i in range(10))
        resto = soma % 11
        dig2 = 0 if resto < 2 else 11 - resto
        return dig2 == nums[10]

    def _validate_cnpj(digits: str) -> bool:
        if len(digits) != 14 or digits == digits[0] * 14:
            return False
        nums = [int(d) for d in digits]
        pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(nums[i] * pesos_1[i] for i in range(12))
        resto = soma % 11
        dig1 = 0 if resto < 2 else 11 - resto
        if dig1 != nums[12]:
            return False
        pesos_2 = [6] + pesos_1
        soma = sum(nums[i] * pesos_2[i] for i in range(13))
        resto = soma % 11
        dig2 = 0 if resto < 2 else 11 - resto
        return dig2 == nums[13]

    def _validate_email(value: str) -> bool:
        if not value:
            return True
        return re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", value) is not None

    def _uppercase_letters_only(value: str) -> str:
        result = []
        for ch in value or "":
            if ch.isalpha() or ch.isspace():
                result.append(ch.upper())
        return "".join(result)

    def _uppercase(value: str) -> str:
        return (value or "").upper()

    def _lowercase(value: str) -> str:
        return (value or "").lower()

    def _now_str() -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def _format_dt(value) -> str:
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M:%S")
        return str(value)

    db_cfg = PostgresConfig()
    db_schema = "oficina"
    db_table = "clientes"

    def _fetch_clientes() -> list[dict]:
        query = sql.SQL(
            """
            SELECT id_cliente, nome, tipo_pessoa, cpf_cnpj, rg_ie, telefone, celular,
                   email, cep, endereco, numero, complemento, bairro, cidade, uf,
                   observacoes, ativo, dt_criacao, dt_atualizacao
            FROM {schema}.{table}
            ORDER BY nome
            """
        ).format(
            schema=sql.Identifier(db_schema),
            table=sql.Identifier(db_table),
        )
        with psycopg2.connect(
            host=db_cfg.host,
            port=db_cfg.port,
            dbname=db_cfg.database,
            user=db_cfg.user,
            password=db_cfg.password,
            sslmode=db_cfg.sslmode,
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                rows = cur.fetchall()
        for row in rows:
            row["dt_criacao"] = _format_dt(row.get("dt_criacao"))
            row["dt_atualizacao"] = _format_dt(row.get("dt_atualizacao"))
        return rows

    def _insert_cliente(data: dict) -> int:
        query = sql.SQL(
            """
            INSERT INTO {schema}.{table} (
                nome, tipo_pessoa, cpf_cnpj, rg_ie, telefone, celular, email, cep,
                endereco, numero, complemento, bairro, cidade, uf, observacoes, ativo
            ) VALUES (
                %(nome)s, %(tipo_pessoa)s, %(cpf_cnpj)s, %(rg_ie)s, %(telefone)s,
                %(celular)s, %(email)s, %(cep)s, %(endereco)s, %(numero)s,
                %(complemento)s, %(bairro)s, %(cidade)s, %(uf)s, %(observacoes)s, %(ativo)s
            )
            RETURNING id_cliente
            """
        ).format(
            schema=sql.Identifier(db_schema),
            table=sql.Identifier(db_table),
        )
        with psycopg2.connect(
            host=db_cfg.host,
            port=db_cfg.port,
            dbname=db_cfg.database,
            user=db_cfg.user,
            password=db_cfg.password,
            sslmode=db_cfg.sslmode,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, data)
                new_id = cur.fetchone()[0]
            conn.commit()
        return int(new_id)

    def _update_cliente(data: dict) -> None:
        query = sql.SQL(
            """
            UPDATE {schema}.{table}
            SET nome=%(nome)s,
                tipo_pessoa=%(tipo_pessoa)s,
                cpf_cnpj=%(cpf_cnpj)s,
                rg_ie=%(rg_ie)s,
                telefone=%(telefone)s,
                celular=%(celular)s,
                email=%(email)s,
                cep=%(cep)s,
                endereco=%(endereco)s,
                numero=%(numero)s,
                complemento=%(complemento)s,
                bairro=%(bairro)s,
                cidade=%(cidade)s,
                uf=%(uf)s,
                observacoes=%(observacoes)s,
                ativo=%(ativo)s,
                dt_atualizacao=CURRENT_TIMESTAMP
            WHERE id_cliente=%(id_cliente)s
            """
        ).format(
            schema=sql.Identifier(db_schema),
            table=sql.Identifier(db_table),
        )
        with psycopg2.connect(
            host=db_cfg.host,
            port=db_cfg.port,
            dbname=db_cfg.database,
            user=db_cfg.user,
            password=db_cfg.password,
            sslmode=db_cfg.sslmode,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, data)
            conn.commit()

    def _delete_cliente(id_cliente_value: int) -> None:
        query = sql.SQL(
            "DELETE FROM {schema}.{table} WHERE id_cliente = %s"
        ).format(
            schema=sql.Identifier(db_schema),
            table=sql.Identifier(db_table),
        )
        with psycopg2.connect(
            host=db_cfg.host,
            port=db_cfg.port,
            dbname=db_cfg.database,
            user=db_cfg.user,
            password=db_cfg.password,
            sslmode=db_cfg.sslmode,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (id_cliente_value,))
            conn.commit()

    try:
        clientes_data = _fetch_clientes()
    except Exception:
        clientes_data = []

    selected_id: int | None = None
    pending_action: str | None = None
    edit_snapshot: dict | None = None
    cep_lookup_required = False
    page_size = 10
    current_page = 1
    search_query = ""

    def _action_label() -> str:
        if pending_action == "new":
            return "Inclusão"
        if pending_action == "edit":
            return "Alteração"
        if pending_action == "delete":
            return "Exclusão"
        return "Navegação"

    id_cliente = DS_TextField(label="ID Cliente", state="readonly", theme_manager=theme_manager)
    def _set_value(control: ft.Control, value: str) -> None:
        control.value = value
        if getattr(control, "page", None) is not None:
            control.update()

    nome = DS_TextField(
        label="Nome",
        state="required",
        theme_manager=theme_manager,
        on_change=lambda e: _set_value(e.control, _uppercase_letters_only(e.control.value)),
    )
    tipo_pessoa = DS_Dropdown(
        label="Tipo de pessoa",
        options=[
            DropdownOption(label="Física", value="PF"),
            DropdownOption(label="Jurídica", value="PJ"),
        ],
        state="required",
        theme_manager=theme_manager,
    )
    tipo_pessoa.value = "PF"
    cpf_cnpj = DS_TextField(
        label="CPF/CNPJ",
        theme_manager=theme_manager,
        on_focus=lambda e: _set_value(e.control, _digits_only(e.control.value)),
    )
    rg_ie = DS_TextField(label="RG/IE", theme_manager=theme_manager)
    telefone = DS_TextField(
        label="Telefone",
        theme_manager=theme_manager,
        prefix_icon=ft.Icons.PHONE,
        on_focus=lambda e: _set_value(e.control, _digits_only(e.control.value)),
    )
    celular = DS_TextField(
        label="Celular",
        theme_manager=theme_manager,
        prefix_icon=ft.Icons.PHONE_ANDROID,
        on_focus=lambda e: _set_value(e.control, _digits_only(e.control.value)),
    )
    email = DS_TextField(
        label="Email",
        theme_manager=theme_manager,
        on_change=lambda e: _set_value(e.control, _lowercase(e.control.value)),
    )
    cep = DS_TextField(
        label="CEP",
        theme_manager=theme_manager,
        prefix_icon=ft.Icons.LOCATION_ON,
        on_focus=lambda e: _set_value(e.control, _digits_only(e.control.value)),
    )
    endereco = DS_TextField(
        label="Endereco",
        theme_manager=theme_manager,
        on_change=lambda e: _set_value(e.control, _uppercase(e.control.value)),
    )
    numero = DS_TextField(label="Numero", theme_manager=theme_manager)
    complemento = DS_TextField(label="Complemento", theme_manager=theme_manager)
    bairro = DS_TextField(
        label="Bairro",
        theme_manager=theme_manager,
        on_change=lambda e: _set_value(e.control, _uppercase(e.control.value)),
    )
    cidade = DS_TextField(
        label="Cidade",
        theme_manager=theme_manager,
        on_change=lambda e: _set_value(e.control, _uppercase(e.control.value)),
    )
    uf = DS_Dropdown(
        label="UF",
        options=[
            DropdownOption("AC", "AC"),
            DropdownOption("AL", "AL"),
            DropdownOption("AP", "AP"),
            DropdownOption("AM", "AM"),
            DropdownOption("BA", "BA"),
            DropdownOption("CE", "CE"),
            DropdownOption("DF", "DF"),
            DropdownOption("ES", "ES"),
            DropdownOption("GO", "GO"),
            DropdownOption("MA", "MA"),
            DropdownOption("MT", "MT"),
            DropdownOption("MS", "MS"),
            DropdownOption("MG", "MG"),
            DropdownOption("PA", "PA"),
            DropdownOption("PB", "PB"),
            DropdownOption("PR", "PR"),
            DropdownOption("PE", "PE"),
            DropdownOption("PI", "PI"),
            DropdownOption("RJ", "RJ"),
            DropdownOption("RN", "RN"),
            DropdownOption("RS", "RS"),
            DropdownOption("RO", "RO"),
            DropdownOption("RR", "RR"),
            DropdownOption("SC", "SC"),
            DropdownOption("SP", "SP"),
            DropdownOption("SE", "SE"),
            DropdownOption("TO", "TO"),
        ],
        max_menu_height=120,
        theme_manager=theme_manager,
    )
    uf.content_padding = tipo_pessoa.content_padding
    uf.text_size = tipo_pessoa.text_size
    uf.dense = tipo_pessoa.dense
    observacoes = DS_TextField(
        label="Observacoes",
        multiline=True,
        min_lines=3,
        max_lines=3,
        theme_manager=theme_manager,
    )
    ativo = DS_Checkbox(label="Ativo", value=True, theme_manager=theme_manager)
    dt_criacao = DS_TextField(label="Data de criacao", state="readonly", theme_manager=theme_manager)
    dt_atualizacao = DS_TextField(label="Data de atualizacao", state="readonly", theme_manager=theme_manager)

    editable_text_fields = [
        nome,
        cpf_cnpj,
        rg_ie,
        telefone,
        celular,
        email,
        cep,
        endereco,
        numero,
        complemento,
        bairro,
        cidade,
        observacoes,
    ]
    editable_dropdowns = [tipo_pessoa, uf]

    def _set_form_readonly(readonly: bool) -> None:
        for field in editable_text_fields:
            field.read_only = readonly
        for dd in editable_dropdowns:
            dd.disabled = readonly
        ativo.disabled = readonly
        if _is_mounted():
            page.update()

    def _is_mounted() -> bool:
        return any(
            getattr(ctrl, "page", None) is not None
            for ctrl in [id_cliente, nome, cpf_cnpj, telefone, celular, email, cep, endereco, numero]
        )

    def _apply_action_state() -> None:
        if pending_action == "delete":
            _set_form_readonly(True)
        elif pending_action in ("new", "edit"):
            _set_form_readonly(False)
        else:
            _set_form_readonly(True)
        _apply_action_button_colors()
        _apply_action_buttons_visibility()

    def _apply_cpf_cnpj_mask(e: ft.ControlEvent) -> None:
        digits = _digits_only(e.control.value)
        if not digits:
            return
        if len(digits) == 11:
            if not _validate_cpf(digits):
                _show_snack("CPF invalido.")
            e.control.value = _format_cpf(digits)
        elif len(digits) == 14:
            if not _validate_cnpj(digits):
                _show_snack("CNPJ invalido.")
            e.control.value = _format_cnpj(digits)
        else:
            _show_snack("CPF/CNPJ com tamanho invalido.")
            e.control.value = digits
        e.control.update()

    def _apply_phone_mask(e: ft.ControlEvent) -> None:
        digits = _digits_only(e.control.value)
        if not digits:
            return
        e.control.value = _format_phone(digits)
        e.control.update()

    def _apply_cep_mask(e: ft.ControlEvent) -> None:
        nonlocal cep_lookup_required
        digits = _digits_only(e.control.value)
        if not digits:
            cep_lookup_required = False
            numero.helper_text = None
            if getattr(numero, "page", None) is not None:
                numero.update()
            return
        if len(digits) != 8:
            _show_snack("CEP com tamanho invalido.")
            e.control.value = digits
            e.control.update()
            cep_lookup_required = False
            numero.helper_text = None
            if getattr(numero, "page", None) is not None:
                numero.update()
            return
        e.control.value = _format_cep(digits)
        e.control.update()
        _apply_cep_lookup(digits)
        
    def _apply_cep_lookup(cep_digits: str) -> None:
        nonlocal cep_lookup_required
        try:
            resp = requests.get(f"https://viacep.com.br/ws/{cep_digits}/json/", timeout=5)
            if resp.status_code != 200:
                _show_snack("Falha ao consultar CEP.")
                return
            data = resp.json()
        except Exception:
            _show_snack("Falha ao consultar CEP.")
            return
        if data.get("erro"):
            _show_snack("CEP nao encontrado.")
            return
        cep_lookup_required = True
        numero.helper_text = "Obrigatorio"
        if getattr(numero, "page", None) is not None:
            numero.update()

        logradouro = (data.get("logradouro") or "").strip()
        bairro_val = (data.get("bairro") or "").strip()
        cidade_val = (data.get("localidade") or "").strip()
        uf_val = (data.get("uf") or "").strip()
        complemento_val = (data.get("complemento") or "").strip()

        if logradouro:
            _set_value(endereco, _uppercase(logradouro))
        if bairro_val:
            _set_value(bairro, _uppercase(bairro_val))
        if cidade_val:
            _set_value(cidade, _uppercase(cidade_val))
        if uf_val:
            uf.value = uf_val.upper()
            uf.update()
        if complemento_val:
            _set_value(complemento, complemento_val)

    def _validate_email_blur(e: ft.ControlEvent) -> None:
        value = (e.control.value or "").strip()
        if not _validate_email(value):
            _show_snack("Email invalido.")

    cpf_cnpj.on_blur = _apply_cpf_cnpj_mask
    telefone.on_blur = _apply_phone_mask
    celular.on_blur = _apply_phone_mask
    cep.on_blur = _apply_cep_mask
    email.on_blur = _validate_email_blur

    def _set_form(cliente: dict) -> None:
        nonlocal selected_id
        selected_id = cliente.get("id_cliente")
        id_cliente.value = str(cliente.get("id_cliente", "") or "")
        nome.value = cliente.get("nome", "") or ""
        tipo_pessoa.value = cliente.get("tipo_pessoa", "") or "PF"
        cpf_cnpj.value = cliente.get("cpf_cnpj", "") or ""
        rg_ie.value = cliente.get("rg_ie", "") or ""
        telefone.value = cliente.get("telefone", "") or ""
        celular.value = cliente.get("celular", "") or ""
        email.value = cliente.get("email", "") or ""
        cep.value = cliente.get("cep", "") or ""
        endereco.value = cliente.get("endereco", "") or ""
        numero.value = cliente.get("numero", "") or ""
        complemento.value = cliente.get("complemento", "") or ""
        bairro.value = cliente.get("bairro", "") or ""
        cidade.value = cliente.get("cidade", "") or ""
        uf.value = cliente.get("uf", "") or ""
        observacoes.value = cliente.get("observacoes", "") or ""
        ativo.value = bool(cliente.get("ativo", True))
        dt_criacao.value = cliente.get("dt_criacao", "") or _now_str()
        dt_atualizacao.value = cliente.get("dt_atualizacao", "") or _now_str()
        if _is_mounted():
            page.update()

    def _update_action_subtitle() -> None:
        action_state_text.value = f"- {_action_label()}"
        if getattr(action_state_text, "page", None) is not None:
            action_state_text.update()

    def _collect_form() -> dict:
        def _null_if_empty(value: str):
            v = (value or "").strip()
            return v if v else None
        return {
            "id_cliente": int(id_cliente.value) if str(id_cliente.value or "").isdigit() else None,
            "nome": (nome.value or "").strip(),
            "tipo_pessoa": _null_if_empty(tipo_pessoa.value or ""),
            "cpf_cnpj": _null_if_empty(_digits_only(cpf_cnpj.value)),
            "rg_ie": _null_if_empty(rg_ie.value or ""),
            "telefone": _null_if_empty(_digits_only(telefone.value)),
            "celular": _null_if_empty(_digits_only(celular.value)),
            "email": _null_if_empty(email.value or ""),
            "cep": _null_if_empty(_digits_only(cep.value)),
            "endereco": _null_if_empty(endereco.value or ""),
            "numero": _null_if_empty(numero.value or ""),
            "complemento": _null_if_empty(complemento.value or ""),
            "bairro": _null_if_empty(bairro.value or ""),
            "cidade": _null_if_empty(cidade.value or ""),
            "uf": _null_if_empty(uf.value or ""),
            "observacoes": _null_if_empty(observacoes.value or ""),
            "ativo": bool(ativo.value),
            "dt_criacao": dt_criacao.value or _now_str(),
            "dt_atualizacao": _now_str(),
        }

    def _collect_form_state() -> dict:
        return {
            "id_cliente": int(id_cliente.value) if str(id_cliente.value or "").isdigit() else None,
            "nome": (nome.value or "").strip(),
            "tipo_pessoa": tipo_pessoa.value or "",
            "cpf_cnpj": _digits_only(cpf_cnpj.value),
            "rg_ie": rg_ie.value or "",
            "telefone": _digits_only(telefone.value),
            "celular": _digits_only(celular.value),
            "email": (email.value or "").strip(),
            "cep": _digits_only(cep.value),
            "endereco": (endereco.value or "").strip(),
            "numero": (numero.value or "").strip(),
            "complemento": complemento.value or "",
            "bairro": (bairro.value or "").strip(),
            "cidade": (cidade.value or "").strip(),
            "uf": uf.value or "",
            "observacoes": observacoes.value or "",
            "ativo": bool(ativo.value),
            "dt_criacao": dt_criacao.value or "",
        }

    def _is_dirty() -> bool:
        if pending_action != "edit" or edit_snapshot is None:
            return False
        return _collect_form_state() != edit_snapshot

    def _refresh_table(keep_id: int | None = None) -> None:
        nonlocal clientes_data, current_page
        try:
            clientes_data = _fetch_clientes()
        except Exception:
            _show_snack("Falha ao carregar clientes do banco.")
            clientes_data = clientes_data or []
        total = _total_pages()
        if current_page > total:
            current_page = total
        table._rows = _table_rows()
        table._refresh()
        pagination_text.value = f"pag {current_page} de {total}"
        if getattr(pagination_text, "page", None) is not None:
            pagination_text.update()
        if keep_id is not None:
            for cliente in clientes_data:
                if cliente.get("id_cliente") == keep_id:
                    _set_form(cliente)
                    _mark_selected_row()
                    return
        _mark_selected_row()

    def _handle_confirm(e: ft.ControlEvent) -> None:
        nonlocal pending_action, edit_snapshot
        data = _collect_form()
        if not data.get("nome"):
            _show_snack("Nome obrigatorio.")
            return
        if not data.get("tipo_pessoa"):
            _show_snack("Tipo de pessoa obrigatorio.")
            return
        if cep_lookup_required and not (numero.value or "").strip():
            _show_snack("Numero obrigatorio.")
            return
        if pending_action == "delete":
            if data.get("id_cliente") is None:
                _show_snack("Selecione um cliente para excluir.")
                return
            delete_confirm_modal.open_modal(page)
            return

        if data.get("id_cliente") is None:
            try:
                new_id = _insert_cliente(data)
            except Exception:
                _show_snack("Falha ao incluir cliente.")
                return
            pending_action = None
            _refresh_table(new_id)
            _show_snack("Cliente incluido.", ft.Colors.GREEN_600)
            _update_action_subtitle()
            _apply_action_state()
            return

        try:
            _update_cliente(data)
        except Exception:
            _show_snack("Falha ao atualizar cliente.")
            return
        pending_action = None
        edit_snapshot = None
        _refresh_table(data["id_cliente"])
        _show_snack("Cliente atualizado.", ft.Colors.GREEN_600)
        _update_action_subtitle()
        _apply_action_state()
        return

    def _handle_cancel_confirm(e: ft.ControlEvent | None = None) -> None:
        nonlocal pending_action, edit_snapshot
        pending_action = None
        edit_snapshot = None
        if selected_id is not None:
            _refresh_table(selected_id)
        elif clientes_data:
            _refresh_table(clientes_data[0].get("id_cliente"))
        _update_action_subtitle()
        _apply_action_state()

    def _handle_cancel(e: ft.ControlEvent) -> None:
        if pending_action == "delete":
            _handle_cancel_confirm()
            return
        needs_confirm = pending_action == "new" or _is_dirty()
        if not needs_confirm:
            _handle_cancel_confirm()
            return
        cancel_modal.open_modal(page)

    def _handle_new(e: ft.ControlEvent) -> None:
        nonlocal pending_action
        pending_action = "new"
        _set_form({
            "id_cliente": "",
            "nome": "",
            "tipo_pessoa": "PF",
            "cpf_cnpj": "",
            "rg_ie": "",
            "telefone": "",
            "celular": "",
            "email": "",
            "cep": "",
            "endereco": "",
            "numero": "",
            "complemento": "",
            "bairro": "",
            "cidade": "",
            "uf": "",
            "observacoes": "",
            "ativo": True,
            "dt_criacao": _now_str(),
            "dt_atualizacao": _now_str(),
        })
        _update_action_subtitle()
        _apply_action_state()

    def _handle_edit(cliente: dict):
        def _inner(e: ft.ControlEvent) -> None:
            nonlocal pending_action, edit_snapshot
            pending_action = "edit"
            _set_form(cliente)
            edit_snapshot = _collect_form_state()
            _update_action_subtitle()
            _apply_action_state()
        return _inner

    def _handle_delete(cliente: dict):
        def _inner(e: ft.ControlEvent) -> None:
            nonlocal pending_action, edit_snapshot
            pending_action = "delete"
            _set_form(cliente)
            edit_snapshot = None
            _update_action_subtitle()
            _apply_action_state()
        return _inner

    def _build_action_button(
        *,
        icon,
        tooltip,
        on_click,
        icon_only=True,
        width=28,
        height=28,
        icon_color=None,
        bg_color=None,
    ):
        btn = DS_Button(
            icon=icon,
            icon_only=icon_only,
            width=width,
            height=height,
            tooltip=tooltip,
            on_click=on_click,
            theme_manager=None,
            auto_apply_theme=False,
        )
        if icon_color is not None and getattr(btn, "_icon_control", None) is not None:
            btn._icon_control.color = icon_color
        if bg_color is not None:
            btn.style = ft.ButtonStyle(
                bgcolor=bg_color,
                color="transparent",
                shape=ft.RoundedRectangleBorder(radius=6),
                padding=ft.padding.all(0),
                alignment=ft.alignment.center,
            )
        return btn

    def _filtered_clientes() -> list[dict]:
        if not search_query:
            return clientes_data
        term = search_query.strip().lower()
        if not term:
            return clientes_data
        result = []
        for cliente in clientes_data:
            for value in cliente.values():
                if value is None:
                    continue
                if term in str(value).lower():
                    result.append(cliente)
                    break
        return result

    def _total_pages() -> int:
        data = _filtered_clientes()
        if not data:
            return 1
        return max(1, (len(data) + page_size - 1) // page_size)

    def _page_slice() -> list[dict]:
        data = _filtered_clientes()
        start = (current_page - 1) * page_size
        end = start + page_size
        return data[start:end]

    def _table_rows() -> list[TableRow]:
        nonlocal selected_id
        rows = []
        page_rows = _page_slice()
        for idx, cliente in enumerate(page_rows):
            def _make_handler(data):
                def _handler(e: ft.ControlEvent) -> None:
                    _set_form(data)
                    _mark_selected_row()
                return _handler
            cliente_with_actions = dict(cliente)
            cliente_with_actions["acoes"] = cliente
            rows.append(
                TableRow(
                    data=cliente_with_actions,
                    on_click=_make_handler(cliente),
                )
            )
        return rows

    base_table_token = theme_manager.theme.table
    compact_table_token = TK_TableToken(**{
        **vars(base_table_token),
        "cell_padding_vertical": 4,
    })

    table = DS_Table(
        columns=[
            TableColumn(
                label="Ativo",
                key="ativo",
                render=lambda v: ft.Icon(
                    name=ft.Icons.CHECK_CIRCLE if v else ft.Icons.CANCEL,
                    color=ft.Colors.GREEN_600 if v else ft.Colors.RED_600,
                    size=18,
                ),
            ),
            TableColumn(label="Nome", key="nome"),
            TableColumn(
                label="Celular",
                key="celular",
                render=lambda v: ft.Text(_format_phone(_digits_only(str(v)))),
            ),
            TableColumn(label="Tipo", key="tipo_pessoa"),
            TableColumn(
                label="Acoes",
                key="acoes",
                render=lambda v: ft.Row(
                    spacing=6,
                    controls=[
                        _build_action_button(
                            icon=ft.Icons.EDIT,
                            icon_only=True,
                            width=28,
                            height=28,
                            tooltip="Alterar",
                            on_click=_handle_edit(v),
                            icon_color=ft.Colors.WHITE,
                            bg_color=ft.Colors.GREEN_400,
                        ),
                        _build_action_button(
                            icon=ft.Icons.DELETE,
                            icon_only=True,
                            width=28,
                            height=28,
                            tooltip="Excluir",
                            on_click=_handle_delete(v),
                            icon_color=ft.Colors.WHITE,
                            bg_color=ft.Colors.RED_400,
                        ),
                    ],
                ),
            ),
        ],
        rows=_table_rows(),
        selectable=False,
        token=compact_table_token,
        theme_manager=None,
        auto_apply_theme=False,
    )

    def _mark_selected_row() -> None:
        table._selected = set()
        page_rows = _page_slice()
        for idx, cliente in enumerate(page_rows):
            if cliente.get("id_cliente") == selected_id:
                table._selected = {idx}
                break
        table._refresh()

    table_view = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row(
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[table],
                ),
            ],
        ),
    )

    add_button = DS_Button(
        icon=ft.Icons.ADD,
        icon_only=True,
        tooltip="Incluir cliente",
        on_click=_handle_new,
        theme_manager=None,
        auto_apply_theme=False,
    )
    if getattr(add_button, "_icon_control", None) is not None:
        add_button._icon_control.color = ft.Colors.WHITE
    add_button.style = ft.ButtonStyle(
        bgcolor=ft.Colors.BLUE_600,
        color="transparent",
        shape=ft.RoundedRectangleBorder(radius=6),
        padding=ft.padding.all(0),
        alignment=ft.alignment.center,
    )
    pagination_text = ft.Text(value="pag 1 de 1")

    def _set_page(new_page: int) -> None:
        nonlocal current_page
        total = _total_pages()
        current_page = max(1, min(total, new_page))
        table._rows = _table_rows()
        table._refresh()
        _mark_selected_row()
        pagination_text.value = f"pag {current_page} de {total}"
        if getattr(pagination_text, "page", None) is not None:
            pagination_text.update()

    def _select_by_index(idx: int) -> None:
        page_rows = _page_slice()
        if not page_rows:
            return
        idx = max(0, min(len(page_rows) - 1, idx))
        _set_form(page_rows[idx])
        _mark_selected_row()

    def _handle_table_keys(e: ft.KeyboardEvent) -> None:
        key = (e.key or "").lower()
        if key == "escape":
            if search_query:
                _clear_search()
            return
        if pending_action is not None:
            return
        if not clientes_data:
            return
        page_rows = _page_slice()
        if not page_rows:
            return
        current_idx = 0
        for i, row in enumerate(page_rows):
            if row.get("id_cliente") == selected_id:
                current_idx = i
                break
        if key == "arrow down":
            if current_idx < len(page_rows) - 1:
                _select_by_index(current_idx + 1)
            elif current_page < _total_pages():
                _set_page(current_page + 1)
                _select_by_index(0)
        elif key == "arrow up":
            if current_idx > 0:
                _select_by_index(current_idx - 1)
            elif current_page > 1:
                _set_page(current_page - 1)
                _select_by_index(len(_page_slice()) - 1)
        elif key == "page down":
            if current_page < _total_pages():
                _set_page(current_page + 1)
                _select_by_index(min(current_idx, len(_page_slice()) - 1))
        elif key == "page up":
            if current_page > 1:
                _set_page(current_page - 1)
                _select_by_index(min(current_idx, len(_page_slice()) - 1))
        elif key == "home":
            _select_by_index(0)
        elif key == "end":
            _select_by_index(len(page_rows) - 1)

    def _first_page(e: ft.ControlEvent) -> None:
        _set_page(1)

    def _prev_page(e: ft.ControlEvent) -> None:
        _set_page(current_page - 1)

    def _next_page(e: ft.ControlEvent) -> None:
        _set_page(current_page + 1)

    def _last_page(e: ft.ControlEvent) -> None:
        _set_page(_total_pages())

    nav_btn_size = 28
    pagination_refresh_button = DS_Button(
        icon=ft.Icons.REFRESH,
        icon_only=True,
        width=nav_btn_size,
        height=nav_btn_size,
        tooltip="Atualizar tabela",
        on_click=lambda e: _refresh_table(selected_id),
        theme_manager=None,
        auto_apply_theme=False,
    )
    pagination_controls = ft.Row(
        spacing=6,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            DS_Button(
                icon=ft.Icons.FIRST_PAGE,
                icon_only=True,
                width=nav_btn_size,
                height=nav_btn_size,
                tooltip="Primeira pagina",
                on_click=_first_page,
                theme_manager=None,
                auto_apply_theme=False,
            ),
            DS_Button(
                icon=ft.Icons.CHEVRON_LEFT,
                icon_only=True,
                width=nav_btn_size,
                height=nav_btn_size,
                tooltip="Pagina anterior",
                on_click=_prev_page,
                theme_manager=None,
                auto_apply_theme=False,
            ),
            pagination_refresh_button,
            DS_Button(
                icon=ft.Icons.CHEVRON_RIGHT,
                icon_only=True,
                width=nav_btn_size,
                height=nav_btn_size,
                tooltip="Proxima pagina",
                on_click=_next_page,
                theme_manager=None,
                auto_apply_theme=False,
            ),
            DS_Button(
                icon=ft.Icons.LAST_PAGE,
                icon_only=True,
                width=nav_btn_size,
                height=nav_btn_size,
                tooltip="Ultima pagina",
                on_click=_last_page,
                theme_manager=None,
                auto_apply_theme=False,
            ),
            pagination_text,
        ],
    )

    page_size_value = "10"
    page_size_display = DS_Button(
        label=page_size_value,
        icon_only=False,
        disabled=True,
        width=44,
        tooltip="Linhas por pagina",
        theme_manager=None,
        auto_apply_theme=False,
    )
    page_size_display.style = ft.ButtonStyle(
        bgcolor=ft.Colors.GREY_700,
        color=ft.Colors.WHITE,
        shape=ft.RoundedRectangleBorder(radius=6),
        padding=ft.padding.all(0),
        alignment=ft.alignment.center,
    )
    page_size_button = DS_Button(
        label="",
        icon=ft.Icons.ARROW_DROP_DOWN,
        icon_only=True,
        width=28,
        height=28,
        tooltip="Linhas por pagina",
        on_click=lambda e: None,
        theme_manager=None,
        auto_apply_theme=False,
    )

    def _set_page_size(new_value: str) -> None:
        nonlocal page_size, current_page, page_size_value
        page_size_value = new_value
        page_size_display.text = new_value
        try:
            page_size = int(new_value)
        except Exception:
            page_size = 10
        current_page = 1
        _set_page(current_page)
        if getattr(page_size_display, "page", None) is not None:
            page_size_display.update()

    def _close_page_size_modal(e: ft.ControlEvent) -> None:
        page_size_modal.close_modal(page)

    def _make_page_size_action(val: str):
        return lambda e: (_set_page_size(val), page_size_modal.close_modal(page))

    page_size_modal = DS_Modal(
        title="Linhas por pagina",
        subtitle="Selecione a quantidade",
        icon=ft.Icons.FORMAT_LIST_NUMBERED,
        actions=[
            ModalAction(label="5", on_click=_make_page_size_action("5")),
            ModalAction(label="10", on_click=_make_page_size_action("10"), primary=True),
            ModalAction(label="20", on_click=_make_page_size_action("20")),
            ModalAction(label="50", on_click=_make_page_size_action("50")),
            ModalAction(label="100", on_click=_make_page_size_action("100")),
            ModalAction(label="200", on_click=_make_page_size_action("200")),
            ModalAction(label="Fechar", on_click=_close_page_size_modal, icon=ft.Icons.CLOSE),
        ],
        theme_manager=None,
        auto_apply_theme=False,
    )

    def _open_page_size_modal(e: ft.ControlEvent) -> None:
        page_size_modal.open_modal(page)

    page_size_button.on_click = _open_page_size_modal

    page_size_wrapper = ft.Row(
        spacing=4,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[page_size_display, page_size_button],
    )


    search_field = DS_Search(
        hint_text="Buscar em todas as colunas",
        width=220,
        theme_manager=theme_manager,
    )
    search_field.height = nav_btn_size

    def _apply_search_now() -> None:
        nonlocal search_query, current_page
        search_query = (search_field.value or "").strip()
        current_page = 1
        table._rows = _table_rows()
        table._refresh()
        pagination_text.value = f"pag {current_page} de {_total_pages()}"
        if getattr(pagination_text, "page", None) is not None:
            pagination_text.update()

    def _apply_search_debounced(e: ft.ControlEvent) -> None:
        # Flet 0.28.3 nao possui Timer: aplica imediatamente
        _apply_search_now()

    def _clear_search() -> None:
        search_field.value = ""
        if getattr(search_field, "page", None) is not None:
            search_field.update()
        _apply_search_now()

    search_field.on_change = _apply_search_debounced

    left_panel = DS_Card(
        title="Clientes",
        subtitle="Lista de clientes",
        icon=ft.Icons.PEOPLE,
        content=ft.Container(
            padding=8,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(height=1),
                    ft.Row(
                        spacing=8,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    add_button,
                                    ft.Container(expand=True, content=search_field),
                                ],
                            ),
                        ],
                    ),
                    table_view,
                    ft.Container(height=1),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        spacing=8,
                        controls=[
                            pagination_controls,
                            page_size_wrapper,
                        ],
                    ),
                ],
                spacing=4,
            ),
        ),
        theme_manager=None,
        auto_apply_theme=False,
    )

    action_title_text = ft.Text(
        value="Cadastro completo",
        size=12,
        weight="normal",
    )
    action_state_text = ft.Text(
        value=f"- {_action_label()}",
        size=16,
        weight="bold",
    )

    focus_fields = [
        nome,
        cpf_cnpj,
        rg_ie,
        telefone,
        celular,
        email,
        cep,
        endereco,
        numero,
        complemento,
        bairro,
        cidade,
        observacoes,
    ]

    def _focus_next(current: ft.Control) -> None:
        if pending_action not in ("new", "edit"):
            return
        try:
            idx = focus_fields.index(current)
        except ValueError:
            return
        next_idx = (idx + 1) % len(focus_fields)
        focus_fields[next_idx].focus()
        page.update()

    for field in focus_fields:
        field.on_submit = (lambda f: lambda e: _focus_next(f))(field)

    confirm_button = DS_Button(
        label="Confirmar",
        icon=ft.Icons.CHECK,
        on_click=_handle_confirm,
        theme_manager=None,
        auto_apply_theme=False,
    )
    cancel_button = DS_Button(
        label="Cancelar",
        icon=ft.Icons.CLOSE,
        on_click=_handle_cancel,
        theme_manager=None,
        auto_apply_theme=False,
    )
    action_buttons_row = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        spacing=12,
        controls=[cancel_button, confirm_button],
    )

    def _apply_action_button_colors() -> None:
        if pending_action == "delete":
            confirm_bg = ft.Colors.RED_600
            cancel_bg = ft.Colors.BLUE_500
        else:
            confirm_bg = ft.Colors.GREEN_600
            cancel_bg = ft.Colors.RED_600
        confirm_button.style = ft.ButtonStyle(
            bgcolor=confirm_bg,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        cancel_button.style = ft.ButtonStyle(
            bgcolor=cancel_bg,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        if getattr(confirm_button, "page", None) is not None:
            confirm_button.update()
        if getattr(cancel_button, "page", None) is not None:
            cancel_button.update()

    def _apply_action_buttons_visibility() -> None:
        visible = pending_action in ("new", "edit", "delete")
        action_buttons_row.visible = visible
        if getattr(action_buttons_row, "page", None) is not None:
            action_buttons_row.update()

    cadastro_content = ft.Column(
        spacing=12,
        controls=[
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=4, content=id_cliente),
                    ft.Container(col=8, content=nome),
                ],
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=4, content=tipo_pessoa),
                    ft.Container(col=8, content=cpf_cnpj),
                ],
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=4, content=rg_ie),
                    ft.Container(col=4, content=telefone),
                    ft.Container(col=4, content=celular),
                ],
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=6, content=email),
                    ft.Container(col=3, content=cep),
                    ft.Container(col=3, content=uf),
                ],
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=6, content=endereco),
                    ft.Container(col=2, content=numero),
                    ft.Container(col=4, content=complemento),
                ],
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=4, content=bairro),
                    ft.Container(col=4, content=cidade),
                    ft.Container(col=4, content=ativo),
                ],
            ),
            observacoes,
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col=6, content=dt_criacao),
                    ft.Container(col=6, content=dt_atualizacao),
                ],
            ),
            action_buttons_row,
        ],
    )

    ordens_content = ft.Container(
        padding=12,
        content=ft.Text("Ordens de serviço", size=16, weight="bold"),
    )

    veiculos_content = ft.Container(
        padding=12,
        content=ft.Text("Veículos", size=16, weight="bold"),
    )
    orcamentos_content = ft.Container(
        padding=12,
        content=ft.Text("Orçamentos", size=16, weight="bold"),
    )
    financeiro_content = ft.Container(
        padding=12,
        content=ft.Text("Financeiro", size=16, weight="bold"),
    )

    tabs = DS_Tabs(
        tabs=[
            TabItem(label="Cadastro", content=cadastro_content, icon=ft.Icons.BADGE),
            TabItem(label="Ordens de serviço", content=ordens_content, icon=ft.Icons.BUILD),
            TabItem(label="Veículos", content=veiculos_content, icon=ft.Icons.DIRECTIONS_CAR),
            TabItem(label="Orçamentos", content=orcamentos_content, icon=ft.Icons.RECEIPT_LONG),
            TabItem(label="Financeiro", content=financeiro_content, icon=ft.Icons.ACCOUNT_BALANCE_WALLET),
        ],
        selected_index=0,
        expand_content=False,
        theme_manager=theme_manager,
    )

    form = ft.Column(
        spacing=12,
        controls=[
            ft.Row(
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    action_title_text,
                    action_state_text,
                ],
            ),
            tabs,
        ],
    )

    def _close_cancel_modal(e: ft.ControlEvent) -> None:
        cancel_modal.close_modal(page)

    def _confirm_cancel_modal(e: ft.ControlEvent) -> None:
        cancel_modal.close_modal(page)
        _handle_cancel_confirm()

    cancel_modal = DS_Modal(
        title="Cancelar operacao",
        subtitle="Voce perdera as alteracoes efetuadas.",
        icon=ft.Icons.WARNING_AMBER,
        actions=[
            ModalAction(label="Voltar", on_click=_close_cancel_modal, icon=ft.Icons.ARROW_BACK),
            ModalAction(label="Cancelar operacao", on_click=_confirm_cancel_modal, icon=ft.Icons.CLOSE, primary=True),
        ],
        theme_manager=None,
        auto_apply_theme=False,
    )

    def _close_delete_modal(e: ft.ControlEvent) -> None:
        delete_confirm_modal.close_modal(page)

    def _confirm_delete_modal(e: ft.ControlEvent) -> None:
        nonlocal pending_action
        delete_confirm_modal.close_modal(page)
        data = _collect_form()
        try:
            _delete_cliente(int(data["id_cliente"]))
        except Exception:
            _show_snack("Falha ao excluir cliente.")
            return
        pending_action = None
        _refresh_table()
        if clientes_data:
            _set_form(clientes_data[0])
        _show_snack("Cliente excluido.", ft.Colors.GREEN_600)
        _update_action_subtitle()
        _apply_action_state()

    delete_confirm_modal = DS_Modal(
        title="Confirmar exclusao",
        subtitle="Esta acao e irreversivel. Deseja continuar?",
        icon=ft.Icons.DELETE_FOREVER,
        actions=[
            ModalAction(label="Voltar", on_click=_close_delete_modal, icon=ft.Icons.ARROW_BACK),
            ModalAction(label="Excluir", on_click=_confirm_delete_modal, icon=ft.Icons.DELETE, primary=True),
        ],
        theme_manager=None,
        auto_apply_theme=False,
    )

    right_panel = DS_Card(
        title="Detalhes do cliente",
        subtitle="",
        icon=ft.Icons.BADGE,
        content=form,
        theme_manager=None,
        auto_apply_theme=False,
    )

    layout = ft.Row(
        expand=True,
        spacing=16,
        controls=[
            ft.Container(expand=4, content=left_panel),
            ft.Container(expand=8, content=right_panel),
        ],
    )

    if clientes_data:
        _set_form(clientes_data[0])
        _update_action_subtitle()
        _apply_action_state()
        _mark_selected_row()

    page.on_keyboard_event = _handle_table_keys

    page._clientes_guard = {
        "is_dirty": _is_dirty,
    }

    return layout
