import { formatScore } from './format';

// Régua de 0 a 1 com as três faixas, o limiar de decisão do modelo (tracejado) e o score (marcador).
export default function ScoreBar({ score, info }) {
  const medium = info.medium_threshold * 100;
  const high = info.high_threshold * 100;
  return (
    <div className="watson-score-bar">
      <div className="watson-score-bar__track" role="img"
        aria-label={`Score ${formatScore(score)}. Médio a partir de ${formatScore(info.medium_threshold)}, alto a partir de ${formatScore(info.high_threshold)}.`}>
        <span className="watson-score-bar__zone watson-score-bar__zone--low" style={{ width: `${medium}%` }} />
        <span className="watson-score-bar__zone watson-score-bar__zone--medium" style={{ width: `${high - medium}%` }} />
        <span className="watson-score-bar__zone watson-score-bar__zone--high" style={{ width: `${100 - high}%` }} />
        <span className="watson-score-bar__threshold" style={{ left: `${info.decision_threshold * 100}%` }} />
        <span className="watson-score-bar__marker" style={{ left: `calc(${Math.min(score, 1) * 100}% - 2px)` }} />
      </div>
      <div className="watson-score-bar__scale cds--type-label-01" aria-hidden="true">
        <span style={{ left: 0 }}>0</span>
        <span style={{ left: `${medium}%` }}>{formatScore(info.medium_threshold)}</span>
        <span style={{ left: `${high}%` }}>{formatScore(info.high_threshold)}</span>
        <span style={{ right: 0 }}>1</span>
      </div>
    </div>
  );
}
