#!/bin/bash
set -e

if [ -d ".venv" ]; then
  source .venv/Scripts/activate
else
  echo "▶ .venv não encontrado, crie com: python -m venv .venv"
  exit 1
fi

COMMIT_MSG=${1:-"style: format with black & ruff"}

if ! py -m pip show black > /dev/null 2>&1; then
  echo "▶ Instalando black..."
  py -m pip install black
fi

if ! py -m pip show ruff > /dev/null 2>&1; then
  echo "▶ Instalando ruff..."
  py -m pip install ruff
fi

echo "▶ Corrigindo com Ruff..."
py -m ruff check . --fix

echo "▶ Formatando com Black..."
py -m black .

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
