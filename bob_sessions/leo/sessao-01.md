# Sessão 1 no Bob — Leo

Tarefa rodada no Bob IDE (modo agent), branch `docs/regras-bob-documentacao` criada a partir de `develop`.

| Tarefa | Início | Commit |
|---|---|---|
| Criar `.bob/rules/docs.md` — regras de documentação para as sessões no Bob | 04/11 14:43 UTC | `fa4f6c3` |

## O que a revisão humana verificou

- Leitura dos três arquivos de referência antes de escrever: `.bob/rules/backend.md`, `docs/README.md` e `artefatos/documentacao/README.md`.
- Estrutura e tom alinhados com o `backend.md` existente (seções em H2, listas de bullet, linguagem imperativa).
- Commit separado por assunto (`chore(bob)` para arquivo em `.bob/`), mensagem em português, minúsculo, no imperativo, com escopo entre parênteses — padrão do histórico do repositório.
- Push e PR #22 abertos para `develop` via `gh pr create`.

## Resumo final da tarefa

### Criar `.bob/rules/docs.md`

`fa4f6c3`

```text
Arquivo criado com 33 linhas cobrindo:

## Escopo
- docs/, artefatos/, README.md da raiz e READMEs de pastas.
- docs/design/ fora de alcance; instrução de parar e avisar se necessário.
- Sem tocar em watson/ nem em código.

## Fontes da verdade
- docs/specs/contrato_api.md (contrato da API)
- docs/plano_implementacao.md (produto e regras)
- artefatos/documentacao/direcional_entregas.md (entregas D01–D13)
- Ordem de precedência: plano > código; spec > documentação antiga.
  Em caso de ambiguidade, parar e perguntar.

## Convenções de artefatos
- Cada Dxx: ID, versão/data, responsável por função, estado, origem.
- Estados distintos: revisão documental, teste automatizado, ensaio pela
  interface e validação com participantes.
- IDs FON/HIP/DEC e prefixos P1 e P4-T preservados (citados no histórico).
- Resultados reais em artefatos/evidencias/ com versão, método e limite.
  Sem credenciais ou dados bancários identificáveis.

## Proibições
- Não criar falas, participantes, métricas de uso, capturas do Bob
  nem comprovantes de submissão.
- Não inventar datas, decisões ou estados.
- Documentar ausências com próximo passo; não preencher lacunas.

## Revisão cruzada
- Quem escreveu não marca como revisado.
  Outra pessoa deve revisar antes do encerramento da entrega.

## Idioma e nomenclatura
- Texto em português.
- Nomes de arquivos e pastas como já existem no repositório.

## Forma de trabalhar
- Terminar o pedido e parar; não adiantar passos nem refatorar adjacentes.
- Ler o documento por inteiro antes de editar.
- Não alterar .bobignore.
```
