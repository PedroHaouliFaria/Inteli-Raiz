# Inteli-Raiz

Projeto da optativa IBM do Inteli: confirmação assistida de compras pelo associado, com dados sintéticos e ações financeiras simuladas.

## Comece aqui

- **[Guia de uso da demonstração](docs/03_computacao/guia_de_uso.md):** preparação, Docker, credenciais, percurso associado–analista, reset e solução de problemas.
- **[Documentação](docs/README.md):** índice por área e tabela das entregas D01–D13 com o estado de cada uma.
- [O que falta concluir](docs/05_gestao/criterios_e_pendencias.md): revisões cruzadas, ensaio pela interface, pesquisa/piloto e pacote final.
- [Como reproduzir o MVP](docs/03_computacao/D11_fluxo_mvp.md): preparação local, cenários e log dos 207 testes de backend aprovados em 04/11/2026.
- [Código da aplicação](watson/README.md): frontend React + Carbon e backend FastAPI.

## Estrutura

```text
docs/              toda a documentação, separada por área
  01_negocios/       D01, D04, D05, D07, D08 e canvas de proposta de valor
  02_ux_design/      D02, D03, D06, D12, D13, pesquisa e processo de design
  03_computacao/     D09, D10, D11, arquitetura e contratos
  04_dados_e_modelo/ análise, base balanceada, modelo e dados da aplicação
  05_gestao/         plano, direcional, pendências, evidências/hipóteses e pacote IBM
  06_evidencias/     logs e ambiente das execuções
watson/            código da aplicação e infraestrutura
data/              orientações, dicionário e bases processadas
notebooks/         análise, preparação e avaliação do modelo
scripts/           rotinas auxiliares
outputs/           resultados e modelo serializado
contexto/          materiais do programa IBM
bob_sessions/      evidências reais de uso do IBM Bob
```

A consolidação documental não equivale a teste com usuários. Backend reproduzido; LLM externo real, ensaio independente pela interface e validação de experiência têm pendências registradas em [critérios e pendências](docs/05_gestao/criterios_e_pendencias.md).
