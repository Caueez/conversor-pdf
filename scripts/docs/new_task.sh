#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Uso:
  scripts/docs/new_task.sh --scope root --titulo "Titulo da tarefa" [--status "Em planejamento"] [--risco "Media / Medio prazo"] [--commit "-"] [--branch "-"]
  scripts/docs/new_task.sh --scope service --service account-service --titulo "Titulo da tarefa" [--status "Em planejamento"] [--risco "Media / Medio prazo"] [--commit "-"] [--branch "-"]

Regras:
  - --scope root: apenas tarefas de escopo geral do monorepo.
  - --scope service: tarefas especificas de um servico.
USAGE
}

scope=""
service=""
titulo=""
status="Em planejamento"
risco="Media / Medio prazo"
commit_ref=""
branch_ref=""

now="$(date '+%Y-%m-%d %H:%M:%S %z')"

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
  completion_date="$now"
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
- Data de criacao: ${now}
- Ultima atualizacao: ${now}
- Data de finalizacao: ${completion_date}
- Status: ${status}
- Escopo principal: ${scope_label}
- Servico alvo: ${service_label}
- Risco/Urgencia: ${risco}
- Branch de implementacao: ${branch_ref}
- Commit de implementacao: ${commit_ref}

## Solicitacoes Versionadas (Chat)

### Versao 1 - ${now}
- Descrever a solicitacao inicial do chat.

## Analise Consolidada Da Task
- Objetivo consolidado:
- Estado atual consolidado:
- Consistencia entre solicitacoes:
- Controle de duplicidade e divergencia:
- Pontos de atencao atuais:

## Escopos Alterados E Mudancas Planejadas
- Escopo:
  - Mudanca planejada:

## Arquivos Previstos Para Alteracao (Quando Houver Liberacao)
- \`caminho/arquivo\`
  - O que sera alterado.

## Mudancas Previstas Por Arquivo (Rascunho)
1. \`caminho/arquivo\`
   - Mudanca prevista.

## Plano Evolutivo Da Task (Por Etapas)

### Etapa 1 - Estruturacao Inicial
1. [ ] Registrar solicitacao inicial da task.
2. [ ] Consolidar analise inicial.
3. [ ] Mapear escopos e arquivos previstos sem implementar.

### Etapa 2 - Refinamento
1. [ ] Incorporar novas versoes de solicitacao com marcacao temporal.
2. [ ] Revalidar consistencia do plano.
3. [ ] Refinar mudancas previstas por arquivo.

### Etapa 3 - Liberacao
1. [ ] Validar planejamento com o programador.
2. [ ] Ajustar pendencias finais do plano.
3. [ ] Aguardar autorizacao explicita para iniciar implementacao.

### Etapa 4 - Implementacao
1. [ ] Executar implementacao autorizada.
2. [ ] Validar implementacao do agente (escopo, requisitos e testes).
3. [ ] Registrar resultado da validacao para revisao do programador.

### Etapa 5 - Versionamento Git
1. [ ] Solicitar autorizacao explicita do programador para iniciar versionamento Git apos validacao da implementacao.
2. [ ] Classificar arquivos alterados e revisar diff final.
3. [ ] Executar versionamento Git autorizado (branch, commit, push e merge conforme instrucao do programador).
TASK

echo "Tarefa criada: ${file_path}"
