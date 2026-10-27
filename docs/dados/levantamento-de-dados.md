# Levantamento: que dados o Watson precisa guardar

> Termos seguem o [glossário do Watson](../design/glossario.md): **alerta** é o que o sistema gera, **caso** é o que a analista trata, **aviso de compra** é a mensagem ao associado.
>
> Técnica: rastreamos cada dado até **uma necessidade de pessoa ou de tela** (personas, Hills, contramedidas da anti-persona e wireframe escolhido: B com a fila da A e o quadro da C). Dado sem dono não entra. Fontes: `design/00-descoberta/`, `design/01-wireframe/` e o dicionário do case (`data/dicionario_dados_case_prevencao_sicredi.xlsx`, 297 colunas).

## 1. De onde vem cada dado

| Origem | O que é | Como o Watson trata |
|---|---|---|
| **Sistemas da cooperativa** (simulados pelo dataset do case) | Associado, conta, cartão, estabelecimento, dispositivo, transação | Só leitura. Copiamos para o Watson apenas as colunas que alguma tela ou o modelo usa. |
| **Modelo de risco** | Score, fatores explicáveis, versão do modelo | Gravado pelo Watson a cada transação avaliada. |
| **Agente Watson** | Agrupamento de alertas, resumo, recomendação, justificativa gerada, conversa | Gravado pelo Watson. Sempre com versão e confiança. |
| **Pessoas** | Decisão da analista, resposta do associado no app | Gravado pelo Watson. Fonte da trilha de auditoria. |

## 2. Necessidade → dado

| Necessidade (quem, onde) | Dados que precisam existir |
|---|---|
| Fila ordenada por **risco × valor** (Camila, fila da A) | score, faixa de risco, valor, tempo na fila, status do caso |
| **Por que é suspeito**, com peso de cada fator, inclusive os que reduzem o risco (Camila, caso B) | fatores do score: código, texto em linguagem de negócio, peso, sentido (+/−), evidência ("5 tentativas em 7 min") |
| **Linha do tempo do cartão** (caso B) | transações do mesmo cartão com horário, valor, loja, cidade, canal (presente / não presente) e situação (normal, retida, em análise) |
| Mapa, distância, dispositivo, perfil do associado (caso A) | lat/long do terminal, do IP e do estabelecimento; região de costume do associado; dispositivo e se é novo |
| **Quadro** com colunas Novo, Aguardando associado, Em análise, Resolvido (C) | status do caso e histórico de mudanças com quem e quando |
| **Agrupar alertas do mesmo cartão** em um só caso (C) | relação caso → vários alertas, motivo do agrupamento |
| **Resumo do agente** e recomendação com confiança, "ainda não sei" (B e C) | recomendação: ação sugerida, confiança, texto, fatores usados, lacunas, versão do agente |
| **Pergunte ao Watson** (painel lateral B) | mensagens da conversa por caso: autor (analista ou agente), texto, horário |
| Ações **Bloquear, Perguntar ao associado, Liberar, Escalar**, "nada acontece sem sua confirmação" | decisão da analista: ação, se aceitou a recomendação, confirmação; ações executadas e o resultado (cartão bloqueado, compras retidas recusadas) |
| **Justificativa gerada, editável, vai para a auditoria** | texto gerado e texto final, separados, mais autor da edição |
| **Aviso de compra** "Foi você?" no app (Valdir, app B) | aviso enviado: canal (só in-app), horário de envio, leitura, resposta (Fui eu, Não reconheço, Falar com uma pessoa), horário da resposta |
| **Atrito assimétrico**: "Fui eu" no alto risco pede biometria (anti-persona) | se biometria foi exigida e se passou |
| **Aparelho trocado recentemente** não aceita "Fui eu" sozinho (anti-persona) | aparelhos do app do associado com data de cadastro; flags de troca de telefone e e-mail |
| Estado final tranquilizador para o Valdir (cartão protegido, nada cobrado) | status do cartão e das transações retidas |
| KPIs: casos abertos, alto risco, **Tempo até a decisão**, aguardando associado (A) | derivados do caso e do registro de eventos do caso (horários criado, aberto, decidido); não precisam de tabela própria |
| Métricas contra o Impostor: "Fui eu" em casos que viraram fraude, tempo até o bloqueio, falsos positivos por associado | desfecho final de cada caso (fraude confirmada ou legítima) ligado à resposta do associado e às datas |
| Monitoramento do modelo (PR-AUC, drift; depois do MVP) | versão do modelo, limiar usado, rótulo final de cada transação (`feedback_label`) |

## 3. O que o dataset do case já traz (e o que aproveitamos)

| Categoria no dicionário | Colunas | Exemplos que usamos | Exemplos que **não** guardamos |
|---|---|---|---|
| cliente (associado) | 51 | `customer_id`, `customer_name`, `customer_city`, `customer_region`, `customer_registration_date`, `customer_risk_rating`, `customer_segment`, `customer_phone_change_flag`, `customer_email_change_flag` | `customer_ssn`, `customer_passport_number`, `customer_driver_license`, `customer_citizen_id_number`, renda, data de nascimento |
| conta | 33 | `account_id`, `account_status`, `account_type`, `account_credit_limit`, `account_available_credit` | IBAN, BIC, assinatura digital |
| cartão | 28 | `card_id`, `card_last4`, `card_brand`, `card_type`, `card_status`, `card_presence_flag`, `card_credit_limit` | `card_pan` (número completo), `card_ver_data` |
| estabelecimento | 23 | `acceptor_id`, `acceptor_name`, `acceptor_city`, `acceptor_latitude/longitude`, `acceptor_risk`, `acceptor_risky_flag`, `mcc` | telefones, e-mail, endereço completo |
| dispositivo/terminal | 36 | `device_id`, `device_fingerprint`, `device_ip_country_code`, `device_ip_latitude/longitude`, `terminal_id`, `terminal_city`, `terminal_latitude/longitude` | campos técnicos de POS (`pos_*_len`) |
| transação | 4 | `amount`, `tipo_transacao`, `modalidade_transacao` | |
| evento/modelo | 121 | `event_external_id`, `event_occurred_at`, `fraud_score`, `decision`, `transaction_status`, `secure_3d_indicator`, `malware_flag`, `proxy_flag`, `cp_card_term_vel_1h` | maioria dos campos de protocolo (`atc1`, `tvr`, `mti`...) |
| alvo | 1 | `feedback_label` (rótulo fraude) | |

**Regra de minimização (LGPD):** o Watson guarda só o que alguma tela ou o modelo usa. Documentos pessoais e o número completo do cartão ficam fora. Mesmo no dataset sintético, praticamos como se fosse real.

## 4. O que ainda não sabemos
Ver a seção "Decisões em aberto" em [modelo-de-dados.md](modelo-de-dados.md#decisoes-em-aberto).
