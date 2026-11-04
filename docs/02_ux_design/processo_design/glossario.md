# Glossário do Watson

Vocabulário único, usado nas telas, nas tooltips educativas e nos materiais (decisão do Leo em 26/10/2026: o usuário aprende usando a plataforma).

| Termo | Definição (texto da tooltip) | Quem vê |
|---|---|---|
| **Alerta** | Transação que o modelo marcou como suspeita (score acima do limite). É gerado automaticamente, um por compra. | Analista |
| **Caso** | Unidade de trabalho da analista. Junta os alertas do mesmo cartão e guarda investigação, contato com o associado, decisão e justificativa. Ex.: 3 compras em rajada = 3 alertas, 1 caso. | Analista |
| **Score de risco** | Probabilidade estimada de fraude, de 0 a 1. Acima de 0,80 é alto risco. | Analista |
| **Tempo até a decisão** | Tempo médio entre o caso entrar na fila e a analista registrar a decisão (bloquear, liberar ou escalar). Medido pelo Watson a partir do registro de eventos do caso. No MVP: medido em teste de usabilidade (tarefa T1). | Analista / gestão |
| **Aguardando associado** | Enviamos um aviso de compra ao associado e esperamos a resposta no app. | Analista |
| **Confiança do agente** | Quanto o Watson confia na recomendação, com base na força e na concordância dos sinais. A decisão final é sempre da analista. | Analista |
| **Rajada** | Muitas tentativas do mesmo cartão em pouco tempo. No case ela vem como contador pronto (tentativas no terminal na última hora), não como compras separadas. | Analista |
| **Tentativa simulada** | Tentativa gerada pela simulação do Watson para a demonstração, coerente com o contador de rajada do case. Não vem do case, não recebe score, não vira alerta e não conta nas métricas. Aparece com o selo "Simulada". | Analista |
| **Aviso de compra** | Mensagem no app pedindo ao associado que confirme uma compra diferente do costume. Nunca se chama "alerta" para o associado. | Associado |
