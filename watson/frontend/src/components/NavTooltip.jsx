import { useEffect, useState } from 'react';

// Nome da seção ao passar o mouse (ou focar) num ícone do trilho da navegação lateral.
// Fica fora do SideNav e com posição fixa, porque a lista do trilho corta o que passa da largura dele.
export default function NavTooltip({ disabled }) {
  const [tip, setTip] = useState(null);

  useEffect(() => {
    const show = (e) => {
      const link = e.target.closest?.('.cds--side-nav__link');
      if (!link || disabled) return setTip(null);
      const r = link.getBoundingClientRect();
      setTip({ text: link.textContent.trim(), top: r.top + r.height / 2, left: r.right + 8 });
    };
    const hide = (e) => {
      const link = e.target.closest?.('.cds--side-nav__link');
      if (link && !link.contains(e.relatedTarget)) setTip(null);
    };
    document.addEventListener('mouseover', show);
    document.addEventListener('mouseout', hide);
    document.addEventListener('focusin', show);
    document.addEventListener('focusout', hide);
    return () => {
      document.removeEventListener('mouseover', show);
      document.removeEventListener('mouseout', hide);
      document.removeEventListener('focusin', show);
      document.removeEventListener('focusout', hide);
    };
  }, [disabled]);

  if (!tip || disabled) return null;
  return (
    <div className="watson-nav-tooltip" role="tooltip" style={{ top: tip.top, left: tip.left }}>
      {tip.text}
    </div>
  );
}
