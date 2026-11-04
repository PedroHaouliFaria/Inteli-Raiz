# Artefatos do projeto

**Revisão:** 04/11/2026 · **Escopo:** confirmação assistida de compras pelo associado, com ações financeiras simuladas.

Aqui estão as **13 entregas em uma única pasta**, organizadas por assunto e ID. Responsáveis e revisores aparecem nos documentos; a navegação não depende de uma divisão por pessoa. D01–D11 correspondem às entregas nomeadas nas aulas; D12/D13 organizam apoio à prototipação e validação. Não são 13 submissões obrigatórias separadas.

A revisão documental e a consolidação estão feitas. O backend teve **207 testes aprovados**, com [log preservado](evidencias/2026-11-04/pytest.log). Pesquisa, teste do pitch, ensaio independente pela interface e comparação A/B ainda não foram executados nesta revisão.

## Entregas

| ID | Artefato | Estado e próximo aceite |
|---|---|---|
| [D01](D01_oportunidades.md) | Oportunidades, problema, evidências e HMW/POV | Rascunho documental; Pesquisa revisa recorte e necessidades |
| [D02](D02_mapa_empatia.md) | Mapa de empatia | Hipóteses rastreáveis; coletar observações reais |
| [D03](D03_cenario_atual.md) | Jornada e cenário atual | Cenário hipotético; confirmar canais/processo com pesquisa ou domínio |
| [D04](D04_priorizacao.md) | Alternativas e priorização | Comparação revisada; discussão coletiva pendente |
| [D05](D05_conceito_solucao.md) | Conceito da solução | Conceito e limites revisados; revisão cruzada de Pesquisa |
| [D06](D06_persona_e_cenarios.md) | Protopersona e cenários atual/futuro | Proposta rastreável; validar a compreensão e o contexto |
| [D07](D07_ideia.md) | Ideia e pitch | Roteiro pronto; testar explicação com alguém de fora |
| [D08](D08_proposta_valor_ia.md) | Valor, necessidade de IA e viabilidade | Cenários ilustrativos calculáveis; faltam cotações e medidas reais |
| [D09](D09_estrutura_solucao.md) | Estrutura e critérios de sucesso | Estado alinhado ao código; metas e coleta definidas para revisão |
| [D10](D10_arquitetura.md) | Arquitetura, ferramentas e contratos | Contratos corrigidos; rastro com LLM real e revisão cruzada pendentes |
| [D11](D11_fluxo_mvp.md) | Fluxo e reprodução | Backend reproduzido; ensaio UI por outra pessoa pendente |
| [D12](D12_prototipo_experiencia.md) | Experiência e decisões de interface | Código atual inspecionado; teste visual, acessibilidade e compreensão pendentes |
| [D13](D13_validacao_melhorias.md) | Protocolo, resultados e reteste | Protocolo pronto; sem participantes/resultados reais |

## Documentação e evidências

- [Documentação: fontes, método e revisão](documentacao/README.md).

- [Direcional completo e critérios por entrega](documentacao/direcional_entregas.md).

- [Matriz de aceite e pendências do conjunto](documentacao/criterios_e_pendencias.md).

- [Registro único de fontes, hipóteses e decisões](documentacao/evidencias_e_hipoteses.md).

- [Roteiro de pesquisa](documentacao/roteiro_pesquisa.md) e [matriz de cenários técnicos](documentacao/matriz_cenarios_e_evidencias.md).

- [Pacote final IBM: roteiro, declarações e checklist](documentacao/pacote_final_ibm.md).

- [Evidências executadas e limites](evidencias/README.md).

## Organização

```text
artefatos/
├── README.md
├── D01_oportunidades.md ... D13_validacao_melhorias.md
├── documentacao/   # direcional, fontes, pesquisa, matriz de aceite e pacote final
└── evidencias/     # logs e ambiente da execução; histórico identificado
```

A documentação técnica de apoio permanece em [docs/](../docs/README.md); código em [watson/](../watson/README.md); dados, notebooks e resultados mantêm suas pastas. Os materiais visuais anteriores estão em [docs/design/](../docs/design/README.md). Eles apoiam as entregas e não criam uma segunda versão oficial de D01–D13.
