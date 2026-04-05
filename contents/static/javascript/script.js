/* AI Imager — Frontend Script */

/* ── Mobile nav ───────────────────────────────── */
function openMobileNav() {
  document.getElementById('mobileOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMobileNav() {
  document.getElementById('mobileOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

/* ── File upload label update ─────────────────── */
function updateFilename(input, labelId) {
  const el = document.getElementById(labelId);
  if (!el) return;
  if (input.files && input.files[0]) {
    el.textContent = input.files[0].name;
    el.classList.add('visible');
  } else {
    el.textContent = '';
    el.classList.remove('visible');
  }
}

/* ── Form submission ──────────────────────────── */
async function submitForm(relativeApiLink) {
  const apiUrl   = window.location.origin + relativeApiLink;
  const form     = document.getElementById('gen-form');
  const btn      = document.getElementById('gen-btn');
  const loader   = document.getElementById('loader');
  const errorBox = document.getElementById('error-box');
  const errorMsg = document.getElementById('error-msg');
  const label    = document.getElementById('results-label');
  const grid     = document.getElementById('results-grid');

  /* Reset state */
  errorBox.classList.remove('visible');
  label.classList.remove('visible');
  grid.innerHTML = '';
  loader.classList.add('visible');
  btn.disabled = true;
  btn.querySelector('svg').style.animation = 'spin 1s linear infinite';

  const formData = new FormData(form);

  try {
    const res = await fetch(apiUrl, { method: 'POST', body: formData });
    const data = await res.json();
    loader.classList.remove('visible');

    if (data.error) {
      errorMsg.innerHTML = data.error;
      errorBox.classList.add('visible');
    } else if (data.url && data.url.length > 0) {
      label.classList.add('visible');
      grid.innerHTML = data.url.map(url => buildImageCard(url)).join('');
    } else {
      errorMsg.textContent = 'No images were returned. Please try again.';
      errorBox.classList.add('visible');
    }
  } catch (err) {
    loader.classList.remove('visible');
    errorMsg.textContent = 'Network error. Please check your connection and try again.';
    errorBox.classList.add('visible');
  } finally {
    btn.disabled = false;
    btn.querySelector('svg').style.animation = '';
  }
}

function buildImageCard(url) {
  return `
    <div class="result-img-wrap">
      <img src="${escapeHtml(url)}" alt="Generated image" loading="lazy" onerror="this.closest('.result-img-wrap').style.display='none'">
      <div class="result-img-actions">
        <a href="${escapeHtml(url)}" target="_blank" class="img-action-btn view">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M1 6.5A5.5 5.5 0 1 0 12 6.5 5.5 5.5 0 0 0 1 6.5zm3.5 0a2 2 0 1 1 4 0 2 2 0 0 1-4 0" fill="currentColor"/></svg>
          View
        </a>
        <a href="${escapeHtml(url)}" download="ai-image.jpg" class="img-action-btn download" onclick="downloadImage(event, '${escapeHtml(url)}')">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1v8M3 6.5l3.5 3.5L10 6.5M1 12h11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Save
        </a>
      </div>
    </div>`;
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

async function downloadImage(e, url) {
  e.preventDefault();
  try {
    const res = await fetch(url);
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'ai-image-' + Date.now() + '.jpg';
    a.click();
    URL.revokeObjectURL(a.href);
  } catch {
    window.open(url, '_blank');
  }
}

/* ── Docs tab switcher ────────────────────────── */
function switchTab(group, tab) {
  const panels = document.querySelectorAll(`[id^="${group}-"]`);
  panels.forEach(p => p.classList.add('hidden'));

  const active = document.getElementById(`${group}-${tab}`);
  if (active) active.classList.remove('hidden');

  const tabGroup = active ? active.closest('.docs-section') || document : document;
  const buttons = tabGroup.querySelectorAll(`.tabs[data-tab-group="${group}"] .tab-btn`);
  buttons.forEach((btn, i) => {
    const labels = ['curl','python','js'];
    btn.classList.toggle('active', labels[i] === tab);
  });
}

/* ── Docs sidebar active link on scroll ──────── */
(function initDocsSidebar() {
  const links = document.querySelectorAll('.sidebar-link[href^="#"]');
  if (!links.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const link = document.querySelector(`.sidebar-link[href="#${entry.target.id}"]`);
        if (link) link.classList.add('active');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  document.querySelectorAll('.docs-section[id]').forEach(s => observer.observe(s));
})();

/* ── Highlight active nav link ────────────────── */
(function() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
})();
