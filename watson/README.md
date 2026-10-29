# Watson

Aplicação web de prevenção a fraudes em cartão do time Raiz (optativa IBM do Inteli). Aqui fica só o código; a documentação (design, dados e arquitetura) está em [`docs/`](../docs/).

| Pasta | Papel |
|---|---|
| [frontend/](frontend/README.md) | Console da analista e app do associado (React, Vite, Carbon) |
| [backend/](backend/README.md) | API, regras de negócio, agentes e acesso ao banco (Python, FastAPI) |
| [infra/](infra/README.md) | Docker, deploy na IBM Cloud e CI |

Documentação relacionada:

- [Arquitetura](../docs/arquitetura/visao-geral.md) e [decisões](../docs/arquitetura/decisoes/)
- [Design da interface](../docs/design/README.md)
- [Modelo de dados](../docs/dados/README.md)

## Rodar tudo

```bash
# a partir de watson/
docker compose -f infra/docker-compose.yml up --build
# frontend: http://localhost:8080 · API: http://localhost:8000/docs
```

Ou cada parte separada, como explicado no README do [frontend](frontend/README.md) e do [backend](backend/README.md).

## Convenções

- Rotas, pastas, arquivos e código em inglês; textos da tela e documentação em português.
- Todo commit leva os 5 integrantes do grupo como coautores.
