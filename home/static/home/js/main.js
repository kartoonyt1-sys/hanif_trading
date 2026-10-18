// ===== Hanif Aimaq - Final Mobile Fixed Version =====
(function() {
  "use strict";

  // Wait for DOM
  function init() {
    
    /* ---- 1. Mobile nav toggle - FIXED ---- */
    var hamburger = document.getElementById("hamburgerBtn");
    var nav = document.getElementById("mainNav");
    if (hamburger && nav) {
      hamburger.addEventListener("click", function(e) {
        e.stopPropagation();
        nav.classList.toggle("open");
        nav.classList.toggle("active"); // پشتیبانی هر دو کلاس
        hamburger.classList.toggle("active");
      });
      
      // بستن منو با کلیک بیرون
      document.addEventListener("click", function(e) {
        if (!nav.contains(e.target) && !hamburger.contains(e.target)) {
          nav.classList.remove("open", "active");
          hamburger.classList.remove("active");
        }
      });
      
      // بستن منو با کلیک روی لینک
      nav.querySelectorAll("a").forEach(function(link) {
        link.addEventListener("click", function() {
          nav.classList.remove("open", "active");
          hamburger.classList.remove("active");
        });
      });
    }

    /* ---- 2. Scroll reveal - unified ---- */
    var revealEls = document.querySelectorAll(".reveal, [data-reveal]");
    var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    
    if (!prefersReduced && "IntersectionObserver" in window) {
      var revealObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view", "is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
      
      revealEls.forEach(function(el, i) {
        el.style.setProperty("--i", i % 6);
        revealObserver.observe(el);
      });
    } else {
      revealEls.forEach(function(el) {
        el.classList.add("in-view", "is-visible");
      });
    }

    /* ---- 3. Animated stat counters - single version ---- */
    var statNumbers = document.querySelectorAll(".stat-number, [data-count]");
    if (statNumbers.length > 0 && !prefersReduced) {
      var countObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            var raw = el.getAttribute("data-count") || el.textContent;
            var match = raw.match(/(\d+)(.*)/);
            if (!match) return;
            
            var target = parseInt(match[1], 10);
            var suffix = match[2] || "";
            var current = 0;
            var step = Math.max(1, Math.ceil(target / 40));
            
            var interval = setInterval(function() {
              current += step;
              if (current >= target) {
                current = target;
                clearInterval(interval);
              }
              el.textContent = current + suffix;
            }, 30);
            
            countObserver.unobserve(el);
          }
        });
      }, { threshold: 0.5 });
      
      statNumbers.forEach(function(el) {
        countObserver.observe(el);
      });
    }

    /* ---- 4. Header shadow on scroll ---- */
    var header = document.getElementById("siteHeader");
    if (header) {
      var ticking = false;
      window.addEventListener("scroll", function() {
        if (!ticking) {
          window.requestAnimationFrame(function() {
            if (window.scrollY > 40) {
              header.style.boxShadow = "0 8px 20px rgba(0,0,0,0.35)";
            } else {
              header.style.boxShadow = "none";
            }
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });
    }
  }

  // Run
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
