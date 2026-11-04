#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

usage() {
  cat <<EOF
Uso: ./dev.sh <comando> [argumentos]

Comandos:
  up          Levanta el proyecto (reconstruye si hay cambios)
  down        Detiene y elimina los contenedores
  ps          Muestra el estado de los servicios
  logs [svc]  Sigue los logs de un servicio (por defecto: api)
  rebuild     Reconstruye las imágenes desde cero, sin caché
  migrate     Aplica las migraciones
  seed        Carga los datos de ejemplo
  test [args] Ejecuta los tests en el host (requiere uv)
  psql        Abre una consola de Postgres
  shell       Abre una terminal dentro del contenedor de la API
  reset       Borra todo, incluidos los datos, y levanta de nuevo
  clean       Elimina contenedores, volúmenes e imágenes del proyecto
EOF
}

die() {
  echo "Error: $1" >&2
  exit 1
}

require_docker() {
  docker info >/dev/null 2>&1 || die "Docker no está corriendo."
}

cmd="${1:-}"
[ $# -gt 0 ] && shift

case "$cmd" in
  up)
    require_docker
    docker compose up --build
    ;;
  down)
    require_docker
    docker compose down
    ;;
  ps)
    require_docker
    docker compose ps -a
    ;;
  logs)
    require_docker
    docker compose logs -f "${1:-api}"
    ;;
  rebuild)
    require_docker
    docker compose build --no-cache
    ;;
  migrate)
    require_docker
    docker compose run --build --rm migrate
    ;;
  seed)
    require_docker
    docker compose run --build --rm seed
    ;;
  test)
    require_docker
    docker compose run --rm test  
    ;;
  build)
    require_docker
    docker compose build "$@"
    ;;
  psql)
    require_docker
    docker compose exec db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
    ;;
  shell)
    require_docker
    docker compose exec api sh
    ;;
  reset)
    require_docker
    docker compose down -v
    docker compose up --build
    ;;
  clean)
    require_docker
    docker compose down -v --rmi local
    ;;
  *)
    usage
    exit 1
    ;;
esac