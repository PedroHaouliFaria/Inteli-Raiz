# infra

Como subir e publicar o Watson.

| Pasta / arquivo | Papel |
|---|---|
| `docker-compose.yml` | Sobe PostgreSQL + backend + frontend locais com um comando |
| `docker/` | Dockerfile de cada serviço |
| `docker/app.Dockerfile` | Imagem única (frontend + backend + modelo) para publicar a demonstração |
| `../../render.yaml` | Blueprint do Render que usa a imagem única |
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

## Publicar no Render

A demonstração publicada roda num único serviço: `docker/app.Dockerfile` junta o frontend (Nginx), o backend (FastAPI) e o modelo de risco. Frontend e API ficam na mesma origem, então o cookie de sessão funciona sem CORS. O banco é SQLite dentro do container: os dados voltam ao padrão a cada deploy ou reinício, e o botão **Restaurar dados da demonstração** continua disponível.

No plano gratuito, o serviço "dorme" após 15 minutos sem acesso e leva cerca de 1 minuto para acordar. Abra o link um pouco antes de apresentar.

### Opção A: Blueprint (quem tem acesso de administrador ao repositório no GitHub)

1. Em <https://dashboard.render.com>, **New → Blueprint** e escolha este repositório.
2. O Render lê o `render.yaml` da raiz e cria o serviço `raiz`.
3. Preencha `GROQ_API_KEY` quando for pedido (opcional; sem ela, só o chat fica indisponível).
4. Novos pushes na branch configurada publicam sozinhos.

### Opção B: repositório público (qualquer integrante)

1. Em <https://dashboard.render.com>, **New → Web Service → Public Git Repository** e cole `https://github.com/PedroHaouliFaria/Inteli-Raiz`.
2. Preencha:

| Campo | Valor |
|---|---|
| Branch | `develop` (ou a branch que tiver estes arquivos) |
| Language | `Docker` |
| Root Directory | deixe vazio |
| Dockerfile Path | `./watson/infra/docker/app.Dockerfile` |
| Docker Build Context Directory | `.` |
| Instance Type | `Free` |
| Health Check Path (em Advanced) | `/health` |

3. Em **Environment Variables**:

| Variável | Valor |
|---|---|
| `SESSION_SECRET` | um valor aleatório: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `SESSION_SECURE` | `true` |
| `DEMO_MODE` | `true` |
| `CONFIRMATION_TTL_SECONDS` | `2592000` |
| `GROQ_API_KEY` | chave da Groq (opcional) |

4. **Create Web Service**. O primeiro build leva alguns minutos. Nesse modo, um push novo não publica sozinho: use **Manual Deploy → Deploy latest commit**.

### Testar a imagem localmente

```bash
# a partir da raiz do repositório
docker build -f watson/infra/docker/app.Dockerfile -t raiz .
docker run --rm -p 8090:10000 -e SESSION_SECRET=troque-isto -e DEMO_MODE=true -e CONFIRMATION_TTL_SECONDS=2592000 raiz
# http://localhost:8090
```

A chave da Groq configurada no Render é usada por qualquer pessoa que abrir o chat do link publicado. Use uma chave da equipe e acompanhe o consumo no painel da Groq.
