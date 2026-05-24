import './style.css';
import { BusRouter } from './routing.js';
import { BusMap } from './map.js';

const router = new BusRouter();
const map = new BusMap('map-container');

// Elements
const elFrom = document.getElementById('from-input');
const elTo = document.getElementById('to-input');
const elAcFrom = document.getElementById('from-autocomplete');
const elAcTo = document.getElementById('to-autocomplete');
const btnSwap = document.getElementById('swap-btn');
const btnSearch = document.getElementById('search-btn');
const btnLocate = document.getElementById('locate-me');
const elResults = document.getElementById('results-container');
const elStats = document.getElementById('route-stats');
const elMapNote = document.getElementById('map-note');

// Theme Elements
const html = document.documentElement;
const btnThemeToggle = document.getElementById('theme-toggle');

/* --- Initialization --- */
async function init() {
  const loaded = await router.loadData();
  if (!loaded) {
    elResults.innerHTML = `<div class="empty-state"><h3>Error loading data</h3><p>Please check your connection and refresh.</p></div>`;
    return;
  }
  
  setupAutocomplete(elFrom, elAcFrom);
  setupAutocomplete(elTo, elAcTo);
  
  // Populate dataset stats
  document.getElementById('meta-routes').textContent = router.routes.length;
  document.getElementById('meta-stops').textContent = router.stops.length;
  
  // Randomly select theme: Bus or Taxi
  const randomTheme = Math.random() > 0.5 ? 'bus' : 'taxi';
  setTheme(randomTheme);

  // Load saved dark/light mode preference
  const savedMode = localStorage.getItem('busbabu-mode') || 'light';
  setMode(savedMode);

  // Hide splash screen after a small delay to ensure smooth transition
  setTimeout(() => {
    const splash = document.getElementById('splash-screen');
    if (splash) splash.classList.add('hidden');
  }, 800);
}

/* --- Theming --- */
function setTheme(theme) {
  html.setAttribute('data-theme', theme);
}

function setMode(mode) {
  html.setAttribute('data-mode', mode);
  localStorage.setItem('busbabu-mode', mode);
}

btnThemeToggle.addEventListener('click', () => {
  const currentMode = html.getAttribute('data-mode');
  setMode(currentMode === 'light' ? 'dark' : 'light');
});

/* --- UI Logic --- */
btnSwap.addEventListener('click', () => {
  const t = elFrom.value;
  elFrom.value = elTo.value;
  elTo.value = t;
  // If both have values, auto search
  if(elFrom.value && elTo.value) doSearch();
});

btnLocate.addEventListener('click', () => {
  if (!navigator.geolocation) return alert('Geolocation not supported');
  
  btnLocate.style.opacity = '0.5';
  navigator.geolocation.getCurrentPosition(
    pos => {
      btnLocate.style.opacity = '1';
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;
      
      // Find nearest stop
      let nearest = null;
      let minDist = Infinity;
      
      for (const [stop, [slat, slng]] of Object.entries(router.coords)) {
        // Simple euclidean approx (good enough for local city scale)
        const d = Math.pow(lat - slat, 2) + Math.pow(lng - slng, 2);
        if (d < minDist) {
          minDist = d;
          nearest = stop;
        }
      }
      
      if (nearest) {
        elFrom.value = nearest;
        if(elTo.value) doSearch();
      }
    },
    err => {
      btnLocate.style.opacity = '1';
      alert('Could not get your location.');
    }
  );
});

btnSearch.addEventListener('click', doSearch);

/* --- Autocomplete --- */
const esc = v => String(v).replace(/[&<>"']/g, ch => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[ch]));

function setupAutocomplete(input, box) {
  let hi = -1, items = [];
  
  function close() { 
    box.classList.add('hidden'); 
    hi = -1; 
  }
  
  function render(q) {
    q = q.toLowerCase().trim();
    items = q ? router.stopNames.filter(s => s.toLowerCase().includes(q)).slice(0, 20)
              : router.stopNames.slice(0, 20);
              
    if (!items.length) { close(); return; }
    
    box.innerHTML = items.map(s => {
      const n = router.stopRoutes[s] ? router.stopRoutes[s].length : 0;
      return `<div class="ac-item" data-v="${esc(s)}">
                <span class="ac-name">${esc(s)}</span>
                <span class="ac-meta">${n} route${n !== 1 ? 's' : ''}</span>
              </div>`;
    }).join('');
    
    box.classList.remove('hidden');
    hi = -1;
    
    box.querySelectorAll('.ac-item').forEach(d => {
      d.onmousedown = e => { 
        e.preventDefault(); 
        input.value = d.dataset.v; 
        close(); 
      };
    });
  }
  
  input.addEventListener('input', () => render(input.value));
  input.addEventListener('focus', () => render(input.value));
  input.addEventListener('blur', () => setTimeout(close, 150));
  
  input.addEventListener('keydown', e => {
    const ds = box.querySelectorAll('.ac-item');
    if (e.key === 'ArrowDown') { hi = Math.min(hi + 1, ds.length - 1); }
    else if (e.key === 'ArrowUp') { hi = Math.max(hi - 1, 0); }
    else if (e.key === 'Enter') { 
      if (hi >= 0 && ds[hi]) { 
        input.value = ds[hi].dataset.v; 
        close(); 
        e.preventDefault(); 
      } else { 
        close(); 
        doSearch(); 
      } 
      return; 
    }
    else if (e.key === 'Escape') { close(); return; }
    else return;
    
    ds.forEach((d, i) => d.classList.toggle('highlight', i === hi));
    if (ds[hi]) ds[hi].scrollIntoView({ block: 'nearest' });
    e.preventDefault();
  });
}

/* --- Search & Render --- */
function doSearch() {
  const o = elFrom.value.trim();
  const d = elTo.value.trim();
  
  if (!o || !d) return;
  if (!router.stopRoutes[o] || !router.stopRoutes[d]) {
    elResults.innerHTML = `<div class="empty-state">
      <div class="empty-icon">⚠️</div>
      <h3>Stop not found</h3>
      <p>Please select valid stands from the dropdown.</p>
    </div>`;
    elStats.classList.add('hidden');
    return;
  }
  
  const res = router.find(o, d);
  renderResults(res);
  
  // Plot first direct route or first 1-change route if direct not available
  map.init();
  let stats;
  if (res.direct.length) {
    stats = map.plotJourney(res.direct[0], router.coords);
  } else if (res.one.length) {
    stats = map.plotJourney(res.one[0], router.coords);
  } else if (res.two.length) {
    stats = map.plotJourney(res.two[0], router.coords);
  }
  
  if (stats) {
    if (stats.missing > 0) {
      elMapNote.innerHTML = `⚠️ Plotted ${stats.plotted} stops &mdash; ${stats.missing} stops are missing map coordinates.`;
      elMapNote.style.color = '#b45309';
    } else {
      elMapNote.textContent = 'Showing quickest route on map';
      elMapNote.style.color = '';
    }
  }
}

function renderResults(res) {
  let htmlStr = '';
  let count = 0;
  
  const renderGroup = (title, items, groupClass) => {
    if (!items.length) return '';
    count += items.length;
    let groupHtml = `<div class="route-group">
      <div class="group-title ${groupClass}">${title} <small>(${items.length})</small></div>`;
      
    items.forEach((j, idx) => {
      const legs = j.legs;
      const buses = legs.map((l, i) => 
        `<span class="bus-badge leg-${i} ${l.kind==='government'?'gov':''}">${esc(l.route)}</span>`
      ).join(' <span class="arrow">&rsaquo;</span> ');
      
      const changes = legs.slice(0, -1).map(l => `<b>${esc(l.to)}</b>`);
      const changeTxt = changes.length ? `Change at ${changes.join(' &amp; ')}` : 'Direct';
      
      const legHtml = legs.map((l, i) => {
        const mid = l.stops.slice(1, -1);
        const sl = mid.length
          ? `<button class="stop-toggle" onclick="event.stopPropagation();this.nextElementSibling.classList.toggle('show')">${mid.length} stops in between &#9662;</button>
             <div class="stop-list">${l.stops.map(s => `<span>${esc(s)}</span>`).join(' &middot; ')}</div>`
          : '';
        return `
          <div class="leg-step leg-${i}">
            <div class="leg-dot"></div>
            <div class="leg-content">
              <div class="leg-title">${esc(l.from)} &rarr; ${esc(l.to)}</div>
              <div class="leg-meta">Via ${esc(l.route)} (${l.kind})</div>
              ${sl}
            </div>
          </div>
        `;
      }).join('');
      
      // Store journey JSON to plot on click
      const journeyJson = esc(JSON.stringify(j));
      
      groupHtml += `
        <div class="journey-card" onclick="window.plotSelectedJourney(this, '${journeyJson}')">
          <div class="journey-top">
            ${buses}
            <div class="journey-cost">${changeTxt}</div>
          </div>
          <div class="journey-legs">
            ${legHtml}
          </div>
        </div>
      `;
    });
    groupHtml += `</div>`;
    return groupHtml;
  };
  
  htmlStr += renderGroup('Direct Buses', res.direct, 'direct');
  htmlStr += renderGroup('One Change', res.one, 'one-change');
  htmlStr += renderGroup('Two Changes', res.two, 'two-changes');
  
  if (!count) {
    htmlStr = `<div class="empty-state">
      <div class="empty-icon">😕</div>
      <h3>No routes found</h3>
      <p>Try searching for a nearby major stand instead.</p>
    </div>`;
  }
  
  elResults.innerHTML = htmlStr;
  elStats.textContent = `${count} Routes`;
  elStats.classList.remove('hidden');
}

window.plotSelectedJourney = function(cardEl, jStr) {
  document.querySelectorAll('.journey-card').forEach(c => c.classList.remove('active'));
  cardEl.classList.add('active');
  const j = JSON.parse(jStr.replace(/&quot;/g, '"'));
  const stats = map.plotJourney(j, router.coords);
  
  if (stats.missing > 0) {
    elMapNote.innerHTML = `⚠️ Plotted ${stats.plotted} stops &mdash; ${stats.missing} stops are missing map coordinates.`;
    elMapNote.style.color = '#b45309';
  } else {
    elMapNote.textContent = 'Showing selected route on map';
    elMapNote.style.color = '';
  }
  
  // Smooth scroll to map on mobile
  if (window.innerWidth < 900) {
    document.querySelector('.map-panel').scrollIntoView({ behavior: 'smooth' });
  }
};

init();
