# Inteli-Raiz

Projeto da optativa IBM do Inteli: confirmação assistida de compras pelo associado, com dados sintéticos e ações financeiras simuladas.

## Comece aqui

- **[Artefatos D01–D13](artefatos/README.md):** entregas em uma única pasta, documentação, fontes, evidências e estado de aceite.
- [O que falta concluir](artefatos/documentacao/criterios_e_pendencias.md): revisões cruzadas, ensaio pela interface, pesquisa/piloto e pacote final.
- [Como reproduzir o MVP](artefatos/D11_fluxo_mvp.md): preparação local, cenários e log dos 207 testes de backend aprovados em 04/11/2026.
- [Documentação técnica](docs/README.md): dados, modelo, design, arquitetura, contratos e planejamento.
- [Código da aplicação](watson/README.md): frontend React + Carbon e backend FastAPI.

## Estrutura

```text
artefatos/     entregas D01–D13, documentacao/ e evidencias/
docs/          apoio técnico: arquitetura, dados, design, specs e planejamento
watson/        código da aplicação e infraestrutura
data/          orientações, dicionário e bases processadas
notebooks/     análise, preparação e avaliação do modelo
scripts/       rotinas auxiliares
outputs/       resultados e modelo serializado
contexto/      materiais do programa IBM
bob_sessions/  evidências reais de uso do IBM Bob
```

A consolidação documental não equivale a teste com usuários. Backend reproduzido; LLM externo real, ensaio UI independente e validação de experiência têm pendências identificadas no índice.
