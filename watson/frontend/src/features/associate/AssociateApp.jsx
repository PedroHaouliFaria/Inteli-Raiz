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
import { useCallback, useEffect, useRef, useState } from 'react';
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
import { ArrowLeft, Renew, Logout } from '@carbon/icons-react';
import { useNavigate, useParams } from 'react-router-dom';
import { ApiError, getPurchases } from '../../api/client.js';
import { useSession } from '../session/SessionGate.jsx';
import PurchaseList from './PurchaseList.jsx';
import PurchaseDetail from './PurchaseDetail.jsx';
import DemoResetButton from './DemoResetButton.jsx';

export default function AssociateApp() {
  const session = useSession();
  const navigate = useNavigate();
  const { caseId = null } = useParams();

  const [purchases, setPurchases] = useState(null);
  const [listLoading, setListLoading] = useState(true);
  const [listError, setListError] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [loggingOut, setLoggingOut] = useState(false);
  const [mobileDetailOpen, setMobileDetailOpen] = useState(Boolean(caseId));
  const [routeNotFound, setRouteNotFound] = useState(false);

  const detailRef = useRef(null);
  const caseIdRef = useRef(caseId);
  caseIdRef.current = caseId;
  // Rastreia se o painel de detalhe já foi aberto ao menos uma vez,
  // para não roubar foco no carregamento inicial da página.
  const detailEverOpenedRef = useRef(false);

  const loadPurchases = useCallback(async () => {
    setListLoading(true);
    setListError(null);
    try {
      const data = await getPurchases();
      setPurchases(data.purchases);
      // Mantém a compra selecionada entre recarregamentos.
      // Se a seleção atual não existir mais na lista nova, cai para a primeira.
      setSelectedId((atual) => {
        const ids = data.purchases.map((p) => p.case_id);
        const requestedCaseId = caseIdRef.current;
        if (requestedCaseId) {
          return ids.includes(requestedCaseId) ? requestedCaseId : null;
        }
        if (atual && ids.includes(atual)) return atual;
        return data.purchases[0]?.case_id ?? null;
      });
    } catch (err) {
      setListError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar compras.');
    } finally {
      setListLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPurchases();
  }, [loadPurchases]);

  // A URL é uma entrada não confiável: só seleciona o caso depois de confirmar
  // que ele veio da lista autorizada para a sessão atual.
  useEffect(() => {
    if (purchases === null) return;
    if (!caseId) {
      setRouteNotFound(false);
      setMobileDetailOpen(false);
      return;
    }

    const authorized = purchases.some((purchase) => purchase.case_id === caseId);
    setRouteNotFound(!authorized);
    setSelectedId(authorized ? caseId : null);
    setMobileDetailOpen(true);
  }, [caseId, purchases]);

  // Quando o detalhe abre no celular: rola para o topo e leva foco ao painel.
  useEffect(() => {
    if (!mobileDetailOpen) return;
    window.scrollTo(0, 0);
    detailRef.current?.focus({ preventScroll: true });
  }, [mobileDetailOpen, selectedId]);

  // Quando o detalhe fecha no celular: devolve foco ao item ativo na lista.
  useEffect(() => {
    if (mobileDetailOpen) {
      detailEverOpenedRef.current = true;
      return;
    }
    if (!detailEverOpenedRef.current) return; // primeiro carregamento, sem ação
    const btn = document.querySelector('.associate-list__item--active button');
    if (btn) {
      btn.focus({ preventScroll: true });
      btn.scrollIntoView({ block: 'center' });
    }
  }, [mobileDetailOpen]);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await session.endSession();
    } finally {
      setLoggingOut(false);
    }
  };

  return (
    <Theme theme="g10">
      <Theme theme="g100">
        <Header aria-label="Raiz · Confirmação de compras">
          <SkipToContent />
          <HeaderName href="/associate/purchases" prefix="Raiz">Confirmação de compras</HeaderName>
          <HeaderGlobalBar>
            <Tag
              size="sm"
              type="teal"
              style={{ marginRight: '0.5rem', alignSelf: 'center' }}
              aria-label={`Sessão: ${session.display_name}`}
            >
              {session.display_name}
            </Tag>
            {session.demo_mode && (
              <DemoResetButton
                onReset={() => {
                  setSelectedId(null);
                  setMobileDetailOpen(false);
                  navigate('/associate/purchases', { replace: true });
                  loadPurchases();
                }}
              />
            )}
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

      <main
        className={`associate-app${mobileDetailOpen ? ' associate-app--detail-open' : ''}`}
        aria-label="Suas compras para confirmação"
      >
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
              onSelect={(id) => {
                setSelectedId(id);
                setRouteNotFound(false);
                setMobileDetailOpen(true);
                navigate(`/associate/purchases/${encodeURIComponent(id)}`);
              }}
            />
          )}
        </aside>

        {/* Coluna direita: detalhe */}
        <div className="associate-content">
          {/* Botão de voltar visível apenas no celular */}
          <Button
            kind="ghost"
            size="sm"
            renderIcon={ArrowLeft}
            className="associate-back-button"
            onClick={() => {
              setMobileDetailOpen(false);
              navigate('/associate/purchases');
            }}
          >
            Voltar para a lista
          </Button>
          {/* Âncora de foco ao abrir o detalhe no celular */}
          {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex */}
          <span ref={detailRef} tabIndex={-1} style={{ outline: 'none' }} />
          {routeNotFound ? (
            <div className="associate-empty-state" role="status">
              <h1 className="cds--type-heading-compact-02">Compra não encontrada</h1>
              <p className="cds--type-body-01" style={{ marginTop: '0.5rem' }}>
                Esta compra não está disponível para a sessão atual.
              </p>
              <Button
                kind="ghost"
                size="sm"
                style={{ marginTop: '0.5rem' }}
                onClick={() => navigate('/associate/purchases', { replace: true })}
              >
                Voltar para suas compras
              </Button>
            </div>
          ) : selectedId ? (
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
