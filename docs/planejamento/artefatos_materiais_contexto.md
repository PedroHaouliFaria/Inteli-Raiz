# Artefatos identificados nos materiais de contexto

Confer├¬ncia inicial em 20/10/2026, com organiza├º├úo atualizada em 27/10/2026. Os nomes abaixo v├¬m dos PDFs locais da pasta `contexto/`; a divis├úo em pilares serve apenas para facilitar a organiza├º├úo. As semanas s├úo as do programa IBM. A produ├º├úo das entregas segue o [direcional](../direcional_entregas.md), agora dividido entre quatro pessoas e centrado no associado.

## 1. Entregas nomeadas nos slides de desenvolvimento

| Pilar | Artefato nomeado no material | Conte├║do a registrar | Onde aparece |
|---|---|---|---|
| Neg├│cios/pesquisa | Documento de Mapeamento de Oportunidades | Problema, p├║blico afetado, dores e oportunidades de atua├º├úo | S1 p.60; S2 p.63 pede finaliza├º├úo |
| Design/pesquisa | Mapa de Empatia | Necessidades, objetivos, dificuldades e contexto do usu├írio | S1 p.60 |
| Design/pesquisa | Mapeamento de Cen├írio Atual | Como o problema ├® enfrentado hoje e onde h├í fric├º├úo | S1 p.60 |
| Neg├│cios/design | Agrupamento e Prioriza├º├úo de Ideias | Alternativas consideradas, agrupamentos e motivos da escolha | S2 p.63 |
| Neg├│cios/design | Conceito da Solu├º├úo | Dire├º├úo escolhida e a capacidade que a solu├º├úo cria para o usu├írio | S2 p.63 |
| Design/pesquisa | Persona e Cen├írio Atual Refinado ÔåÆ Cen├írio Futuro | Usu├írio principal e compara├º├úo entre a experi├¬ncia atual e a proposta | S2 p.63; elementos da persona em p.47 |
| Neg├│cios | Ideia preliminar e descri├º├úo | S├¡ntese da ideia e do problema que pretende resolver | S3 p.22 |
| Neg├│cios | Proposta de valor e justificativa de uso de IA | Dor, p├║blico, valor esperado e motivo de precisar de IA | S3 p.22; exerc├¡cio de proposta em uma p├ígina em p.17 |
| Produto/tecnologia | Estrutura da Solu├º├úo | Problema, usu├írio, intelig├¬ncia necess├íria, arquitetura e crit├®rios de sucesso | S4 p.29 |
| Programa├º├úo | Arquitetura T├®cnica | Agentes, pap├®is e padr├Áes de orquestra├º├úo | S4 p.29 |
| Programa├º├úo/produto | Fluxo Principal do MVP | Caminho funcional ponta a ponta, mesmo que inicial | S5 p.22 |

Esses nomes n├úo exigem necessariamente 11 documentos separados. ├ë poss├¡vel reunir oportunidades/empatia/cen├írio em uma entrega de descoberta, e ideias/conceito/persona/cen├írio futuro em uma entrega de concep├º├úo, preservando se├º├Áes claras e evid├¬ncias.

## 2. Atividades de apoio apresentadas nas aulas

As sess├Áes de design thinking tamb├®m apresentam entrevistas, observa├º├úo, jornada do usu├írio, mapa de stakeholders, perguntas HMW (ÔÇ£Como poder├¡amos...ÔÇØ), brainstorming, prototipa├º├úo e testes. Elas orientam a produ├º├úo dos artefatos; n├úo devem ser automaticamente apresentadas como documentos obrigat├│rios adicionais.

S1 p.38 descreve um prot├│tipo de baixa ou m├®dia fidelidade como entrega esperada da etapa de prototipa├º├úo. S1 p.40 orienta testar situa├º├Áes normais, amb├¡guas e de falha, registrar evid├¬ncias e converter o aprendizado em ajustes. Isso sustenta um prot├│tipo de design e um registro de valida├º├úo, sem estabelecer a obriga├º├úo de desenvolver um front-end pr├│prio.

## 3. Pacote final explicitamente solicitado no guia

O guia, p.13, lista quatro itens para o envio final:

1. **V├¡deo de demonstra├º├úo de 3 minutos**, contendo problema, usu├írio-alvo, solu├º├úo, principais recursos e demonstra├º├úo.
2. **Declara├º├úo escrita do problema e da solu├º├úo, com link para o prot├│tipo funcional.**
3. **Declara├º├úo escrita sobre a tecnologia.**
4. **Relat├│rios das sess├Áes de tarefas do IBM Bob no reposit├│rio de c├│digo.** O guia tamb├®m permite incluir link do GitHub ou pasta compartilhada com os ativos. Nas p.30-31, orienta a inclus├úo das capturas dos resumos relevantes de cada integrante em `bob_sessions/`.

Na mesma p├ígina, o guia esclarece que as tarefas semanais s├úo recomendadas e que os entreg├íveis obrigat├│rios s├úo **o checkpoint intermedi├írio e o envio final**. Os PDFs consultados n├úo fornecem nesta se├º├úo um formul├írio completo com os campos do checkpoint; o guia remete ├á plataforma de participantes para a vis├úo geral das tarefas. N├úo deduzir esses campos a partir do pacote final.

## 4. Como isso muda a organiza├º├úo proposta

- Os c├│digos D01ÔÇôD11 do direcional correspondem ├ás 11 entregas nomeadas nos slides; D12/D13 organizam prototipa├º├úo e valida├º├úo como apoio. Os c├│digos A01ÔÇôA12 anteriores foram substitu├¡dos, com correspond├¬ncia no [plano operacional](plano_15_dias.md).
- Pesquisa, concep├º├úo, proposta de valor, estrutura da solu├º├úo, arquitetura e fluxo funcional t├¬m correspond├¬ncia direta com os materiais.
- EDA, contrato de dados e relat├│rio de modelo s├úo desdobramentos t├®cnicos ├║teis ao case Sicredi. As orienta├º├Áes do dataset sugerem EDA, qualidade, valida├º├úo temporal, preven├º├úo de vazamento, m├®tricas para desbalanceamento e avalia├º├úo de custo; n├úo os definem como entregas oficiais separadas do programa.
- O projeto aproveita o frontend React + Carbon do Watson, produzido por Leonardo no PR #7, para adapta├º├úo e integra├º├úo ao associado. C10/C13/C18/C27 est├úo ativos. Prot├│tipo e fluxo integrado t├¬m aceites distintos: sess├úo, v├¡nculo da compra, tr├¬s respostas, ajuda separada e resultado persistido precisam ser comprovados. A adapta├º├úo ├® decis├úo do projeto; a aula n├úo exige essa stack.
- A documenta├º├úo de reprodu├º├úo e os registros de avalia├º├úo apoiam as declara├º├Áes e a demonstra├º├úo final. Esfor├ºo e datas ser├úo acordados conforme a disponibilidade das quatro pessoas; as estimativas antigas de 15 dias n├úo s├úo compromissos atuais.
- Pessoa 1 lidera neg├│cio/produto; Pessoa 2, pesquisa/usu├írio; Pessoa 3, estrutura/arquitetura; Pessoa 4, prot├│tipo/evid├¬ncias/valida├º├úo. O direcional cont├®m apoio, revis├úo e aceite por entrega. Os nomes e os executores da implementa├º├úo ser├úo definidos pela equipe.

## 5. Fontes e p├íginas conferidas

- **S1:** [Primeira sess├úo de Design Thinking](../../contexto/First%20DT%20Session%20deck.pdf), p.28, 38, 40 e 60.
- **S2:** [Segunda sess├úo de Design Thinking](../../contexto/Updated_Second%20Session%20DT%20and%20AI%20Agents_BR_Saulo%20%281%29%20%281%29.pdf), p.47, 54 e 63.
- **S3:** [Empreendedorismo em IA](../../contexto/Updated_Deck_Empreendedorismo_IA_PT_v9.pdf), p.17 e 22.
- **S4:** [Primeira sess├úo t├®cnica](../../contexto/1st%20Technical%20session-Prototyping%20AI%20Solutions%20with%20IBM%20AI%20Technologies%20%E2%80%93%20Technical%20Session_updated.pdf), p.29.
- **S5:** Segunda sess├úo t├®cnica, arquivo cujo nome come├ºa por `sess├úo 2 IBM Agentic AI Technologies`, p.22, na [pasta de contexto](../../contexto/).
- **Guia:** [Guia IBM](../../contexto/2H26%20GuideBob_IBM%20SkillsBuild_AI%20Experiential%20Learning%20Lab%20BR.pdf), p.13 e 30-31.
- **Dataset:** [Orienta├º├Áes do case Sicredi](../../data/Orientacoes_case_prevencao_sicredi.txt), se├º├úo ÔÇ£Uso pedag├│gico sugeridoÔÇØ.
