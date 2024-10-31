#!/bin/bash
# Caminho para o arquivo .env
ENV_FILE=".env"
# Verifica se o arquivo .env existe
if [ ! -f "$ENV_FILE" ]; then
  echo "Arquivo $ENV_FILE não encontrado!"
  exit 1
fi
# Exporta cada linha do arquivo .env como uma variável de ambiente
# Ignora linhas que começam com '#' (comentários) ou estão vazias
export $(grep -v '^#' "$ENV_FILE" | xargs)

echo "Variáveis de ambiente carregadas do $ENV_FILE."
