document.addEventListener("DOMContentLoaded", function () {
  /* ---- Scroll reveal ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  }

  /* ---- Mobile nav toggle ---- */
  var hamburger = document.getElementById("hamburgerBtn");
  var nav = document.getElementById("mainNav");
  if (hamburger && nav) {
    hamburger.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
  }

  /* ---- Animated stat counters ---- */
  var statNumbers = document.querySelectorAll(".stat-number");
  statNumbers.forEach(function (el) {
    var raw = el.getAttribute("data-count") || el.textContent;
    var match = raw.match(/(\d+)(\D*)/);
    if (!match) return;
    var target = parseInt(match[1], 10);
    var suffix = match[2] || "";
    var started = false;

    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !started) {
            started = true;
            var current = 0;
            var step = Math.max(1, Math.ceil(target / 40));
            var interval = setInterval(function () {
              current += step;
              if (current >= target) {
                current = target;
                clearInterval(interval);
              }
              el.textContent = current + suffix;
            }, 30);
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );
    counterObserver.observe(el);
  });

  /* ---- Header shrink-on-scroll ---- */
  var header = document.getElementById("siteHeader");
  if (header) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 40) {
        header.style.boxShadow = "0 8px 20px rgba(0,0,0,0.35)";
      } else {
        header.style.boxShadow = "none";
      }
    });
  }
});
