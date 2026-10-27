---
name: ibm-estilo-materiais
description: Use ao criar ou revisar qualquer material do Watson (telas, slides, documentos, retratos de personas) para mantê-lo no estilo IBM Design Language e Carbon.
---

# Estilo IBM para todos os materiais do Watson

Todo material do time (interfaces, slides, documentação, retratos de personas) segue a IBM Design Language e o Carbon Design System. **Estilo não é marca**: não use o logotipo IBM nem apresente o Watson como produto oficial da IBM ou do Sicredi sem autorização do programa.

## 1. Tema

- Carbon tem 4 temas: **White**, **Gray 10 (g10)**, **Gray 90 (g90)**, **Gray 100 (g100)**. White e g10 são claros; g90 e g100 são escuros.
- Padrão do Watson: **g10** para o app e documentos; **g100** para modo escuro e slides de abertura/destaque. Não misture temas na mesma tela sem motivo (ex.: só o UI shell escuro).
- Use **tokens** (nomes por função), nunca hex solto no código. O token se mantém; o valor muda por tema.

## 2. Tokens de cor principais (valores de @carbon/themes v11)

| Token | g10 | g100 |
|---|---|---|
| `background` | #f4f4f4 (Gray 10) | #161616 (Gray 100) |
| `layer-01` | #ffffff | #262626 (Gray 90) |
| `layer-02` | #f4f4f4 | #393939 (Gray 80) |
| `border-subtle-01` | #e0e0e0 (Gray 20) | #525252 (Gray 70) |
| `text-primary` | #161616 | #f4f4f4 |
| `text-secondary` | #525252 | #c6c6c6 (Gray 30) |
| `link-primary` | #0f62fe (Blue 60) | #78a9ff (Blue 40) |
| `interactive` | #0f62fe | #4589ff (Blue 50) |
| `focus` | #0f62fe | #ffffff |
| `button-primary` | #0f62fe | #0f62fe |
| `support-error` | #da1e28 (Red 60) | #fa4d56 (Red 50) |
| `support-success` | #24a148 (Green 50) | #42be65 (Green 40) |
| `support-warning` | #f1c21b (Yellow 30) | #f1c21b |
| `support-info` | #0043ce (Blue 70) | #4589ff (Blue 50) |

Regras: texto corrido neutro; azul para links e ação primária; cores de suporte **só** para status (erro, sucesso, alerta, info), nunca decoração. Status de fraude sempre com cor + ícone + texto.

## 3. Tipografia

- Família **IBM Plex**: Plex Sans (interface e texto), Plex Serif (editorial, opcional), Plex Mono (código, IDs de transação).
- Pesos: **Light 300, Regular 400, SemiBold 600**. SemiBold só em títulos curtos. Itálico só para ênfase pontual.
- **Conjunto produtivo** (tokens `-01`): compacto, para o app e tarefas. **Conjunto expressivo** (tokens `-02`): maior, para slides, páginas editoriais e leitura longa. Não use expressivo dentro do app.
- Escala (px): 12, 14, 16, 18, 20, 24, 28, 32, 36, 42, 48, 54, 60, 68, 76, 84, 92.
- Alinhamento à esquerda; **sentence case** (só a primeira letra maiúscula); evite CAIXA ALTA; linhas curtas; títulos longos quebrados em 2–3 linhas.

## 4. 2x Grid

- **Mini unidade de 8 px**; tudo (colunas, margens, paddings) em múltiplos: 8, 16, 24, 32, 48, 64, 80.
- Breakpoints: sm 320 px (4 col.), md 672 px (8 col.), lg 1056 px (16 col.), xlg 1312 px (16 col.), max 1584 px (16 col.). Gutter de 32 px quando usado.
- Divisões de dois (2, 4, 8, 16 colunas); mantenha a mesma grade em todo o material.
- Proporções de imagem e área: 16:9, 4:3, 3:2, 2:1 ou 1:1.

## 5. Componentes chave do Watson

- **UI shell**: header no topo, nome do produto à esquerda, ícones utilitários à direita (busca à esquerda do grupo, troca de app sempre à extrema direita); side nav opcional; link "Pular para o conteúdo" como primeiro foco.
- **Data table** (transações): tamanho de linha igual no header e nas linhas; ordenação por coluna; seleção por checkbox e barra de ações em lote; até 5 ações na toolbar; paginação embaixo; skeleton em vez de spinner; títulos de coluna com 1–2 palavras.
- **Tag**: categorizar (ex.: "Online", "Internacional"); cores diferentes por categoria; não use tag como link.
- **Notification**: inline (no fluxo, persiste), toast (canto superior direito, some sozinha — nunca só ela para info crítica), actionable (uma ação), callout (orientação fixa, sem sucesso/erro). Título curto, sem ponto final; erro sempre diz o que fazer.
- **Button**: **um primário por tela**; secundário só junto do primário (Cancelar/Voltar); danger para bloquear/excluir; rótulo verbo + substantivo ("Bloquear cartão"), sentence case, nunca truncado.
- **Modal**: só para confirmar decisão ou informação urgente; transacional (Cancelar à esquerda, primário à direita); danger para irreversível. Não use para mensagens não críticas nem tarefas frequentes.
- **IA (Carbon for AI)**: marque conteúdo gerado/recomendado pela IA com o **AI label**, que abre explicação resumida; permita ao usuário sobrescrever e **reverter** a sugestão da IA. O estilo de presença de IA é só para identificar IA, nunca decoração.

## 6. Slides

- Grade 2x: 16:9, margens e espaçamentos em múltiplos da mini unidade; 8 ou 16 colunas; conteúdo alinhado à grade e à esquerda.
- **Uma ideia por slide**; título é a conclusão em sentence case ("O associado decide em menos de 30 s"), não o assunto ("Resultados").
- Hierarquia por tamanho e peso (Plex Sans, conjunto expressivo): título, subtítulo, corpo; no máximo 3 níveis.
- Fundo g10/White ou g100; azul 60 como cor de destaque; cores de suporte só para status; sem gradientes, sombras ou clip-arts.
- Texto mínimo: até ~30 palavras de corpo; dados em gráfico simples com rótulo direto.
- Contraste AA (4,5:1 texto, 3:1 elementos gráficos).

## 7. Retratos, fotos e ilustração de pessoas (personas)

**Fotografia**
- Realista e sincera: "IBM imagery is allergic to artificiality." Cenas reais, não encenadas.
- Luz natural; sem tons quentes de pôr do sol, filtros, color grading, sobreposições ou retoques visíveis.
- **Altura dos olhos** (relação de igual para igual); foco nítido; um ponto focal claro; recorte 16:9, 4:3, 3:2, 2:1 ou 1:1.
- Evite clichês de banco de imagem (cadeado brilhante, hacker de capuz) e abstrações.

**Ilustração de pessoas**
- Simples, mas realista; proporções reais (figura de 8 cabeças); **nunca caricatura ou exagero**.
- Expressão **neutra**; retrato deve parecer retrato, não desenho animado.
- Diversidade de gênero, idade, raça, deficiência, tipos de corpo e cultura; adereços culturais com moderação.
- Paleta de pele/cabelo própria (Rose e Almond), só para pessoas.

**Personas geradas por IA**: rotule como ilustração fictícia; não use rosto de pessoa real; evite estereótipos ligados a fraude (ex.: idoso confuso, jovem "golpista").

## 8. Checklist final (antes de entregar qualquer material)

- [ ] Tema único e coerente (g10 ou g100); cores via tokens.
- [ ] Só IBM Plex; pesos 300/400/600; sentence case; alinhado à esquerda.
- [ ] Espaçamentos em múltiplos de 8 px; grade 2x respeitada.
- [ ] Um botão primário por tela; modais só onde necessário.
- [ ] Status com cor + ícone + texto; conteúdo de IA com AI label e reversão.
- [ ] Contraste AA verificado; alvos ≥ 24 px; foco visível.
- [ ] Slides: uma ideia por slide, título-conclusão, ≤ 3 níveis.
- [ ] Imagens realistas, neutras, diversas, sem caricatura nem clichê.
- [ ] Sem logotipo IBM/Sicredi não autorizado; dados fictícios.

## Referências

- Carbon Design System: https://carbondesignsystem.com
- Carbon, temas: https://carbondesignsystem.com/elements/themes/overview/
- Carbon, tokens de cor: https://carbondesignsystem.com/elements/color/tokens
- Fonte dos valores g10/g100: https://cdn.jsdelivr.net/npm/@carbon/themes@11.40.0/src/g10.js , https://cdn.jsdelivr.net/npm/@carbon/themes@11.40.0/src/g100.js , https://cdn.jsdelivr.net/npm/@carbon/themes@11.40.0/src/component-tokens/button/tokens.js , https://cdn.jsdelivr.net/npm/@carbon/colors@11.61.0/lib/index.js
- Carbon, tipografia: https://carbondesignsystem.com/elements/typography/overview/
- Carbon, 2x Grid: https://carbondesignsystem.com/elements/2x-grid/overview/
- IBM Design Language, 2x Grid: https://ibm.com/design/language/2x-grid
- IBM Design Language, type basics: https://ibm.com/design/language/typography/type-basics
- Carbon, UI shell: https://carbondesignsystem.com/components/UI-shell-header/usage/
- Carbon, data table: https://carbondesignsystem.com/components/data-table/usage/
- Carbon, tag: https://carbondesignsystem.com/components/tag/usage/
- Carbon, notification: https://carbondesignsystem.com/components/notification/usage/
- Carbon, button: https://carbondesignsystem.com/components/button/usage/
- Carbon, modal: https://carbondesignsystem.com/components/modal/usage/
- Carbon for AI e AI label: https://carbondesignsystem.com/guidelines/carbon-for-ai/ , https://carbondesignsystem.com/components/ai-label/usage/
- Carbon, acessibilidade: https://carbondesignsystem.com/guidelines/accessibility/overview/
- IBM Design Language, fotografia: https://www.ibm.com/design/language/photography/overview e https://ibm.com/design/language/photography/tips-and-techniques
- IBM Design Language, ilustração de pessoas: https://ibm.com/design/language/illustration/people
