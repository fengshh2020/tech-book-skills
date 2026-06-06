// 顶部下拉章节目录
(function() {
  var btn = document.querySelector('.toc-toggle');
  var dropdown = document.querySelector('.toc-dropdown');
  if (!btn || !dropdown) return;

  var content = document.querySelector('.chapter-content');
  if (!content) return;

  var allH = content.querySelectorAll('h2');
  var headings = [];
  allH.forEach(function(h) {
    if (!h.closest('.sidebar')) headings.push(h);
  });

  if (headings.length < 2) { btn.style.display = 'none'; return; }

  headings.forEach(function(h, i) {
    var id = 'sect-' + i;
    h.id = id;
    var a = document.createElement('a');
    a.href = '#' + id;
    a.textContent = h.textContent;
    a.addEventListener('click', function(e) {
      e.preventDefault();
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      closeDropdown();
    });
    dropdown.appendChild(a);
  });

  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    var open = dropdown.classList.toggle('open');
    btn.classList.toggle('active', open);
  });

  function closeDropdown() {
    dropdown.classList.remove('open');
    btn.classList.remove('active');
  }

  document.addEventListener('click', function(e) {
    if (!btn.contains(e.target) && !dropdown.contains(e.target)) closeDropdown();
  });

  var links = dropdown.querySelectorAll('a');
  function onScroll() {
    var scrollY = window.scrollY + 120;
    var active = -1;
    headings.forEach(function(h, i) { if (h.offsetTop <= scrollY) active = i; });
    links.forEach(function(a, i) {
      if (i === active) a.classList.add('active');
      else a.classList.remove('active');
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// 键盘翻页
(function() {
  document.addEventListener('keydown', function(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    var prev = document.querySelector('.page-nav .prev');
    var next = document.querySelector('.page-nav .next');
    if (e.key === 'ArrowLeft' && prev) prev.click();
    if (e.key === 'ArrowRight' && next) next.click();
  });
})();

// 语法高亮（highlight.js — 自动检测语言，通用）
(function() {
  var s = document.createElement('script');
  s.src = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js';
  s.onload = function() {
    hljs.highlightAll();
  };
  document.head.appendChild(s);
})();
