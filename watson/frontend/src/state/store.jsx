import { createContext, useContext, useReducer } from 'react';
import { CASES } from '../mocks/cases';
import { NOTICE_POLICY, initialHandling } from './noticePolicy';

// Estado compartilhado entre o console da analista e o app do associado (protótipo 3, Playback 3).
// O agente coordena: envia o aviso de compra, recebe a resposta e aplica a regra combinada com a analista.

const clock = (m) => `03:${String(m).padStart(2, '0')}`;

// Casos de risco médio ainda abertos já começam com o aviso enviado pelo Watson.
function withAutoNotice(c) {
  const open = c.status !== 'resolved';
  const handling = initialHandling(c.score);
  if (handling === 'route_to_analyst') return { ...c, escalationReason: 'high_risk' };
  if (!open || handling !== 'auto_send_notice') return c;
  return { ...c, status: 'awaiting_member', autoNotice: true };
}

const initialState = (deviceChanged = false) => {
  const cases = CASES.map((c) => ({ ...withAutoNotice(c), ungrouped: false }));
  const events = { 4821: [] };
  cases.filter((c) => c.autoNotice).forEach((c) => {
    events[c.id] = [{ time: '03:10', type: 'sent', title: 'Aviso de compra enviado pelo Watson', detail: 'Risco médio: o Watson envia sozinho. Você só entra se houver exceção.', ai: true }];
  });
  return {
    minute: 16,
    deviceChanged,
    cases,
    events,
    phone: { screen: 'locked', notifications: [] },
    toast: null,
  };
};

function addEvent(state, caseId, type, title, detail, ai = false) {
  const list = state.events[caseId] ?? [];
  return { ...state.events, [caseId]: [...list, { time: clock(state.minute), type, title, detail, ai }] };
}

function setStatus(state, caseId, status, extra = {}) {
  return state.cases.map((c) => (c.id === caseId ? { ...c, status, ...extra } : c));
}

function reducer(state, action) {
  switch (action.type) {
    case 'reset':
      return initialState(action.deviceChanged ?? state.deviceChanged);
    case 'sendNotice': {
      const s = { ...state, minute: state.minute + 1 };
      return {
        ...s,
        cases: setStatus(s, action.caseId, 'awaiting_member', { decision: null }),
        events: addEvent(s, action.caseId, 'sent', 'Aviso de compra enviado ao associado', 'Pedido pela analista, texto do Watson. Se ele não reconhecer, o Watson bloqueia.', true),
        phone: { screen: 'locked', notifications: [{ title: 'Aviso de compra no seu cartão', body: 'R$ 2.349,90 na Loja Exemplo Eletrônicos. Foi você?' }] },
        toast: { kind: 'info', title: 'Aviso de compra enviado', subtitle: 'Caso aguardando o associado.' },
      };
    }
    case 'openNotice':
      return { ...state, phone: { ...state.phone, screen: 'notice' } };
    case 'notMe': {
      const s = { ...state, minute: state.minute + 1 };
      let events = addEvent(s, action.caseId, 'response', 'Associado respondeu: não reconheço', 'Resposta pelo app autenticado.');
      events = addEvent({ ...s, events }, action.caseId, 'block', 'Cartão bloqueado pelo Watson', 'Regra combinada com a analista: não reconhecida = bloquear. Pode ser revertido.', true);
      return {
        ...s, events,
        cases: setStatus(s, action.caseId, 'resolved', { decision: 'blocked', by: 'Watson' }),
        phone: { screen: 'protected', notifications: [] },
        toast: { kind: 'success', title: 'Cartão •••• 4821 bloqueado pelo Watson', subtitle: 'O associado não reconheceu a compra.' },
      };
    }
    case 'itWasMe':
      return { ...state, phone: { ...state.phone, screen: 'biometrics' } };
    case 'biometrics': {
      const s = { ...state, minute: state.minute + 1 };
      const events = addEvent(s, action.caseId, 'response', 'Associado confirmou: fui eu (com biometria)', 'Resposta pelo app autenticado.');
      if (!NOTICE_POLICY.autoCloseOnItWasMe) {
        return {
          ...s,
          events: addEvent({ ...s, events }, action.caseId, 'alert', 'Voltou para você: confirmação para conferir', 'Pela política atual, "Fui eu" não fecha o caso sozinho.', true),
          cases: setStatus(s, action.caseId, 'in_review', { decision: null, escalationReason: 'confirmation_review' }),
          phone: { screen: 'reviewing', notifications: [] },
          toast: { kind: 'info', title: 'Caso #4821 voltou para você', subtitle: 'O associado confirmou a compra. Confira antes de liberar.' },
        };
      }
      if (state.deviceChanged) {
        return {
          ...s,
          events: addEvent({ ...s, events }, action.caseId, 'alert', 'Voltou para você: aparelho trocado há 2 dias', 'Contramedida da anti-persona: o Watson não libera sozinho quando o aparelho é novo.', true),
          cases: setStatus(s, action.caseId, 'in_review', { decision: null, escalationReason: 'device_changed' }),
          phone: { screen: 'reviewing', notifications: [] },
          toast: { kind: 'warning', title: 'Caso #4821 voltou para você', subtitle: 'Confirmação veio de um aparelho trocado há 2 dias.' },
        };
      }
      return {
        ...s,
        events: addEvent({ ...s, events }, action.caseId, 'released', 'Compra liberada pelo Watson', 'Regra combinada: confirmada com biometria em aparelho conhecido = liberar.', true),
        cases: setStatus(s, action.caseId, 'resolved', { decision: 'released', by: 'Watson' }),
        phone: { screen: 'released', notifications: [] },
        toast: { kind: 'success', title: 'Compra liberada', subtitle: 'O associado confirmou com biometria.' },
      };
    }
    case 'decide': {
      const s = { ...state, minute: state.minute + 1 };
      const titles = { blocked: 'Cartão bloqueado pela analista', released: 'Compra liberada pela analista', escalated: 'Caso escalado' };
      return {
        ...s,
        events: addEvent(s, action.caseId, action.decision, titles[action.decision], action.justification),
        cases: setStatus(s, action.caseId, action.decision === 'escalated' ? 'in_review' : 'resolved', { decision: action.decision, by: 'Analista' }),
        phone: action.decision === 'blocked' ? { screen: 'protected', notifications: [{ title: 'Bloqueamos seu cartão final 4821', body: 'Por segurança. Nada foi cobrado.' }] } : state.phone,
        toast: { kind: 'success', title: titles[action.decision], subtitle: 'Decisão registrada com justificativa.' },
      };
    }
    case 'resendNotices': {
      const s = { ...state, minute: state.minute + 1 };
      return { ...s, toast: { kind: 'info', title: `Aviso reenviado a ${action.ids.length} associados`, subtitle: action.ids.map((i) => `#${i}`).join(', ') } };
    }
    case 'ungroup':
      return {
        ...state,
        cases: state.cases.map((c) => (c.id === action.caseId ? { ...c, alertCount: 2, ungrouped: true } : c)),
        toast: { kind: 'info', title: `Agrupamento do caso #${action.caseId} desfeito`, subtitle: 'A compra presencial virou um caso separado.' },
      };
    case 'closeToast':
      return { ...state, toast: null };
    default:
      return state;
  }
}

const Ctx = createContext(null);

export function WatsonProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, undefined, () => initialState());
  return <Ctx.Provider value={{ state, dispatch }}>{children}</Ctx.Provider>;
}

export function useWatson() {
  return useContext(Ctx);
}
