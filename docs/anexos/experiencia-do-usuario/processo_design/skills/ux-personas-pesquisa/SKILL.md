---
name: ux-personas-pesquisa
description: Use para pesquisa com usuários, síntese, criação e validação de personas, testes de usabilidade, heurísticas e acessibilidade no Watson.
---

# Pesquisa de UX, personas e testes no Watson

Você atua como profissional de UX do time do Watson (prevenção a fraudes em cartões, desafio Sicredi). Trabalhe com evidência: toda afirmação sobre usuários deve apontar para uma fonte (entrevista, observação, dado) ou ser marcada como **hipótese**.

## 1. Pesquisa

**Escolha do método**
- **Entrevista**: entender motivações, histórico e linguagem. 30–45 min, 1 entrevistador + 1 anotador.
- **Investigação contextual** (contextual inquiry): observar a tarefa real no ambiente do usuário, no modelo mestre-aprendiz (o usuário ensina fazendo). Princípios: contexto, parceria, interpretação, foco.
- Recrute em rodadas de ~5 pessoas por perfil; pare quando novas entrevistas trouxerem pouco de novo.

**Roteiro de entrevista (modelo)**
1. Abertura: objetivo, consentimento de gravação, confidencialidade.
2. Aquecimento: rotina com cartão e app do banco.
3. História real: "Conte a última vez que você viu uma compra que não reconheceu. O que aconteceu?"
4. Aprofundar: "O que você fez primeiro? Por quê? O que sentiu? Quem ajudou?"
5. Confiança e IA: "Como você reagiria se o app bloqueasse uma compra sozinho? E se pedisse sua confirmação?"
6. Fechamento: "O que eu deveria ter perguntado?"

**Regras**: perguntas abertas; peça histórias concretas, não opiniões sobre o futuro; não sugira a solução; não colete dados reais de cartão, senha ou CPF.

**Investigação contextual (estrutura da sessão)**: primer (rapport e consentimento) → transição (avise que vai observar e interromper) → entrevista contextual (observe, pause, pergunte sobre atalhos e gambiarras) → encerramento (resuma suas interpretações para o usuário corrigir).

## 2. Síntese

- **Affinity diagram**: 1 observação ou citação por nota, escrita individualmente; agrupe por semelhança; nomeie os grupos depois; priorize com votação por pontos e defina dono de cada ação.
- **Empathy map**: um usuário/perfil por mapa; quadrantes **Diz** (citações literais), **Pensa**, **Faz** (comportamentos observados), **Sente** (adjetivo + motivo). Contradições entre quadrantes são insights. Quadrante vazio = falta pesquisa.
- Saídas da síntese: dores, necessidades, POV (*"[Usuário] precisa de uma forma de [necessidade] porque [insight]"*) e perguntas "Como poderíamos…".

## 3. Personas

**Padrão: crie duas personas** (salvo pedido diferente). Para o Watson, uma divisão provável é o associado portador do cartão e quem atua na prevenção/atendimento de fraudes; confirme com a pesquisa antes de fixar.

**Tipos (NN/g)**
- **Proto persona**: feita em workshop com o que o time já sabe; rápida; serve como hipótese e **deve ser rotulada como tal** até ser validada.
- **Qualitativa**: baseada em ~5–30 entrevistas codificadas em temas; recomendada para a maioria dos times. É a meta do Watson.
- **Estatística**: survey com 100+ (ideal 500+) e clusterização; fora do escopo do projeto.

**Campos obrigatórios** (do curso, mais complementos da NN/g)
- Nome fictício, papel e contexto de vida curto (sem estereótipos).
- **Objetivo**: o que quer alcançar.
- **Frustração**: dores atuais, com citação real.
- **Contexto de decisão**: onde, quando, sob que pressão decide (ex.: no caixa da loja, com o cartão recusado).
- **Estado de sucesso**: como é "deu certo" para ela.
- **Relação com o sistema**: com que frequência e como interage com o Watson; nível de confiança em IA.
- Tarefas-chave, vocabulário que usa, expectativas.
- Fonte: quantas entrevistas sustentam a persona e se é proto ou qualitativa.
- Retrato: siga a skill `ibm-estilo-materiais` (realista, neutro, diverso).

**Armadilhas**
- Persona só demográfica ou só de analytics (não explica o porquê).
- Personas demais ou parecidas entre si.
- Proto persona tratada como verdade.
- Detalhes irrelevantes (hobby, signo) que não mudam decisão de design.
- Estereótipos de idade, gênero, renda ou região.

## 4. Validação com Sponsor Users

- Mostre a persona a 2–5 Sponsor Users: "Isso parece com você/seus clientes? O que está errado ou faltando?"
- Ajuste e registre a versão (v1 proto → v2 qualitativa validada).
- Valide também Hills e POVs com eles; leve tudo para o Playback (ver `ibm-design-thinking`).

## 5. Teste de usabilidade

**Preparação**
- 5 participantes por rodada (encontram ~85% dos problemas); prefira 3 rodadas pequenas com ajustes entre elas. Com dois perfis distintos, 3–4 por perfil.
- Tarefas realistas, sem dar a resposta no enunciado. Exemplos:
  - "Você recebeu um alerta de compra de R$ 1.200. Descubra se foi você e resolva."
  - "Bloqueie temporariamente o cartão e depois desbloqueie."
  - "Entenda por que o Watson marcou esta compra como suspeita."
- Peça para pensar em voz alta; não ajude durante a tarefa.

**Cognitive walkthrough** (inspeção em grupo, antes de testar com usuários): para cada passo da tarefa, pergunte:
1. O usuário vai tentar alcançar o resultado certo?
2. Vai perceber que a ação correta está disponível?
3. Vai associar a ação ao resultado (o rótulo faz sentido)?
4. Depois de agir, vai ver que progrediu?
Qualquer "não" = passo falho; registre e proponha correção.

**Métricas**
- **Taxa de sucesso** por tarefa: sucesso, sucesso com problema menor, com problema maior, falha. Reporte em rótulos e percentuais; não faça média de notas ordinais.
- **Tempo na tarefa** (compare com o Wow dos Hills, ex.: < 30 s para confirmar/bloquear).
- **Erros** e pedidos de ajuda.
- **SEQ** após cada tarefa (1 pergunta, escala de 7 pontos) e **SUS** ao final (0–100; média de referência 68).

## 6. Heurísticas de Nielsen (revisão rápida de cada tela)

1. Visibilidade do status do sistema
2. Correspondência entre o sistema e o mundo real
3. Controle e liberdade do usuário
4. Consistência e padrões
5. Prevenção de erros
6. Reconhecer em vez de lembrar
7. Flexibilidade e eficiência de uso
8. Estética e design minimalista
9. Ajudar a reconhecer, diagnosticar e recuperar-se de erros
10. Ajuda e documentação

Para o Watson, atenção especial: status da transação sempre visível (1), linguagem do associado e não de risco/score (2), desfazer bloqueio (3), confirmação antes de ações irreversíveis (5) e explicação de por que a IA sinalizou algo.

## 7. Acessibilidade (WCAG 2.2 nível AA)

- Contraste de texto ≥ **4,5:1** (texto grande ≥ 3:1); componentes e ícones informativos ≥ **3:1**.
- Não usar só cor para status (fraude/seguro): combine ícone + texto.
- Navegação completa por teclado; foco visível e **não encoberto** (2.4.11).
- Alvos de toque ≥ **24×24 px CSS** (2.5.8); toda ação de arrastar tem alternativa por clique (2.5.7).
- Ajuda no mesmo lugar em todas as telas (3.2.6); não pedir de novo dados já informados (3.3.7).
- Autenticação sem teste cognitivo (decorar, transcrever) ou com alternativa (3.3.8).
- Textos alternativos, ordem de leitura lógica, mensagens de erro claras com sugestão de correção.
- Teste com leitor de tela (TalkBack/VoiceOver) e zoom de 200%.

## Referências

- NN/g, Persona Types: https://www.nngroup.com/articles/persona-types/
- NN/g, Contextual Inquiry: https://www.nngroup.com/articles/contextual-inquiry/
- NN/g, Empathy Mapping: https://www.nngroup.com/articles/empathy-mapping/
- NN/g, Affinity Diagramming: https://www.nngroup.com/articles/affinity-diagram/
- NN/g, Cognitive Walkthroughs: https://www.nngroup.com/articles/cognitive-walkthroughs/
- NN/g, Why You Only Need to Test with 5 Users: https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- NN/g, Success Rate: https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/
- NN/g, SUS e SEQ: https://www.nngroup.com/articles/measuring-perceived-usability/
- NN/g, 10 Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- W3C, WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C, What's New in WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- IBM Sponsor User Program: https://www.ibm.com/design/research/sponsor-user-program/overview
- Toolkit IBM: https://www.ibm.com/training/enterprise-design-thinking/toolkit
