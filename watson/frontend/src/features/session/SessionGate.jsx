/**
 * SessionGate — guarda de sessão do associado/analista.
 *
 * Fluxo:
 *   1. Ao montar, chama GET /api/session.
 *   2. Se 401 (NOT_AUTHENTICATED), carrega personas e exibe tela de login Carbon.
 *   3. Após login bem-sucedido, guarda o objeto de sessão em memória (nunca em
 *      localStorage) e renderiza os filhos com o contexto de sessão disponível.
 *   4. O botão "Sair" chama DELETE /api/session e volta à tela de login.
 *
 * Regras respeitadas:
 *   - Identidade vem apenas do cookie: o componente nunca lê nem grava customer_id.
 *   - Sem biometria, bloqueio ou novos comportamentos de produto.
 *   - Sem dependências novas — usa apenas React e @carbon/react já instalados.
 */
import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import {
  Button,
  InlineLoading,
  InlineNotification,
  RadioButton,
  RadioButtonGroup,
  Stack,
  Tag,
  Theme,
  Tile,
} from '@carbon/react';
import { Logout } from '@carbon/icons-react';
import { ApiError, getPersonas, getSession, login, logout } from '../../api/client.js';

// ── Contexto de sessão ────────────────────────────────────────────────────────

const SessionContext = createContext(null);

/** Hook: retorna a sessão ativa ({ persona_id, display_name, role, simulation }). */
export function useSession() {
  return useContext(SessionContext);
}

// ── Tela de login ─────────────────────────────────────────────────────────────

function LoginScreen({ onLoginSuccess }) {
  const [personas, setPersonas] = useState(null);
  const [personasError, setPersonasError] = useState(null);
  const [selected, setSelected] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [loginError, setLoginError] = useState(null);

  // Carrega personas ao montar
  useEffect(() => {
    let cancelled = false;
    getPersonas()
      .then((data) => {
        if (!cancelled) {
          setPersonas(data.personas);
          if (data.personas.length > 0) setSelected(data.personas[0].persona_id);
        }
      })
      .catch((err) => {
        if (!cancelled) setPersonasError(err.message ?? 'Não foi possível carregar as personas.');
      });
    return () => { cancelled = true; };
  }, []);

  const handleLogin = async () => {
    if (!selected) return;
    setSubmitting(true);
    setLoginError(null);
    try {
      const session = await login(selected);
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

  const roleLabel = (role) =>
    role === 'ANALISTA' ? 'Analista' : 'Associado';

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
        <Tile style={{ maxWidth: '28rem', width: '100%' }}>
          <Stack gap={6}>
            <div>
              <p className="cds--type-label-01" style={{ marginBottom: '0.25rem', color: 'var(--cds-text-helper)' }}>
                Simulação — Inteli Raiz
              </p>
              <h1 className="cds--type-heading-03">Escolha sua persona</h1>
              <p className="cds--type-body-01" style={{ marginTop: '0.5rem', color: 'var(--cds-text-secondary)' }}>
                Esta é uma demonstração fictícia. Nenhuma transação real será executada.
              </p>
            </div>

            {/* Estado: carregando personas */}
            {!personas && !personasError && (
              <InlineLoading description="Carregando personas…" status="active" />
            )}

            {/* Estado: erro ao carregar personas */}
            {personasError && (
              <InlineNotification
                kind="error"
                title="Erro ao carregar personas"
                subtitle={personasError}
                hideCloseButton
                lowContrast
              />
            )}

            {/* Lista de personas */}
            {personas && (
              <RadioButtonGroup
                legendText="Personas disponíveis"
                name="persona"
                valueSelected={selected}
                onChange={(val) => setSelected(val)}
                orientation="vertical"
              >
                {personas.map((p) => (
                  <RadioButton
                    key={p.persona_id}
                    id={`persona-${p.persona_id}`}
                    value={p.persona_id}
                    labelText={
                      <span>
                        {p.display_name}&nbsp;
                        <Tag size="sm" type={p.role === 'ANALISTA' ? 'blue' : 'teal'}>
                          {roleLabel(p.role)}
                        </Tag>
                      </span>
                    }
                  />
                ))}
              </RadioButtonGroup>
            )}

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
              onClick={handleLogin}
              disabled={!selected || submitting || !personas}
              style={{ maxWidth: '100%' }}
            >
              {submitting ? <InlineLoading description="Entrando…" status="active" /> : 'Entrar'}
            </Button>
          </Stack>
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

  const checkSession = useCallback(() => {
    setStatus('loading');
    setCheckError(null);
    getSession()
      .then((data) => {
        setSession(data);
        setStatus('authenticated');
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
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

  const handleLoginSuccess = useCallback((sessionData) => {
    setSession(sessionData);
    setStatus('authenticated');
  }, []);

  const handleLogout = useCallback(() => {
    setSession(null);
    setStatus('unauthenticated');
  }, []);

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
    <SessionContext.Provider value={session}>
      {children}
      {!['ASSOCIADO', 'ANALISTA'].includes(session.role) && (
        <SessionBar session={session} onLogout={handleLogout} />
      )}
    </SessionContext.Provider>
  );
}
