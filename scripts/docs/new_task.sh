#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Uso:
  scripts/docs/new_task.sh --scope root --titulo "Titulo da tarefa" [--status "Pendente"] [--risco "Media / Medio prazo"] [--commit "-"] [--branch "-"]
  scripts/docs/new_task.sh --scope service --service account-service --titulo "Titulo da tarefa" [--status "Pendente"] [--risco "Media / Medio prazo"] [--commit "-"] [--branch "-"]

Regras:
  - --scope root: apenas tarefas de escopo geral do monorepo.
  - --scope service: tarefas especificas de um servico.
USAGE
}

scope=""
service=""
titulo=""
status="Pendente"
risco="Media / Medio prazo"
commit_ref=""
branch_ref=""

today="$(date +%F)"

slugify() {
  local value="$1"
  local slug
  if command -v iconv >/dev/null 2>&1; then
    slug="$(printf '%s' "$value" | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null || printf '%s' "$value")"
  else
    slug="$value"
  fi

  slug="$(printf '%s' "$slug" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-{2,}/-/g')"

  if [[ -z "$slug" ]]; then
    slug="tarefa"
  fi

  printf '%s' "$slug"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope)
      scope="${2:-}"
      shift 2
      ;;
    --service)
      service="${2:-}"
      shift 2
      ;;
    --titulo)
      titulo="${2:-}"
      shift 2
      ;;
    --status)
      status="${2:-}"
      shift 2
      ;;
    --risco)
      risco="${2:-}"
      shift 2
      ;;
    --commit)
      commit_ref="${2:-}"
      shift 2
      ;;
    --branch)
      branch_ref="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Argumento invalido: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$scope" || -z "$titulo" ]]; then
  echo "Erro: --scope e --titulo sao obrigatorios." >&2
  usage
  exit 1
fi

case "$scope" in
  root)
    target_dir="docs/tasks"
    scope_label="Geral do monorepo"
    service_label="-"
    ;;
  service)
    if [[ -z "$service" ]]; then
      echo "Erro: --service e obrigatorio quando --scope service." >&2
      exit 1
    fi
    target_dir="src/services/${service}/docs/tasks"
    scope_label="Servico"
    service_label="$service"
    ;;
  *)
    echo "Erro: --scope deve ser root ou service." >&2
    exit 1
    ;;
esac

mkdir -p "$target_dir"

last_number="$(find "$target_dir" -maxdepth 1 -type f -name 'task-*.md' \
  | sed -E 's/.*task-([0-9]{3})-.*/\1/' \
  | sort -n \
  | tail -n 1)"

if [[ -z "$last_number" ]]; then
  next_number=1
else
  next_number=$((10#$last_number + 1))
fi

number_padded="$(printf '%03d' "$next_number")"
slug="$(slugify "$titulo")"
file_path="$target_dir/task-${number_padded}-${slug}.md"

if [[ "$status" == Concluida* ]]; then
  completion_date="$today"
  if [[ -z "$commit_ref" ]]; then
    commit_ref="nao informado (registrar hash apos commit)"
  fi
  if [[ -z "$branch_ref" ]]; then
    branch_ref="nao informada (registrar nome apos commit)"
  fi
else
  completion_date="-"
  if [[ -z "$commit_ref" ]]; then
    commit_ref="-"
  fi
  if [[ -z "$branch_ref" ]]; then
    branch_ref="-"
  fi
fi

cat > "$file_path" <<TASK
# Tarefa ${number_padded} - ${titulo}

## Metadados
- Data de criacao: ${today}
- Data de finalizacao: ${completion_date}
- Commit de implementacao: ${commit_ref}
- Branch de implementacao: ${branch_ref}
- Risco/Urgencia: ${risco}

## Status
${status}

## Escopo
- Escopo principal: ${scope_label}
- Servico alvo: ${service_label}

## Linha Do Tempo
1. [ ] Definir ordem de implementacao desta task no fluxo.
2. [ ] Registrar dependencias de tasks anteriores (mesmo servico, raiz ou outro servico).
3. [ ] Registrar tarefas posteriores desbloqueadas por esta entrega.

## Dependencias
- Nenhuma dependencia registrada.

## Conflitos Mapeados
- Nenhum conflito identificado ate o momento.

## Contexto
Descreva o contexto da tarefa.

## Evidencias
- Adicionar evidencias aqui.

## Observacoes
- Sem observacoes adicionais.
TASK

echo "Tarefa criada: ${file_path}"
