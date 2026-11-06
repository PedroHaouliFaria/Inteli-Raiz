/**
 * SessionGate — guarda de sessão do associado/analista.
 *
 * Fluxo:
 *   1. Ao montar, chama GET /api/session.
 *   2. Se 401 (NOT_AUTHENTICATED), exibe o formulário de e-mail e senha.
 *   3. Após login bem-sucedido, guarda o objeto de sessão em memória (nunca em
 *      localStorage) e renderiza os filhos com o contexto de sessão disponível.
 *   4. O botão "Sair" chama DELETE /api/session e volta à tela de login.
 *
 * Regras respeitadas:
 *   - Depois do login, a identidade vem apenas do cookie; o componente nunca lê
 *     nem grava customer_id ou persona_id.
 *   - Sem biometria, bloqueio ou novos comportamentos de produto.
 *   - Sem dependências novas — usa apenas React e @carbon/react já instalados.
 */
import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import {
  Button,
  InlineLoading,
  InlineNotification,
  Stack,
  Tag,
  TextInput,
  Theme,
  Tile,
} from '@carbon/react';
import { Logout } from '@carbon/icons-react';
import { ApiError, getSession, login, logout } from '../../api/client.js';

// ── Contexto de sessão ────────────────────────────────────────────────────────

const SessionContext = createContext(null);
const SESSION_CHANNEL = 'raiz-session';

/** Hook: retorna a sessão ativa ({ persona_id, display_name, role, simulation }). */
export function useSession() {
  return useContext(SessionContext);
}

// ── Tela de login ─────────────────────────────────────────────────────────────

function LoginScreen({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [loginError, setLoginError] = useState(null);

  const handleLogin = async (event) => {
    event?.preventDefault();
    if (!email.trim() || !password) return;
    setSubmitting(true);
    setLoginError(null);
    try {
      const session = await login(email.trim(), password);
      onLoginSuccess(session);
    } catch (err) {
      setLoginError(
        err instanceof ApiError
          ? err.message
          : 'Erro ao entrar. Verifique se o servidor está em execução.',
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Theme theme="g10">
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          background: 'var(--cds-background)',
        }}
        role="main"
        aria-label="Tela de acesso"
      >
        <Tile className="session-login-card">
          <form onSubmit={handleLogin}>
          <Stack gap={6}>
            <div>
              <p className="cds--type-label-01" style={{ marginBottom: '0.25rem', color: 'var(--cds-text-helper)' }}>
                Simulação — Inteli Raiz
              </p>
              <h1 className="cds--type-heading-03">Acessar demonstração</h1>
              <p className="cds--type-body-01" style={{ marginTop: '0.5rem', color: 'var(--cds-text-secondary)' }}>
                Entre com as credenciais do seu usuário fictício.
              </p>
            </div>

            <TextInput
              id="login-email"
              name="email"
              type="email"
              labelText="E-mail"
              placeholder="nome@raiz.demo"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              autoComplete="username"
              disabled={submitting}
              required
            />

            <TextInput
              id="login-password"
              name="password"
              type="password"
              labelText="Senha"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
              disabled={submitting}
              required
            />

            {/* Erro de login */}
            {loginError && (
              <InlineNotification
                kind="error"
                title="Não foi possível entrar"
                subtitle={loginError}
                hideCloseButton
                lowContrast
              />
            )}

            <Button
              type="submit"
              disabled={!email.trim() || !password || submitting}
              style={{ maxWidth: '100%' }}
            >
              {submitting ? <InlineLoading description="Entrando…" status="active" /> : 'Entrar'}
            </Button>
          </Stack>
          </form>
        </Tile>
      </div>
    </Theme>
  );
}

// ── Barra de sessão ───────────────────────────────────────────────────────────

function SessionBar({ session, onLogout }) {
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
    } catch {
      // Se o servidor falhar, limpa localmente mesmo assim.
    } finally {
      setLoggingOut(false);
      onLogout();
    }
  };

  const roleLabel = session.role === 'ANALISTA' ? 'Analista' : 'Associado';

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '1rem',
        right: '1rem',
        zIndex: 9000,
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        background: 'var(--cds-layer-02)',
        border: '1px solid var(--cds-border-subtle)',
        borderRadius: '0.25rem',
        padding: '0.5rem 0.75rem',
        boxShadow: 'var(--cds-shadow)',
      }}
      aria-label="Sessão ativa"
    >
      <Tag size="sm" type={session.role === 'ANALISTA' ? 'blue' : 'teal'}>
        {roleLabel}
      </Tag>
      <span className="cds--type-body-compact-01">{session.display_name}</span>
      <Button
        kind="ghost"
        size="sm"
        renderIcon={Logout}
        iconDescription="Sair"
        hasIconOnly
        tooltipPosition="left"
        onClick={handleLogout}
        disabled={loggingOut}
        aria-label="Sair da sessão"
      />
    </div>
  );
}

// ── Componente principal ──────────────────────────────────────────────────────

export default function SessionGate({ children }) {
  // 'loading' | 'unauthenticated' | 'authenticated' | 'error'
  const [status, setStatus] = useState('loading');
  const [session, setSession] = useState(null);
  const [checkError, setCheckError] = useState(null);
  const sessionChannelRef = useRef(null);

  const checkSession = useCallback(({ silent = false } = {}) => {
    if (!silent) setStatus('loading');
    setCheckError(null);
    return getSession()
      .then((data) => {
        setSession(data);
        setStatus('authenticated');
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          setSession(null);
          setStatus('unauthenticated');
        } else {
          setCheckError(
            err instanceof ApiError
              ? err.message
              : 'Erro de rede ao verificar a sessão. Verifique se o servidor está em execução.',
          );
          setStatus('error');
        }
      });
  }, []);

  useEffect(() => {
    checkSession();
  }, [checkSession]);

  useEffect(() => {
    const handleFocus = () => checkSession({ silent: true });
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') handleFocus();
    };

    window.addEventListener('focus', handleFocus);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    if ('BroadcastChannel' in window) {
      const channel = new BroadcastChannel(SESSION_CHANNEL);
      channel.addEventListener('message', handleFocus);
      sessionChannelRef.current = channel;
    }

    return () => {
      window.removeEventListener('focus', handleFocus);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      sessionChannelRef.current?.close();
      sessionChannelRef.current = null;
    };
  }, [checkSession]);

  const notifySessionChange = useCallback(() => {
    sessionChannelRef.current?.postMessage('changed');
  }, []);

  const handleLoginSuccess = useCallback((sessionData) => {
    setSession(sessionData);
    setStatus('authenticated');
    notifySessionChange();
  }, [notifySessionChange]);

  const handleLogout = useCallback(() => {
    setSession(null);
    setStatus('unauthenticated');
    notifySessionChange();
  }, [notifySessionChange]);

  const endSession = useCallback(async () => {
    try {
      await logout();
    } finally {
      // A interface volta ao login mesmo se o servidor ficar indisponível.
      handleLogout();
    }
  }, [handleLogout]);

  if (status === 'loading') {
    return (
      <div
        style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
        role="status"
        aria-live="polite"
        aria-label="Verificando sessão"
      >
        <InlineLoading description="Verificando sessão…" status="active" />
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div
        style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}
        role="alert"
      >
        <Tile style={{ maxWidth: '28rem', width: '100%' }}>
          <Stack gap={4}>
            <InlineNotification
              kind="error"
              title="Erro ao verificar sessão"
              subtitle={checkError}
              hideCloseButton
              lowContrast
            />
            <Button kind="secondary" onClick={checkSession}>Tentar novamente</Button>
          </Stack>
        </Tile>
      </div>
    );
  }

  if (status === 'unauthenticated') {
    return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
  }

  // status === 'authenticated'
  return (
    <SessionContext.Provider value={{ ...session, endSession }}>
      {children}
      {!['ASSOCIADO', 'ANALISTA'].includes(session.role) && (
        <SessionBar session={session} onLogout={handleLogout} />
      )}
    </SessionContext.Provider>
  );
}
