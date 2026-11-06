# Anexos e fontes do projeto

A [documentação principal](../documentacao-do-projeto.md) explica a história e as decisões. Estes arquivos preservam os detalhes, a origem e as evidências. Consulte-os pelo assunto quando precisar aprofundar.

## Por assunto

| Assunto | Onde consultar | Conteúdo |
|---|---|---|
| Produto e proposta de valor | [produto/](produto/README.md) | Contexto, escolhas e solução |
| Pesquisa e experiência do usuário | [experiencia-do-usuario/](experiencia-do-usuario/README.md) | Persona, jornada, telas e protocolo |
| Sistema e execução | [sistema/](sistema/README.md) | Requisitos, arquitetura, API e reprodução |
| Dados e modelo | [dados-e-modelo/](dados-e-modelo/README.md) | Análise, preparação, avaliação e dados da aplicação |
| Gestão, fontes e orçamento | [gestao/](gestao/README.md) | Regras, exigências IBM, pendências e premissas financeiras |
| Evidências de execução | [evidencias/](evidencias/README.md) | Logs, ambiente e registros datados |
| Planos históricos | [historico/](historico/) | Versões recuperadas do Git; não descrevem o estado atual |

## Outros materiais do repositório

- [Código da aplicação](../../watson/README.md).
- [Notebooks de análise e modelo](../../notebooks/).
- [Dados e orientações do case](../../data/).
- [Materiais de aula e guia IBM](../../contexto/).
- [Sessões registradas em bob_sessions](../../bob_sessions/).
- Roteiros pessoais de pesquisa e validação em `bob_sessions/pedro_faria/`: planejamento local, não coleta executada; ainda não versionados nesta revisão.

## Inventário completo

Todos os anexos existentes estão relacionados abaixo. Imagens e canvas sustentam a documentação; logs e JSON preservam registros de execução. Skills de design são materiais de método, não resultados de pesquisa.

### Produto e proposta de valor

- [README.md](produto/README.md)
- [beneficios-e-uso-da-ia.md](produto/beneficios-e-uso-da-ia.md)
- [como-a-solucao-funciona.md](produto/como-a-solucao-funciona.md)
- [escolha-da-solucao.md](produto/escolha-da-solucao.md)
- [problema-e-oportunidades.md](produto/problema-e-oportunidades.md)
- [proposta-de-valor.md](produto/proposta-de-valor.md)
- [resumo-do-projeto.md](produto/resumo-do-projeto.md)

### Pesquisa e experiência do usuário

- [README.md](experiencia-do-usuario/README.md)
- [jornada-atual-do-usuario.md](experiencia-do-usuario/jornada-atual-do-usuario.md)
- [necessidades-do-usuario.md](experiencia-do-usuario/necessidades-do-usuario.md)
- [perfil-do-usuario-e-cenarios.md](experiencia-do-usuario/perfil-do-usuario-e-cenarios.md)
- [plano-de-testes-com-usuarios.md](experiencia-do-usuario/plano-de-testes-com-usuarios.md)
- [processo_design/00-descoberta/README.md](experiencia-do-usuario/processo_design/00-descoberta/README.md)
- [processo_design/00-descoberta/anti-persona.md](experiencia-do-usuario/processo_design/00-descoberta/anti-persona.md)
- [processo_design/00-descoberta/canvas/AntiPersona.dc.html](experiencia-do-usuario/processo_design/00-descoberta/canvas/AntiPersona.dc.html)
- [processo_design/00-descoberta/canvas/Empatia.dc.html](experiencia-do-usuario/processo_design/00-descoberta/canvas/Empatia.dc.html)
- [processo_design/00-descoberta/canvas/Hills.dc.html](experiencia-do-usuario/processo_design/00-descoberta/canvas/Hills.dc.html)
- [processo_design/00-descoberta/canvas/Personas.dc.html](experiencia-do-usuario/processo_design/00-descoberta/canvas/Personas.dc.html)
- [processo_design/00-descoberta/cenario-as-is.md](experiencia-do-usuario/processo_design/00-descoberta/cenario-as-is.md)
- [processo_design/00-descoberta/hills-e-pov.md](experiencia-do-usuario/processo_design/00-descoberta/hills-e-pov.md)
- [processo_design/00-descoberta/imagens/anti-persona.png](experiencia-do-usuario/processo_design/00-descoberta/imagens/anti-persona.png)
- [processo_design/00-descoberta/imagens/as-is-pov-hills.png](experiencia-do-usuario/processo_design/00-descoberta/imagens/as-is-pov-hills.png)
- [processo_design/00-descoberta/imagens/empathy-maps.png](experiencia-do-usuario/processo_design/00-descoberta/imagens/empathy-maps.png)
- [processo_design/00-descoberta/imagens/personas.png](experiencia-do-usuario/processo_design/00-descoberta/imagens/personas.png)
- [processo_design/00-descoberta/mapas-de-empatia.md](experiencia-do-usuario/processo_design/00-descoberta/mapas-de-empatia.md)
- [processo_design/00-descoberta/personas.md](experiencia-do-usuario/processo_design/00-descoberta/personas.md)
- [processo_design/00-descoberta/premissas-e-perguntas.md](experiencia-do-usuario/processo_design/00-descoberta/premissas-e-perguntas.md)
- [processo_design/04-alta-fidelidade/README.md](experiencia-do-usuario/processo_design/04-alta-fidelidade/README.md)
- [processo_design/04-alta-fidelidade/telas/apresentacao-1-fila.png](experiencia-do-usuario/processo_design/04-alta-fidelidade/telas/apresentacao-1-fila.png)
- [processo_design/04-alta-fidelidade/telas/apresentacao-6-resolvido.png](experiencia-do-usuario/processo_design/04-alta-fidelidade/telas/apresentacao-6-resolvido.png)
- [processo_design/04-alta-fidelidade/telas/apresentacao-7-aparelho-trocado.png](experiencia-do-usuario/processo_design/04-alta-fidelidade/telas/apresentacao-7-aparelho-trocado.png)
- [processo_design/04-alta-fidelidade/telas/produto-1-fila.png](experiencia-do-usuario/processo_design/04-alta-fidelidade/telas/produto-1-fila.png)
- [processo_design/04-alta-fidelidade/telas/produto-4-enviado.png](experiencia-do-usuario/processo_design/04-alta-fidelidade/telas/produto-4-enviado.png)
- [processo_design/05-laboratorio-do-modelo/README.md](experiencia-do-usuario/processo_design/05-laboratorio-do-modelo/README.md)
- [processo_design/05-laboratorio-do-modelo/canvas/LAB-A-Bancada.dc.html](experiencia-do-usuario/processo_design/05-laboratorio-do-modelo/canvas/LAB-A-Bancada.dc.html)
- [processo_design/05-laboratorio-do-modelo/canvas/LAB-B-E-se.dc.html](experiencia-do-usuario/processo_design/05-laboratorio-do-modelo/canvas/LAB-B-E-se.dc.html)
- [processo_design/05-laboratorio-do-modelo/canvas/LAB-C-Explorador.dc.html](experiencia-do-usuario/processo_design/05-laboratorio-do-modelo/canvas/LAB-C-Explorador.dc.html)
- [processo_design/README.md](experiencia-do-usuario/processo_design/README.md)
- [processo_design/glossario.md](experiencia-do-usuario/processo_design/glossario.md)
- [processo_design/skills/ibm-design-thinking/SKILL.md](experiencia-do-usuario/processo_design/skills/ibm-design-thinking/SKILL.md)
- [processo_design/skills/ibm-estilo-materiais/SKILL.md](experiencia-do-usuario/processo_design/skills/ibm-estilo-materiais/SKILL.md)
- [processo_design/skills/ux-personas-pesquisa/SKILL.md](experiencia-do-usuario/processo_design/skills/ux-personas-pesquisa/SKILL.md)
- [roteiro-de-entrevistas.md](experiencia-do-usuario/roteiro-de-entrevistas.md)
- [telas-e-fluxo-do-usuario.md](experiencia-do-usuario/telas-e-fluxo-do-usuario.md)

### Sistema e execução

- [README.md](sistema/README.md)
- [arquitetura/decisoes/0001-backend-fastapi.md](sistema/arquitetura/decisoes/0001-backend-fastapi.md)
- [arquitetura/decisoes/0002-banco-trocavel.md](sistema/arquitetura/decisoes/0002-banco-trocavel.md)
- [arquitetura/decisoes/0003-codigo-em-ingles.md](sistema/arquitetura/decisoes/0003-codigo-em-ingles.md)
- [arquitetura/decisoes/0004-aviso-automatico-risco-medio.md](sistema/arquitetura/decisoes/0004-aviso-automatico-risco-medio.md)
- [arquitetura/visao-geral.md](sistema/arquitetura/visao-geral.md)
- [arquitetura-do-sistema.md](sistema/arquitetura-do-sistema.md)
- [cenarios-e-evidencias-de-teste.md](sistema/cenarios-e-evidencias-de-teste.md)
- [como-usar-a-demonstracao.md](sistema/como-usar-a-demonstracao.md)
- [reproducao-e-testes-do-fluxo.md](sistema/reproducao-e-testes-do-fluxo.md)
- [requisitos-da-solucao.md](sistema/requisitos-da-solucao.md)
- [specs/contrato-da-api.md](sistema/specs/contrato-da-api.md)
- [specs/evolucao-front-app-associado-analista.md](sistema/specs/evolucao-front-app-associado-analista.md)
- [specs/teste-historico-watsonx.md](sistema/specs/teste-historico-watsonx.md)

### Dados e modelo

- [README.md](dados-e-modelo/README.md)
- [analise-dos-dados.md](dados-e-modelo/analise-dos-dados.md)
- [assets/analise_critica.png](dados-e-modelo/assets/analise_critica.png)
- [assets/distribuicao_scores.png](dados-e-modelo/assets/distribuicao_scores.png)
- [assets/feature_importance.png](dados-e-modelo/assets/feature_importance.png)
- [assets/feature_importance_comparacao.png](dados-e-modelo/assets/feature_importance_comparacao.png)
- [assets/forca_dos_sinais.png](dados-e-modelo/assets/forca_dos_sinais.png)
- [assets/nulos_por_coluna.png](dados-e-modelo/assets/nulos_por_coluna.png)
- [assets/painel_retrato_fraude.png](dados-e-modelo/assets/painel_retrato_fraude.png)
- [assets/pr_curve.png](dados-e-modelo/assets/pr_curve.png)
- [assets/triagem_colunas.png](dados-e-modelo/assets/triagem_colunas.png)
- [avaliacao-do-modelo.md](dados-e-modelo/avaliacao-do-modelo.md)
- [dados/README.md](dados-e-modelo/dados/README.md)
- [dados/como-os-dados-ja-foram-usados.md](dados-e-modelo/dados/como-os-dados-ja-foram-usados.md)
- [dados/levantamento-de-dados.md](dados-e-modelo/dados/levantamento-de-dados.md)
- [dados/linha-do-tempo.md](dados-e-modelo/dados/linha-do-tempo.md)
- [dados/modelo-de-dados.md](dados-e-modelo/dados/modelo-de-dados.md)
- [dados/uso-dos-dados-na-aplicacao.md](dados-e-modelo/dados/uso-dos-dados-na-aplicacao.md)
- [preparacao-dos-dados.md](dados-e-modelo/preparacao-dos-dados.md)

### Gestão, fontes e orçamento

- [README.md](gestao/README.md)
- [entrega-final-ibm.md](gestao/entrega-final-ibm.md)
- [exigencias-da-ibm.md](gestao/exigencias-da-ibm.md)
- [fontes-e-hipoteses.md](gestao/fontes-e-hipoteses.md)
- [guia-das-entregas.md](gestao/guia-das-entregas.md)
- [o-que-falta-concluir.md](gestao/o-que-falta-concluir.md)
- [premissas-financeiras.json](gestao/premissas-financeiras.json)
- [regras-do-produto.md](gestao/regras-do-produto.md)
- [revisao-da-documentacao-2026-11-04.md](gestao/revisao-da-documentacao-2026-11-04.md)

### Evidências de execução

- [2026-11-04/ambiente.json](evidencias/2026-11-04/ambiente.json)
- [2026-11-04/documentos.json](evidencias/2026-11-04/documentos.json)
- [2026-11-04/pytest.log](evidencias/2026-11-04/pytest.log)
- [README.md](evidencias/README.md)
- [historico-dos-testes-2026-10-28.md](evidencias/historico-dos-testes-2026-10-28.md)

### Planos históricos

- [backlog-2026-10-28.md](historico/backlog-2026-10-28.md)
- [plano-inicial-2026-10-22.md](historico/plano-inicial-2026-10-22.md)
- [plano-operacional-2026-10-28.md](historico/plano-operacional-2026-10-28.md)

- [pacote-negocio-produto-2026-11-03.md](historico/pacote-negocio-produto-2026-11-03.md) — índice histórico recuperado da develop; não é estado atual.

- [Integração da develop em 05/11: 86 testes](evidencias/2026-11-05/integracao-develop.json).
