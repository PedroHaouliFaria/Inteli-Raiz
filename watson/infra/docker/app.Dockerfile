# Imagem única para publicar a demonstração (Render ou outra plataforma de containers).
# Junta frontend (Nginx), backend (FastAPI) e modelo de risco num só serviço, na mesma
# origem, para o cookie de sessão funcionar sem CORS. Build a partir da RAIZ do repositório:
#   docker build -f watson/infra/docker/app.Dockerfile -t raiz .

FROM node:22-alpine AS frontend
WORKDIR /app
COPY watson/frontend/package.json watson/frontend/package-lock.json ./
RUN npm ci
COPY watson/frontend ./
# Vazio: o frontend chama /api, /health e /model-lab na própria origem.
ENV VITE_API_URL=""
RUN npm run build

FROM python:3.12-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx gettext-base \
    && rm -rf /var/lib/apt/lists/* /etc/nginx/sites-enabled/default

WORKDIR /app
COPY watson/backend/pyproject.toml watson/backend/alembic.ini ./
COPY watson/backend/app ./app
RUN pip install --no-cache-dir ".[risk]"

# Modelo e bases do notebook 03 (no compose eles entram por volume).
COPY outputs/modelo_rf.joblib /risk/outputs/modelo_rf.joblib
COPY data/processed /risk/data/processed

COPY --from=frontend /app/dist /usr/share/nginx/html
COPY watson/infra/docker/app-nginx.conf.template /etc/nginx/app.conf.template
COPY watson/infra/docker/app-start.sh /start.sh

# SQLite dentro do container: os dados da demo voltam ao padrão a cada deploy ou reinício.
ENV DATABASE_URL=sqlite:////data/watson.db \
    RISK_MODEL_PATH=/risk/outputs/modelo_rf.joblib \
    RISK_DATA_DIR=/risk/data/processed \
    PORT=10000
RUN mkdir -p /data

EXPOSE 10000
CMD ["bash", "/start.sh"]
