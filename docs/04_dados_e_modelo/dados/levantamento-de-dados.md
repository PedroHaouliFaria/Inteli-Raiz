# Levantamento: que dados a aplicação precisa guardar

**Versão:** 1.0 · 04/11/2026 · **Estado:** alinhado ao [plano](../../05_gestao/plano_implementacao.md) (associado como usuário principal) e ao código atual.

> Técnica: rastreamos cada dado até **uma necessidade de pessoa ou de tela**. Dado sem dono não entra. Fontes: [D02](../../02_ux_design/D02_mapa_empatia.md), [D06](../../02_ux_design/D06_persona_e_cenarios.md), [D12](../../02_ux_design/D12_prototipo_experiencia.md), requisitos R01–R12 de [D09](../../03_computacao/D09_estrutura_solucao.md) e o dicionário do case (`data/dicionario_dados_case_prevencao_sicredi.xlsx`, 297 colunas).

## 1. De onde vem cada dado

| Origem | O que é | Como a aplicação trata |
|---|---|---|
| **Case Sicredi** (linhas de `teste_proporcao_real.csv`) | A compra e as 28 features do modelo | Só leitura, pelas fixtures. Sem o rótulo de fraude |
| **Modelo de risco** | Score, origem e versão do modelo, lacunas da análise | Gravado na compra. Visível só para a analista |
| **Regras de sinais** | Sinais compreensíveis (sem cartão físico, madrugada, primeira compra) | Calculados das features a cada leitura |
| **Associado** | Resposta à confirmação, pedido de atendimento, perguntas no chat | Gravado, com evento de auditoria |
| **Agente** | Respostas no chat, ferramentas usadas, revisões que abriu | Gravado; nunca grava resposta à confirmação |
| **Sistema** | Prazo, expiração, revisão por falha do modelo | Gravado como evento |

## 2. Necessidade → dado

| Necessidade (quem, requisito) | Dados que precisam existir |
|---|---|
| Ver **qual compra** está sendo confirmada (associado, R02) | valor, data/hora, categoria (MCC), bandeira e final do cartão, canal |
| Entender **por que** foi sinalizada, sem número de risco (associado, R02, R07) | sinais com texto em linguagem simples, derivados das features |
| **Responder** com três opções e saber o efeito (associado, R03) | pedido de confirmação, resposta, horário da resposta, estado resultante |
| Saber o **prazo** e o que acontece se não responder (associado, R04) | `expires_at`; estado `CONFIRMACAO_EXPIRADA` |
| **Tirar dúvida** sem inventar informação (associado, R08) | histórico do chat; ferramentas usadas; lacunas da análise (ex.: nome do estabelecimento indisponível) |
| **Pedir atendimento** sem perder a resposta (associado, plano §3) | revisão `DUVIDA` com protocolo, motivo e detalhes; a confirmação continua aberta |
| Ver o **resultado e o próximo passo** depois de responder, sabendo que é simulação (associado, R03, R11) | estado final, protocolo da revisão, aviso de simulação |
| Não ver compras de outra pessoa (segurança, R05) | dono da compra ligado à sessão |
| Resposta repetida não duplicar ação (segurança, R06) | `version` da compra e chave de idempotência |
| Tratar **exceções** (analista) | revisões abertas, tipo, motivo, quem abriu, score interno e versão do modelo |
| Auditar o que aconteceu (equipe, R10) | eventos com estado anterior/novo e horário |
| Avaliar o modelo depois (equipe) | versão do modelo e da política em cada análise |

O modelo físico dessas necessidades está em [modelo-de-dados.md](modelo-de-dados.md).

## 3. O que o dataset do case traz (e o que aproveitamos)

A aplicação usa só as **28 features** do modelo (lista em `data/processed/dicionario_base_modelo.csv`) e o identificador do cartão para o final de 4 dígitos. A tabela abaixo mostra o que existe no case e o que deixamos de fora por minimização.

| Categoria no dicionário | Colunas | Exemplos que usamos | Exemplos que **não** guardamos |
|---|---|---|---|
| cliente (associado) | 51 | `customer_region`, `customer_risk_rating`, renda declarada e presumida (como features) | `customer_ssn`, `customer_passport_number`, `customer_driver_license`, `customer_citizen_id_number`, data de nascimento |
| conta | 33 | `account_balance`, `account_available_credit` | IBAN, BIC, assinatura digital |
| cartão | 28 | `card_brand`, `card_type`, `card_presence_flag`, `card_credit_limit`; final do `card_id` | `card_pan` (número completo), `card_ver_data` |
| estabelecimento | 23 | `mcc`, `acceptor_region`, `acceptor_risk` | nome, telefones, e-mail, endereço |
| dispositivo/terminal | 36 | contadores de velocidade (`cp_card_term_vel_1h`, `cp_card_prev_term_dist_1h`) | `device_fingerprint`, IP, campos técnicos de POS |
| transação | 4 | `amount`, `tipo_transacao`, `modalidade_transacao` | |
| evento/modelo | 121 | `cardid_count_1m`, `digitalwallettoken_count_3m` | `fraud_score`, `decision`, `transaction_status` (vazamento) |
| alvo | 1 | — | `feedback_label`: nunca entra na aplicação |

**Regra de minimização (LGPD):** a aplicação guarda só o que alguma tela ou o modelo usa. Mesmo com dados sintéticos, praticamos como se fossem reais.

**Lacuna conhecida:** o nome do estabelecimento não está disponível na base usada. Por isso o agente declara esse limite em vez de inventar um nome (DEC-09 no [registro de evidências](../../05_gestao/evidencias_e_hipoteses.md)).
