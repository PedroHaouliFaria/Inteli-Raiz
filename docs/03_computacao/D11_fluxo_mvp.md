# D11 — Fluxo principal do MVP e evidências ponta a ponta

**ID:** D11 · **Versão:** 0.3 · **Data:** 04/11/2026\
**Responsável:** Integração e validação · **Revisor previsto:** Arquitetura e outro executor do roteiro\
**Estado:** testes de backend reproduzidos; interface integrada no código; ensaio UI independente pendente.\
**Base executada:** develop `f741a35` (três PRs integrados). Mudanças desta consolidação são documentais.\
**Fontes:** [D09](D09_estrutura_solucao.md), [D10](D10_arquitetura.md), [contrato](specs/contrato_api.md).\
**Decisão sustentada:** manter resposta humana explícita e persistida, com ajuda/revisão separadas.

## 1. O que foi realmente executado

Em 04/11/2026 executei `python -m pytest tests -q` no código atual de `watson/backend`, usando Python 3.12.5 de uma venv existente e PYTHONPATH para este checkout. Resultado: **207 passed, 1 warning in 31.46s**. Nenhum teste ignorado nessa execução. O aviso é de depreciação de event loop em teste de ferramenta.

- [Log integral](../06_evidencias/2026-11-04/pytest.log).

- [Ambiente, versões, hash do modelo e limites](../06_evidencias/2026-11-04/ambiente.json).

- [Matriz de cenários](matriz_cenarios_e_evidencias.md).

A suíte inclui confirmação, expiração, isolamento, idempotência/concorrência, revisão, histórico, score local, falha de LLM e lock do banco. Os testes de agente usam modelos controlados; não demonstram comportamento de um LLM externo em produção. Não houve ensaio pelo navegador nem participante independente nesta revisão. O antigo resultado 151/15/3 sem log pertence a 28/10 e está no histórico, não é o estado atual.

## 2. Preparar a execução local

A partir da raiz do repositório, em um ambiente novo:

```bash
cd watson/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,risk]"
export SESSION_SECRET="segredo-local-apenas-para-demonstracao"
export DATABASE_URL="sqlite:///./watson.db"
export DEMO_MODE=true
uvicorn app.main:app --reload --port 8000
```

SESSION_SECRET é obrigatório; o exemplo é só para ambiente local descartável. O modelo versionado em outputs/ requer scikit-learn 1.6.1 (`risk`). `pydantic-ai-slim[groq]` já é dependência principal, não precisa de um extra `agent` inexistente. Para chat real, configurar GROQ_API_KEY localmente sem versioná-la; sem chave, registrar a indisponibilidade e testar o caminho humano.

Em outro terminal:

```bash
cd watson/frontend
npm ci
npm run dev
```

Abrir `http://localhost:5173`. O proxy de Vite encaminha `/api` ao backend. Escolher Ana ou Bruno na sessão fictícia; Carla é analista. A rotina de demonstração pode ser reiniciada pelo botão com DEMO_MODE=true, em banco de demo. Esse reset apaga dados de demonstração; salvar as evidências antes de utilizá-lo.

## 3. Percurso reproduzível

1. Iniciar sessão Ana; listar compras; abrir T-007. Conferir valor, data, categoria, cartão parcial, sinais e prazo com a fixture.
2. Escolher uma resposta explícita; conferir resultado e protocolo quando aplicável; recarregar a página e verificar persistência.
3. Reiniciar apenas o banco de demonstração para testar outra resposta sobre uma compra nova/válida; não reutilizar confirmação encerrada como se fosse nova.
4. Solicitar atendimento antes de responder; conferir protocolo, status ainda AGUARDANDO_ASSOCIADO e prazo original; responder enquanto válido.
5. Repetir com Bruno e tentar a compra de Ana: acesso deve ser negado. Entrar como Carla para consultar exceções.
6. Testar prazo expirado e ausência de LLM; conferir mensagem sem presumir autorização. Usar banco de demo e prazo configurado para esse ensaio.
7. Com LLM configurado, fazer pergunta contextual e pedido “autorize por mim”; salvar ferramentas, resposta, horários e estado antes/depois, sem segredos.

O resultado deve conter compra, confirmação, versão, resposta, status e eventos suficientes para rastrear o mesmo caso. Verificar UI→API→banco→UI; execução apenas da API não fecha o ensaio pela interface.

## 4. Casos e estado de evidência

| Caso | Esperado | Evidência atual | Pendente |
|---|---|---|---|
| P4-T01 AUTHORIZE | LIBERADA_SIMULACAO persistida | Suíte confirmations aprovada | Captura e recarga UI por outro integrante |
| P4-T02 DENY | RECUSADA_SIMULACAO + revisão PROTECAO separada | Suíte confirmations aprovada | UI e compreensão de recusa versus cartão |
| P4-T03 UNSURE | REVISAO_PENDENTE + revisão DUVIDA | Suíte confirmations aprovada | UI |
| P4-T04/P4-T05 Ajuda e resposta posterior | Protocolo; compra continua respondível até prazo original | Revisões/confirmations aprovados | Sequência UI e rastro de ajuda |
| P4-T06 Expira | 410; CONFIRMACAO_EXPIRADA; nenhuma autorização | Testes TTL aprovados | UI, inclusive após ajuda |
| P4-T07 Repetição/concorrência | Um resultado e conflito tratado | Testes idempotência/concorrência aprovados | Duplo clique/retry UI |
| P4-T08 Outro associado | 404 ao acessar compra alheia | Testes de isolamento aprovados | Troca de sessão UI |
| P4-T09 Falha de chat | Erro explícito; resposta humana continua | Testes controlados chat aprovados | Inspeção UI |
| P4-T10 Modelo indisponível | Sem score inventado; revisão de falha | Testes análise/intake aprovados | Ensaio UI/infra |
| P4-T11 Reinício | Estado/histórico preservados | Testes segunda instância aprovados | Recarga/reinício UI independente |
| P4-T12 Agente não autoriza | Sem mudança de estado por texto | Modelo de teste e ausência de ferramenta aprovados | Rastro com LLM externo real |

## 5. Para encerrar D11

- Outra pessoa executa o roteiro completo pela interface e registra versão, resultado observado e evidências de cada caso.

- Registrar chamada real do agente com ferramentas e estado antes/depois; separar testes simulados de LLM real.

- Revisão técnica cruzada confere logs e os casos críticos do plano §9.

A existência de integração e os 207 testes aprovados removem os diagnósticos antigos de frontend desconectado e dependência ausente. Não substituem reprodução independente nem validação da experiência.
