# Guia de uso da demonstração

Este é o caminho mais curto para executar e demonstrar o Inteli Raiz do início ao fim.

## Versão publicada (sem instalar nada)

A aplicação está no ar em <https://raiz-jq28.onrender.com>. Use os logins da [seção 4](#4-entrar) e o [percurso principal](#5-percurso-principal).

- No plano gratuito do Render, o servidor "dorme" após 15 minutos sem acesso e leva cerca de 1 minuto para acordar. Abra o link um pouco antes de apresentar.
- Todos os visitantes compartilham a mesma base de demonstração. Os dados voltam ao estado inicial quando o servidor reinicia ou quando alguém usa **Restaurar dados da demonstração**.
- Como a publicação é configurada: [infraestrutura](../../../watson/infra/README.md#publicar-no-render).

Para rodar no seu computador, siga as seções 1 a 3.

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

Sem Docker, siga os READMEs do [backend](../../../watson/backend/README.md) e do [frontend](../../../watson/frontend/README.md). Dois cuidados: use Python 3.12 ou 3.13 no backend (o scikit-learn 1.6.1 do modelo não instala no 3.14) e defina `CONFIRMATION_TTL_SECONDS=2592000` no `backend/.env`; sem isso, o prazo padrão de 15 minutos faz as compras expirarem durante a demonstração.

## 4. Entrar

| Usuário | Papel | E-mail | Senha |
|---|---|---|---|
| Ana Souza | Associado | `ana@raiz.demo` | `Ana@123` |
| Bruno Lima | Associado | `bruno@raiz.demo` | `Bruno@123` |
| Carla Reis | Analista | `carla@raiz.demo` | `Carla@123` |

São credenciais exclusivamente fictícias. Não as reutilize em outros sistemas.

## 5. Percurso principal

1. Entre como Ana ou Bruno.
2. Na lista **Suas compras**, abra uma compra com status **Aguardando sua resposta**. Compras **Bloqueadas** também aceitam resposta.
3. Confira valor, data, categoria, cartão parcial e os motivos do alerta.
4. Abra o copiloto pelo ícone no cabeçalho, se a chave da Groq estiver configurada.
5. Escolha **Estou em dúvida** ou, em **Prefiro falar com uma pessoa**, solicite uma revisão por analista.
6. Saia e entre como Carla.
7. Na aba **Pendentes**, abra o caso, escreva uma justificativa (10 a 500 caracteres) e escolha **Autorizar compra** ou **Recusar compra**.
8. Saia, volte ao associado e atualize a lista para conferir o novo status.

Para manter as duas contas abertas ao mesmo tempo, entre com a analista numa janela anônima: o login fica guardado no navegador, então duas abas da mesma janela usam a mesma conta.

Esse percurso demonstra a cadeia completa: interface → API → banco → revisão humana → decisão → atualização para o associado.

## 6. Outros percursos

- **Autorizar:** o associado escolhe que reconhece a compra; o status vira `LIBERADA_SIMULACAO`.
- **Recusar:** o associado informa que não reconhece a compra; o status vira `RECUSADA_SIMULACAO` e o caso ganha revisão de proteção.
- **Isolamento:** Ana e Bruno veem apenas as próprias compras.
- **Analista:** Carla acessa revisões abertas e o score interno do modelo; associados não acessam essa fila. As abas **Histórico**, **Fluxo atual** e **Dados** mostram revisões encerradas, a situação de todas as compras e indicadores da base.

## 7. Recomeçar a demonstração

Com `DEMO_MODE=true`, a coluna **Suas compras** do associado e a tela da analista mostram **Restaurar dados da demonstração**. A opção apaga respostas, conversas e revisões da demonstração e recarrega as fixtures com prazo novo.

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

Use **Restaurar dados da demonstração**. O Docker local e a versão publicada configuram prazo de 30 dias para as confirmações fictícias. Fora do Docker, defina `CONFIRMATION_TTL_SECONDS=2592000` no `backend/.env` e reinicie o backend.

### O backend não sobe: `malformed database schema`

O arquivo SQLite local (`watson/backend/watson.db`) foi corrompido, em geral porque os arquivos auxiliares `watson.db-wal` e `watson.db-shm` foram apagados ou alterados. Pare o backend, renomeie ou apague os três arquivos `watson.db*` e suba de novo: o backend recria o banco e carrega os dados da demonstração.

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

- [Fluxo e evidências do MVP](reproducao-e-testes-do-fluxo.md)
- [Arquitetura](arquitetura/visao-geral.md)
- [Contrato da API](specs/contrato-da-api.md)
- [Dados usados pela aplicação](../dados-e-modelo/dados/uso-dos-dados-na-aplicacao.md)
- [Infraestrutura Docker e publicação no Render](../../../watson/infra/README.md)
