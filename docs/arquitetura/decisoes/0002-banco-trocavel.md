# 0002 · Camada de dados trocável entre PostgreSQL e Db2

**Status:** proposta pelo Leo e incorporada ao plano no [alinhamento de 28/10](../../plano_implementacao.md#alinhamento-com-o-watson-2810): o SQLAlchemy fica, e a demonstração usa SQLite com volume persistente.

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

## Sugestão para o banco de produção
PostgreSQL local no `docker-compose` e IBM Cloud Databases for PostgreSQL na nuvem. Se o time preferir Db2, a troca é de configuração.
