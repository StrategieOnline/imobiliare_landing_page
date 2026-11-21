import './css/viewing.css';
import { gsap, ScrollTrigger, MQ, splitChars } from './util.js';
import { RESIDENCES } from './residences.js';

const RULES = {
  name: (v) => (v.trim().length >= 2 ? '' : 'Spune-ne cum te numești.'),
  email: (v) => (!v.trim() ? 'Avem nevoie de o adresă de email.'
    : /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? '' : 'Adresa de email nu pare validă.'),
  phone: (v) => (!v.trim() ? 'Avem nevoie de un număr de telefon.'
    : /^\+?[\d\s().-]{9,}$/.test(v.trim()) && v.replace(/\D/g, '').length >= 9 ? '' : 'Numărul de telefon nu pare valid.'),
};

const field = (id, label, input, hint = '') => `
  <div class="field" data-field="${id}">
    <label class="field__label mono" for="f-${id}">${label}${hint ? ` <span>${hint}</span>` : ''}</label>
    ${input}
    <p class="field__err mono" id="f-${id}-err" aria-live="polite"></p>
  </div>`;

export function mountViewing(content) {
  const sec = document.createElement('section');
  sec.className = 'sec viewing';
  sec.id = 'vizionare';
  sec.setAttribute('aria-labelledby', 'vizionare-h');
  sec.innerHTML = `
    <p class="sec-label mono">05 / VIZITĂ</p>
    <h2 class="display viewing__h" id="vizionare-h">
      <span class="viewing__l1">HAI SĂ NE</span>
      <em class="viewing__l2">vedem acolo.</em>
    </h2>
    <div class="viewing__grid">
      <div class="viewing__info">
        <p class="viewing__body">Programează o vizită în showroom-ul de pe șantier. Îți arătăm planurile, materialele reale și apartamentele încă disponibile.</p>
        <dl class="contact mono">
          <div><dt>SHOWROOM</dt><dd>Șoseaua Nordului 12, București</dd></div>
          <div><dt>PROGRAM</dt><dd>LUN–SÂM · 10:00–19:00</dd></div>
          <div><dt>TELEFON</dt><dd>+40 21 000 0000</dd></div>
          <div><dt>EMAIL</dt><dd>vizionari@orizont.example</dd></div>
        </dl>
      </div>
      <div class="viewing__formwrap">
        <form class="vform" novalidate>
          ${field('name', 'Nume', '<input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-err">')}
          ${field('email', 'Email', '<input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="f-email-err">')}
          ${field('phone', 'Telefon', '<input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="f-phone-err">')}
          ${field('type', 'Tip rezidență', `<div class="field__select"><select id="f-type" name="type">
              ${RESIDENCES.map((r) => `<option value="${r.key}">${r.option}</option>`).join('')}
              <option value="" selected>Încă nu știu</option>
            </select></div>`)}
          ${field('msg', 'Mesaj', '<textarea id="f-msg" name="msg" rows="3"></textarea>', '(opțional)')}
          <button class="pill vform__submit" type="submit"><span>TRIMITE CEREREA</span><span aria-hidden="true">→</span></button>
          <p class="vform__legal mono">Datele tale sunt folosite doar pentru a stabili vizita.</p>
        </form>
        <div class="vdone" hidden tabindex="-1">
          <p class="mono vdone__k">CERERE PRIMITĂ</p>
          <p class="vdone__h display">MULȚUMIM, <em class="vdone__name"></em></p>
          <p class="vdone__t">Un consultant te sună în cel mult o zi lucrătoare ca să stabilim ora vizitei.</p>
          <button class="pill pill--ghost vdone__again" type="button">TRIMITE O ALTĂ CERERE</button>
        </div>
      </div>
    </div>`;
  content.append(sec);

  smear(sec);
  wireForm(sec);
}

/** Letters start stretched (scaleY ~2.2), blurred and pushed off, then settle with a stagger, scrubbed. */
function smear(sec) {
  const chars = [sec.querySelector('.viewing__l1'), sec.querySelector('.viewing__l2')].flatMap(splitChars);
  gsap.matchMedia().add(MQ.motion, () => {
    gsap.fromTo(chars, {
      scaleY: 2.2, scaleX: 0.86, yPercent: -28, opacity: 0, filter: 'blur(14px)',
      x: () => gsap.utils.random(-18, 18),
    }, {
      scaleY: 1, scaleX: 1, yPercent: 0, x: 0, opacity: 1, filter: 'blur(0px)',
      ease: 'power2.out', stagger: { each: 0.035, from: 'start' },
      scrollTrigger: { trigger: sec.querySelector('.viewing__h'), start: 'top 92%', end: 'top 34%', scrub: 0.7 },
    });
  });
}

function wireForm(sec) {
  const form = sec.querySelector('.vform');
  const done = sec.querySelector('.vdone');
  const select = form.querySelector('#f-type');

  const check = (name) => {
    const input = form.elements[name];
    const msg = RULES[name](input.value);
    const wrap = input.closest('.field');
    wrap.classList.toggle('is-invalid', !!msg);
    input.setAttribute('aria-invalid', String(!!msg));
    wrap.querySelector('.field__err').textContent = msg;
    return !msg;
  };

  Object.keys(RULES).forEach((name) => {
    const input = form.elements[name];
    input.addEventListener('blur', () => { if (input.value) check(name); });
    input.addEventListener('input', () => { if (input.closest('.field').classList.contains('is-invalid')) check(name); });
  });
  form.querySelectorAll('input, select, textarea').forEach((el) => {
    const sync = () => el.closest('.field').classList.toggle('is-filled', !!el.value);
    el.addEventListener('input', sync);
    el.addEventListener('change', sync);
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const bad = Object.keys(RULES).filter((n) => !check(n));
    if (bad.length) { form.elements[bad[0]].focus(); return; }
    done.querySelector('.vdone__name').textContent = `${form.elements.name.value.trim().split(/\s+/)[0]}.`;
    form.hidden = true;
    done.hidden = false;
    done.focus({ preventScroll: true });
    ScrollTrigger.refresh();   // the page got shorter; the footer wordmark range depends on it
    gsap.from(done.children, { y: 24, opacity: 0, duration: .8, ease: 'power3.out', stagger: .08 });
  });

  sec.querySelector('.vdone__again').addEventListener('click', () => {
    form.reset();
    form.querySelectorAll('.field').forEach((f) => f.classList.remove('is-filled', 'is-invalid'));
    done.hidden = true;
    form.hidden = false;
    ScrollTrigger.refresh();
    form.elements.name.focus();
  });

  // Clicking a residence row preselects it here.
  document.addEventListener('orizont:residence', (e) => {
    select.value = e.detail;
    select.closest('.field').classList.add('is-filled');
  });
}
