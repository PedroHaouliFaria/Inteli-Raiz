/**
 * AssociateApp — experiência conectada à API para sessão ASSOCIADO.
 *
 * Renderiza:
 *   - Header com nome da pessoa e botão de sair (via SessionGate)
 *   - Lista de compras reais (GET /api/purchases)
 *   - Detalhe da compra selecionada (PurchaseDetail)
 *   - Copiloto global da pessoa, independente da compra selecionada
 *
 * Não usa o estado mockado de src/state/store.jsx.
 * Não renderiza biometria, aparelho trocado ou bloqueio de cartão.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Button,
  Header,
  HeaderGlobalBar,
  HeaderGlobalAction,
  HeaderName,
  InlineLoading,
  InlineNotification,
  Search,
  Select,
  SelectItem,
  SkipToContent,
  Tag,
  Theme,
} from '@carbon/react';
import { ArrowLeft, Renew, Logout, WatsonxAi } from '@carbon/icons-react';
import { useNavigate, useParams } from 'react-router-dom';
import { ApiError, getPurchases } from '../../api/client.js';
import { useSession } from '../session/SessionGate.jsx';
import PurchaseList from './PurchaseList.jsx';
import PurchaseDetail from './PurchaseDetail.jsx';
import DemoResetButton from './DemoResetButton.jsx';
import AssociateCopilot from './AssociateCopilot.jsx';
import { statusMeta } from './utils.js';

export default function AssociateApp() {
  const session = useSession();
  const navigate = useNavigate();
  const { caseId = null } = useParams();

  const [purchases, setPurchases] = useState(null);
  const [listLoading, setListLoading] = useState(true);
  const [listError, setListError] = useState(null);
  const [loggingOut, setLoggingOut] = useState(false);
  const [routeNotFound, setRouteNotFound] = useState(false);
  const [merchantFilter, setMerchantFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [copilotOpen, setCopilotOpen] = useState(() => (
    typeof window === 'undefined' || window.matchMedia('(min-width: 55.01rem)').matches
  ));

  const detailRef = useRef(null);

  const statusOptions = useMemo(() => {
    const options = new Map();
    (purchases ?? []).forEach((purchase) => {
      options.set(purchase.status, statusMeta(purchase.status).shortLabel);
    });
    return [...options.entries()];
  }, [purchases]);

  const filteredPurchases = useMemo(() => {
    const normalizedMerchant = merchantFilter.trim().toLocaleLowerCase('pt-BR');
    return (purchases ?? []).filter((purchase) => {
      const matchesMerchant = !normalizedMerchant
        || purchase.merchant_display.toLocaleLowerCase('pt-BR').includes(normalizedMerchant);
      const matchesStatus = !statusFilter || purchase.status === statusFilter;
      return matchesMerchant && matchesStatus;
    });
  }, [merchantFilter, purchases, statusFilter]);

  const filtersActive = merchantFilter.trim() !== '' || statusFilter !== '';

  const loadPurchases = useCallback(async () => {
    setListLoading(true);
    setListError(null);
    try {
      const data = await getPurchases();
      setPurchases(data.purchases);
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
      return;
    }

    const authorized = purchases.some((purchase) => purchase.case_id === caseId);
    setRouteNotFound(!authorized);
  }, [caseId, purchases]);

  // Ao abrir uma compra, rola para o topo e leva foco ao conteúdo novo.
  useEffect(() => {
    if (!caseId) return;
    window.scrollTo(0, 0);
    detailRef.current?.focus({ preventScroll: true });
  }, [caseId]);

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
            <HeaderGlobalAction
              aria-label={copilotOpen ? 'Fechar copiloto' : 'Abrir copiloto'}
              isActive={copilotOpen}
              onClick={() => setCopilotOpen((current) => !current)}
            >
              <WatsonxAi size={20} />
            </HeaderGlobalAction>
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
        className={`associate-app${caseId ? ' associate-app--detail-open' : ''}${copilotOpen ? ' associate-app--copilot-open' : ''}`}
        aria-label="Suas compras para confirmação"
      >
        <div className="associate-workspace">
          {!caseId && (
            <section className="associate-overview" aria-labelledby="associate-purchases-title">
              <div className="associate-overview__header">
                <div>
                  <p className="cds--type-label-01 associate-overview__eyebrow">Visão geral</p>
                  <h1 id="associate-purchases-title" className="cds--type-heading-04">Suas compras</h1>
                  <p className="cds--type-body-compact-01 associate-overview__description">
                    Acompanhe suas transações e abra uma compra quando quiser conferir os detalhes.
                  </p>
                </div>
                <span className="cds--type-label-01 associate-overview__count">
                  {filtersActive
                    ? `${filteredPurchases.length} de ${purchases?.length ?? 0}`
                    : (purchases?.length ?? 0)}{' '}
                  {filteredPurchases.length === 1 ? 'compra' : 'compras'}
                </span>
              </div>
              {session.demo_mode && (
                <div className="associate-overview__demo">
                  <DemoResetButton
                    variant="button"
                    onReset={() => {
                      setMerchantFilter('');
                      setStatusFilter('');
                      navigate('/associate/purchases', { replace: true });
                      loadPurchases();
                    }}
                  />
                </div>
              )}

              {!listLoading && !listError && purchases !== null && purchases.length > 0 && (
                <div className="associate-filters" aria-label="Filtros das compras">
                  <Search
                    id="associate-merchant-filter"
                    size="lg"
                    labelText="Buscar por estabelecimento"
                    placeholder="Buscar estabelecimento"
                    value={merchantFilter}
                    onChange={(event) => setMerchantFilter(event.target.value)}
                  />
                  <Select
                    id="associate-status-filter"
                    labelText="Status da compra"
                    value={statusFilter}
                    onChange={(event) => setStatusFilter(event.target.value)}
                  >
                    <SelectItem value="" text="Todos os status" />
                    {statusOptions.map(([value, label]) => (
                      <SelectItem key={value} value={value} text={label} />
                    ))}
                  </Select>
                  {filtersActive && (
                    <Button
                      kind="ghost"
                      size="sm"
                      className="associate-filters__reset"
                      onClick={() => {
                        setMerchantFilter('');
                        setStatusFilter('');
                      }}
                    >
                      Limpar filtros
                    </Button>
                  )}
                </div>
              )}

          {listLoading && (
            <div className="associate-overview__feedback" role="status" aria-live="polite">
              <InlineLoading description="Carregando…" status="active" />
            </div>
          )}

          {listError && (
            <div className="associate-overview__feedback">
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
              purchases={filteredPurchases}
              emptyMessage={filtersActive
                ? 'Nenhuma compra encontrada para estes filtros.'
                : 'Nenhuma compra encontrada para esta sessão.'}
              onSelect={(id) => {
                setRouteNotFound(false);
                navigate(`/associate/purchases/${encodeURIComponent(id)}`);
              }}
            />
          )}
            </section>
          )}

          {caseId && (
            <div className="associate-content">
              <Button
                kind="ghost"
                size="sm"
                renderIcon={ArrowLeft}
                className="associate-back-button"
                onClick={() => navigate('/associate/purchases')}
              >
                Voltar para suas compras
              </Button>
              {/* Âncora de foco ao abrir o detalhe */}
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
              ) : (
                <PurchaseDetail
                  key={caseId}
                  caseId={caseId}
                  onPurchaseChanged={loadPurchases}
                />
              )}
            </div>
          )}
        </div>

        {copilotOpen && (
          <AssociateCopilot
            selectedCaseId={routeNotFound ? null : caseId}
            onClose={() => setCopilotOpen(false)}
            onAction={loadPurchases}
          />
        )}
      </main>
    </Theme>
  );
}
