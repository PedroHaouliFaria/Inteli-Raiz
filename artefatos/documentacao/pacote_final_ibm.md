# Pacote final IBM — conteúdo e pendências

**Versão:** 0.1 · **Data:** 04/11/2026 · **Estado:** minuta para consolidação; não submetido.\
**Fontes:** guia IBM p.13 e pp.30–31, conforme [mapa de fontes](fontes_e_exigencias_ibm.md). Conferir campos/regras vigentes na plataforma antes do envio; não há acesso a ela nesta revisão.

## 1. Declaração de problema e solução — minuta

Investigamos a hipótese de que o associado tenha dificuldade para reconhecer uma compra sinalizada e compreender o efeito da resposta quando o contexto é insuficiente. A proposta apresenta dados da compra e sinais disponíveis, permite autorizar, não reconhecer ou informar dúvida e mostra o resultado persistido. Um agente pode consultar contexto e solicitar revisão; a decisão sobre a confirmação continua explícita na interface humana. Analistas recebem exceções. O MVP usa dados sintéticos e ações financeiras simuladas, sem integração bancária produtiva. A vantagem da conversa sobre a mesma interface sem chat ainda precisa de piloto.

**Link funcional para submissão:** pendente de hospedagem/acesso validado por outra pessoa. O roteiro local é [D11](../D11_fluxo_mvp.md). Não usar um localhost como link público final.

## 2. Declaração tecnológica — minuta

React + Carbon no frontend; FastAPI, SQLAlchemy e SQLite no backend; modelo Random Forest/scikit-learn 1.6.1 carregado de joblib; agente Pydantic AI com configuração Groq no chat atual. Modelo produz indicador de ranqueamento; política conservadora decide tratamento; agente consulta ferramentas e não registra a resposta humana. Bob é ferramenta de desenvolvimento, cujas sessões reais devem ser exportadas por integrante. Há teste histórico de deploy watsonx.ai documentado na spec; não foi repetido nesta revisão nem implica que o chat atual use esse serviço.

Base executada nesta revisão: f741a35; 207 testes de backend aprovados com log. LLM externo real, ensaio independente UI, pesquisa com usuários e efeito operacional permanecem sem evidência nesta revisão. Preencher versão do deploy final e componentes efetivamente usados antes da submissão.

## 3. Roteiro de vídeo — 3 minutos

| Tempo | Conteúdo | Evidência a exibir |
|---|---|---|
| 0:00–0:25 | Problema, associado e hipótese de valor | Fricção de D01, com limite da pesquisa |
| 0:25–0:45 | Solução, simulação e limites | Sessão fictícia e compra identificada |
| 0:45–1:40 | Percurso integrado e resposta explícita | UI, resultado, protocolo e recarga |
| 1:40–2:15 | Dúvida contextual e limite do agente | Ferramentas e resposta real sem inventar estabelecimento |
| 2:15–2:40 | Exceção/falha e persistência | Revisão/expiração, sem autorização presumida |
| 2:40–3:00 | Tecnologia, validação disponível e próximos limites | Log/teste e resultado de piloto somente se executado |

Ensaiar e gravar a versão realmente executada. Um roteiro não é um vídeo concluído. Se não houver agente real configurado, declarar o limite; não editar a gravação para aparentar execução inexistente.

## 4. Checklist de submissão

- [ ] Vídeo de três minutos gravado, acessível e coerente com a versão final.

- [ ] Declaração problema/solução revisada, com link funcional testado externamente.

- [ ] Declaração tecnológica ajustada ao runtime efetivamente usado.

- [ ] Sessões reais do IBM Bob por integrante em bob_sessions/, com índice de atividade/artefato.

- [ ] Revisão cruzada e limites de pesquisa/teste declarados.

- [ ] Regras/campos de checkpoint e envio conferidos pelo líder cadastrado na plataforma.

- [ ] Comprovante de submissão preservado após o envio.

Este documento consolida conteúdo já disponível, sem inventar requisitos de plataforma, participantes, resultado financeiro, vídeo, URL pública ou evidências do Bob.
