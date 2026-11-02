// B案：動き（GSAP + ScrollTrigger、Swiper）。メニュー・フォーム・スタッフ動画は main.js
{
const root = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------- ヘッダー：ヒーローの上では透明、下にスクロールで隠れ、上に戻すと出る ----------
const bh = document.querySelector('.bh');
const hero = document.querySelector('.bhero');
let lastY = scrollY;
function onScroll() {
  const y = scrollY;
  if (hero) bh.classList.toggle('is-over', y < hero.querySelector('.bhero-photo').offsetTop - bh.offsetHeight);
  if (!document.body.classList.contains('menu-open')) bh.classList.toggle('is-hidden', y > lastY && y > 400);
  lastY = y;
}
addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ---------- スマホメニュー ----------
const menuBtn = document.querySelector('.bh-menu');
if (menuBtn) {
  menuBtn.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    menuBtn.setAttribute('aria-expanded', open);
    bh.classList.remove('is-hidden');
  });
  document.querySelectorAll('.bm a').forEach((a) => a.addEventListener('click', () => document.body.classList.remove('menu-open')));
}

// ---------- 動画モーダル ----------
const modal = document.querySelector('.b-modal');
if (modal) {
  const video = modal.querySelector('video');
  document.querySelectorAll('[data-movie]').forEach((btn) => btn.addEventListener('click', () => {
    video.src = btn.dataset.movie;
    modal.showModal();
    video.play().catch(() => {});
  }));
  modal.querySelector('.b-modal-close').addEventListener('click', () => modal.close());
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.close(); });
  modal.addEventListener('close', () => { video.pause(); video.removeAttribute('src'); video.load(); });
}

// ---------- お知らせの絞り込み ----------
document.querySelectorAll('.b-tabs button').forEach((btn, _, all) => btn.addEventListener('click', () => {
  all.forEach((b) => b.setAttribute('aria-pressed', b === btn));
  const cat = btn.dataset.cat;
  document.querySelectorAll('.b-news-list li').forEach((li) => { li.hidden = cat !== 'all' && li.dataset.cat !== cat; });
}));

// ---------- トピックバナー：ゆっくり流れ続け、指でスワイプもできる ----------
if (window.Swiper && document.querySelector('.b-topics')) {
  new Swiper('.b-topics', {
    slidesPerView: 'auto', spaceBetween: 16, loop: true, grabCursor: true,
    speed: reduce ? 500 : 7000,
    autoplay: reduce ? false : { delay: 0, disableOnInteraction: false, pauseOnMouseEnter: true },
    freeMode: { enabled: true, momentum: true },
    breakpoints: { 861: { spaceBetween: 28 } },
  });
}

// ---------- 文字を1文字ずつ span に分ける ----------
function splitChars(el) {
  const text = el.textContent;
  el.setAttribute('aria-label', text);
  el.innerHTML = [...text].map((c) => `<span class="ch" aria-hidden="true">${c === ' ' ? '&nbsp;' : c}</span>`).join('');
  return el.querySelectorAll('.ch');
}

// ---------- GSAP ----------
if (!window.gsap || !window.ScrollTrigger || reduce) {
  root.classList.remove('anim');
  document.querySelector('.b-open')?.remove();
} else {
  gsap.registerPlugin(ScrollTrigger);
  const tl = gsap.timeline();
  const mmHero = gsap.matchMedia();

  // オープニング（トップ・セッション中1回だけ）
  const open = document.querySelector('.b-open');
  if (open) {
    if (sessionStorage.getItem('akari-b-opened')) {
      open.remove();
    } else {
      sessionStorage.setItem('akari-b-opened', '1');
      tl.to(open.querySelector('img'), { opacity: 1, y: 0, duration: .6, ease: 'power2.out' })
        .to(open.querySelector('i'), { width: 160, duration: .7, ease: 'power3.inOut' }, '-=.2')
        .to(open, { clipPath: 'inset(0 0 100% 0)', duration: .9, ease: 'power4.inOut' }, '+=.15')
        .add(() => open.remove());
    }
  }

  // ヒーロー：文字が下からせり上がり、写真が続いて浮かび上がる
  if (hero) {
    tl.set('.bhero-title', { opacity: 1 }, open ? '-=.5' : 0)
      .from('.bhero-title .ch', { yPercent: 115, rotate: 6, duration: 1.2, ease: 'power4.out', stagger: .05 }, '<')
      .fromTo('.bhero [data-hero]:not(.bhero-title)', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.1, ease: 'power3.out', stagger: .14 }, '-=.9');
    // スクロールで写真が画面いっぱいに広がる
    const photo = { trigger: '.bhero-media', start: 'top 80%', end: 'top 10%', scrub: true };
    mmHero.add('(min-width: 861px)', () => {
      gsap.fromTo('.bhero-media', { clipPath: 'inset(0% 7% 0% 7% round 28px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'none', scrollTrigger: photo });
    });
    mmHero.add('(max-width: 860px)', () => {
      gsap.fromTo('.bhero-media', { clipPath: 'inset(0% 4% 0% 4% round 18px)' }, { clipPath: 'inset(0% 0% 0% 0% round 0px)', ease: 'none', scrollTrigger: photo });
    });
    gsap.fromTo('.bhero-media img', { scale: 1.18 }, { scale: 1, ease: 'none', scrollTrigger: { ...photo, end: 'bottom top' } });
  }

  // 大きな英字見出し：1文字ずつ下から
  document.querySelectorAll('[data-split]').forEach((el) => {
    const chars = splitChars(el);
    gsap.from(chars, { yPercent: 100, opacity: 0, duration: 1, ease: 'power4.out', stagger: .04,
      scrollTrigger: { trigger: el, start: 'top 88%' } });
  });

  // ふわっと出る / 子要素を順番に / 写真が窓から広がる
  document.querySelectorAll('[data-anim]').forEach((el) => {
    const type = el.dataset.anim;
    const st = { trigger: el, start: 'top 86%' };
    if (type === 'stagger') {
      gsap.set(el, { opacity: 1 });
      gsap.from(el.children, { opacity: 0, y: 50, duration: 1, ease: 'power3.out', stagger: .14, scrollTrigger: st });
    } else if (type === 'clip') {
      gsap.set(el, { opacity: 1 });
      gsap.fromTo(el, { clipPath: 'inset(16% 16% 16% 16%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.4, ease: 'power4.out', scrollTrigger: st });
      const img = el.querySelector('img');
      if (img) gsap.from(img, { scale: 1.35, duration: 1.8, ease: 'power3.out', scrollTrigger: st });
    } else {
      gsap.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: st });
    }
  });

  // 数字のカウントアップ
  document.querySelectorAll('[data-count]').forEach((el) => {
    const end = Number(el.dataset.count);
    const obj = { v: 0 };
    gsap.to(obj, { v: end, duration: 2, ease: 'power2.out', scrollTrigger: { trigger: el, start: 'top 85%' },
      onUpdate: () => { el.textContent = Math.round(obj.v); } });
  });

  // 想い：スクロールに合わせて文字が順に灯る
  const about = document.querySelector('.b-about-text');
  if (about) {
    gsap.to(about.querySelectorAll('.ch'), { color: '#ffffff', stagger: .1, ease: 'none',
      scrollTrigger: { trigger: about, start: 'top 78%', end: 'bottom 50%', scrub: true } });
    gsap.fromTo('.b-about-glow', { yPercent: -20, scale: .8 }, { yPercent: 30, scale: 1.15, ease: 'none',
      scrollTrigger: { trigger: '.b-about', start: 'top bottom', end: 'bottom top', scrub: true } });
  }

  // 写真がスクロールより少し遅れて動く
  document.querySelectorAll('[data-parallax] img').forEach((img) => {
    gsap.fromTo(img, { yPercent: -12 }, { yPercent: 0, ease: 'none',
      scrollTrigger: { trigger: img.closest('[data-parallax]'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  // 業務案内：PCは縦スクロールで横に進む
  const mm = gsap.matchMedia();
  mm.add('(min-width: 861px)', () => {
    const track = document.querySelector('.b-svc-track');
    if (!track) return;
    const bar = document.querySelector('.b-svc-progress i');
    const dist = () => track.scrollWidth - innerWidth;
    gsap.to(track, { x: () => -dist(), ease: 'none',
      scrollTrigger: { trigger: '.b-svc', start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 1, invalidateOnRefresh: true,
        onUpdate: (self) => { if (bar) bar.style.transform = `scaleX(${self.progress})`; } } });
  });
  mm.add('(max-width: 860px)', () => {
    gsap.utils.toArray('.b-svc-card').forEach((card) => {
      gsap.from(card, { opacity: 0, y: 60, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: card, start: 'top 90%' } });
    });
  });

  // 下層ページ：見出しが1文字ずつ、写真が広がる
  const pageH1 = document.querySelector('.page-hero h1');
  if (pageH1) {
    const chars = splitChars(pageH1);
    gsap.from(chars, { yPercent: 60, opacity: 0, duration: .9, ease: 'power3.out', stagger: .04 });
    gsap.from('.page-hero p, .breadcrumb', { opacity: 0, y: 16, duration: .9, delay: .3, ease: 'power2.out' });
  }
  document.querySelectorAll('.lead-figure, .sub-figure').forEach((fig) => {
    const st = { trigger: fig, start: 'top 88%' };
    gsap.fromTo(fig, { clipPath: 'inset(12% 12% 12% 12%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.3, ease: 'power4.out', scrollTrigger: st });
    gsap.from(fig.querySelector('img'), { scale: 1.25, duration: 1.6, ease: 'power3.out', scrollTrigger: st });
  });

  addEventListener('load', () => ScrollTrigger.refresh());
}
}
