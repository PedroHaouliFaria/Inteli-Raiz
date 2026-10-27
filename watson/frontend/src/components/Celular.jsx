import { Button, Tile, InlineNotification, Link } from '@carbon/react';
import { Checkmark, Close, FingerprintRecognition } from '@carbon/icons-react';
import { useState } from 'react';
import { useWatson } from '../state/store';

// App do associado (Valdir). Atrito assimétrico: "Não reconheço" é um toque; "Sim, fui eu" pede biometria.
export default function Celular({ casoId = '4821' }) {
  const { state, dispatch } = useWatson();
  const [porque, setPorque] = useState(false);
  const { tela, notificacoes } = state.celular;
  const d = (tipo) => () => dispatch({ tipo, casoId });

  return (
    <section aria-label="Celular do associado" className="watson-celular">
      <p className="cds--type-label-01" style={{ marginBottom: '0.5rem' }}>App do associado · Valdir (simulado)</p>
      <div className="watson-celular__tela">
        <InlineNotification kind="info" lowContrast hideCloseButton title="Nunca pedimos senha ou código por telefone." />
        {tela === 'bloqueado' && (
          notificacoes.length === 0 ? (
            <p className="watson-celular__vazio">Nenhum aviso. A analista pode enviar um aviso de compra pelo caso.</p>
          ) : (
            notificacoes.map((n) => (
              <Tile key={n.titulo}>
                <p className="cds--type-heading-compact-01">{n.titulo}</p>
                <p style={{ margin: '0.5rem 0' }}>{n.corpo}</p>
                <Button size="lg" onClick={d('abrirAviso')}>Abrir aviso</Button>
              </Tile>
            ))
          )
        )}
        {tela === 'aviso' && (
          <>
            <h3 className="cds--type-heading-03">Aviso de compra no seu cartão final 4821</h3>
            <Tile>
              <p>R$ 2.349,90 · Loja Exemplo Eletrônicos</p>
              <p>São Paulo, SP · hoje, 03:14</p>
            </Tile>
            <p className="cds--type-heading-02">Foi você que comprou?</p>
            <Button kind="tertiary" size="xl" renderIcon={Checkmark} onClick={d('fuiEu')}>Sim, fui eu</Button>
            <Button kind="tertiary" size="xl" renderIcon={Close} onClick={d('naoReconheco')}>Não reconheço</Button>
            <Link href="#" aria-expanded={porque} onClick={(e) => { e.preventDefault(); setPorque((v) => !v); }}>Por que recebi este aviso?</Link>
            {porque && <p>Vimos uma compra diferente do seu costume. Confirmar ajuda a proteger seu cartão.</p>}
          </>
        )}
        {tela === 'biometria' && (
          <>
            <h3 className="cds--type-heading-03">Confirme com a digital do celular</h3>
            <p>Para compras de valor alto, pedimos a sua digital.</p>
            <Button size="xl" renderIcon={FingerprintRecognition} onClick={d('biometria')}>Usar digital (simulado)</Button>
          </>
        )}
        {tela === 'liberado' && <InlineNotification kind="success" hideCloseButton title="Compra liberada" subtitle="Obrigado, Valdir. Seu cartão continua funcionando." />}
        {tela === 'protegido' && <InlineNotification kind="success" hideCloseButton title="Cartão protegido" subtitle="Bloqueamos o cartão final 4821 e nada foi cobrado. Um cartão novo chega em até 7 dias úteis." />}
        {tela === 'conferindo' && <InlineNotification kind="info" hideCloseButton title="Recebemos sua resposta" subtitle="Por segurança, uma analista vai conferir a compra. Ela segue pausada e nada foi cobrado." />}
        <Link href="#" onClick={(e) => e.preventDefault()}>Prefiro falar com uma pessoa</Link>
      </div>
    </section>
  );
}
