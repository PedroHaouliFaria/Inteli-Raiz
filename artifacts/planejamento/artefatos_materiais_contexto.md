# Artefatos identificados nos materiais de contexto

Conferência inicial em 20/10/2026, com organização atualizada em 27/10/2026. Os nomes abaixo vêm dos PDFs locais da pasta `contexto/`; a divisão em pilares serve apenas para facilitar a organização. As semanas são as do programa IBM. A produção das entregas segue o [direcional](../../docs/direcional_entregas.md), agora dividido entre quatro pessoas e centrado no associado.

## 1. Entregas nomeadas nos slides de desenvolvimento

| Pilar | Artefato nomeado no material | Conteúdo a registrar | Onde aparece |
|---|---|---|---|
| Negócios/pesquisa | Documento de Mapeamento de Oportunidades | Problema, público afetado, dores e oportunidades de atuação | S1 p.60; S2 p.63 pede finalização |
| Design/pesquisa | Mapa de Empatia | Necessidades, objetivos, dificuldades e contexto do usuário | S1 p.60 |
| Design/pesquisa | Mapeamento de Cenário Atual | Como o problema é enfrentado hoje e onde há fricção | S1 p.60 |
| Negócios/design | Agrupamento e Priorização de Ideias | Alternativas consideradas, agrupamentos e motivos da escolha | S2 p.63 |
| Negócios/design | Conceito da Solução | Direção escolhida e a capacidade que a solução cria para o usuário | S2 p.63 |
| Design/pesquisa | Persona e Cenário Atual Refinado → Cenário Futuro | Usuário principal e comparação entre a experiência atual e a proposta | S2 p.63; elementos da persona em p.47 |
| Negócios | Ideia preliminar e descrição | Síntese da ideia e do problema que pretende resolver | S3 p.22 |
| Negócios | Proposta de valor e justificativa de uso de IA | Dor, público, valor esperado e motivo de precisar de IA | S3 p.22; exercício de proposta em uma página em p.17 |
| Produto/tecnologia | Estrutura da Solução | Problema, usuário, inteligência necessária, arquitetura e critérios de sucesso | S4 p.29 |
| Programação | Arquitetura Técnica | Agentes, papéis e padrões de orquestração | S4 p.29 |
| Programação/produto | Fluxo Principal do MVP | Caminho funcional ponta a ponta, mesmo que inicial | S5 p.22 |

Esses nomes não exigem necessariamente 11 documentos separados. É possível reunir oportunidades/empatia/cenário em uma entrega de descoberta, e ideias/conceito/persona/cenário futuro em uma entrega de concepção, preservando seções claras e evidências.

## 2. Atividades de apoio apresentadas nas aulas

As sessões de design thinking também apresentam entrevistas, observação, jornada do usuário, mapa de stakeholders, perguntas HMW (“Como poderíamos...”), brainstorming, prototipação e testes. Elas orientam a produção dos artefatos; não devem ser automaticamente apresentadas como documentos obrigatórios adicionais.

S1 p.38 descreve um protótipo de baixa ou média fidelidade como entrega esperada da etapa de prototipação. S1 p.40 orienta testar situações normais, ambíguas e de falha, registrar evidências e converter o aprendizado em ajustes. Isso sustenta um protótipo de design e um registro de validação, sem estabelecer a obrigação de desenvolver um front-end próprio.

## 3. Pacote final explicitamente solicitado no guia

O guia, p.13, lista quatro itens para o envio final:

1. **Vídeo de demonstração de 3 minutos**, contendo problema, usuário-alvo, solução, principais recursos e demonstração.
2. **Declaração escrita do problema e da solução, com link para o protótipo funcional.**
3. **Declaração escrita sobre a tecnologia.**
4. **Relatórios das sessões de tarefas do IBM Bob no repositório de código.** O guia também permite incluir link do GitHub ou pasta compartilhada com os ativos. Nas p.30-31, orienta a inclusão das capturas dos resumos relevantes de cada integrante em `bob_sessions/`.

Na mesma página, o guia esclarece que as tarefas semanais são recomendadas e que os entregáveis obrigatórios são **o checkpoint intermediário e o envio final**. Os PDFs consultados não fornecem nesta seção um formulário completo com os campos do checkpoint; o guia remete à plataforma de participantes para a visão geral das tarefas. Não deduzir esses campos a partir do pacote final.

## 4. Como isso muda a organização proposta

- Os códigos D01–D11 do direcional correspondem às 11 entregas nomeadas nos slides; D12/D13 organizam prototipação e validação como apoio. Os códigos A01–A12 anteriores foram substituídos, com correspondência no [plano operacional](plano_15_dias.md).
- Pesquisa, concepção, proposta de valor, estrutura da solução, arquitetura e fluxo funcional têm correspondência direta com os materiais.
- EDA, contrato de dados e relatório de modelo são desdobramentos técnicos úteis ao case Sicredi. As orientações do dataset sugerem EDA, qualidade, validação temporal, prevenção de vazamento, métricas para desbalanceamento e avaliação de custo; não os definem como entregas oficiais separadas do programa.
- Front-end próprio fica sem responsável e fora da alocação. O protótipo de design e o fluxo funcional permanecem distintos. A interface escolhida precisa suportar sessão, vínculo da compra, resposta humana explícita e apresentação do resultado. Texto livre do chat não substitui autorização humana válida.
- A documentação de reprodução e os registros de avaliação apoiam as declarações e a demonstração final. Esforço e datas serão acordados conforme a disponibilidade das quatro pessoas; as estimativas antigas de 15 dias não são compromissos atuais.
- Pessoa 1 lidera negócio/produto; Pessoa 2, pesquisa/usuário; Pessoa 3, estrutura/arquitetura; Pessoa 4, protótipo/evidências/validação. O direcional contém apoio, revisão e aceite por entrega. Os nomes e os executores da implementação serão definidos pela equipe.

## 5. Fontes e páginas conferidas

- **S1:** [Primeira sessão de Design Thinking](../../contexto/First%20DT%20Session%20deck.pdf), p.28, 38, 40 e 60.
- **S2:** [Segunda sessão de Design Thinking](../../contexto/Updated_Second%20Session%20DT%20and%20AI%20Agents_BR_Saulo%20%281%29%20%281%29.pdf), p.47, 54 e 63.
- **S3:** [Empreendedorismo em IA](../../contexto/Updated_Deck_Empreendedorismo_IA_PT_v9.pdf), p.17 e 22.
- **S4:** [Primeira sessão técnica](../../contexto/1st%20Technical%20session-Prototyping%20AI%20Solutions%20with%20IBM%20AI%20Technologies%20%E2%80%93%20Technical%20Session_updated.pdf), p.29.
- **S5:** Segunda sessão técnica, arquivo cujo nome começa por `sessão 2 IBM Agentic AI Technologies`, p.22, na [pasta de contexto](../../contexto/).
- **Guia:** [Guia IBM](../../contexto/2H26%20GuideBob_IBM%20SkillsBuild_AI%20Experiential%20Learning%20Lab%20BR.pdf), p.13 e 30-31.
- **Dataset:** [Orientações do case Sicredi](../../data/Orientacoes_case_prevencao_sicredi.txt), seção “Uso pedagógico sugerido”.
