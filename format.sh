#!/bin/bash
set -e

# Mensagem de commit como parâmetro (default se não passar nada)
COMMIT_MSG=${1:-"style: format with black & ruff"}

# Instala black e ruff só se não tiverem
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
git push
