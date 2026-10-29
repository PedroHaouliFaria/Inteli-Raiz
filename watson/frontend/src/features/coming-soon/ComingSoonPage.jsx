import { useParams, Link as RouterLink } from 'react-router-dom';
import { InlineNotification } from '@carbon/react';

export const FUTURE_SECTIONS = {
  'closed-cases': 'Casos encerrados',
  members: 'Associados',
  'model-monitoring': 'Monitoramento do modelo',
  reports: 'Relatórios',
};

// Itens da navegação lateral do mockup 3 que ainda não têm tela no protótipo.
export default function ComingSoonPage() {
  const { section } = useParams();
  const title = FUTURE_SECTIONS[section] ?? 'Página';
  return (
    <main className="watson-main" id="main-content">
      <h1 className="cds--type-heading-04">{title}</h1>
      <InlineNotification kind="info" lowContrast hideCloseButton title="Tela prevista, ainda não construída."
        subtitle="Ela aparece na navegação lateral do mockup escolhido e entra numa próxima etapa." />
      <p className="cds--type-body-01"><RouterLink to="/">Voltar para a fila</RouterLink></p>
    </main>
  );
}
