# Revisão e consolidação dos artefatos — 04/11/2026

## Resultado

Os PRs #15, #16 e #17 da Isadora foram aprovados e integrados no develop. O #17 exigiu resolução de conflitos de movimentação; o texto UTF-8 de D09/D10 foi preservado. Os arquivos de planejamento também tinham caracteres corrompidos; foram restaurados a partir da versão anterior e seus links atualizados.

| PR | Conteúdo | Merge no develop |
|---|---|---|
| [#15](https://github.com/PedroHaouliFaria/Inteli-Raiz/pull/15) | Estrutura/arquitetura | 846beeb |
| [#16](https://github.com/PedroHaouliFaria/Inteli-Raiz/pull/16) | Negócio/produto | eb0a18a |
| [#17](https://github.com/PedroHaouliFaria/Inteli-Raiz/pull/17) | Reorganização | f741a35 |

A base f741a35 foi inspecionada e teve os testes de backend reproduzidos. Esta consolidação altera documentação e estrutura dos artefatos, sem alterar o código da aplicação.

## Organização anterior e atual

| Antes | Agora |
|---|---|
| docs/entregas/pessoa1/ | D01, D04, D05, D07 e D08 diretamente em artefatos/ |
| docs/entregas/pessoa2/ | D02, D03 e D06 diretamente em artefatos/; roteiro/registro em documentacao/ |
| docs/entregas/pessoa3/ | D09 e D10 diretamente em artefatos/ |
| docs/entregas/pessoa4/ | D11, D12 e D13 diretamente em artefatos/; matriz/aceite e evidências comuns |
| D05/D07/D08 no mesmo arquivo | Três documentos, localizáveis individualmente |
| Registros de evidências separados | Registro único, preservando IDs FON/HIP/DEC e prefixos históricos |
| docs/direcional_entregas.md | artefatos/documentacao/direcional_entregas.md |
| docs/planejamento/artefatos_materiais_contexto.md | artefatos/documentacao/fontes_e_exigencias_ibm.md |

Os READMEs por pessoa foram substituídos pelo índice único e pela matriz de aceite. Conteúdo histórico continua acessível pelo Git e pelo registro datado de evidências, sem manter uma segunda versão atual dos artefatos. Os relatórios originais de bob_sessions/ foram preservados.

## Revisão de conteúdo

- D01/D02/D03/D06 preservam fontes e natureza hipotética; a consolidação não cria pesquisa primária.

- D04 compara alternativas com os mesmos dados. Presença de IA não recebe vantagem por si só; HIP-P1-05 é a hipótese comparativa correta.

- D05/D07 deixam de afirmar como fato uma ausência de canal institucional ainda não pesquisada e atualizam dependências técnicas.

- D08 mantém valor como hipótese, corrige a comparação com texto determinístico e apresenta cenários ilustrativos com unidades consistentes, sem cotação sem fonte.

- D09 distingue código implementado, evidência de execução e validação da qualidade do modelo; define coleta por função e metas candidatas.

- D10 acompanha prefixos/rotas reais, cabeçalho Idempotency-Key, corpo do chat, retorno estruturado, ferramentas com identidade injetada, política conservadora e score não exposto ao agente.

- D11 registra execução atual com log, ambiente e hash do modelo; mantém pendente ensaio independente pela interface.

- D12 descreve SessionGate/AssociateApp/PurchaseDetail, não o MemberPhone legado como se fosse a UI atual. Acessibilidade e compreensão exigem teste.

- D13 mantém protocolo pronto sem participantes inventados; A/B deve variar somente chat, com mesmos dados e revisão.

- Pacote final reúne minutas de problema/solução e tecnologia, roteiro de três minutos e checklist real de submissão.

## Validação e limites

Backend: **207 passed, 1 warning in 31.46s**, Python 3.12.5, código f741a35. [Log](../evidencias/2026-11-04/pytest.log) e [ambiente](../evidencias/2026-11-04/ambiente.json). Os testes do agente usam modelos controlados, sem chamada externa real. Não foi executado navegador, leitor de tela, piloto de pesquisa, novo treino ou deploy watsonx.ai nesta revisão.

A conferência documental verifica um arquivo por D01–D13, metadados, links locais, ausência das pastas antigas e caracteres corrompidos. Seu resultado está em [validação documental](../evidencias/2026-11-04/documentos.json). Git diff --check verifica conflitos e whitespace introduzidos.

## O que ainda falta

A [matriz central](o-que-falta-concluir.md) é o registro vigente: revisão cruzada, pitch/discussão da equipe, pesquisa, LLM real, ensaio UI independente, correções/reteste, cotações e pacote final publicado. O prompt do agente possui uma divergência sobre a existência da ação de revisão na UI; foi registrado em TEC-01 para correção/teste pelos autores. Nenhum desses itens é marcado como concluído pela mera organização dos arquivos.
