import { useEffect, useState } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import {
  Header, HeaderName, HeaderNavigation, HeaderMenuItem, HeaderGlobalBar, HeaderGlobalAction, SkipToContent,
  Theme, Toggle, Button, ToastNotification, ProgressIndicator, ProgressStep, IconButton,
} from '@carbon/react';
import { Help, Renew, Mobile, Close } from '@carbon/icons-react';
import { DicionarioProvider, PainelDicionario, useDicionario } from './components/Dicionario';
import { WatsonProvider, useWatson } from './state/store';
import Celular from './components/Celular';
import Fila from './pages/Fila';
import Quadro from './pages/Quadro';
import Caso from './pages/Caso';

// Alta fidelidade do protótipo 3 (ponta a ponta) com os chips do protótipo 2. Escolha do Leo (26/10/2026):
// produto: o celular do associado abre num painel quando o Watson envia um aviso (variação 2);
// modo apresentação: celular sempre visível e narração em 5 passos, para a banca e o vídeo (variação 3).

const PASSOS = [
  { titulo: 'Abrir a fila', texto: 'A Camila começa o turno na fila. O Watson sugere o caso #4821 (maior risco × valor). Clique em “Abrir #4821”.' },
  { titulo: 'Entender o caso', texto: 'Três alertas viraram um caso. O trilho explica o score; experimente o chip “Por que 0,92?” e depois “Preparar aviso”.' },
  { titulo: 'Perguntar ao associado', texto: 'O Watson enviou o aviso de compra. O caso está aguardando o Valdir. Abra o aviso no celular.' },
  { titulo: 'Valdir responde', texto: '“Não reconheço” bloqueia com um toque. “Sim, fui eu” pede a digital: é o atrito contra o Impostor.' },
  { titulo: 'Watson aplica a regra', texto: 'A regra combinada foi aplicada e registrada na linha do tempo. Ligue “Aparelho trocado” e reinicie para ver o caso voltar para a Camila.' },
];

function passoAtual(state, pathname) {
  const c = state.casos.find((x) => x.id === '4821');
  if (c.estado === 'resolvido' || (c.estado === 'analise' && (state.eventos['4821'] ?? []).length > 0)) return 4;
  if (['aviso', 'biometria'].includes(state.celular.tela)) return 3;
  if (c.estado === 'aguardando') return 2;
  if (pathname.startsWith('/caso')) return 1;
  return 0;
}

function lerApresentacao() {
  // ?apresentacao no servidor local ou #apresentacao no link publicado
  if (new URLSearchParams(window.location.search).has('apresentacao') || window.location.hash === '#apresentacao') return true;
  try { return localStorage.getItem('watson-apresentacao') === '1'; } catch { return false; }
}

function Shell() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { aberto, alternar } = useDicionario();
  const { state, dispatch } = useWatson();
  const [apresentacao, setApresentacao] = useState(lerApresentacao);
  const [painel, setPainel] = useState(false);
  const ir = (rota) => (e) => { e.preventDefault(); navigate(rota); };

  useEffect(() => { try { localStorage.setItem('watson-apresentacao', apresentacao ? '1' : '0'); } catch { /* sem armazenamento */ } }, [apresentacao]);
  // No produto o painel do celular abre sozinho quando chega um aviso.
  useEffect(() => { if (state.celular.notificacoes.length > 0) setPainel(true); }, [state.celular.notificacoes]);

  const reiniciar = (aparelhoTrocado) => { dispatch({ tipo: 'reiniciar', aparelhoTrocado }); navigate('/'); };
  const passo = passoAtual(state, pathname);
  const lateral = apresentacao ? <Celular /> : null;

  return (
    <>
      <Theme theme="g100">
        <Header aria-label="Watson · Prevenção a fraudes">
          <SkipToContent />
          <HeaderName href="/" prefix="Watson" onClick={ir('/')}>Prevenção a fraudes</HeaderName>
          <HeaderNavigation aria-label="Navegação">
            <HeaderMenuItem href="/" isActive={pathname === '/'} onClick={ir('/')}>Fila</HeaderMenuItem>
            <HeaderMenuItem href="/quadro" isActive={pathname === '/quadro'} onClick={ir('/quadro')}>Quadro do processo</HeaderMenuItem>
          </HeaderNavigation>
          <HeaderGlobalBar>
            {!apresentacao && (
              <HeaderGlobalAction aria-label="Celular do associado" isActive={painel} onClick={() => setPainel((v) => !v)}>
                <Mobile size={20} />
              </HeaderGlobalAction>
            )}
            <HeaderGlobalAction aria-label="Dicionário do Watson" isActive={aberto} onClick={alternar} tooltipAlignment="end">
              <Help size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
          <PainelDicionario />
        </Header>
      </Theme>

      <div style={{ paddingTop: '3rem' }}>
        <div className="watson-prototipo" role="region" aria-label="Controles do protótipo">
          <span className="cds--type-label-01">Controles da demonstração</span>
          <Toggle id="apresentacao" size="sm" labelText="Modo apresentação" labelA="Desligado" labelB="Ligado"
            toggled={apresentacao} onToggle={setApresentacao} />
          <Toggle id="aparelho" size="sm" labelText="Cenário" labelA="Aparelho conhecido" labelB="Aparelho trocado há 2 dias"
            toggled={state.aparelhoTrocado} onToggle={(v) => reiniciar(v)} />
          <Button size="sm" kind="ghost" renderIcon={Renew} onClick={() => reiniciar(state.aparelhoTrocado)}>Reiniciar</Button>
        </div>

        {apresentacao && (
          <div className="watson-narracao" aria-live="polite">
            <ProgressIndicator currentIndex={passo} spaceEqually>
              {PASSOS.map((p) => <ProgressStep key={p.titulo} label={p.titulo} />)}
            </ProgressIndicator>
            <p className="cds--type-body-02"><strong>Passo {passo + 1}.</strong> {passo === 4 && state.aparelhoTrocado
              ? 'O Watson não liberou sozinho: a confirmação veio de um aparelho trocado há 2 dias, sinal do Impostor. O caso voltou para a Camila decidir.'
              : PASSOS[passo].texto}</p>
          </div>
        )}

        <Routes>
          <Route path="/" element={<Fila comCelular={lateral} />} />
          <Route path="/quadro" element={<Quadro comCelular={lateral} />} />
          <Route path="/caso/:id" element={<Caso comCelular={lateral} />} />
        </Routes>
      </div>

      {!apresentacao && painel && (
        <div className="watson-flutuante" role="dialog" aria-label="Celular do associado">
          <IconButton kind="ghost" size="sm" label="Fechar celular" align="left" className="watson-flutuante__fechar" onClick={() => setPainel(false)}>
            <Close />
          </IconButton>
          <Celular />
        </div>
      )}

      {state.toast && (
        <div className="watson-toast">
          <ToastNotification
            key={state.toast.titulo + state.minuto}
            kind={state.toast.tipo}
            title={state.toast.titulo}
            subtitle={state.toast.sub}
            timeout={6000}
            onClose={() => { dispatch({ tipo: 'fecharToast' }); return false; }}
          />
        </div>
      )}
    </>
  );
}

export default function App() {
  return (
    <WatsonProvider>
      <DicionarioProvider>
        <Shell />
      </DicionarioProvider>
    </WatsonProvider>
  );
}
