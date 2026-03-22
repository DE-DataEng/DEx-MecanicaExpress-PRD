# DEx MecanicaExpress

## Visao geral
Aplicacao em Python/Flet para a MecanicaExpress.

## Requisitos
- Python 3.10 (definido em `runtime.txt` e `render.yaml`)
- Flet 0.28.3 (definido em `requirements.txt`)

## Execucao local (local)
1. Crie e ative o ambiente virtual (virtual environment):
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Instale dependencias (dependencies):
   ```powershell
   pip install -r requirements.txt
   ```
3. Execute a aplicacao:
   ```powershell
   python main.py
   ```
4. A aplicacao inicia em `http://localhost:8000`.

## Deploy no Render
### Passos (Render)
1. Crie um novo servico do tipo `Web Service` (servico web).
2. Conecte este repositorio.
3. O Render detectara o `render.yaml` e aplicara:
   - `buildCommand`: `pip install -r requirements.txt`
   - `startCommand`: `python main.py`
   - `PYTHON_VERSION`: `3.10.13`
4. Garanta que a variavel de ambiente `PORT` seja numerica (ex.: `8000`), sem `"$PORT"`.

## Observacoes
- O app inicia com `ft.app(..., host="0.0.0.0", port=PORT)`, adequado para execucao web.
- Se houver falha de porta, verifique se `PORT` esta definido como numero.
