# Plano operacional por entregas — Inteli-Raiz

**Revisão de 27/10/2026 · Quatro pessoas · Confirmação de compras pelo associado.**

O nome `plano_15_dias.md` foi mantido para preservar os links existentes. A organização vigente é por entregas e dependências. A janela de 15 dias, a equipe de cinco pessoas e as estimativas de horas da proposta anterior não são compromissos atuais. Datas e disponibilidade precisam ser combinadas pela equipe.

**Objetivo:** entregar uma prova de conceito de IA agêntica que ajude o associado a entender e responder a uma compra sinalizada, com resultado registrado e revisão humana das exceções. Dados e ações financeiras são simulados.

## 1. Como usar os documentos

| Documento | Papel |
|---|---|
| [Plano de implementação](../../docs/plano_implementacao.md) | Define produto, política, estados, contratos, requisitos e testes |
| [Direcional das entregas](../../docs/direcional_entregas.md) | Explica D01–D13: conteúdo, produção, revisão, fontes e critérios de qualidade |
| [Backlog](backlog.md) | Transforma o plano em cards C01–C32, com responsáveis e dependências |
| [Catálogo dos materiais](artefatos_materiais_contexto.md) | Identifica entregas recomendadas e pacote obrigatório da IBM |

Este documento organiza a execução; não substitui o detalhamento dos requisitos ou das entregas. Os cards são planejamento e não evidência de implementação concluída.

## 2. Fluxo e limites do produto

1. Uma compra sintética é recebida e avaliada pela ferramenta de risco.
2. Uma política determinística e versionada decide liberação simulada, solicitação de confirmação ou revisão de exceção.
3. O associado vê a compra, seus detalhes e o motivo verificável da solicitação.
4. O associado pode reconhecer e autorizar, não reconhecer ou informar dúvida. A conversa ajuda a esclarecer contexto; a resposta explícita acontece pelo controle humano previsto.
5. O backend valida sessão, vínculo da compra, versão, validade e repetição; persiste resposta, ação e status.
6. Sem resposta, a confirmação expira sem autorização presumida. Falta de contexto ou falha de serviço gera tratamento explícito e revisão quando aplicável.

O agente consulta informações e solicita revisão. Ele não autoriza em nome do associado. Recusar a compra não equivale a bloquear automaticamente todo o cartão. O analista participa das exceções; uma mesa completa de análise não faz parte do recorte.

**Interface:** desenvolvimento de front-end próprio continua sem responsável e fora da alocação ativa. O grupo deve escolher e comprovar uma interface que permita resposta humana explícita, sessão, vínculo da compra e apresentação do resultado. Um chat de texto livre sozinho não atende a esses requisitos. Se a ferramenta disponível não suportar esse caminho, a equipe precisa resolver essa dependência antes de declarar o MVP completo.

**Prioridade:** caminho completo, contexto fiel, persistência, testes e experiência compreensível. Segundo modelo, dashboards, telas decorativas, RAG ou múltiplos agentes só entram depois, com necessidade demonstrada. Integração bancária real, bloqueio efetivo e streaming produtivo permanecem fora do escopo.

## 3. Divisão em quatro pessoas

Usar Pessoa 1–4 até a equipe informar os nomes. Esses rótulos não reaproveitam automaticamente os cinco nomes do planejamento anterior.

| Pessoa | Liderança | Apoio e revisão | Pacote final |
|---|---|---|---|
| Pessoa 1 | D01 Oportunidades; D04 Priorização; D05 Conceito; D07 Ideia; D08 Valor/IA | Revisa empatia/persona; mantém escopo e narrativa coerentes | Texto de problema/solução e roteiro de apresentação |
| Pessoa 2 | D02 Empatia; D03 Cenário Atual; D06 Persona e Cenários | Apoia pesquisa, linguagem, protótipo e moderação; revisa D12/D13 | Confere narrativa do usuário, achados e limites |
| Pessoa 3 | D09 Estrutura; D10 Arquitetura | Consolida contratos, dados/modelo e estado real das integrações; revisa D04/D08/D11 | Declaração tecnológica e instruções técnicas |
| Pessoa 4 | D11 Registro do Fluxo; D12 Protótipo; D13 Validação | Organiza reprodução, evidências, testes e correções com os autores | Vídeo, índice, links e conferência de acesso |

A [matriz por entrega](../../docs/direcional_entregas.md#organização-em-quatro-pessoas-responsáveis-sequência-e-revisão) define o revisor principal e o resultado para aceite. Liderar o documento não significa desenvolver sozinho os componentes associados. Pessoa 3 coordena a definição dos executores técnicos; cada card de implementação só fica pronto para iniciar quando executor e revisor com competência técnica estiverem identificados. Pessoa 4 registra e testa o fluxo entregue pelos autores técnicos.

Cada integrante entrega suas próprias evidências do IBM Bob. O líder cadastrado na plataforma realiza o envio, independentemente da função documental acima.

## 4. Sequência por dependência

| Etapa | Trabalho | Evidência para avançar |
|---|---|---|
| Descoberta | Pessoas 1 e 2 produzem D01–D03; Pessoa 3 verifica acessos/contratos; Pessoa 4 prepara esboço e teste | Problema, contexto, fontes, hipóteses e dependências identificados |
| Escolha e valor | Pessoa 1 facilita D04 e consolida D05/D07/D08; Pessoa 2 fecha D06 | Alternativas comparadas, persona funcional e valor/IA justificados |
| Estrutura e protótipo | Pessoa 3 fecha D09/D10; Pessoa 4 refina D12 com Pessoa 2 | Requisitos, estados, contratos e resposta humana explícita compatíveis |
| Implementação e integração | Autores técnicos implementam ferramentas, avaliação, política, persistência e resposta; Pessoa 4 prepara D11 | Mesma compra rastreável pelos componentes, inclusive em falha |
| Validação e melhoria | Pessoa 4 consolida D13, Pessoa 2 modera e autores corrigem | Observações, métricas, correções e reteste documentados |
| Consolidação | As quatro pessoas fecham declarações, vídeo, links e Bob | Evidências e acesso conferidos na mesma versão candidata |

Contratos e exemplos sintéticos identificados permitem trabalho paralelo. Protótipo de design permite testar compreensão antes da aplicação integrada. O teste final de D11/D13 deve registrar qual versão e qual ambiente foram usados.

## 5. Cuidados de dados e modelo preservados

O planejamento anterior registrou uma cópia local com 160.000 linhas, 297 colunas e 146 positivos em `feedback_label`, apesar da referência a 900.000 linhas no nome/orientações. Esses números são um registro da conferência anterior, não uma nova execução nesta revisão. Reproduzir as contagens e identificar a versão da base antes de publicar métricas.

Verificações necessárias, relacionadas aos cards C04, C05, C11 e C16:

- Confirmar alvo, período, ausências, tipos e positivos por partição. Auditar disponibilidade temporal de `fraud`, `fraud_score`, `decision`, disputas e feedbacks antes de aprovar preditores.
- Reconciliar o manifesto de 28 features com documentos que mencionam 31; alinhar definição de madrugada, nulos, categorias e ordem das classes entre treino e inferência.
- Ajustar preparo e limiar na validação; preservar avaliação final independente. O teste já consultado para escolha de limiar é exploratório.
- Comparar o candidato com uma baseline e com/sem as quatro features de velocidade pré-calculadas. Métricas perfeitas na base sintética exigem investigação.
- Declarar a convenção de PR-AUC/average precision; registrar precision, recall, falsos positivos, matriz de confusão e volume de alertas no limiar escolhido.
- Versionar pré-processamento, atributos, modelo, política e contrato. Chamar score de probabilidade calibrada apenas com avaliação que sustente essa interpretação.

O [plano §7](../../docs/plano_implementacao.md) e a [documentação do modelo](../../docs/03_modelo.md) orientam esse trabalho. Qualquer alternativa por regras precisa de identificação, política própria e declaração honesta na demonstração.

## 6. Marcos de revisão e critérios de corte

| Marco | Critério de passagem | Ação diante de pendência |
|---|---|---|
| Recorte revisado | D01–D08 coerentes, com evidências ou hipóteses identificadas | Investigar a hipótese que pode mudar a escolha antes de expandir |
| Contratos e interface viáveis | Ferramentas, sessão, resposta explícita e estados demonstráveis | Priorizar acesso/integração e decidir interface mínima compatível |
| Primeira integração | Compra → avaliação → política → confirmação → resposta → persistência | Concentrar executores no caminho; adiar recursos adicionais |
| Versão candidata | Modelo/política/contrato identificados; cenários críticos executados | Abrir correções com dono e preservar rastreabilidade |
| Validação revisada | D13 com achados, correções e retestes; sem falha crítica aberta | Corrigir e repetir o cenário afetado antes da gravação final |
| Envio | Outra pessoa reproduz; vídeo, declarações, links e Bob conferidos | Resolver acesso/versão e guardar confirmação da plataforma |

Não transportar estimativas de horas da equipe de cinco pessoas. Acordar disponibilidade das quatro pessoas e esforço por card, reservando espaço para integração e correção. O critério principal de corte é preservar o fluxo seguro e compreensível e o pacote obrigatório.

## 7. Gestão e conclusão

- Quadro: **Backlog → Pronto para iniciar → Em andamento → Em revisão → Concluído**. Registrar impedimento, responsável por destravar e próximo passo.
- Um responsável e um revisor diferentes por entrega; critérios e evidências determinam o aceite.
- Reuniões curtas acompanham resultado, próximo compromisso e dependência. Limitar atividades simultâneas e ajudar nas revisões quando houver espera.
- Registrar mudanças de contrato e atualizar consumidores, documentação e evidências na mesma versão.
- Para pesquisa: fonte e implicação; para design: percurso e estados; para negócio: premissas e evidência; para programação: execução e verificações relevantes.

O [direcional](../../docs/direcional_entregas.md) relaciona as entregas aos quatro critérios IBM. As tarefas recomendadas apoiam a qualidade; checkpoint e envio final continuam sendo as entregas obrigatórias, conforme o guia. Conferir situação, campos e prazo vigente na plataforma antes da submissão.

## 8. Correspondência com a proposta anterior

Os códigos A01–A12 deixam de orientar o quadro vigente. A correspondência abaixo preserva o propósito das atividades úteis; não comprova conclusão nem migra automaticamente os critérios do recorte antigo.

| Referência anterior | Destino no planejamento vigente |
|---|---|
| A01 Pesquisa/oportunidades | D01, D04 e base de pesquisa de D02/D03 |
| A02 Jornada/histórias | D02, D03, D06 e requisitos do associado em D09 |
| A03 Valor/viabilidade | D08 e seus cenários de custo/adoção |
| A04 Dados e A07 Modelo | Insumos de D09/D10/D11; C04, C05, C11, C16 e C25 |
| A05 Arquitetura/contratos | D09/D10 |
| A06 Protótipo | D12, agora centrado na compra e resposta do associado |
| A08 Agente/backend | Implementação necessária a D10/D11, com política externa e autorização humana |
| A09 Front-end próprio | Continua sem alocação; decisão da interface mínima é dependência explícita |
| A10 Validação | D13, com teste de compreensão e correções |
| A11 Reprodução | D11, C28 e declaração tecnológica |
| A12 Pacote final | C23 e C29–C32; divisão entre quatro pessoas no direcional |
