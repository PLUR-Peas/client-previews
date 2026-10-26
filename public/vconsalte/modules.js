/* Подложки и крестики используют одни и те же границы, а не независимые отступы. */
(() => {
  const targets = document.querySelectorAll('.industry-toggle, .case-card, .project-panel');
  const update = element => {
    const width = element.clientWidth;
    const height = element.clientHeight;
    if (!width || !height) return;
    const inset = 24;
    const scaleX = (width - inset * 2) / (5 * 63.4375);
    const scaleY = (height - inset * 2) / (8 * 62.685);
    element.style.setProperty('--module-bg-width', `${962.889 * scaleX}px`);
    element.style.setProperty('--module-bg-height', `${635.913 * scaleY}px`);
    element.style.setProperty('--module-bg-x', `${inset - 37.38275 * scaleX}px`);
    element.style.setProperty('--module-bg-y', `${inset - 4.90907 * scaleY}px`);
  };
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(entries => entries.forEach(entry => update(entry.target)));
    targets.forEach(element => observer.observe(element));
  } else window.addEventListener('resize', () => targets.forEach(update));
  targets.forEach(update);
})();
