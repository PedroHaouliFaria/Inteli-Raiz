import { useEffect, useState } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import {
  Header, HeaderName, HeaderMenuButton, HeaderGlobalBar, HeaderGlobalAction, SkipToContent,
  SideNav, SideNavItems, SideNavLink, SideNavDivider,
  Theme, Toggle, Button, ToastNotification, ProgressIndicator, ProgressStep, IconButton, Select, SelectItem,
} from '@carbon/react';
import { Help, Renew, Mobile, Close, WatsonxAi, List, Column, Archive, UserMultiple, ChartLineData, Report } from '@carbon/icons-react';
import { GlossaryProvider, GlossaryPanel, useGlossary } from '../components/Glossary';
import { WatsonProvider, useWatson } from '../state/store';
import { RailProvider, useRail, RAIL_VARIANTS } from '../components/RailPreferences';
import MemberPhone from '../features/member-app/MemberPhone';
import QueuePage from '../features/queue/QueuePage';
import BoardPage from '../features/board/BoardPage';
import CasePage from '../features/case/CasePage';
import ComingSoonPage from '../features/coming-soon/ComingSoonPage';

// Alta fidelidade do protótipo 3 (ponta a ponta) com os chips do protótipo 2. Escolha do Leo (26/10/2026):
// produto: o celular do associado abre num painel quando o Watson envia um aviso (variação 2);
// modo apresentação: celular sempre visível e narração em 5 passos, para a banca e o vídeo (variação 3).

const STEPS = [
  { title: 'Abrir a fila', text: 'A Camila começa o turno na fila. O Watson sugere o caso #4821 (maior risco × valor). Clique em “Abrir #4821”.' },
  { title: 'Entender o caso', text: 'Três alertas viraram um caso. O trilho explica o score; experimente o chip “Por que 0,92?” e depois “Preparar aviso”.' },
  { title: 'Perguntar ao associado', text: 'O Watson enviou o aviso de compra. O caso está aguardando o Valdir. Abra o aviso no celular.' },
  { title: 'Valdir responde', text: '“Não reconheço” bloqueia com um toque. “Sim, fui eu” pede a digital: é o atrito contra o Impostor.' },
  { title: 'Watson aplica a regra', text: 'A regra combinada foi aplicada e registrada na linha do tempo. Ligue “Aparelho trocado” e reinicie para ver o caso voltar para a Camila.' },
];

function currentStep(state, pathname) {
  const c = state.cases.find((x) => x.id === '4821');
  if (c.status === 'resolved' || (c.status === 'in_review' && (state.events['4821'] ?? []).length > 0)) return 4;
  if (['notice', 'biometrics'].includes(state.phone.screen)) return 3;
  if (c.status === 'awaiting_member') return 2;
  if (pathname.startsWith('/cases')) return 1;
  return 0;
}

function readPresentationMode() {
  // ?presentation no servidor local ou #presentation no link publicado (#apresentacao continua valendo nos links antigos)
  const params = new URLSearchParams(window.location.search);
  if (params.has('presentation') || params.has('apresentacao') || ['#presentation', '#apresentacao'].includes(window.location.hash)) return true;
  try { return localStorage.getItem('watson-presentation') === '1'; } catch { return false; }
}

function Shell() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { isOpen: glossaryOpen, toggle: toggleGlossary } = useGlossary();
  const { state, dispatch } = useWatson();
  const rail = useRail();
  const [presentation, setPresentation] = useState(readPresentationMode);
  const [phoneOpen, setPhoneOpen] = useState(false);
  const [navOpen, setNavOpen] = useState(false);
  const go = (route) => (e) => { e.preventDefault(); setNavOpen(false); navigate(route); };

  useEffect(() => { try { localStorage.setItem('watson-presentation', presentation ? '1' : '0'); } catch { /* sem armazenamento */ } }, [presentation]);
  // No produto o painel do celular abre sozinho quando chega um aviso.
  useEffect(() => { if (state.phone.notifications.length > 0) setPhoneOpen(true); }, [state.phone.notifications]);

  const reset = (deviceChanged) => { dispatch({ type: 'reset', deviceChanged }); navigate('/'); };
  const step = currentStep(state, pathname);
  const phoneSlot = presentation ? <MemberPhone /> : null;

  return (
    <>
      <Theme theme="g100">
        <Header aria-label="Watson · Prevenção a fraudes">
          <SkipToContent />
          <HeaderMenuButton isCollapsible aria-label={navOpen ? 'Recolher o menu' : 'Abrir o menu'} isActive={navOpen} onClick={() => setNavOpen((v) => !v)} />
          <HeaderName href="/" prefix="Watson" onClick={go('/')}>Prevenção a fraudes</HeaderName>
          <HeaderGlobalBar>
            {rail.variant === 'header' && (
              <HeaderGlobalAction aria-label={rail.collapsed ? 'Mostrar o painel do Watson' : 'Esconder o painel do Watson'} isActive={!rail.collapsed} onClick={rail.toggle}>
                <WatsonxAi size={20} />
              </HeaderGlobalAction>
            )}
            {!presentation && (
              <HeaderGlobalAction aria-label="Celular do associado" isActive={phoneOpen} onClick={() => setPhoneOpen((v) => !v)}>
                <Mobile size={20} />
              </HeaderGlobalAction>
            )}
            <HeaderGlobalAction aria-label="Dicionário do Watson" isActive={glossaryOpen} onClick={toggleGlossary} tooltipAlignment="end">
              <Help size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
          <GlossaryPanel />
        </Header>
      </Theme>

      {/* Navegação lateral do mockup 3: trilho de ícones que abre com os nomes (botão do menu ou passar o mouse). */}
      <SideNav aria-label="Navegação principal" isRail expanded={navOpen} onOverlayClick={() => setNavOpen(false)}>
        <SideNavItems>
          <SideNavLink renderIcon={List} href="/" isActive={pathname === '/' || pathname.startsWith('/cases')} onClick={go('/')}>Fila</SideNavLink>
          <SideNavLink renderIcon={Column} href="/board" isActive={pathname === '/board'} onClick={go('/board')}>Quadro do processo</SideNavLink>
          <SideNavDivider />
          <SideNavLink renderIcon={Archive} href="/soon/closed-cases" isActive={pathname === '/soon/closed-cases'} onClick={go('/soon/closed-cases')}>Casos encerrados</SideNavLink>
          <SideNavLink renderIcon={UserMultiple} href="/soon/members" isActive={pathname === '/soon/members'} onClick={go('/soon/members')}>Associados</SideNavLink>
          <SideNavLink renderIcon={ChartLineData} href="/soon/model-monitoring" isActive={pathname === '/soon/model-monitoring'} onClick={go('/soon/model-monitoring')}>Monitoramento do modelo</SideNavLink>
          <SideNavLink renderIcon={Report} href="/soon/reports" isActive={pathname === '/soon/reports'} onClick={go('/soon/reports')}>Relatórios</SideNavLink>
        </SideNavItems>
      </SideNav>

      <div className="watson-content" style={{ paddingTop: '3rem' }}>
        <div className="watson-demo-controls" role="region" aria-label="Controles do protótipo">
          <span className="cds--type-label-01">Controles da demonstração</span>
          <Toggle id="presentation" size="sm" labelText="Modo apresentação" labelA="Desligado" labelB="Ligado"
            toggled={presentation} onToggle={setPresentation} />
          <Toggle id="device-changed" size="sm" labelText="Cenário" labelA="Aparelho conhecido" labelB="Aparelho trocado há 2 dias"
            toggled={state.deviceChanged} onToggle={(v) => reset(v)} />
          <Select id="rail-variant" size="sm" inline labelText="Painel do Watson" value={rail.variant}
            onChange={(e) => { rail.setVariant(e.target.value); rail.setCollapsed(true); }}>
            {Object.entries(RAIL_VARIANTS).map(([value, text]) => <SelectItem key={value} value={value} text={text} />)}
          </Select>
          <Button size="sm" kind="ghost" renderIcon={Renew} onClick={() => reset(state.deviceChanged)}>Reiniciar</Button>
        </div>

        {presentation && (
          <div className="watson-narration" aria-live="polite">
            <ProgressIndicator currentIndex={step} spaceEqually>
              {STEPS.map((p) => <ProgressStep key={p.title} label={p.title} />)}
            </ProgressIndicator>
            <p className="cds--type-body-02"><strong>Passo {step + 1}.</strong> {step === 4 && state.deviceChanged
              ? 'O Watson não liberou sozinho: a confirmação veio de um aparelho trocado há 2 dias, sinal do Impostor. O caso voltou para a Camila decidir.'
              : STEPS[step].text}</p>
          </div>
        )}

        <Routes>
          <Route path="/" element={<QueuePage phoneSlot={phoneSlot} />} />
          <Route path="/board" element={<BoardPage phoneSlot={phoneSlot} />} />
          <Route path="/cases/:id" element={<CasePage phoneSlot={phoneSlot} />} />
          <Route path="/soon/:section" element={<ComingSoonPage />} />
        </Routes>
      </div>

      {!presentation && phoneOpen && (
        <div className="watson-floating" role="dialog" aria-label="Celular do associado">
          <IconButton kind="ghost" size="sm" label="Fechar celular" align="left" className="watson-floating__close" onClick={() => setPhoneOpen(false)}>
            <Close />
          </IconButton>
          <MemberPhone />
        </div>
      )}

      {state.toast && (
        <div className="watson-toast">
          <ToastNotification
            key={state.toast.title + state.minute}
            kind={state.toast.kind}
            title={state.toast.title}
            subtitle={state.toast.subtitle}
            timeout={6000}
            onClose={() => { dispatch({ type: 'closeToast' }); return false; }}
          />
        </div>
      )}
    </>
  );
}

export default function App() {
  return (
    <WatsonProvider>
      <GlossaryProvider>
        <RailProvider>
          <Shell />
        </RailProvider>
      </GlossaryProvider>
    </WatsonProvider>
  );
}
