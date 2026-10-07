// hero-modern.js
// Two small, self-contained behaviours:
//  1. Scroll-reveal: any element with [data-reveal] fades/rises into view once.
//  2. Stat counters: elements with [data-count] count up from 0 when revealed.
// Both respect prefers-reduced-motion by skipping straight to the end state.

(function () {
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-count').replace(/[^\d.]/g, ''));
    if (isNaN(target)) return;
    if (prefersReduced) { el.textContent = el.getAttribute('data-count'); return; }

    var suffix = el.getAttribute('data-count').replace(/[\d.,]/g, '');
    var duration = 1200;
    var start = null;

    function step(ts) {
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var value = Math.round(target * eased);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function init() {
    var revealEls = document.querySelectorAll('[data-reveal]');
    var countEls = document.querySelectorAll('[data-count]');

    if (!('IntersectionObserver' in window) || prefersReduced) {
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
      countEls.forEach(animateCount);
      return;
    }

    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });

    revealEls.forEach(function (el, i) {
      el.style.setProperty('--i', i % 6);
      revealObserver.observe(el);
    });

    var countObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });

    countEls.forEach(function (el) { countObserver.observe(el); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();