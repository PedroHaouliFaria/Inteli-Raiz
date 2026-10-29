/**
 * AssociateApp — experiência conectada à API para sessão ASSOCIADO.
 *
 * Renderiza:
 *   - Header com nome da pessoa e botão de sair (via SessionGate)
 *   - Lista de compras reais (GET /api/purchases)
 *   - Detalhe da compra selecionada (PurchaseDetail)
 *
 * Não usa o estado mockado de src/state/store.jsx.
 * Não renderiza biometria, aparelho trocado, bloqueio de cartão ou chat.
 */
import { useCallback, useEffect, useState } from 'react';
import {
  Button,
  Header,
  HeaderGlobalBar,
  HeaderGlobalAction,
  HeaderName,
  InlineLoading,
  InlineNotification,
  SkipToContent,
  Tag,
  Theme,
} from '@carbon/react';
import { Renew, Logout } from '@carbon/icons-react';
import { ApiError, getPurchases, logout } from '../../api/client.js';
import { useSession } from '../session/SessionGate.jsx';
import PurchaseList from './PurchaseList.jsx';
import PurchaseDetail from './PurchaseDetail.jsx';

export default function AssociateApp() {
  const session = useSession();

  const [purchases, setPurchases] = useState(null);
  const [listLoading, setListLoading] = useState(true);
  const [listError, setListError] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [loggingOut, setLoggingOut] = useState(false);

  const loadPurchases = useCallback(async () => {
    setListLoading(true);
    setListError(null);
    try {
      const data = await getPurchases();
      setPurchases(data.purchases);
      // Seleciona automaticamente a primeira compra ao carregar
      if (data.purchases.length > 0 && !selectedId) {
        setSelectedId(data.purchases[0].case_id);
      }
    } catch (err) {
      setListError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar compras.');
    } finally {
      setListLoading(false);
    }
  // selectedId intencionalmente omitido: queremos só no mount
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    loadPurchases();
  }, [loadPurchases]);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
    } catch {
      // Se o servidor falhar, recarrega a página para limpar o estado
    } finally {
      // Força recarga completa para que SessionGate volte à tela de login
      window.location.reload();
    }
  };

  return (
    <Theme theme="g10">
      <Theme theme="g100">
        <Header aria-label="Raiz · Confirmação de compras">
          <SkipToContent />
          <HeaderName href="#" prefix="Raiz">Confirmação de compras</HeaderName>
          <HeaderGlobalBar>
            <Tag
              size="sm"
              type="teal"
              style={{ marginRight: '0.5rem', alignSelf: 'center' }}
              aria-label={`Sessão: ${session.display_name}`}
            >
              {session.display_name}
            </Tag>
            <HeaderGlobalAction
              aria-label="Atualizar lista de compras"
              onClick={loadPurchases}
              disabled={listLoading}
            >
              <Renew size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction
              aria-label="Sair da sessão"
              onClick={handleLogout}
              disabled={loggingOut}
              tooltipAlignment="end"
            >
              <Logout size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
        </Header>
      </Theme>

      <main className="associate-app" aria-label="Suas compras para confirmação">
        {/* Coluna esquerda: lista */}
        <aside className="associate-sidebar" aria-label="Lista de compras">
          <div className="associate-sidebar__header">
            <h1 className="cds--type-heading-compact-02">Suas compras</h1>
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)', marginTop: '0.25rem' }}>
              Simulação — Inteli Raiz
            </p>
          </div>

          {listLoading && (
            <div style={{ padding: '1rem' }} role="status" aria-live="polite">
              <InlineLoading description="Carregando…" status="active" />
            </div>
          )}

          {listError && (
            <div style={{ padding: '1rem' }}>
              <InlineNotification
                kind="error"
                title="Erro ao carregar compras"
                subtitle={listError}
                hideCloseButton
                lowContrast
              />
              <Button kind="ghost" size="sm" onClick={loadPurchases} style={{ marginTop: '0.5rem' }}>
                Tentar novamente
              </Button>
            </div>
          )}

          {!listLoading && !listError && purchases !== null && (
            <PurchaseList
              purchases={purchases}
              selectedId={selectedId}
              onSelect={(id) => setSelectedId(id)}
            />
          )}
        </aside>

        {/* Coluna direita: detalhe */}
        <div className="associate-content">
          {selectedId ? (
            <PurchaseDetail
              key={selectedId}
              caseId={selectedId}
              onPurchaseChanged={loadPurchases}
            />
          ) : (
            !listLoading && (
              <div className="associate-empty-state" role="status">
                <p className="cds--type-body-01">
                  {purchases?.length === 0
                    ? 'Não há compras para revisar no momento.'
                    : 'Selecione uma compra na lista para ver os detalhes.'}
                </p>
              </div>
            )
          )}
        </div>
      </main>
    </Theme>
  );
}
