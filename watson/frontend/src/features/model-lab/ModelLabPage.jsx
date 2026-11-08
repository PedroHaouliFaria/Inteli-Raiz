import { useEffect, useMemo, useState } from 'react';
import {
  Button, ComboBox, ContentSwitcher, Switch, Tag, InlineNotification, InlineLoading, TextInput, Select, SelectItem,
  Table, TableHead, TableRow, TableHeader, TableBody, TableCell,
} from '@carbon/react';
import { Renew, Shuffle, DocumentBlank, ArrowDown, ArrowUp, Send } from '@carbon/icons-react';
import {
  getModelLabInfo, searchModelLabSamples, getModelLabSample, getRandomModelLabSample, scoreTransaction,
} from '../../api/client';
import Term from '../../components/Term';
import ScoreBar from './ScoreBar';
import { BANDS, formatDelta, formatScore, formatTime, formatValue } from './format';

// Laboratório do modelo, versão B "E se?" (escolha do Leo em 27/10/2026): parte de uma transação,
// edita campos e compara o score original com o editado. Ambiente experimental: não gera alerta, caso nem aviso.

const TOP_FIELDS = 10;

function sampleTitle(sample) {
  if (!sample.id) return 'Transação típica (em branco)';
  const amount = sample.amount === null ? 'valor vazio' : `R$ ${formatValue({ kind: 'numeric' }, sample.amount)}`;
  return `${sample.id} · ${amount} · MCC ${sample.mcc} · ${sample.hour ?? '?'}h`;
}

function ResultSide({ title, result, info, features, empty }) {
  if (!result) {
    return (
      <section className="watson-lab__side" aria-label={title}>
        <p className="cds--type-label-01">{title}</p>
        <p className="cds--type-body-01 watson-lab__muted">{empty}</p>
      </section>
    );
  }
  const band = BANDS[result.band];
  const top = result.factors.filter((f) => f.contribution > 0).slice(0, 3);
  return (
    <section className="watson-lab__side" aria-label={title}>
      <p className="cds--type-label-01">{title}</p>
      <div className="watson-lab__score">
        <span className="watson-lab__score-value">{formatScore(result.score)}</span>
        <Tag type={band.tag}>{band.label}</Tag>
        {result.above_decision_threshold && <Tag type="outline">Acima do limiar do modelo</Tag>}
      </div>
      <ScoreBar score={result.score} info={info} />
      {top.length > 0 && (
        <p className="cds--type-helper-text-01 watson-lab__muted">
          Mais pesou: {top.map((f) => `${features[f.feature].label} ${formatDelta(f.contribution)}`).join(' · ')}
        </p>
      )}
    </section>
  );
}

function FieldInput({ feature, value, onChange }) {
  const id = `lab-${feature.name}`;
  if (feature.kind === 'numeric') {
    return (
      <TextInput id={id} size="sm" type="number" step="any" hideLabel labelText={feature.label}
        value={value ?? ''} onChange={(e) => onChange(e.target.value === '' ? null : Number(e.target.value))} />
    );
  }
  const options = feature.kind === 'binary' ? [1, 0] : ['nan', ...feature.options];
  return (
    <Select id={id} size="sm" hideLabel labelText={feature.label} value={String(value ?? '')}
      onChange={(e) => onChange(feature.kind === 'binary' ? Number(e.target.value) : e.target.value)}>
      {options.map((o) => <SelectItem key={o} value={String(o)} text={formatValue(feature, o)} />)}
    </Select>
  );
}

export default function ModelLabPage() {
  const [info, setInfo] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [sample, setSample] = useState(null); // transação de partida: { id, is_fraud, features, ... }
  const [original, setOriginal] = useState(null); // resultado do modelo para a transação de partida
  const [edited, setEdited] = useState({}); // campos como estão na coluna "Editado"
  const [editedResult, setEditedResult] = useState(null);
  const [view, setView] = useState('top');
  const [suggestions, setSuggestions] = useState([]);
  const [history, setHistory] = useState([]);

  const features = useMemo(() => Object.fromEntries((info?.features ?? []).map((f) => [f.name, f])), [info]);
  const changed = useMemo(
    () => (sample ? Object.keys(edited).filter((k) => edited[k] !== sample.features[k]) : []),
    [sample, edited],
  );

  const run = async (task) => {
    setBusy(true);
    setError(null);
    try { await task(); } catch (e) { setError(e.message); } finally { setBusy(false); }
  };

  const remember = (entry) => setHistory((h) => [{ ...entry, at: new Date() }, ...h].slice(0, 20));

  // Pontua a transação de partida; sempre chamado dentro de run().
  const start = async (next) => {
    const result = await scoreTransaction(next.features);
    setSample(next);
    setOriginal(result);
    setEdited(next.features);
    setEditedResult(null);
    remember({ label: `Original · ${next.id ?? 'transação típica'}`, sample: next, original: result, edited: next.features, result });
  };

  useEffect(() => {
    run(async () => {
      const loaded = await getModelLabInfo();
      setInfo(loaded);
      setSuggestions(await searchModelLabSamples('', 'fraud'));
    });
  }, []);

  const blankSample = () => ({
    id: null, is_fraud: null, amount: null, mcc: '', hour: null,
    features: Object.fromEntries(info.features.map((f) => [f.name, f.typical_value])),
  });

  const sendEdited = () => run(async () => {
    const result = await scoreTransaction(edited);
    setEditedResult(result);
    const what = changed.map((k) => `${features[k].label} ${formatValue(features[k], sample.features[k])} → ${formatValue(features[k], edited[k])}`);
    remember({ label: what.join(' · ') || 'Sem mudanças', sample, original, edited, result });
  });

  const restore = (entry) => {
    setSample(entry.sample);
    setOriginal(entry.original);
    setEdited(entry.edited);
    setEditedResult(entry.edited === entry.sample.features ? null : entry.result);
  };

  const weights = useMemo(() => Object.fromEntries((original?.factors ?? []).map((f) => [f.feature, f.contribution])), [original]);
  const rows = useMemo(() => {
    if (!info) return [];
    const byWeight = [...info.features].sort((a, b) => Math.abs(weights[b.name] ?? 0) - Math.abs(weights[a.name] ?? 0));
    if (view === 'changed') return byWeight.filter((f) => changed.includes(f.name));
    if (view === 'top') return byWeight.filter((f, i) => i < TOP_FIELDS || changed.includes(f.name));
    return info.features;
  }, [info, weights, view, changed]);

  const delta = editedResult && original ? editedResult.score - original.score : null;

  return (
    <main className="watson-main watson-lab" id="main-content">
      <div className="watson-lab__title">
        <h1 className="cds--type-heading-04">Laboratório do modelo</h1>
        <Tag type="purple">Ambiente experimental</Tag>
      </div>
      <div className="cds--type-body-01 watson-lab__muted">
        Nada aqui gera alerta, caso ou aviso. Escolha uma transação, mude os campos e veja como o <Term id="score" /> responde. As faixas seguem a política do
        aviso de compra; o tracejado é o limiar do modelo.
      </div>

      {error && (
        <InlineNotification kind="error" lowContrast title="Não consegui falar com o modelo."
          subtitle="Confira se o backend está rodando com o extra risk (veja watson/backend/README.md)." onClose={() => setError(null)} />
      )}
      {!info && !error && <InlineLoading description="Carregando o modelo e o conjunto de teste" />}

      {info && (
        <>
          <div className="watson-lab__start">
            <ComboBox id="lab-sample" titleText={`Transação de partida · ${info.test_set_size.toLocaleString('pt-BR')} no conjunto de teste, ${info.test_set_frauds} fraudes`}
              placeholder="Busque pelo id (EVT_SYN_…)" items={suggestions} itemToString={(s) => (s ? sampleTitle(s) : '')}
              selectedItem={sample?.id ? suggestions.find((s) => s.id === sample.id) ?? null : null}
              onInputChange={(text) => { if (text && !text.includes('·')) searchModelLabSamples(text).then(setSuggestions).catch(() => {}); }}
              onChange={({ selectedItem }) => selectedItem && run(async () => start(await getModelLabSample(selectedItem.id)))} />
            <div className="watson-lab__start-actions">
              <Button kind="tertiary" size="md" renderIcon={Shuffle} disabled={busy}
                onClick={() => run(async () => start(await getRandomModelLabSample('fraud')))}>Fraude aleatória</Button>
              <Button kind="tertiary" size="md" renderIcon={Shuffle} disabled={busy}
                onClick={() => run(async () => start(await getRandomModelLabSample('legit')))}>Legítima aleatória</Button>
              <Button kind="ghost" size="md" renderIcon={DocumentBlank} disabled={busy} onClick={() => run(() => start(blankSample()))}>Em branco</Button>
            </div>
          </div>

          {sample && (
            <p className="cds--type-body-compact-01">
              <span className="watson-lab__mono">{sampleTitle(sample)}</span>{' '}
              {sample.is_fraud !== null && (
                <Tag type={sample.is_fraud ? 'red' : 'green'} size="sm">Rótulo real: {sample.is_fraud ? 'fraude' : 'legítima'}</Tag>
              )}
            </p>
          )}

          {!sample && (
            <p className="cds--type-body-01 watson-lab__muted">Escolha uma transação acima, sorteie uma ou comece em branco (todos os campos no valor típico de uma compra legítima).</p>
          )}

          {sample && (
            <>
              <div className="watson-lab__duo">
                <ResultSide title="Original" result={original} info={info} features={features} />
                <ResultSide title={`Editado · ${changed.length} ${changed.length === 1 ? 'campo alterado' : 'campos alterados'}`}
                  result={editedResult} info={info} features={features}
                  empty="Mude um ou mais campos na tabela e clique em “Enviar edição ao modelo”." />
              </div>
              {delta !== null && (
                <p className="cds--type-body-compact-01 watson-lab__delta">
                  {delta < 0 ? <ArrowDown /> : <ArrowUp />}
                  {formatDelta(delta)} no score
                  {editedResult.band !== original.band && ` · saiu de ${BANDS[original.band].short.toLowerCase()} para ${BANDS[editedResult.band].short.toLowerCase()}`}
                  {editedResult.band === 'medium' && editedResult.band !== original.band && ': o Watson mandaria o aviso de compra sozinho'}
                </p>
              )}

              <div className="watson-lab__grid">
                <section className="watson-lab__table" aria-label="Campos da transação">
                  <div className="watson-lab__toolbar">
                    <ContentSwitcher size="sm" selectedIndex={['top', 'changed', 'all'].indexOf(view)}
                      onChange={({ name }) => setView(name)}>
                      <Switch name="top" text={`Top ${TOP_FIELDS}`} />
                      <Switch name="changed" text={`Alterados (${changed.length})`} />
                      <Switch name="all" text="Todos (28)" />
                    </ContentSwitcher>
                    <div className="watson-lab__toolbar-actions">
                      <Button kind="secondary" size="md" renderIcon={Renew} disabled={busy || changed.length === 0}
                        onClick={() => { setEdited(sample.features); setEditedResult(null); }}>Restaurar original</Button>
                      <Button kind="primary" size="md" renderIcon={Send} disabled={busy || changed.length === 0} onClick={sendEdited}>
                        Enviar edição ao modelo
                      </Button>
                    </div>
                  </div>
                  <Table size="md" useZebraStyles={false}>
                    <TableHead>
                      <TableRow>
                        <TableHeader>Campo</TableHeader>
                        <TableHeader>Original</TableHeader>
                        <TableHeader>Editado</TableHeader>
                        <TableHeader>Peso no original</TableHeader>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rows.map((f) => (
                        <TableRow key={f.name} className={changed.includes(f.name) ? 'watson-lab__row--changed' : undefined}>
                          <TableCell>
                            {f.label}
                            <span className="cds--type-helper-text-01 watson-lab__muted"> · {f.group}</span>
                          </TableCell>
                          <TableCell className="watson-lab__mono">{formatValue(f, sample.features[f.name])}</TableCell>
                          <TableCell className="watson-lab__input">
                            <FieldInput feature={f} value={edited[f.name]} onChange={(v) => setEdited((e) => ({ ...e, [f.name]: v }))} />
                          </TableCell>
                          <TableCell className="watson-lab__mono">
                            {weights[f.name] === undefined ? '—' : formatDelta(weights[f.name])}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  {view === 'changed' && changed.length === 0 && (
                    <p className="cds--type-body-01 watson-lab__muted watson-lab__empty">Nenhum campo alterado ainda.</p>
                  )}
                  <p className="cds--type-helper-text-01 watson-lab__muted watson-lab__empty">
                    Peso = quanto o score cai se só aquele campo voltar ao valor típico de uma compra legítima.
                    “—” = o campo já está no valor típico.
                  </p>
                </section>

                <aside className="watson-lab__history" aria-label="Histórico desta sessão">
                  <h2 className="cds--type-heading-compact-01">Histórico desta sessão</h2>
                  {history.length === 0 && <p className="cds--type-body-01 watson-lab__muted">Os envios aparecem aqui.</p>}
                  <ul>
                    {history.map((h) => (
                      <li key={h.at.getTime()}>
                        <button type="button" className="watson-lab__history-item" onClick={() => restore(h)}>
                          <span className="watson-lab__mono">{formatTime(h.at)}</span>
                          <span className="watson-lab__history-label">{h.label}</span>
                          <span className="watson-lab__mono">{formatScore(h.result.score)}</span>
                          <Tag type={BANDS[h.result.band].tag} size="sm">{BANDS[h.result.band].short}</Tag>
                        </button>
                      </li>
                    ))}
                  </ul>
                  <p className="cds--type-helper-text-01 watson-lab__muted">
                    Clique para voltar a um cenário. O histórico some quando você fecha a aba.
                  </p>
                  <p className="cds--type-helper-text-01 watson-lab__muted">
                    Modelo {original?.model_name ?? info.name} · {info.provider === 'local' ? 'rodando local' : 'watsonx.ai'}
                    {original && ` · ${original.latency_ms} ms`}
                  </p>
                </aside>
              </div>
            </>
          )}
        </>
      )}
    </main>
  );
}
