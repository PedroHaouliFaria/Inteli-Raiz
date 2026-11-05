# Critérios de aceite e pendências do conjunto

**Revisão:** 04/11/2026 · **Base:** develop f741a35, após PRs #15–#17.\
**Resultado:** todas as 13 entregas possuem documento localizável; a revisão documental foi consolidada. Isso não encerra pesquisa, piloto ou demonstração final.

## 1. Correções concluídas nesta revisão

- Três PRs aprovados e integrados; conflitos de #17 resolvidos preservando UTF-8.

- Documentação reunida em docs/, separada por área, com navegação por D01–D13 no índice.

- D05, D07 e D08 separados; registros de fontes/hipóteses reunidos sem perder IDs.

- API real documentada: prefixo /api, compra no caminho do chat, Idempotency-Key no cabeçalho e reply estruturado.

- Estados de backend, interface, modelo e agente atualizados a partir do código; diagnóstico antigo de reducer local deixa de ser tratado como atual.

- D04/D08 com comparação equivalente e hipótese correta HIP-P1-05; sem atribuir superioridade à presença de LLM.

- Custos com unidades consistentes e cenários ilustrativos explícitos; preços sem fonte removidos.

- Backend executado: 207 passed, 1 warning; log e ambiente preservados.

## 2. Próximos aceites por artefato

| ID | Critério ainda aberto | Responsável por função | Evidência para encerrar |
|---|---|---|---|
| D01 | Revisão do recorte, necessidades e HMW | Produto + Pesquisa | Revisor distinto, data e decisão; pesquisa disponível com limites |
| D02 | Distinguir hipótese de comportamento observado | Pesquisa + Produto | OBS anonimizada ligada à hipótese; sem inventar citação |
| D03 | Confirmar/refutar canais e ruptura prioritária | Pesquisa + domínio quando acessível | Relato/fonte com alcance e cenário atualizado |
| D04 | Discutir alternativas e confirmar/ajustar escolha | Produto + equipe; Arquitetura revisa | Ata curta de decisão e comparação nos mesmos critérios |
| D05 | Revisão cruzada de conceito/cenários | Produto + Pesquisa | Registro de coerência com D06/D12 |
| D06 | Revisão e teste da protopersona/cenários | Pesquisa + Produto | Evidência que sustenta ou muda as decisões de design |
| D07 | Testar o pitch e revisar com integração | Produto + Integração | Respostas às perguntas de D07; ajustes documentados |
| D08 | Preços públicos e cenários preenchidos em 05/11; medir uso, esforço, capacidade e atualizar valor | Produto + Arquitetura/Pesquisa | [Orçamento e fontes](../../documentacao-do-projeto.md#financeiro); substituir hipóteses por observações, sem alegar perda evitada |
| D09 | Acordar metas antes da coleta e revisar estrutura | Arquitetura + Integração/Pesquisa | Metas aprovadas e responsáveis confirmados |
| D10 | Revisão técnica e rastro com agente real | Arquitetura + revisor distinto | Ferramentas, contexto autorizado, resposta e limites no hash testado |
| D11 | Outro integrante reproduz fluxo pela interface | Integração + Arquitetura | Resultados/capturas de todos os casos críticos; logs com versão |
| D12 | Testar celular/teclado/foco/textos e compreensão | Pesquisa + Integração | Problemas, gravidade, alterações e reteste |
| D13 | Aplicar piloto e retestar problemas | Pesquisa + Integração | Contagens por condição, perfil, versão, observações e reteste |

Responsabilidade por função organiza o trabalho; confirmar os nomes com a equipe. A consolidação não atribui novas tarefas pessoais automaticamente.

## 3. Pendências transversais

| ID | Pendência | Prioridade e responsável | Critério de encerramento |
|---|---|---|---|
| TEC-01 | Prompt atual afirma que a tela só tem botões e chat, mas HumanReviewRequest existe | Antes de encerrar D12/D13; autor do agente + frontend | Alinhar prompt à UI, preservar proibição de autorizar e testar interação real. Nesta revisão foi identificado, sem alterar aplicação. |
| TEC-02 | Preparar condição A sem chat com os mesmos dados e revisão | Antes de comparação A/B; Integração | Versão/forma de ocultar chat documentadas; nenhuma vantagem de informação entre condições |
| TEC-03 | Reprodutibilidade/avaliação do modelo | Antes de alegar desempenho; Dados | Corte, manifesto 28 features, madrugada/nulos, baseline/velocidade e limiar documentados; holdout novo se necessário |
| TEC-04 | Ambiente com LLM real e persistência de deploy | Antes da demonstração; Arquitetura | Chave configurada fora do Git, rastro real, volume durável e acesso testado |
| FIN-01 | Vídeo, URL funcional e versão final das declarações | Antes da submissão; Produto/Integração | Pacote final completo e acesso conferido por outra pessoa |
| FIN-02 | Evidências individuais do IBM Bob e regras da plataforma | Antes da submissão; cada integrante/líder cadastrado | Índice de sessões reais, arquivos existentes e comprovante de envio |

## 4. Regras de encerramento

Cada item exige versão, evidência e revisor distinto. Teste automatizado de backend não substitui UI ou participante real. D02/D03/D06 podem permanecer hipóteses documentais com limites explícitos; não chamar isso de pesquisa validada. Um piloto pequeno mostra problemas/sinais, sem generalizar para todos os associados ou para perdas financeiras reais.

## Atualização documental de 05/11/2026

A [documentação principal](../../documentacao-do-projeto.md) reúne o percurso e incorpora orçamento com referências de mercado. Consulta de preços e cálculo não encerram D08: consumo, esforço, retorno, validação com usuários e revisão cruzada continuam pendentes. Não houve nova execução de backend nesta atualização.
