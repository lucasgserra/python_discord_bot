#!/bin/bash
set -e

VENV_PY=".venv/Scripts/python.exe"

if [ ! -f "$VENV_PY" ]; then
  echo "▶ .venv não encontrado, criando..."
  py -m venv .venv
fi

echo "▶ Usando Python do .venv: $VENV_PY"

COMMIT_MSG=${1:-"style: format with black & ruff"}

# garante dependências no venv
if ! "$VENV_PY" -m pip show black > /dev/null 2>&1; then
  echo "▶ Instalando black..."
  "$VENV_PY" -m pip install black
fi

if ! "$VENV_PY" -m pip show ruff > /dev/null 2>&1; then
  echo "▶ Instalando ruff..."
  "$VENV_PY" -m pip install ruff
fi

echo "▶ Corrigindo com Ruff..."
"$VENV_PY" -m ruff check . --fix

echo "▶ Formatando com Black..."
"$VENV_PY" -m black .

echo "▶ Adicionando mudanças..."
git add -A

echo "▶ Commitando..."
git commit -m "$COMMIT_MSG" || echo "Nenhuma mudança para commitar"

echo "▶ Dando push..."
BRANCH=$(git rev-parse --abbrev-ref HEAD)

if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git push
else
  echo "▶ Branch sem upstream, configurando com 'git push -u origin $BRANCH'"
  git push -u origin "$BRANCH"
fi