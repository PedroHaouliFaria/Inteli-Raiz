# Glossário

Vocabulário único para telas, documentos e apresentação. **Revisão:** 04/11/2026, alinhada ao [plano](../../05_gestao/plano_implementacao.md) e aos textos do app do associado.

## Termos atuais

| Termo | Definição | Quem vê |
|---|---|---|
| **Compra sinalizada** | Compra que o sistema avaliou e para a qual pede confirmação do associado. Nunca dizemos ao associado que é "fraude". | Associado |
| **Pedido de confirmação** | Pergunta individual sobre uma compra, com prazo. No código: `confirmation` / `challenge_id`. | Associado |
| **Motivos do alerta** (sinais) | Características da compra em linguagem simples, como "Feita sem o cartão físico", "Feita de madrugada" ou "Primeira compra registrada com este cartão". Descrevem a compra; não são a causa comprovada da avaliação. | Associado |
| **Reconheço e autorizo** | Resposta `AUTHORIZE`. A compra é liberada **na simulação**. | Associado |
| **Não reconheço** | Resposta `DENY`. A compra é recusada na simulação e abre uma revisão de proteção. **O cartão não é bloqueado.** | Associado |
| **Estou em dúvida** | Resposta `UNSURE`. A compra não é autorizada e vai para revisão humana. | Associado |
| **Prefiro falar com uma pessoa** | Pedido de atendimento. Abre uma revisão, mas **não** responde à confirmação nem estende o prazo: o associado ainda pode responder enquanto o prazo vale. No plano e nas entregas aparece como "Quero falar com alguém". | Associado |
| **Prazo / Prazo encerrado** | Tempo para responder (900 s na demo, configurável). Depois dele a confirmação expira e **nada é autorizado**. | Associado |
| **Revisão** | Pedido de análise humana, com protocolo (`RZ-AAAAMMDD-0001`). Tipos: dúvida, proteção e falha da avaliação. | Associado e analista |
| **Assistente** | Agente de IA do chat. Consulta a compra e o status, explica e pode abrir revisão; **não** responde à confirmação pelo associado e não inventa informação que não tem (por exemplo, o nome do estabelecimento). | Associado |
| **Simulação** | Toda compra e ação é fictícia. Nenhuma transação, bloqueio ou comunicação financeira real acontece. | Todos |
| **Score interno do modelo** | Número de 0 a 1 calculado pelo modelo de risco. Aparece só para a analista, como número decimal; não é "probabilidade de fraude" e nunca é mostrado ao associado nem ao assistente. | Analista |
| **Política conservadora** | Regra em uso: toda compra avaliada pede confirmação, até haver evidência para liberar alguma automaticamente. | Equipe |

## Estados da compra

| Estado | Significado |
|---|---|
| `AGUARDANDO_ASSOCIADO` | Esperando a resposta dentro do prazo |
| `LIBERADA_SIMULACAO` | Autorizada pelo associado |
| `RECUSADA_SIMULACAO` | Recusada pelo associado; revisão de proteção aberta |
| `REVISAO_PENDENTE` | Em dúvida ou falha da avaliação; aguardando revisão humana |
| `CONFIRMACAO_EXPIRADA` | Prazo encerrado sem resposta; nada autorizado |

## Termos do console antigo

Usados na alta fidelidade de 26/10 e nos dados fixos do console antigo (`watson/frontend/src/mocks/glossary.js`). Não valem para o fluxo atual.

| Termo antigo | O que era | Equivalente hoje |
|---|---|---|
| Alerta | Transação marcada pelo modelo como suspeita | Compra sinalizada |
| Caso | Unidade de trabalho da analista, juntando alertas do mesmo cartão | Revisão (só nas exceções) |
| Aviso de compra / "Foi você?" | Mensagem ao associado no app | Pedido de confirmação |
| "Fui eu" | Resposta de reconhecimento, com biometria no alto risco | Reconheço e autorizo (sem biometria no MVP) |
| Aguardando associado | Status do caso enquanto o aviso esperava resposta | `AGUARDANDO_ASSOCIADO` |
| Score de risco (acima de 0,80 = alto) | Mostrado à analista como probabilidade | Score interno do modelo, sem faixas na política atual |
| Confiança do agente / Tempo até a decisão | Indicadores do console da analista | Fora do fluxo atual |
| Rajada / Tentativa simulada | Indicador e tentativas geradas para a linha do tempo do cartão | Fora do fluxo atual ([linha do tempo](../../04_dados_e_modelo/dados/linha-do-tempo.md)) |
