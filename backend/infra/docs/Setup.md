# Setup

## Objetivo
Documentar como preparar o modulo `infra` para uso local no workspace.

## Pre-Requisitos

- Python 3.12+
- `uv`

## Execucao No Workspace

Da raiz do repositorio:

```bash
uv sync --all-packages
```

## Validacao Rapida

```bash
uv run --package infra python -c "import infra; print(infra.__name__)"
```
