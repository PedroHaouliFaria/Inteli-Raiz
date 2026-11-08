#!/usr/bin/env bash
# Sobe backend e Nginx no mesmo container (usado por app.Dockerfile).
# Se qualquer um dos dois cair, o container encerra e a plataforma reinicia.
set -euo pipefail

envsubst '${PORT}' < /etc/nginx/app.conf.template > /etc/nginx/conf.d/default.conf

uvicorn app.main:app --host 127.0.0.1 --port 8000 --proxy-headers --forwarded-allow-ips='*' &
nginx -g 'daemon off;' &

wait -n
exit $?
