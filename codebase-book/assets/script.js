/**
 * Tech Book — Intelligent Interaction System
 *
 * Auto-detects page structure and adapts all interactions accordingly.
 * Features: Smart TOC · Scroll progress · Code copy · Reveal animations
 *           Keyboard nav · Theme toggle · Back-to-top · Mobile sidebar
 */
(function () {
  'use strict';

  /* ── Structure Detection ──────────────────────────────────── */

  function detectStructure() {
    var container = document.querySelector('.chapter-content, .art, .chapter');
    if (!container) return { depth: 2, headings: [] };

    var all = container.querySelectorAll('h2, h3, h4, h5');
    var headings = [];
    var skipSelectors = '.sidebar, .dev-task, .debug-map, .change-impact, .practice, .card-bar, .sidebar-title, blockquote';

    all.forEach(function (h) {
      if (h.closest(skipSelectors)) return;
      var level = parseInt(h.tagName[1], 10);
      if (!h.id) h.id = 'h-' + headings.length;
      headings.push({ el: h, level: level, id: h.id, text: h.textContent.trim() });
    });

    var maxLevel = 2;
    headings.forEach(function (h) { if (h.level > maxLevel) maxLevel = h.level; });

    return { depth: maxLevel - 1, headings: headings };
  }

  var structure = detectStructure();

  /* ── Smart TOC Dropdown ───────────────────────────────────── */

  var tocBtn = document.querySelector('.toc-toggle');
  var tocDropdown = document.querySelector('.toc-dropdown');

  if (tocBtn && tocDropdown && structure.headings.length >= 2) {
    var minLevel = Math.min.apply(null, structure.headings.map(function (h) { return h.level; }));

    structure.headings.forEach(function (h) {
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.text;
      a.setAttribute('data-depth', h.level);

      a.addEventListener('click', function (e) {
        e.preventDefault();
        h.el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        closeToc();
      });

      tocDropdown.appendChild(a);
    });

    tocBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = tocDropdown.classList.toggle('open');
      tocBtn.classList.toggle('active', isOpen);
    });

    function closeToc() {
      tocDropdown.classList.remove('open');
      tocBtn.classList.remove('active');
    }

    document.addEventListener('click', function (e) {
      if (!tocBtn.contains(e.target) && !tocDropdown.contains(e.target)) closeToc();
    });

    // Active section tracking
    var tocLinks = tocDropdown.querySelectorAll('a');
    var ticking = false;

    function updateTocActive() {
      var scrollY = window.scrollY + 100;
      var activeIdx = -1;

      for (var i = 0; i < structure.headings.length; i++) {
        if (structure.headings[i].el.offsetTop <= scrollY) activeIdx = i;
      }

      tocLinks.forEach(function (a, i) {
        a.classList.toggle('active', i === activeIdx);
      });

      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(updateTocActive);
        ticking = true;
      }
    }, { passive: true });

    updateTocActive();
  } else if (tocBtn) {
    tocBtn.style.display = 'none';
  }

  /* ── Sidebar Active Link (global nav) ─────────────────────── */

  var sidebarLinks = document.querySelectorAll('.sb-link');
  if (sidebarLinks.length > 0) {
    var currentPath = window.location.pathname.split('/').pop() || 'index.html';

    sidebarLinks.forEach(function (link) {
      var href = link.getAttribute('href');
      if (href && (href === currentPath || href.endsWith('/' + currentPath))) {
        link.classList.add('active');
      }
    });
  }

  /* ── Reading Progress ─────────────────────────────────────── */

  var progBar = document.querySelector('.prog');
  if (progBar) {
    var progTicking = false;

    function updateProgress() {
      var scrollTop = window.scrollY;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      progBar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
      progTicking = false;
    }

    window.addEventListener('scroll', function () {
      if (!progTicking) {
        requestAnimationFrame(updateProgress);
        progTicking = true;
      }
    }, { passive: true });

    updateProgress();
  }

  /* ── Keyboard Navigation ──────────────────────────────────── */

  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;

    var prev = document.querySelector('.page-nav .prev, .pg-btn.prev');
    var next = document.querySelector('.page-nav .next, .pg-btn.next');

    if (e.key === 'ArrowLeft' && prev) { e.preventDefault(); prev.click(); }
    if (e.key === 'ArrowRight' && next) { e.preventDefault(); next.click(); }
  });

  /* ── Syntax Highlighting ──────────────────────────────────── */

  if (!window.hljs) {
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js';
    s.onload = function () { if (window.hljs) hljs.highlightAll(); };
    document.head.appendChild(s);
  }

  /* ── Mermaid Diagrams ─────────────────────────────────────── */

  var mermaidBlocks = document.querySelectorAll('pre.mermaid');
  if (mermaidBlocks.length > 0 && !window.mermaid) {
    var ms = document.createElement('script');
    ms.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
    ms.onload = function () {
      if (window.mermaid) {
        mermaid.initialize({
          startOnLoad: false,
          theme: document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark',
          securityLevel: 'loose'
        });
        mermaidBlocks.forEach(function (el, i) {
          var id = 'mermaid-' + i;
          var code = el.textContent;
          el.innerHTML = '';
          mermaid.render(id, code).then(function (result) {
            el.innerHTML = result.svg;
          }).catch(function () {
            el.innerHTML = '<code>' + code + '</code>';
          });
        });
      }
    };
    document.head.appendChild(ms);
  }

  /* ── Code Copy Buttons ────────────────────────────────────── */

  document.querySelectorAll('pre').forEach(function (pre) {
    if (pre.querySelector('.code-copy')) return;

    var btn = document.createElement('button');
    btn.className = 'code-copy';
    btn.textContent = '复制';
    btn.setAttribute('aria-label', '复制代码');

    btn.addEventListener('click', function () {
      var code = pre.querySelector('code');
      if (!code) return;

      navigator.clipboard.writeText(code.textContent).then(function () {
        btn.textContent = '已复制 ✓';
        btn.classList.add('copied');
        setTimeout(function () {
          btn.textContent = '复制';
          btn.classList.remove('copied');
        }, 2200);
      }).catch(function () {
        // Fallback for older browsers
        var range = document.createRange();
        range.selectNodeContents(code);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        try {
          document.execCommand('copy');
          btn.textContent = '已复制 ✓';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = '复制';
            btn.classList.remove('copied');
          }, 2200);
        } catch (err) { /* silent */ }
        sel.removeAllRanges();
      });
    });

    pre.style.position = 'relative';
    pre.appendChild(btn);
  });

  /* ── Back to Top ──────────────────────────────────────────── */

  var btt = document.querySelector('.btt');
  if (btt) {
    function updateBtt() {
      btt.classList.toggle('vis', window.scrollY > 500);
    }

    window.addEventListener('scroll', updateBtt, { passive: true });

    btt.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    updateBtt();
  }

  /* ── Scroll Reveal ────────────────────────────────────────── */

  if ('IntersectionObserver' in window) {
    var revealTargets = [
      'h2', 'h3', 'h4',
      'pre', 'table',
      '.card', '.sidebar',
      '.dev-task', '.debug-map', '.change-impact', '.practice',
      '.cheatsheet', '.chapter-summary',
      '.pic-frame', '.toc-list li',
      '.parsons-problem'
    ];

    var elements = document.querySelectorAll(revealTargets.join(', '));

    elements.forEach(function (el) {
      // Don't re-observe elements inside containers that will also animate
      if (el.closest('.toc-list li') && el.tagName !== 'LI') return;
      el.classList.add('reveal');
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -30px 0px'
    });

    elements.forEach(function (el) { observer.observe(el); });
  }

  /* ── Mobile Sidebar ───────────────────────────────────────── */

  var sidebar = document.querySelector('.sb');
  var hamburger = document.querySelector('.sb-hamburger');
  var overlay = document.querySelector('.sb-overlay');

  if (sidebar && hamburger && overlay) {
    function openSidebar() {
      sidebar.classList.add('open');
      overlay.classList.add('vis');
      document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
      sidebar.classList.remove('open');
      overlay.classList.remove('vis');
      document.body.style.overflow = '';
    }

    hamburger.addEventListener('click', openSidebar);
    overlay.addEventListener('click', closeSidebar);

    // Close on navigation link click (mobile)
    sidebar.querySelectorAll('.sb-link').forEach(function (link) {
      link.addEventListener('click', closeSidebar);
    });
  }

  /* ── Theme Toggle ─────────────────────────────────────────── */

  var themeBtn = document.querySelector('.sb-toggle');
  if (themeBtn) {
    function getPreferred() {
      try { return localStorage.getItem('theme'); } catch (e) { return null; }
    }

    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      themeBtn.textContent = theme === 'light' ? '🌙' : '☀️';
      themeBtn.setAttribute('aria-label', theme === 'light' ? '切换到暗色主题' : '切换到亮色主题');
      try { localStorage.setItem('theme', theme); } catch (e) { /* silent */ }
    }

    var saved = getPreferred();
    if (saved) {
      setTheme(saved);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
      setTheme('light');
    }

    themeBtn.addEventListener('click', function () {
      var current = document.documentElement.getAttribute('data-theme') || 'dark';
      setTheme(current === 'light' ? 'dark' : 'light');
    });
  }

  /* ── Auto-set data-lang on code blocks ────────────────────── */

  document.querySelectorAll('pre:not([data-lang])').forEach(function (pre) {
    var code = pre.querySelector('code');
    if (!code) return;

    // Detect from hljs class
    var cls = code.className || '';
    var match = cls.match(/language-(\w+)/);
    if (match) {
      pre.setAttribute('data-lang', match[1]);
    }
  });

  /* ── Smooth scroll for all anchor links ────────────────────── */

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;

    var target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });

  /* ══════════════════════════════════════════════════════════════
   *  NEW INTERACTIVE FEATURES
   * ══════════════════════════════════════════════════════════════ */

  /* ── 1. Search Modal (Ctrl+K) ─────────────────────────────── */

  (function () {
    var searchIndex = [];
    var modal = null;
    var input = null;
    var resultsContainer = null;
    var selectedIdx = -1;

    // Build search index from headings and code blocks
    function buildIndex() {
      var container = document.querySelector('.chapter-content, .art, .chapter');
      if (!container) return;

      var skipSelectors = '.sidebar, .card-bar, blockquote';

      // Index headings
      var headings = container.querySelectorAll('h2, h3, h4, h5');
      headings.forEach(function (h) {
        if (h.closest(skipSelectors)) return;
        if (!h.id) h.id = 'search-h-' + searchIndex.length;
        searchIndex.push({
          text: h.textContent.trim(),
          id: h.id,
          type: 'heading',
          preview: h.textContent.trim().substring(0, 120)
        });
      });

      // Index code blocks
      var codeBlocks = container.querySelectorAll('pre code');
      codeBlocks.forEach(function (code, i) {
        var pre = code.closest('pre');
        if (!pre) return;
        if (!pre.id) pre.id = 'search-code-' + i;
        var text = code.textContent.trim();
        if (text.length < 5) return;
        searchIndex.push({
          text: text.substring(0, 200),
          id: pre.id,
          type: 'code',
          preview: text.substring(0, 120)
        });
      });
    }

    function createModal() {
      modal = document.createElement('div');
      modal.className = 'search-modal';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-modal', 'true');
      modal.setAttribute('aria-label', '搜索');

      var backdrop = document.createElement('div');
      backdrop.className = 'search-modal__backdrop';

      var dialog = document.createElement('div');
      dialog.className = 'search-modal__dialog';

      input = document.createElement('input');
      input.type = 'text';
      input.className = 'search-modal__input';
      input.placeholder = '搜索标题和代码...';
      input.setAttribute('aria-label', '搜索');

      resultsContainer = document.createElement('div');
      resultsContainer.className = 'search-modal__results';

      dialog.appendChild(input);
      dialog.appendChild(resultsContainer);
      modal.appendChild(backdrop);
      modal.appendChild(dialog);
      document.body.appendChild(modal);

      backdrop.addEventListener('click', closeSearchModal);
      input.addEventListener('input', handleSearch);
      input.addEventListener('keydown', handleKeydown);
    }

    function openSearchModal() {
      if (!modal) createModal();
      modal.classList.add('open');
      input.value = '';
      resultsContainer.innerHTML = '';
      selectedIdx = -1;
      setTimeout(function () { input.focus(); }, 50);
    }

    function closeSearchModal() {
      if (modal) modal.classList.remove('open');
    }

    function handleSearch() {
      var query = input.value.trim().toLowerCase();
      resultsContainer.innerHTML = '';
      selectedIdx = -1;

      if (!query || query.length < 1) return;

      var results = [];
      for (var i = 0; i < searchIndex.length && results.length < 10; i++) {
        var item = searchIndex[i];
        if (item.text.toLowerCase().indexOf(query) !== -1) {
          results.push(item);
        }
      }

      if (results.length === 0) {
        var empty = document.createElement('div');
        empty.className = 'search-modal__empty';
        empty.textContent = '未找到匹配结果';
        resultsContainer.appendChild(empty);
        return;
      }

      results.forEach(function (item, idx) {
        var el = document.createElement('a');
        el.className = 'search-modal__result';
        el.href = '#' + item.id;
        el.setAttribute('data-index', idx);

        var typeSpan = document.createElement('span');
        typeSpan.className = 'search-modal__type';
        typeSpan.textContent = item.type === 'code' ? '代码' : '标题';

        var textSpan = document.createElement('span');
        textSpan.className = 'search-modal__text';
        textSpan.textContent = item.preview;

        el.appendChild(typeSpan);
        el.appendChild(textSpan);

        el.addEventListener('click', function (e) {
          e.preventDefault();
          var target = document.getElementById(item.id);
          if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          closeSearchModal();
        });

        resultsContainer.appendChild(el);
      });
    }

    function handleKeydown(e) {
      var items = resultsContainer.querySelectorAll('.search-modal__result');
      if (!items.length) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIdx = Math.min(selectedIdx + 1, items.length - 1);
        updateSelection(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIdx = Math.max(selectedIdx - 1, 0);
        updateSelection(items);
      } else if (e.key === 'Enter' && selectedIdx >= 0) {
        e.preventDefault();
        items[selectedIdx].click();
      } else if (e.key === 'Escape') {
        closeSearchModal();
      }
    }

    function updateSelection(items) {
      items.forEach(function (item, i) {
        item.classList.toggle('selected', i === selectedIdx);
      });
      if (selectedIdx >= 0 && items[selectedIdx]) {
        items[selectedIdx].scrollIntoView({ block: 'nearest' });
      }
    }

    // Global Ctrl+K handler
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openSearchModal();
      }
      if (e.key === 'Escape' && modal && modal.classList.contains('open')) {
        closeSearchModal();
      }
    });

    buildIndex();
  })();

  /* ── 2. On This Page Outline ──────────────────────────────── */

  (function () {
    if (window.innerWidth <= 1200) return;

    var container = document.querySelector('.chapter-content, .art, .chapter');
    if (!container) return;

    var skipSelectors = '.sidebar, .card-bar, blockquote, .dev-task, .practice';
    var headings = [];
    var allH = container.querySelectorAll('h2, h3');

    allH.forEach(function (h) {
      if (h.closest(skipSelectors)) return;
      if (!h.id) h.id = 'otp-h-' + headings.length;
      headings.push({ el: h, id: h.id, text: h.textContent.trim(), level: parseInt(h.tagName[1], 10) });
    });

    if (headings.length < 2) return;

    var nav = document.createElement('nav');
    nav.className = 'on-this-page';
    nav.setAttribute('aria-label', '本页目录');

    var title = document.createElement('div');
    title.className = 'on-this-page__title';
    title.textContent = '本页目录';
    nav.appendChild(title);

    var links = [];
    headings.forEach(function (h) {
      var a = document.createElement('a');
      a.className = 'on-this-page__link';
      a.href = '#' + h.id;
      a.textContent = h.text;
      a.setAttribute('data-level', h.level);
      a.addEventListener('click', function (e) {
        e.preventDefault();
        h.el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      nav.appendChild(a);
      links.push(a);
    });

    document.body.appendChild(nav);

    // Track active section via IntersectionObserver
    if ('IntersectionObserver' in window) {
      var activeLink = null;

      var outlineObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            if (activeLink) activeLink.classList.remove('active');
            var found = null;
            for (var i = 0; i < headings.length; i++) {
              if (headings[i].el === entry.target) {
                found = links[i];
                break;
              }
            }
            if (found) {
              found.classList.add('active');
              activeLink = found;
            }
          }
        });
      }, {
        rootMargin: '-80px 0px -60% 0px',
        threshold: 0
      });

      headings.forEach(function (h) { outlineObserver.observe(h.el); });
    }
  })();

  /* ── 3. Collapsible Sections ──────────────────────────────── */

  (function () {
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('.collapsible__trigger');
      if (!trigger) return;

      var collapsible = trigger.closest('.collapsible');
      if (!collapsible) return;

      var body = collapsible.querySelector('.collapsible__body');
      if (!body) return;

      var isOpen = collapsible.classList.contains('open');
      collapsible.classList.toggle('open');
      trigger.setAttribute('aria-expanded', isOpen ? 'false' : 'true');

      if (isOpen) {
        body.style.maxHeight = body.scrollHeight + 'px';
        // Force reflow then collapse
        body.offsetHeight; // eslint-disable-line no-unused-expressions
        body.style.maxHeight = '0px';
      } else {
        body.style.maxHeight = body.scrollHeight + 'px';
        // Remove max-height after transition to allow content changes
        var onEnd = function () {
          if (collapsible.classList.contains('open')) {
            body.style.maxHeight = 'none';
          }
          body.removeEventListener('transitionend', onEnd);
        };
        body.addEventListener('transitionend', onEnd);
      }
    });
  })();

  /* ── 4. Code Tabs ─────────────────────────────────────────── */

  (function () {
    document.addEventListener('click', function (e) {
      var tab = e.target.closest('.code-tabs__tab');
      if (!tab) return;

      var tabsContainer = tab.closest('.code-tabs');
      if (!tabsContainer) return;

      var allTabs = tabsContainer.querySelectorAll('.code-tabs__tab');
      var allPanels = tabsContainer.querySelectorAll('.code-tabs__panel');
      var clickedIdx = -1;

      allTabs.forEach(function (t, i) {
        t.classList.remove('active');
        if (t === tab) clickedIdx = i;
      });

      allPanels.forEach(function (p, i) {
        p.classList.remove('active');
        if (i === clickedIdx) p.classList.add('active');
      });

      tab.classList.add('active');
    });

    // Keyboard navigation for code tabs
    document.addEventListener('keydown', function (e) {
      var tab = e.target.closest('.code-tabs__tab');
      if (!tab) return;

      var tabsContainer = tab.closest('.code-tabs');
      if (!tabsContainer) return;

      var allTabs = tabsContainer.querySelectorAll('.code-tabs__tab');
      var currentIdx = -1;

      allTabs.forEach(function (t, i) {
        if (t === tab) currentIdx = i;
      });

      var newIdx = -1;
      if (e.key === 'ArrowRight') newIdx = (currentIdx + 1) % allTabs.length;
      if (e.key === 'ArrowLeft') newIdx = (currentIdx - 1 + allTabs.length) % allTabs.length;

      if (newIdx >= 0 && allTabs[newIdx]) {
        e.preventDefault();
        allTabs[newIdx].click();
        allTabs[newIdx].focus();
      }
    });
  })();

  /* ── 5. Quiz Validation ───────────────────────────────────── */

  (function () {
    document.addEventListener('click', function (e) {
      var answer = e.target.closest('.quiz__answer');
      if (!answer) return;

      var quiz = answer.closest('.quiz');
      if (!quiz) return;

      // Check if already answered
      if (quiz.getAttribute('data-answered') === 'true') return;
      quiz.setAttribute('data-answered', 'true');

      var isCorrect = answer.getAttribute('data-correct') === 'true';

      answer.setAttribute('data-state', 'selected');

      setTimeout(function () {
        answer.setAttribute('data-state', isCorrect ? 'correct' : 'wrong');

        // Show explanation if it exists
        var explain = quiz.querySelector('.quiz__explain');
        if (explain) explain.style.display = 'block';
      }, 400);

      // Disable all answers in this quiz
      var allAnswers = quiz.querySelectorAll('.quiz__answer');
      allAnswers.forEach(function (a) {
        a.style.pointerEvents = 'none';
      });
    });
  })();

  /* ── 6. File Tree ─────────────────────────────────────────── */

  (function () {
    document.addEventListener('click', function (e) {
      var dir = e.target.closest('.file-tree__dir');
      if (!dir) return;
      dir.classList.toggle('open');
    });
  })();

  /* ── 7. Exercise Reveal ───────────────────────────────────── */

  (function () {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.exercise__solution-btn');
      if (!btn) return;

      var exercise = btn.closest('.exercise');
      if (!exercise) return;

      var solution = exercise.querySelector('.exercise__solution');
      if (!solution) return;

      var isHidden = solution.style.display === 'none' || solution.style.display === '';
      solution.style.display = isHidden ? 'block' : 'none';
      btn.textContent = isHidden ? '隐藏答案' : '显示答案';
    });
  })();

  /* ── 8. Code Fill Validation ──────────────────────────────── */

  (function () {
    document.addEventListener('focusout', function (e) {
      validateCodeFill(e.target);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') validateCodeFill(e.target);
    });

    function validateCodeFill(el) {
      if (!el || !el.classList || !el.classList.contains('code-fill__blank')) return;

      var answer = (el.getAttribute('data-answer') || '').trim();
      var value = (el.value || '').trim();

      // Remove previous feedback
      el.classList.remove('correct', 'wrong');

      // Remove existing feedback element
      var existingFeedback = el.parentNode.querySelector('.code-fill__feedback');
      if (existingFeedback) existingFeedback.remove();

      if (!value) return;

      var isCorrect = value === answer;
      el.classList.add(isCorrect ? 'correct' : 'wrong');

      // Show inline feedback
      var feedback = document.createElement('span');
      feedback.className = 'code-fill__feedback';
      feedback.textContent = isCorrect ? ' ✓' : ' ✗';
      el.parentNode.insertBefore(feedback, el.nextSibling);
    }
  })();

  /* ── 9. Reading Time Calculation ──────────────────────────── */

  (function () {
    var container = document.querySelector('.chapter-content, .art');
    if (!container) return;

    var text = container.textContent || '';
    if (!text.trim()) return;

    // Detect if content is primarily Chinese
    var chineseChars = (text.match(/[一-鿿]/g) || []).length;
    var isChinese = chineseChars > text.length * 0.3;

    var minutes;
    if (isChinese) {
      // ~300 Chinese characters per minute
      minutes = Math.ceil(chineseChars / 300);
    } else {
      // ~250 English words per minute
      var words = text.trim().split(/\s+/).length;
      minutes = Math.ceil(words / 250);
    }

    if (minutes < 1) minutes = 1;

    var timeEl = document.createElement('div');
    timeEl.className = 'reading-time';
    timeEl.textContent = '预计阅读 ' + minutes + ' 分钟';

    var header = document.querySelector('.chapter-header');
    if (header) {
      header.insertBefore(timeEl, header.firstChild);
    } else {
      container.insertBefore(timeEl, container.firstChild);
    }
  })();

  /* ── 10. Chapter Progress (localStorage) ──────────────────── */

  (function () {
    var bookId = document.querySelector('[data-book-id]');
    bookId = bookId ? bookId.getAttribute('data-book-id') : null;
    if (!bookId) {
      // Try to derive book ID from URL
      var pathParts = window.location.pathname.split('/');
      if (pathParts.length >= 2) {
        bookId = pathParts[pathParts.length - 2] || pathParts[pathParts.length - 1];
      }
    }
    if (!bookId) return;

    var storageKey = 'techbook-progress-' + bookId;
    var currentPage = window.location.pathname.split('/').pop() || 'index.html';
    var progressData = {};

    try {
      var stored = localStorage.getItem(storageKey);
      if (stored) progressData = JSON.parse(stored);
    } catch (e) { /* silent */ }

    // Mark current page progress on scroll
    var progressMarked = false;
    var progScrollTicking = false;

    function checkProgress() {
      if (progressMarked) return;
      var scrollTop = window.scrollY;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight > 0 && (scrollTop / docHeight) >= 0.8) {
        progressMarked = true;
        progressData[currentPage] = true;
        try {
          localStorage.setItem(storageKey, JSON.stringify(progressData));
        } catch (e) { /* silent */ }
        updateSidebarProgress();
      }
      progScrollTicking = false;
    }

    window.addEventListener('scroll', function () {
      if (!progScrollTicking && !progressMarked) {
        requestAnimationFrame(checkProgress);
        progScrollTicking = true;
      }
    }, { passive: true });

    // Show visual indicator on sidebar links
    function updateSidebarProgress() {
      var sidebarLinksLocal = document.querySelectorAll('.sb-link');
      sidebarLinksLocal.forEach(function (link) {
        var href = link.getAttribute('href');
        if (href && progressData[href]) {
          link.classList.add('chapter-read');
        }
      });
    }

    updateSidebarProgress();
  })();

  /* ── 11. Keyboard Shortcuts Help ──────────────────────────── */

  (function () {
    var shortcutsOverlay = null;

    function createOverlay() {
      shortcutsOverlay = document.createElement('div');
      shortcutsOverlay.className = 'shortcuts-overlay';
      shortcutsOverlay.setAttribute('role', 'dialog');
      shortcutsOverlay.setAttribute('aria-modal', 'true');
      shortcutsOverlay.setAttribute('aria-label', '键盘快捷键');

      var backdrop = document.createElement('div');
      backdrop.className = 'shortcuts-overlay__backdrop';

      var dialog = document.createElement('div');
      dialog.className = 'shortcuts-overlay__dialog';

      var title = document.createElement('div');
      title.className = 'shortcuts-overlay__title';
      title.textContent = '键盘快捷键';
      dialog.appendChild(title);

      var shortcuts = [
        { keys: '← / →', desc: '上一页 / 下一页' },
        { keys: 'Ctrl + K', desc: '搜索' },
        { keys: '?', desc: '显示快捷键帮助' },
        { keys: 'Esc', desc: '关闭弹窗' }
      ];

      var list = document.createElement('div');
      list.className = 'shortcuts-overlay__list';

      shortcuts.forEach(function (s) {
        var row = document.createElement('div');
        row.className = 'shortcuts-overlay__row';

        var keysEl = document.createElement('kbd');
        keysEl.className = 'shortcuts-overlay__keys';
        keysEl.textContent = s.keys;

        var descEl = document.createElement('span');
        descEl.className = 'shortcuts-overlay__desc';
        descEl.textContent = s.desc;

        row.appendChild(keysEl);
        row.appendChild(descEl);
        list.appendChild(row);
      });

      dialog.appendChild(list);
      shortcutsOverlay.appendChild(backdrop);
      shortcutsOverlay.appendChild(dialog);
      document.body.appendChild(shortcutsOverlay);

      backdrop.addEventListener('click', closeOverlay);
    }

    function openOverlay() {
      if (!shortcutsOverlay) createOverlay();
      shortcutsOverlay.classList.add('open');
    }

    function closeOverlay() {
      if (shortcutsOverlay) shortcutsOverlay.classList.remove('open');
    }

    document.addEventListener('keydown', function (e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;

      if (e.key === '?' || (e.shiftKey && e.key === '/')) {
        if (shortcutsOverlay && shortcutsOverlay.classList.contains('open')) {
          closeOverlay();
        } else {
          openOverlay();
        }
      }
    });
  })();

  /* ── 12. KaTeX Loader ─────────────────────────────────────── */

  (function () {
    var mathBlocks = document.querySelectorAll('.math-block, .math-inline');
    if (mathBlocks.length === 0) return;

    function loadKaTeX() {
      // Load CSS
      var css = document.createElement('link');
      css.rel = 'stylesheet';
      css.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css';
      document.head.appendChild(css);

      // Load JS
      var script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js';
      script.onload = function () {
        if (!window.katex) return;

        mathBlocks.forEach(function (el) {
          var tex = el.textContent.trim();
          if (!tex) return;

          var isInline = el.classList.contains('math-inline');
          try {
            katex.render(tex, el, {
              displayMode: !isInline,
              throwOnError: false
            });
          } catch (err) {
            // Leave original text on error
          }
        });
      };
      document.head.appendChild(script);
    }

    loadKaTeX();
  })();

  /* ── 13. Mermaid Theme Sync ───────────────────────────────── */

  (function () {
    // Patch the existing theme toggle to re-render mermaid on theme change
    var themeToggleBtn = document.querySelector('.sb-toggle');
    if (!themeToggleBtn) return;

    // We observe data-theme attribute changes on <html>
    if (!('MutationObserver' in window)) return;

    var observerTarget = document.documentElement;
    var themeObserver = new MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        if (m.attributeName === 'data-theme') {
          rerenderMermaid();
        }
      });
    });

    themeObserver.observe(observerTarget, { attributes: true });

    function rerenderMermaid() {
      if (!window.mermaid) return;

      var theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark';
      var mermaidDiagrams = document.querySelectorAll('pre.mermaid');

      if (mermaidDiagrams.length === 0) return;

      mermaid.initialize({
        startOnLoad: false,
        theme: theme,
        securityLevel: 'loose'
      });

      mermaidDiagrams.forEach(function (el, i) {
        var id = 'mermaid-sync-' + i + '-' + Date.now();
        var code = el.getAttribute('data-mermaid-source') || el.textContent;

        // Store original source if not already stored
        if (!el.getAttribute('data-mermaid-source')) {
          el.setAttribute('data-mermaid-source', code);
        }

        mermaid.render(id, code).then(function (result) {
          el.innerHTML = result.svg;
        }).catch(function () {
          // Keep current content on error
        });
      });
    }
  })();

  /* ── 14. Learning Objectives Toggle ───────────────────────── */

  (function () {
    var objectiveItems = document.querySelectorAll('.learning-objectives__item');
    if (objectiveItems.length === 0) return;

    // Determine storage key
    var pageId = window.location.pathname;
    var storageKey = 'techbook-objectives-' + pageId;

    // Load saved state
    var savedState = {};
    try {
      var stored = localStorage.getItem(storageKey);
      if (stored) savedState = JSON.parse(stored);
    } catch (e) { /* silent */ }

    objectiveItems.forEach(function (item) {
      var idx = Array.prototype.indexOf.call(objectiveItems, item);
      var key = 'obj-' + idx;

      // Restore saved state
      if (savedState[key]) {
        item.classList.add('achieved');
      }

      item.addEventListener('click', function () {
        item.classList.toggle('achieved');
        savedState[key] = item.classList.contains('achieved');
        try {
          localStorage.setItem(storageKey, JSON.stringify(savedState));
        } catch (e) { /* silent */ }
      });

      item.style.cursor = 'pointer';
    });
  })();

  /* ── 15. Footnote Smooth Scroll ───────────────────────────── */

  (function () {
    document.addEventListener('click', function (e) {
      // Footnote reference click
      var fnRef = e.target.closest('.footnote-ref, a[href^="#fn"]');
      if (fnRef) {
        var href = fnRef.getAttribute('href');
        if (!href) return;
        var target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'center' });
          target.classList.add('footnote-highlight');
          setTimeout(function () {
            target.classList.remove('footnote-highlight');
          }, 2000);
        }
        return;
      }

      // Back-reference click
      var backRef = e.target.closest('.footnotes .backref, .footnotes a[href^="#fnref"], .footnotes__backref');
      if (backRef) {
        var backHref = backRef.getAttribute('href');
        if (!backHref) return;
        var backTarget = document.querySelector(backHref);
        if (backTarget) {
          e.preventDefault();
          backTarget.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }
    });
  })();

})();
