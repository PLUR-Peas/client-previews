/* Тексты согласованы пользователем 26.10.2026. */
const icons = {
  building: '<path d="M7 55V22h13M20 55V8h23v47M43 20h13v35M4 55h55M26 16h3m6 0h3m-12 9h3m6 0h3m-12 9h3m6 0h3M12 30h3m-3 9h3m34-10h2m-2 9h2M29 55V44h7v11"/>',
  megaphone: '<path d="M10 25h12L49 9v44L22 38H10V25Zm12 0v13m-8 0 3 17h8l-3-17M55 19l5-3m-5 15h7m-7 12 5 3"/>',
  cube: '<path d="m32 5 25 14v28L32 61 7 47V19L32 5Zm0 28v28M7 19l25 14 25-14"/>',
  chart: '<path d="M5 56h56M10 56V39h10v17m7 0V26h10v30m7 0V10h10v46"/>',
  rook: '<path d="M17 6h7v10h5V6h7v10h5V6h7v20H17V6Zm2 20h27m-24 0-3 20h27l-3-20M19 46l-6 8v5h39v-5l-6-8M13 54h39"/>',
  gear: '<path d="m26 5 12 0 1 8 6 3 7-4 7 10-6 5v8l6 5-7 10-7-4-6 3-1 9H26l-1-9-7-3-7 4-6-10 6-5v-8l-6-5 6-10 7 4 7-3 1-8Z"/><circle cx="32" cy="31" r="11"/>',
  television: '<path d="M7 18h50v32H7V18Zm13-11 12 11L43 7M32 50v9m-12 0h24"/>',
  bulb: '<path d="M23 44c0-7-9-10-9-22a18 18 0 0 1 36 0c0 12-9 15-9 22H23Zm0 6h18m-15 6h12m-10-12V29m8 15V29m-12-4 8 4 8-4"/>'
};
function svgIcon(name) {
  return `<svg class="icon" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square" stroke-linejoin="miter">${icons[name]}<rect x="1" y="39" width="5" height="5" fill="#927bff" stroke="#fff" stroke-width="1"/></svg>`;
}
const industries = [
  { id:'development', name:'Девелопмент', icon:'building', description:'Федеральные девелоперы и городские жилищные программы: бренд, маркетинг, сквозная аналитика, план продаж.', cases:[
    {title:'Городская жилищная программа', task:'создать и вывести на рынок бренд застройщика государственного уровня, выстроить маркетинг с нуля, разработать и внедрить бизнес-процессы.', work:'разработали бренд и стратегию продвижения, сформировали департамент, связали сайт, CRM и аналитику, запустили online витрину.', result:'бренд запущен. Посещаемость сайта выросла в 2,25 раза: с 68,5 тыс. пользователей в месяц в июле 2025 до 154 тыс. в мае 2026. План продаж выполнен.', metric:'×2,25', caption:'рост посещаемости сайта', icon:'chart'},
    {title:'Федеральный девелопер', task:'снизить долю рекламных расходов и обеспечить выполнение плана продаж.', work:'провели аудит стратегии и рекламы, оптимизировали продвижение и внедрили сквозную аналитику.', result:'снизили долю рекламных расходов до 2,2% от плана продаж. План продаж выполнен.', metric:'2,2%', caption:'рекламных расходов от плана продаж', icon:'rook'},
    {title:'Девелопер столичного региона', task:'усилить бренд и обеспечить вывод жилых проектов на конкурентный рынок.', work:'разработали коммуникационную и креативную стратегии, организовали исследования и рекламную поддержку проектов.', result:'за три года вывели на рынок семь жилых проектов.', metric:'7', caption:'жилых проектов за 3 года', icon:'gear'}
  ]},
  { id:'media', name:'Медиа', icon:'megaphone', description:'Стратегический, тактический маркетинг, медиапланирование и бюджетирование, аналитика, аудит, оптимизация.', cases:[
    {title:'Медиахолдинг', task:'повысить эффективность рекламных кампаний развлекательных телеканалов.', work:'выстроили стратегическое и тактическое продвижение шести телеканалов, медиапланирование и контроль кампаний.', result:'эффективность рекламных кампаний выросла на 20% в 2021 году относительно 2020 года.', metric:'20%', caption:'рост эффективности рекламных кампаний (2021 к 2020)', icon:'television'}
  ]},
  { id:'city', name:'Городские структуры', icon:'cube', description:'Запуск брендов, маркетинговая функция с нуля, KPI и BI-отчётность.', cases:[
    {title:'Городские программы поддержки бизнеса', task:'запустить продвижение инновационных проектов и увеличить количество заявок.', work:'с нуля организовали digital- и offline-продвижение, внедрили маркетинговую аналитику и отчётность.', result:'запущена система продвижения программ поддержки бизнеса и учёта заявок.', metric:'+60', caption:'заявок к 2019 году', icon:'bulb'}
  ]}
];

// Typographic spacing for visible copy; wording stays in the source data above.
function typograph(text) {
  return text
    .replace(/(^|[\s(«])(а|и|в|во|к|ко|с|со|у|о|об|от|до|по|из|за|на|не|ни|но|для|при|без|над|под|про) /giu, '$1$2\u00a0')
    .replace(/(\d) ?%/gu, '$1\u00a0%')
    .replace(/(\d) (тыс\.|млн|млрд|раза|раз|года|году|год|лет)(?=[\s.,:;!?)]|$)/gu, '$1\u00a0$2')
    .replace(/([A-Za-zА-Яа-яЁё])-(?=[A-Za-zА-Яа-яЁё])/gu, '$1\u2011')
    .replace(/ (—|–) /gu, '\u00a0— ')
    .replace(/ (?=[^\s]+$)/u, '\u00a0');
}

// Exact default card from Figma 258:39; case content remains independent.
function industryIcon(industry) {
  const dimensions = {development:[151.295,151.41],media:[180,145.042],city:[181.667,150]};
  const [width,height] = dimensions[industry.id];
  return `<img class="figma-industry-icon figma-${industry.id}-icon" src="assets/figma/card-258/${industry.id === 'city' ? 'city-284-176' : industry.id}.svg" width="${width}" height="${height}" alt="">`;
}
function industryCopy(industry) {
  const description = industry.id === 'development'
    ? 'Федеральные девелоперы и городские жилищные программы бренд, маркетинг, сквозная аналитика.'
    : industry.description;
  return `<span class="industry-copy-text"><span class="industry-name">${typograph(industry.name.toUpperCase())}: </span><span class="industry-description">${typograph(description)}</span></span>`;
}

const root = document.getElementById('industries');
root.innerHTML = industries.map((industry, index) => `
  <div class="card-slot" data-position="${index}">
    <div class="card-rotor">
      <button class="industry-toggle" id="toggle-${industry.id}" aria-expanded="false" aria-controls="${index === 0 ? 'case-position-0 case-position-1 case-position-2' : `case-position-${index}`}" type="button" data-industry="${index}">
        <span class="industry-visual">${industryIcon(industry)}</span>
        <span class="industry-copy">${industryCopy(industry)}</span>
      </button>
      <article class="case-card" id="case-position-${index}" inert aria-hidden="true"></article>
    </div>
  </div>`).join('');
const slots = [...root.querySelectorAll('.card-slot')];
let activeIndustry = null;
let transitionRevision = 0;
const flipAnimations = new WeakMap();
const flipAngles = new WeakMap();
function caseMarkup(project, index) {
  return `<button class="case-back" type="button" aria-label="Вернуться к отраслям из проекта ${project.title}">К отраслям</button>
    <div class="case-surface"><div class="case-body">
    <h3 class="case-title" id="case-heading-${index}">${typograph(project.title)}</h3>
    <div class="case-text"><p><strong>ЗАДАЧА:</strong> ${typograph(project.task)}</p><p><strong>РЕШЕНИЕ:</strong> ${typograph(project.work)}</p><p><strong>РЕЗУЛЬТАТ:</strong> ${typograph(project.result)}</p></div></div>
    ${project.metric ? `<div class="case-metric${project.caption.length > 30 ? ' case-metric--wide' : ''}"><span class="metric-value">${project.metric}</span><span class="metric-caption">${typograph(project.caption).replace(/ (\([^)]*\))$/, ' <span class="metric-caption-period">$1</span>')}</span></div>` : ''}</div>`;
}
function fitCaseCopy(back) {
  const body = back.querySelector('.case-body');
  const metric = back.querySelector('.case-metric');
  if (!body || !metric || back.hidden) return;
  back.style.setProperty('--case-copy-scale', '1');
  for (let step = 0; step < 8; step++) {
    if (body.offsetTop + body.offsetHeight + 8 <= metric.offsetTop) break;
    back.style.setProperty('--case-copy-scale', String(1 - (step + 1) * .025));
  }
}
if ('ResizeObserver' in window) {
  const caseObserver = new ResizeObserver(entries => entries.forEach(entry => fitCaseCopy(entry.target)));
  root.querySelectorAll('.case-card').forEach(card => caseObserver.observe(card));
}
document.fonts?.ready.then(() => root.querySelectorAll('.case-card').forEach(fitCaseCopy));
async function flipSlot(slot, project, index) {
  const rotor = slot.querySelector('.card-rotor');
  const front = slot.querySelector('.industry-toggle');
  const back = slot.querySelector('.case-card');
  // Both faces exist throughout the turn. Only the shared 3D rotor moves.
  const previousAnimation = flipAnimations.get(rotor);
  const progress = previousAnimation?.animation.effect.getComputedTiming().progress ?? 0;
  const fromAngle = previousAnimation
    ? previousAnimation.fromAngle + (previousAnimation.toAngle - previousAnimation.fromAngle) * progress
    : (flipAngles.get(rotor) ?? 0);
  previousAnimation?.animation.cancel();
  if (project && back.dataset.project !== project.title) {
    back.innerHTML = caseMarkup(project, index);
    back.dataset.project = project.title;
    back.setAttribute('aria-labelledby', `case-heading-${index}`);
  }
  const open = Boolean(project);
  front.inert = open;
  front.setAttribute('aria-hidden', String(open));
  front.setAttribute('aria-expanded', String(open));
  back.inert = !open;
  back.setAttribute('aria-hidden', String(!open));
  slot.classList.toggle('is-case', open);
  if (project) fitCaseCopy(back);
  const mobile = matchMedia('(max-width:1000px)').matches;
  const faceAngle = open ? 180 : 0;
  // Keep unwrapped angles: mobile always turns forward, including on return.
  const toAngle = mobile
    ? faceAngle + Math.ceil((fromAngle - faceAngle - .001) / 360) * 360
    : faceAngle;
  const to = `rotateY(${toAngle}deg)`;
  flipAngles.set(rotor, toAngle);
  rotor.style.transform = to;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  rotor.style.willChange = 'transform';
  const animation = rotor.animate([{transform:`rotateY(${fromAngle}deg)`},{transform:to}], {
    duration:640,easing:'cubic-bezier(.4,0,.2,1)',fill:'none'
  });
  flipAnimations.set(rotor, {animation, fromAngle, toAngle});
  try { await animation.finished; }
  catch (error) { if (error.name !== 'AbortError') throw error; }
  finally {
    if (flipAnimations.get(rotor)?.animation === animation) {
      flipAnimations.delete(rotor);
      rotor.style.willChange = '';
      animation.cancel();
    }
  }
}
async function changeIndustry(index) {
  if (activeIndustry === index) return;
  const revision = ++transitionRevision;
  root.setAttribute('aria-busy','true');
  const previous = activeIndustry;
  activeIndustry = index;
  root.classList.toggle('is-development', index === 0);
  try {
    await Promise.all(slots.map((slot, position) => {
      const project = index === null ? null : index === 0 ? industries[0].cases[position] : position === index ? industries[index].cases[0] : null;
      const alreadyCase = slot.classList.contains('is-case');
      if (!project && !alreadyCase) return;
      return flipSlot(slot,project,position);
    }));
    if (revision !== transitionRevision) return;
    const focusTarget = index === null ? slots[previous ?? 0].querySelector('.industry-toggle') : slots[index === 0 ? 0 : index].querySelector('.case-back');
    focusTarget?.focus({preventScroll:true});
    if (focusTarget && focusTarget.getBoundingClientRect().top < 0) focusTarget.scrollIntoView({block:'start',behavior:'instant'});
  } finally { if (revision === transitionRevision) root.removeAttribute('aria-busy'); }
}
root.addEventListener('click', event => {
  const toggle = event.target.closest('.industry-toggle');
  if (toggle) changeIndustry(Number(toggle.dataset.industry));
  else if (event.target.closest('.case-back') || (event.target.closest('.case-card') && !window.getSelection()?.toString())) changeIndustry(null);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && activeIndustry !== null) { event.preventDefault(); changeIndustry(null); }
});
