# 0002 · Camada de dados trocável entre PostgreSQL e Db2

**Status:** aceita; o banco de produção ainda está em aberto (ver [modelo de dados](../../dados/modelo-de-dados.md#decisoes-em-aberto)).

## Decisão
O backend acessa o banco só por SQLAlchemy, em `watson/backend/app/db/`. O banco muda trocando a `DATABASE_URL`:

```
postgresql+psycopg://watson:watson@localhost:5432/watson
db2+ibm_db://watson:senha@host:50000/WATSON
```

## Regras
1. Só tipos portáveis: enums como texto com validação; JSON pelo `PortableJSON` (texto).
2. Consultas só em `db/repositories/`; o domínio nunca escreve SQL.
3. Migrações com Alembic, testadas nos dois dialetos.
4. Testes de integração sempre no PostgreSQL e no Db2 antes de cada entrega, enquanto o Db2 for candidato.

## Sugestão para o banco de produção
PostgreSQL local no `docker-compose` e IBM Cloud Databases for PostgreSQL na nuvem. Se o time preferir Db2, a troca é de configuração.
