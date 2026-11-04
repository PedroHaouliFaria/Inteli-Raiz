# Pacote Pessoa 3 — Estrutura da solução e arquitetura

**Versão:** 0.1 · **Data:** 29/10/2026  
**Responsável:** Pessoa 3  
**Revisores:** Pessoa 4 (D09/D10), autores técnicos (contratos e evidências)  
**Estado geral:** rascunho — documentação estrutural completa; implementação e integração pendentes.

---

## 1. Índice de arquivos

| Arquivo | Entrega | Estado |
|---|---|---|
| `README.md` (este arquivo) | Índice, versões consultadas e pendências | rascunho |
| `D09_estrutura_solucao.md` | D09 — Estrutura da solução e critérios de sucesso | rascunho |
| `D10_arquitetura.md` | D10 — Arquitetura técnica e limites de autonomia | rascunho |

---

## 2. Responsabilidades conforme o direcional

Conforme [`docs/direcional_entregas.md`](../../direcional_entregas.md#organização-em-quatro-pessoas-responsáveis-sequência-e-revisão):

| Entrega | Responsável | Apoio necessário | Revisor principal | Saída para aceite |
|---|---|---|---|---|
| D09 Estrutura | Pessoa 3 | Pessoa 1: escopo; Pessoa 2: sucesso para o usuário | Pessoa 4 | Requisitos ligados a necessidades, métricas e testes |
| D10 Arquitetura | Pessoa 3 | Autores técnicos: contratos e evidências | Pessoa 4 | Diagrama, sequência, papéis, contratos, limites e falhas |

---

## 3. Estado de cada entrega

| Entrega | Estado | Justificativa |
|---|---|---|
| **D09** Estrutura da solução | **rascunho** | Problema, capacidades do agente, componentes, requisitos R01–R12 e critérios de sucesso documentados. Depende de D05/D07/D08 (Pessoa 1) para revisão do escopo. |
| **D10** Arquitetura técnica | **rascunho** | Diagrama de componentes, sequência de execução, ficha do agente, catálogo de ferramentas, contratos de API, máquina de estados, persistência e decisões técnicas documentados. Integração com o frontend e evidências de execução pendentes. |

---

## 4. Pendências prioritárias

| ID | Achado | Prioridade | Responsável |
|---|---|---|---|
| PEN-P3-01 | D09 depende de D05/D07/D08 (Pessoa 1) para confirmar escopo e proposta de valor | P1 | Pessoa 1 (produzir D05/D08); Pessoa 3 (revisar D09 após) |
| PEN-P3-02 | Limiares da política de decisão não definidos — dependem de validação (C16) | P1 | Pessoa 3 / equipe |
| PEN-P3-03 | Provedor LLM não confirmado (Groq/Gemini/Granite) | P1 | Pessoa 3 / equipe |
| PEN-P3-04 | Evidências de execução da seção 11 do D10 todas em "Planejado" | P1 | Pessoa 3 (após C06/C12/C17/C26) |
| PEN-P3-05 | Manifesto de features divergente: código lista 28, docs anteriores mencionam totais diferentes | P2 | Pessoa 3 / time de dados |

---

## 5. Versões consultadas

| Fonte | Local | Observação |
|---|---|---|
| Plano vigente e Direcional | `docs/plano_implementacao.md` e `docs/direcional_entregas.md` | Fonte principal de produto e estrutura |
| Contrato da API | `docs/specs/contrato_api.md` | Base para contratos do D10 |
| Spec de integração watsonx.ai | `docs/specs/teste_integracao_orchestrate_wml.md` | Evidência de deploy watsonx.ai (27/10) |
| Arquitetura geral | `docs/arquitetura/visao-geral.md` | Camadas, regras e árvore do repositório |

---

## 6. Próximos passos concretos

1. **Pessoa 3:** após Pessoa 1 produzir D05/D08, revisar D09 para alinhar escopo e proposta de valor.
2. **Pessoa 3:** confirmar provedor LLM e documentar troca de provedor como configuração no D10.
3. **Pessoa 3:** executar cards C06/C12/C17/C26 e preencher a seção 11 de evidências do D10.
4. **Pessoa 3:** após C16 (validação), definir limiares da política e atualizar seção 7 do D10.
