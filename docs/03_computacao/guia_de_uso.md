# Guia de uso da demonstração

Este é o caminho mais curto para executar e demonstrar o Inteli Raiz do início ao fim.

## 1. Pré-requisitos

- Git.
- Docker Desktop com Docker Compose.
- Portas `5432`, `8000` e `8080` livres.
- Aproximadamente 10 GB livres para imagens, dependências e o banco local.

O chat usa a API da Groq. Sem `GROQ_API_KEY`, login, compras, confirmações e revisão humana continuam funcionando; somente o chat pode responder como indisponível.

## 2. Preparar o ambiente

Na raiz do repositório:

```bash
cd watson
cp backend/.env.example backend/.env
```

O `.env.example` já contém os usuários fictícios. Para uma execução compartilhada, substitua `SESSION_SECRET` no arquivo `backend/.env` por um valor aleatório:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Não versione o arquivo `backend/.env` e não coloque chaves reais no `.env.example`.

## 3. Subir a aplicação

Ainda dentro de `watson/`:

```bash
docker compose -f infra/docker-compose.yml up -d --build
docker compose -f infra/docker-compose.yml ps
```

Espere os serviços `db`, `backend` e `frontend` aparecerem como `healthy`.

- Aplicação: <http://localhost:8080>
- API e documentação interativa: <http://localhost:8000/docs>

## 4. Entrar

| Usuário | Papel | E-mail | Senha |
|---|---|---|---|
| Ana Souza | Associado | `ana@raiz.demo` | `Ana@123` |
| Bruno Lima | Associado | `bruno@raiz.demo` | `Bruno@123` |
| Carla Reis | Analista | `carla@raiz.demo` | `Carla@123` |

São credenciais exclusivamente fictícias. Não as reutilize em outros sistemas.

## 5. Percurso principal

1. Entre como Ana ou Bruno.
2. Abra uma compra com status **Aguardando sua resposta**.
3. Confira valor, data, categoria, cartão parcial e sinais apresentados.
4. Use o chat se a chave da Groq estiver configurada.
5. Escolha **Estou em dúvida** ou solicite uma revisão humana.
6. Saia e entre como Carla.
7. Na fila de revisões, localize o caso e escolha **Liberar compra** ou **Recusar compra**.
8. Saia, volte ao associado e atualize a lista para conferir o novo status.

Esse percurso demonstra a cadeia completa: interface → API → banco → revisão humana → decisão → atualização para o associado.

## 6. Outros percursos

- **Autorizar:** o associado escolhe que reconhece a compra; o status vira `LIBERADA_SIMULACAO`.
- **Recusar:** o associado informa que não reconhece a compra; o status vira `RECUSADA_SIMULACAO` e o caso ganha revisão de proteção.
- **Isolamento:** Ana e Bruno veem apenas as próprias compras.
- **Analista:** Carla acessa revisões abertas e o score interno do modelo; associados não acessam essa fila.

## 7. Recomeçar a demonstração

Com `DEMO_MODE=true`, o cabeçalho mostra **Recomeçar demonstração**. O botão apaga respostas, conversas e revisões da demonstração e recarrega as fixtures com prazo novo.

Use o reset somente em dados fictícios. Todos os usuários compartilham a mesma base local, portanto o reset afeta a demonstração inteira.

## 8. Parar e voltar depois

Parar mantendo o banco:

```bash
docker compose -f infra/docker-compose.yml down
```

Subir novamente:

```bash
docker compose -f infra/docker-compose.yml up -d
```

## 9. Solução rápida de problemas

### Todos os casos aparecem com prazo encerrado

Use **Recomeçar demonstração**. O Docker local configura prazo de 30 dias para as confirmações fictícias.

### O chat está indisponível

Defina `GROQ_API_KEY` em `backend/.env` e recrie o backend. Os demais fluxos não dependem dessa chave.

### Um serviço não fica saudável

```bash
docker compose -f infra/docker-compose.yml ps
docker compose -f infra/docker-compose.yml logs --tail=100 backend frontend db
```

Confira portas ocupadas e espaço livre no disco. Não use `down -v` se precisar preservar o banco.

### Alterei o `.env`

```bash
docker compose -f infra/docker-compose.yml up -d --force-recreate backend frontend
```

## 10. Leitura técnica

- [Fluxo e evidências do MVP](D11_fluxo_mvp.md)
- [Arquitetura](arquitetura/visao-geral.md)
- [Contrato da API](specs/contrato_api.md)
- [Dados usados pela aplicação](../04_dados_e_modelo/dados/uso-dos-dados-na-aplicacao.md)
- [Infraestrutura Docker](../../watson/infra/README.md)

