/* Same-page printing avoids popup blockers and works with downloaded HTML. */
(() => {
  'use strict';
  const packs = [...document.querySelectorAll('[data-print-pack]')];
  if (!packs.length) return;
  const buttons = document.querySelectorAll('[data-print-chart]');
  const reset = () => packs.forEach(pack => pack.classList.remove('print-excluded'));
  buttons.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      const selected = button.dataset.printChart;
      reset();
      packs.forEach(pack => pack.classList.toggle('print-excluded', selected !== 'all' && pack.dataset.printPack !== selected));
      // Layout is already rendered. The print CSS selects only the requested sheets.
      try { window.print(); } catch (error) { reset(); throw error; }
    });
  });
  window.addEventListener('afterprint', reset);
  // Also reset on browsers that signal the print-media transition instead.
  window.matchMedia('print').addEventListener('change', event => { if (!event.matches) reset(); });
})();
