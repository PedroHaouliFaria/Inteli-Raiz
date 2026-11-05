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
cp backend/.env.example backend/.env
# edite backend/.env e defina um SESSION_SECRET aleatório; GROQ_API_KEY é opcional
docker compose -f infra/docker-compose.yml up --build
# frontend: http://localhost:8080 · API: http://localhost:8000/docs
```

Credenciais fictícias configuradas em `backend/.env` e `backend/.env.example`:

| Perfil | E-mail | Senha |
|---|---|---|
| Ana (associado) | `ana@raiz.demo` | `Ana@123` |
| Bruno (associado) | `bruno@raiz.demo` | `Bruno@123` |
| Carla (analista) | `carla@raiz.demo` | `Carla@123` |

O Nginx encaminha `/api`, `/health` e `/model-lab` para o backend dentro da rede do Compose. O navegador usa somente `http://localhost:8080`, mantendo frontend, API e cookie de sessão na mesma origem.
