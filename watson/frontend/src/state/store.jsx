import { createContext, useContext, useReducer } from 'react';
import { CASOS } from '../data/casos';

// Estado compartilhado entre o console da analista e o app do associado (protótipo 3, Playback 3).
// O agente coordena: envia o aviso de compra, recebe a resposta e aplica a regra combinada com a analista.

const hora = (m) => `03:${String(m).padStart(2, '0')}`;

const inicial = (aparelhoTrocado = false) => ({
  minuto: 16,
  aparelhoTrocado,
  casos: CASOS.map((c) => ({ ...c, grupoDesfeito: false })),
  eventos: { 4821: [] },
  celular: { tela: 'bloqueado', notificacoes: [] },
  toast: null,
});

function evento(state, casoId, tipo, titulo, detalhe, ia = false) {
  const lista = state.eventos[casoId] ?? [];
  return { ...state.eventos, [casoId]: [...lista, { hora: hora(state.minuto), tipo, titulo, detalhe, ia }] };
}

function mudarEstado(state, casoId, estado, extra = {}) {
  return state.casos.map((c) => (c.id === casoId ? { ...c, estado, ...extra } : c));
}

function reducer(state, acao) {
  switch (acao.tipo) {
    case 'reiniciar':
      return inicial(acao.aparelhoTrocado ?? state.aparelhoTrocado);
    case 'enviarAviso': {
      const s = { ...state, minuto: state.minuto + 1 };
      return {
        ...s,
        casos: mudarEstado(s, acao.casoId, 'aguardando', { decisao: null }),
        eventos: evento(s, acao.casoId, 'enviado', 'Aviso de compra enviado ao associado', 'Pedido pela analista, texto do Watson. Se ele não reconhecer, o Watson bloqueia.', true),
        celular: { tela: 'bloqueado', notificacoes: [{ titulo: 'Aviso de compra no seu cartão', corpo: 'R$ 2.349,90 na Loja Exemplo Eletrônicos. Foi você?' }] },
        toast: { tipo: 'info', titulo: 'Aviso de compra enviado', sub: 'Caso aguardando o associado.' },
      };
    }
    case 'abrirAviso':
      return { ...state, celular: { ...state.celular, tela: 'aviso' } };
    case 'naoReconheco': {
      const s = { ...state, minuto: state.minuto + 1 };
      let eventos = evento(s, acao.casoId, 'resposta', 'Associado respondeu: não reconheço', 'Resposta pelo app autenticado.');
      eventos = evento({ ...s, eventos }, acao.casoId, 'bloqueio', 'Cartão bloqueado pelo Watson', 'Regra combinada com a analista: não reconhecida = bloquear. Pode ser revertido.', true);
      return {
        ...s, eventos,
        casos: mudarEstado(s, acao.casoId, 'resolvido', { decisao: 'bloqueado', por: 'Watson' }),
        celular: { tela: 'protegido', notificacoes: [] },
        toast: { tipo: 'success', titulo: 'Cartão •••• 4821 bloqueado pelo Watson', sub: 'O associado não reconheceu a compra.' },
      };
    }
    case 'fuiEu':
      return { ...state, celular: { ...state.celular, tela: 'biometria' } };
    case 'biometria': {
      const s = { ...state, minuto: state.minuto + 1 };
      const eventos = evento(s, acao.casoId, 'resposta', 'Associado confirmou: fui eu (com biometria)', 'Resposta pelo app autenticado.');
      if (state.aparelhoTrocado) {
        return {
          ...s,
          eventos: evento({ ...s, eventos }, acao.casoId, 'alerta', 'Voltou para você: aparelho trocado há 2 dias', 'Contramedida da anti-persona: o Watson não libera sozinho quando o aparelho é novo.', true),
          casos: mudarEstado(s, acao.casoId, 'analise', { decisao: null }),
          celular: { tela: 'conferindo', notificacoes: [] },
          toast: { tipo: 'warning', titulo: 'Caso #4821 voltou para você', sub: 'Confirmação veio de um aparelho trocado há 2 dias.' },
        };
      }
      return {
        ...s,
        eventos: evento({ ...s, eventos }, acao.casoId, 'liberado', 'Compra liberada pelo Watson', 'Regra combinada: confirmada com biometria em aparelho conhecido = liberar.', true),
        casos: mudarEstado(s, acao.casoId, 'resolvido', { decisao: 'liberado', por: 'Watson' }),
        celular: { tela: 'liberado', notificacoes: [] },
        toast: { tipo: 'success', titulo: 'Compra liberada', sub: 'O associado confirmou com biometria.' },
      };
    }
    case 'decidir': {
      const s = { ...state, minuto: state.minuto + 1 };
      const titulos = { bloqueado: 'Cartão bloqueado pela analista', liberado: 'Compra liberada pela analista', escalado: 'Caso escalado' };
      return {
        ...s,
        eventos: evento(s, acao.casoId, acao.decisao, titulos[acao.decisao], acao.justificativa),
        casos: mudarEstado(s, acao.casoId, acao.decisao === 'escalado' ? 'analise' : 'resolvido', { decisao: acao.decisao, por: 'Analista' }),
        celular: acao.decisao === 'bloqueado' ? { tela: 'protegido', notificacoes: [{ titulo: 'Bloqueamos seu cartão final 4821', corpo: 'Por segurança. Nada foi cobrado.' }] } : state.celular,
        toast: { tipo: 'success', titulo: titulos[acao.decisao], sub: 'Decisão registrada com justificativa.' },
      };
    }
    case 'reenviarAvisos': {
      const s = { ...state, minuto: state.minuto + 1 };
      return { ...s, toast: { tipo: 'info', titulo: `Aviso reenviado a ${acao.ids.length} associados`, sub: acao.ids.map((i) => `#${i}`).join(', ') } };
    }
    case 'desagrupar':
      return {
        ...state,
        casos: state.casos.map((c) => (c.id === acao.casoId ? { ...c, alertas: 2, grupoDesfeito: true } : c)),
        toast: { tipo: 'info', titulo: `Agrupamento do caso #${acao.casoId} desfeito`, sub: 'A compra presencial virou um caso separado.' },
      };
    case 'fecharToast':
      return { ...state, toast: null };
    default:
      return state;
  }
}

const Ctx = createContext(null);

export function WatsonProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, undefined, () => inicial());
  return <Ctx.Provider value={{ state, dispatch }}>{children}</Ctx.Provider>;
}

export function useWatson() {
  return useContext(Ctx);
}
