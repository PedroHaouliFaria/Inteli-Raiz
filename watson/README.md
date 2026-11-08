# Watson

Aplicação web de prevenção a fraudes em cartão do time Raiz (optativa IBM do Inteli). Aqui fica só o código; a documentação (design, dados e arquitetura) está em [`docs/`](../docs) e o mapa do repositório inteiro no [README da raiz](../README.md#como-navegar-pelo-repositório).

**Versão publicada:** <https://raiz-jq28.onrender.com> (logins no [guia de uso](../docs/anexos/sistema/como-usar-a-demonstracao.md#4-entrar)).

| Pasta | Papel |
|---|---|
| [frontend/](frontend/README.md) | App do associado e revisão de exceções da analista (React, Vite, Carbon) |
| [backend/](backend/README.md) | API, regras de negócio, agentes e acesso ao banco (Python, FastAPI) |
| [infra/](infra/README.md) | Docker Compose local, imagem única da publicação no Render; diretórios históricos de deploy IBM Cloud e CI |

Documentação relacionada:

- [História e fluxo do projeto](../docs/documentacao-do-projeto.md).

- [Arquitetura](../docs/anexos/sistema/arquitetura/visao-geral.md) e [decisões](../docs/anexos/sistema/arquitetura/decisoes)
- [Design da interface](../docs/anexos/experiencia-do-usuario/processo_design/README.md)
- [Modelo de dados](../docs/anexos/dados-e-modelo/dados/README.md)

## Rodar tudo

Para o roteiro completo, incluindo preparação do `.env`, credenciais, percurso de demonstração e solução de problemas, consulte o [guia de uso](../docs/anexos/sistema/como-usar-a-demonstracao.md).

```bash
# a partir de watson/
docker compose -f infra/docker-compose.yml up --build
# frontend: http://localhost:8080 · API: http://localhost:8000/docs
```

Ou cada parte separada, como explicado no README do [frontend](frontend/README.md) e do [backend](backend/README.md).

## Convenções

- Rotas, pastas, arquivos e código em inglês; textos da tela e documentação em português.
- Todo commit leva os 5 integrantes do grupo como coautores.
