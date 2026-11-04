# Documentação — Confirmação assistida de compras (Sicredi)

Projeto da Trilha 4 do **IBM AI Experiential Learning Lab 2026**, na optativa IBM do Inteli. O associado confirma, recusa ou declara dúvida sobre uma compra sinalizada; um agente de IA ajuda com o contexto disponível e encaminha para revisão humana quando não sabe responder. Os dados são sintéticos e as ações financeiras são simuladas.

**Revisão:** 04/11/2026. Toda a documentação fica nesta pasta, separada por área. O código está em [watson/](../watson/README.md).

## Áreas

| Pasta | O que tem | Entregas |
|---|---|---|
| [01_negocios/](01_negocios/README.md) | Problema, alternativas, conceito, pitch e proposta de valor | D01, D04, D05, D07, D08 + canvas |
| [02_ux_design/](02_ux_design/README.md) | Pesquisa, empatia, jornada, persona, protótipo e validação; processo de design (wireframes, mockups) | D02, D03, D06, D12, D13 |
| [03_computacao/](03_computacao/README.md) | Estrutura da solução, arquitetura, contratos da API e fluxo do MVP | D09, D10, D11 |
| [04_dados_e_modelo/](04_dados_e_modelo/README.md) | Análise exploratória, base balanceada, modelo de risco e dados da aplicação | — |
| [05_gestao/](05_gestao/README.md) | Plano do produto, direcional das entregas, pendências, evidências/hipóteses, pacote final IBM e planejamento | — |
| [06_evidencias/](06_evidencias/README.md) | Logs e ambiente das execuções | — |

## Entregas D01–D13

| ID | Entrega | Área | Estado e próximo aceite |
|---|---|---|---|
| [D01](01_negocios/D01_oportunidades.md) | Oportunidades, problema, evidências e HMW/POV | Negócios | Rascunho documental; Pesquisa revisa recorte e necessidades |
| [D02](02_ux_design/D02_mapa_empatia.md) | Mapa de empatia | UX | Hipóteses rastreáveis; coletar observações reais |
| [D03](02_ux_design/D03_cenario_atual.md) | Jornada e cenário atual | UX | Cenário hipotético; confirmar canais/processo com pesquisa ou domínio |
| [D04](01_negocios/D04_priorizacao.md) | Alternativas e priorização | Negócios | Comparação revisada; discussão coletiva pendente |
| [D05](01_negocios/D05_conceito_solucao.md) | Conceito da solução | Negócios | Conceito e limites revisados; revisão cruzada de Pesquisa |
| [D06](02_ux_design/D06_persona_e_cenarios.md) | Protopersona e cenários atual/futuro | UX | Proposta rastreável; validar compreensão e contexto |
| [D07](01_negocios/D07_ideia.md) | Ideia e pitch | Negócios | Roteiro pronto; testar explicação com alguém de fora |
| [D08](01_negocios/D08_proposta_valor_ia.md) | Valor, necessidade de IA e viabilidade | Negócios | Cenários ilustrativos; faltam cotações e medidas reais |
| [D09](03_computacao/D09_estrutura_solucao.md) | Estrutura e critérios de sucesso | Computação | Alinhado ao código; metas e coleta definidas para revisão |
| [D10](03_computacao/D10_arquitetura.md) | Arquitetura, ferramentas e contratos | Computação | Rastro com LLM real e revisão cruzada pendentes |
| [D11](03_computacao/D11_fluxo_mvp.md) | Fluxo e reprodução do MVP | Computação | Backend reproduzido (207 testes); ensaio pela interface pendente |
| [D12](02_ux_design/D12_prototipo_experiencia.md) | Experiência e decisões de interface | UX | Teste visual, acessibilidade e compreensão pendentes |
| [D13](02_ux_design/D13_validacao_melhorias.md) | Protocolo, resultados e reteste | UX | Protocolo pronto; sem participantes/resultados reais |

D01–D11 são as entregas nomeadas nas aulas; D12 e D13 apoiam prototipação e validação. Não são 13 submissões obrigatórias separadas: o que se envia está no [pacote final IBM](05_gestao/pacote_final_ibm.md).

## Por onde começar

1. **Entender o projeto:** [D07 — ideia e pitch](01_negocios/D07_ideia.md) e [canvas de proposta de valor](01_negocios/canvas_proposta_de_valor.md).
2. **Regras do produto:** [plano de implementação](05_gestao/plano_implementacao.md) §§1–3.
3. **O que falta:** [critérios e pendências](05_gestao/criterios_e_pendencias.md).
4. **Rodar o MVP:** [D11 — fluxo e reprodução](03_computacao/D11_fluxo_mvp.md).

## Regras da documentação

- Cada entrega tem ID, versão/data, responsável por função, revisor, estado e fontes. Estados: **rascunho**, **em revisão**, **revisado**, **validado em teste**. Revisão documental não equivale a validação com usuários.
- Toda afirmação sobre dor, comportamento ou valor aponta para um ID do [registro de evidências](05_gestao/evidencias_e_hipoteses.md) (FON, HIP, DEC, OBS, TST).
- Não criar falas, participantes, métricas ou capturas do Bob. Evidências do IBM Bob ficam em [bob_sessions/](../bob_sessions/).
- Documento novo entra na pasta da área a que pertence; o que for transversal (plano, direcional, pendências) fica em [05_gestao/](05_gestao/README.md).

> O CSV original (~290 MB) não é versionado. Para os notebooks, coloque `case_transacoes_cartoes_sintetico_900k.csv` em `data/`. Para gerar as figuras da análise: `python scripts/gerar_figuras_docs.py`.
