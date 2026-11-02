// メニュー開閉
const menuBtn = document.querySelector('.menu-btn');
if (menuBtn) {
  menuBtn.addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    menuBtn.setAttribute('aria-expanded', open);
  });
}

// スクロールでふわっと表示
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// お問い合わせフォーム（デモのため送信しない）
const form = document.querySelector('#contact-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    form.hidden = true;
    document.querySelector('.form-done').classList.add('show');
    window.scrollTo({ top: document.querySelector('.form-done').offsetTop - 120 });
  });
}

// スタッフ紹介：写真の位置で動画を再生
document.querySelectorAll('.staff-media').forEach((box) => {
  box.querySelector('.play-btn').addEventListener('click', () => {
    document.querySelectorAll('.staff-media video').forEach((v) => v.pause());
    const video = document.createElement('video');
    Object.assign(video, { src: box.dataset.video, poster: box.dataset.poster, controls: true, autoplay: true, playsInline: true });
    box.replaceChildren(video);
  });
});
