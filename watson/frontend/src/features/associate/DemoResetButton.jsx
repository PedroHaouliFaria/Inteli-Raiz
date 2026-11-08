/**
 * DemoResetButton — botão "Recomeçar demonstração" exibido no cabeçalho.
 *
 * Aparece somente quando session.demo_mode === true (§9 do contrato).
 * Abre um Modal Carbon (danger) pedindo confirmação antes de chamar
 * POST /api/demo/reset. Após o reset, chama onReset() para que o pai
 * recarregue a lista e o detalhe aberto.
 */
import { useState } from 'react';
import {
  Button,
  HeaderGlobalAction,
  InlineNotification,
  Modal,
} from '@carbon/react';
import { Restart } from '@carbon/icons-react';
import { ApiError, resetDemo } from '../../api/client.js';

export default function DemoResetButton({ onReset, variant = 'header' }) {
  const [open, setOpen] = useState(false);
  const [resetting, setResetting] = useState(false);
  const [resetError, setResetError] = useState(null);

  const handleOpen = () => {
    setResetError(null);
    setOpen(true);
  };

  const handleClose = () => {
    if (!resetting) setOpen(false);
  };

  const handleConfirm = async () => {
    setResetting(true);
    setResetError(null);
    try {
      await resetDemo();
      setOpen(false);
      onReset?.();
    } catch (err) {
      setResetError(err instanceof ApiError ? err.message : 'Erro de rede. Tente novamente.');
    } finally {
      setResetting(false);
    }
  };

  return (
    <>
      {variant === 'button' ? (
        <Button kind="ghost" size="sm" renderIcon={Restart} onClick={handleOpen}>
          Restaurar dados da demonstração
        </Button>
      ) : (
        <HeaderGlobalAction
          aria-label="Recomeçar demonstração"
          onClick={handleOpen}
          tooltipAlignment="end"
        >
          <Restart size={20} />
        </HeaderGlobalAction>
      )}

      <Modal
        open={open}
        danger
        modalHeading="Recomeçar demonstração"
        primaryButtonText={resetting ? 'Aguarde…' : 'Continuar'}
        secondaryButtonText="Cancelar"
        primaryButtonDisabled={resetting}
        onRequestClose={handleClose}
        onRequestSubmit={handleConfirm}
        onSecondarySubmit={handleClose}
      >
        <p>
          Isso apaga respostas, conversas, decisões e revisões da base fictícia
          compartilhada e restaura todas as compras iniciais com prazo novo. A mudança
          afeta Ana, Bruno e a fila da analista. Continuar?
        </p>
        {resetError && (
          <div style={{ marginTop: '1rem' }}>
            <InlineNotification
              kind="error"
              title="Erro ao recomeçar"
              subtitle={resetError}
              hideCloseButton
              lowContrast
            />
          </div>
        )}
      </Modal>
    </>
  );
}
