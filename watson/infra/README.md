# infra

Como subir e publicar o Watson.

| Pasta / arquivo | Papel |
|---|---|
| `docker-compose.yml` | Sobe PostgreSQL + backend + frontend locais com um comando |
| `docker/` | Dockerfile de cada serviço |
| `ibm-cloud/` | Deploy no IBM Cloud Code Engine e configuração dos serviços (a fazer) |
| `ci/` | Testes e build automáticos; o GitHub Actions aponta para cá (a fazer) |

```bash
# a partir de watson/
docker compose -f infra/docker-compose.yml up --build
# frontend: http://localhost:8080 · API: http://localhost:8000/docs
```
