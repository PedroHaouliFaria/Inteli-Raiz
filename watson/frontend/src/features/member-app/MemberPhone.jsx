import { Button, Tile, InlineNotification, Link } from '@carbon/react';
import { Checkmark, Close, FingerprintRecognition } from '@carbon/icons-react';
import { useState } from 'react';
import { useWatson } from '../../state/store';

// App do associado (Valdir). Atrito assimétrico: "Não reconheço" é um toque; "Sim, fui eu" pede biometria.
export default function MemberPhone({ caseId = '4821' }) {
  const { state, dispatch } = useWatson();
  const [showWhy, setShowWhy] = useState(false);
  const { screen, notifications } = state.phone;
  const send = (type) => () => dispatch({ type, caseId });

  return (
    <section aria-label="Celular do associado" className="watson-phone">
      <p className="cds--type-label-01" style={{ marginBottom: '0.5rem' }}>App do associado · Valdir (simulado)</p>
      <div className="watson-phone__screen">
        <InlineNotification kind="info" lowContrast hideCloseButton title="Nunca pedimos senha ou código por telefone." />
        {screen === 'locked' && (
          notifications.length === 0 ? (
            <p className="watson-phone__empty">Nenhum aviso. A analista pode enviar um aviso de compra pelo caso.</p>
          ) : (
            notifications.map((n) => (
              <Tile key={n.title}>
                <p className="cds--type-heading-compact-01">{n.title}</p>
                <p style={{ margin: '0.5rem 0' }}>{n.body}</p>
                <Button size="lg" onClick={send('openNotice')}>Abrir aviso</Button>
              </Tile>
            ))
          )
        )}
        {screen === 'notice' && (
          <>
            <h3 className="cds--type-heading-03">Aviso de compra no seu cartão final 4821</h3>
            <Tile>
              <p>R$ 2.349,90 · Loja Exemplo Eletrônicos</p>
              <p>São Paulo, SP · hoje, 03:14</p>
            </Tile>
            <p className="cds--type-heading-02">Foi você que comprou?</p>
            <Button kind="tertiary" size="xl" renderIcon={Checkmark} onClick={send('itWasMe')}>Sim, fui eu</Button>
            <Button kind="tertiary" size="xl" renderIcon={Close} onClick={send('notMe')}>Não reconheço</Button>
            <Link href="#" aria-expanded={showWhy} onClick={(e) => { e.preventDefault(); setShowWhy((v) => !v); }}>Por que recebi este aviso?</Link>
            {showWhy && <p>Vimos uma compra diferente do seu costume. Confirmar ajuda a proteger seu cartão.</p>}
          </>
        )}
        {screen === 'biometrics' && (
          <>
            <h3 className="cds--type-heading-03">Confirme com a digital do celular</h3>
            <p>Para compras de valor alto, pedimos a sua digital.</p>
            <Button size="xl" renderIcon={FingerprintRecognition} onClick={send('biometrics')}>Usar digital (simulado)</Button>
          </>
        )}
        {screen === 'released' && <InlineNotification kind="success" hideCloseButton title="Compra liberada" subtitle="Obrigado, Valdir. Seu cartão continua funcionando." />}
        {screen === 'protected' && <InlineNotification kind="success" hideCloseButton title="Cartão protegido" subtitle="Bloqueamos o cartão final 4821 e nada foi cobrado. Um cartão novo chega em até 7 dias úteis." />}
        {screen === 'reviewing' && <InlineNotification kind="info" hideCloseButton title="Recebemos sua resposta" subtitle="Por segurança, uma analista vai conferir a compra. Ela segue pausada e nada foi cobrado." />}
        <Link href="#" onClick={(e) => e.preventDefault()}>Prefiro falar com uma pessoa</Link>
      </div>
    </section>
  );
}
