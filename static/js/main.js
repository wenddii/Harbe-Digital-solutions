/* ═══════════════════════════════════════════════════════════════════
   HARBE DIGITAL SOLUTIONS — Frontend Engine
   Scroll reveals, navbar, FAQ accordion, micro-interactions,
   hero parallax, particle canvas, card tilt, stat counters
   ═══════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initScrollReveal();
  initFAQAccordion();
  initSmoothAnchors();
  initAutoHideMessages();
  initAtmosphere();
  initHeroParallax();
  initParticleCanvas();
  initCardTilt();
  initStatCounter();
});


/* ─── Navbar scroll behaviour ─── */
function initNavbar() {
  const nav = document.querySelector('.nav');
  const toggle = document.querySelector('.nav__toggle');
  const links = document.querySelector('.nav__links');
  if (!nav) return;

  // Scroll → compact
  const onScroll = () => {
    if (window.scrollY > 60) {
      nav.classList.add('is-scrolled');
    } else {
      nav.classList.remove('is-scrolled');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // initial state

  // Mobile toggle
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = !links.classList.contains('is-open');
      toggle.classList.toggle('is-open', isOpen);
      links.classList.toggle('is-open', isOpen);
      nav.classList.toggle('is-menu-open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close on link click
    links.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        toggle.classList.remove('is-open');
        links.classList.remove('is-open');
        nav.classList.remove('is-menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }
}


/* ─── Scroll-triggered reveal ─── */
function initScrollReveal() {
  const targets = document.querySelectorAll('.reveal');
  if (!targets.length) return;

  // Respect prefers-reduced-motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    targets.forEach(el => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // only once
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  targets.forEach(el => observer.observe(el));
}


/* ─── FAQ Accordion ─── */
function initFAQAccordion() {
  const items = document.querySelectorAll('.faq-item');
  items.forEach(item => {
    const btn = item.querySelector('.faq-item__question');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const wasOpen = item.classList.contains('is-open');
      // Close all
      items.forEach(i => i.classList.remove('is-open'));
      // Toggle current
      if (!wasOpen) item.classList.add('is-open');
    });
  });
}


/* ─── Smooth scroll for anchor links ─── */
function initSmoothAnchors() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}


/* ─── Auto-hide Django messages after 5 seconds ─── */
function initAutoHideMessages() {
  const messages = document.querySelector('.messages');
  if (!messages) return;
  setTimeout(() => {
    messages.style.transition = 'opacity 0.5s ease';
    messages.style.opacity = '0';
    setTimeout(() => messages.remove(), 500);
  }, 5000);
}

/* ─── Quiet movement for the shared digital atmosphere ─── */
function initAtmosphere() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const root = document.documentElement;
  let frame = null;
  let pointerX = 0;
  let pointerY = 0;

  const update = () => {
    root.style.setProperty('--pointer-x', `${pointerX * 0.35}px`);
    root.style.setProperty('--pointer-y', `${pointerY * 0.35}px`);
    root.style.setProperty('--scroll-depth', `${Math.min(window.scrollY * 0.025, 18)}px`);
    frame = null;
  };

  window.addEventListener('pointermove', event => {
    pointerX = (event.clientX / window.innerWidth - 0.5) * 24;
    pointerY = (event.clientY / window.innerHeight - 0.5) * 24;
    if (!frame) frame = requestAnimationFrame(update);
  }, { passive: true });

  window.addEventListener('scroll', () => {
    if (!frame) frame = requestAnimationFrame(update);
  }, { passive: true });
}


/* ═══════════════════════════════════════════════════════════════════
   NEW — Hero Parallax (Mouse-driven)
   ═══════════════════════════════════════════════════════════════════ */
function initHeroParallax() {
  const hero = document.querySelector('.hero');
  if (!hero) return;

  // Disable on mobile / touch / reduced-motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (window.matchMedia('(hover: none)').matches) return;
  if (window.innerWidth < 768) return;

  const title = hero.querySelector('.hero__title');
  const subtitle = hero.querySelector('.hero__subtitle');

  let targetX = 0;
  let targetY = 0;
  let currentX = 0;
  let currentY = 0;
  let rafId = null;

  function lerp(start, end, factor) {
    return start + (end - start) * factor;
  }

  function updateParallax() {
    currentX = lerp(currentX, targetX, 0.06);
    currentY = lerp(currentY, targetY, 0.06);

    // Background shifts opposite to cursor (max ~15px)
    hero.style.backgroundPosition =
      `calc(50% + ${-currentX * 0.6}px) calc(30% + ${-currentY * 0.4}px)`;

    // Title shifts slightly with cursor
    if (title) {
      title.style.transform = `translate(${currentX * 0.15}px, ${currentY * 0.1}px)`;
    }

    // Subtitle subtle shift
    if (subtitle) {
      subtitle.style.transform = `translate(${currentX * 0.08}px, ${currentY * 0.05}px)`;
    }

    rafId = requestAnimationFrame(updateParallax);
  }

  hero.addEventListener('mousemove', (e) => {
    const rect = hero.getBoundingClientRect();
    targetX = ((e.clientX - rect.left) / rect.width - 0.5) * 24;
    targetY = ((e.clientY - rect.top) / rect.height - 0.5) * 24;
  }, { passive: true });

  hero.addEventListener('mouseleave', () => {
    targetX = 0;
    targetY = 0;
  }, { passive: true });

  // Only run animation loop while hero is in viewport
  const heroObserver = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      if (!rafId) rafId = requestAnimationFrame(updateParallax);
    } else {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    }
  }, { threshold: 0 });

  heroObserver.observe(hero);
}


/* ═══════════════════════════════════════════════════════════════════
   NEW — Particle Canvas (Lightweight glowing particles)
   ═══════════════════════════════════════════════════════════════════ */
function initParticleCanvas() {
  const canvas = document.getElementById('hero-particles');
  if (!canvas) return;

  // Disable for reduced-motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    canvas.style.display = 'none';
    return;
  }

  const ctx = canvas.getContext('2d');
  let animationId = null;
  const isMobile = window.innerWidth < 768;
  const PARTICLE_COUNT = isMobile ? 12 : 35;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
  }
  resize();

  // Debounced resize
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 200);
  }, { passive: true });

  // Create particles
  const particles = [];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: 1.2 + Math.random() * 2.5,
      speedX: (Math.random() - 0.5) * 0.3,
      speedY: (Math.random() - 0.5) * 0.25,
      opacity: 0.15 + Math.random() * 0.35,
      hue: Math.random() > 0.7 ? 35 : 38, // warm golden tones
    });
  }

  function drawParticle(p) {
    const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius * 3);
    gradient.addColorStop(0, `hsla(${p.hue}, 52%, 44%, ${p.opacity})`);
    gradient.addColorStop(1, `hsla(${p.hue}, 52%, 44%, 0)`);
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius * 3, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const p of particles) {
      p.x += p.speedX;
      p.y += p.speedY;

      // Wrap around edges
      if (p.x < -10) p.x = canvas.width + 10;
      if (p.x > canvas.width + 10) p.x = -10;
      if (p.y < -10) p.y = canvas.height + 10;
      if (p.y > canvas.height + 10) p.y = -10;

      drawParticle(p);
    }

    animationId = requestAnimationFrame(animate);
  }

  // Only animate while hero is in viewport
  const canvasObserver = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      if (!animationId) animationId = requestAnimationFrame(animate);
    } else {
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
      }
    }
  }, { threshold: 0 });

  canvasObserver.observe(canvas);
}


/* ═══════════════════════════════════════════════════════════════════
   NEW — Card 3D Tilt on Hover
   ═══════════════════════════════════════════════════════════════════ */
function initCardTilt() {
  // Disable on touch / reduced-motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (window.matchMedia('(hover: none)').matches) return;

  const cards = document.querySelectorAll(
    '.service-card, .project-card, .why-card, .pillar-card'
  );
  if (!cards.length) return;

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;  // -0.5 to 0.5
      const y = (e.clientY - rect.top) / rect.height - 0.5;

      const rotateY = x * 5;   // max ±2.5°
      const rotateX = -y * 5;  // max ±2.5°

      card.style.transform =
        `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px) scale(1.015)`;
    }, { passive: true });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    }, { passive: true });
  });
}


/* ═══════════════════════════════════════════════════════════════════
   NEW — Animated Stat Counter
   ═══════════════════════════════════════════════════════════════════ */
function initStatCounter() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  function animateCount(el) {
    const target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;

    const duration = 2000;
    const startTime = performance.now();

    function tick(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value = Math.round(easeOutQuart(progress) * target);
      el.textContent = value;

      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    }

    requestAnimationFrame(tick);
  }

  // Reduced motion: show final values immediately
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    counters.forEach(el => {
      el.textContent = el.getAttribute('data-count');
    });
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.5
  });

  counters.forEach(el => observer.observe(el));
}
