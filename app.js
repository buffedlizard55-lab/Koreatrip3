(() => {
  const page = document.body.dataset.page || 'itinerary';
  const root = document.body;
  const sourceHref = (url) => {
    try { const u = new URL(url); return ['https:', 'http:'].includes(u.protocol) ? u.href : '#'; }
    catch { return '#'; }
  };
  const esc = (v = '') => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const isFlagged = item => Boolean(item.flag);
  const categoryClass = category => `cat-${String(category).toLowerCase().replace(/[^a-z0-9]+/g, '-')}`;

  document.querySelector('.menu-toggle')?.addEventListener('click', e => {
    const nav = document.querySelector('.main-nav');
    const open = nav.classList.toggle('nav-open');
    e.currentTarget.setAttribute('aria-expanded', String(open));
  });

  fetch(new URL('data/itinerary.json', window.location.href))
    .then(response => { if (!response.ok) throw new Error(`Data request failed (${response.status})`); return response.json(); })
    .then(items => {
      const flaggedCount = items.filter(isFlagged).length;
      document.getElementById('nav-flag-count')?.replaceChildren(document.createTextNode(String(flaggedCount)));
      document.getElementById('stat-items')?.replaceChildren(document.createTextNode(String(items.length)));
      document.getElementById('stat-flags')?.replaceChildren(document.createTextNode(String(flaggedCount)));
      document.getElementById('stat-days')?.replaceChildren(document.createTextNode(String(new Set(items.map(i => i.day)).size)));
      const dayNames = ['Arrival · Myeongdong','N Seoul Tower · shopping','Palace · Bukchon ⚠','Seongsu · DDP','COEX · Gangnam','Ikseon · Insadong','Itaewon · open plan','Open day','KTX → Busan','Haeundae · Dongbaek · Mipo','Gamcheon · Songdo · Nampo','X the SKY · aquarium','Open day','Gwangalli drone show','Open day','KTX → Seoul · Hongdae'];
      const dayFilter = document.getElementById('day-filter');
      if (dayFilter) [...new Set(items.map(i => i.day))].forEach(day => {
        const opt = document.createElement('option'); opt.value = String(day); opt.textContent = `Day ${day}`; dayFilter.append(opt);
      });
      const hashDay = /^#day-(\d+)$/.exec(location.hash)?.[1];
      if (dayFilter && items.some(i => String(i.day) === hashDay)) dayFilter.value = hashDay;
      const picker = document.getElementById('day-picker');
      if (picker) picker.innerHTML = `<button type="button" data-day="all">All days<small>Full trip</small></button>` + [...new Set(items.map(i => i.day))].map(d => `<button type="button" data-day="${d}">Day ${d}<small>${esc(dayNames[d-1])}</small></button>`).join('');
      const categoryFilter = document.getElementById('category-filter');
      if (categoryFilter) [...new Set(items.map(i => i.category))].sort().forEach(category => {
        const opt = document.createElement('option'); opt.value = category; opt.textContent = category; categoryFilter.append(opt);
      });

      const baseFiltered = () => {
        if (page === 'transit') return items.filter(i => i.category === 'Transit');
        if (page === 'food') return items.filter(i => ['Food','Shopping','Nightlife'].includes(i.category));
        if (page === 'stays') return items.filter(i => i.category === 'Stay');
        if (page === 'flags') return items.filter(isFlagged);
        return items;
      };
      const columns = `<thead><tr><th scope="col">Plan item</th><th scope="col">Proposed plan</th><th scope="col">Officially sourced detail</th><th scope="col">Status</th><th scope="col">Source</th></tr></thead>`;
      const row = item => `<tr>
        <td data-label="Plan item"><span class="category ${categoryClass(item.category)}">${esc(item.category)}</span><strong class="item-title">${esc(item.item)}</strong><span class="item-date">${esc(item.date)}</span></td>
        <td data-label="Proposed plan">${esc(item.plan)}</td>
        <td data-label="Officially sourced detail">${item.facts ? esc(item.facts) : '<span class="blank-value" aria-label="Not confirmed">—</span>'}</td>
        <td data-label="Status"><span class="status ${item.verification === 'verified' ? 'status-source' : 'status-pending'}">${item.verification === 'verified' ? (item.checkedAt === '2026-10-26' ? 'Published detail checked' : 'Historical source record') : 'Unverified'}</span>${item.flag ? `<span class="row-flag">${esc(item.flag)}</span>` : ''}</td>
        <td data-label="Source"><a class="source-link" href="${esc(sourceHref(item.source))}" target="_blank" rel="noopener">${esc(item.sourceLabel)} <span aria-hidden="true">↗</span></a><small class="source-scope">${esc(item.sourceScope)} · ${esc(item.checkedAt)}</small></td>
      </tr>`;
      const table = (rows, label) => rows.length ? `<div class="table-scroll"><table class="data-table" aria-label="${esc(label)}">${columns}<tbody>${rows.map(row).join('')}</tbody></table></div>` : '<div class="empty-state">No matching itinerary items.</div>';
      const render = () => {
        const search = (document.getElementById('search')?.value || '').trim().toLowerCase();
        const dayValue = dayFilter?.value || 'all';
        picker?.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.day === dayValue)));
        const categoryValue = categoryFilter?.value || 'all';
        let visible = baseFiltered().filter(item => {
          const text = [item.date,item.category,item.item,item.plan,item.facts,item.flag].join(' ').toLowerCase();
          return (!search || text.includes(search)) && (dayValue === 'all' || String(item.day) === dayValue) && (categoryValue === 'all' || item.category === categoryValue);
        });
        const host = document.getElementById('day-groups');
        if (host) {
          if (!visible.length) { host.innerHTML = '<div class="empty-state">No matching itinerary items.</div>'; return; }
          const days = [...new Set(visible.map(i => i.day))].sort((a,b) => a-b);
          host.innerHTML = days.map(day => {
            const dayItems = visible.filter(i => i.day === day);
            return `<section class="day-card" id="day-${day}"><div class="day-head"><div><span class="day-number">DAY ${day}</span><h3>${esc(dayNames[day-1])}</h3><p>${esc(dayItems[0].date)}</p></div><span class="day-count">${dayItems.length} ${dayItems.length === 1 ? 'item' : 'items'}</span></div>${table(dayItems,`Day ${day} itinerary`)}</section>`;
          }).join('');
        } else {
          const el = document.getElementById('data-table');
          if (el) el.innerHTML = table(visible, page === 'flags' ? 'Flagged itinerary entries' : 'Itinerary items');
        }
      };
      document.getElementById('search')?.addEventListener('input', render);
      const selectDay = () => {
        if (dayFilter) history.replaceState(null, '', dayFilter.value === 'all' ? location.pathname + location.search : `#day-${dayFilter.value}`);
        render();
      };
      dayFilter?.addEventListener('change', selectDay);
      picker?.addEventListener('click', e => {
        const button = e.target.closest('button[data-day]');
        if (button && dayFilter) { dayFilter.value = button.dataset.day; selectDay(); }
      });
      window.addEventListener('hashchange', () => {
        const day = /^#day-(\d+)$/.exec(location.hash)?.[1];
        if (dayFilter) { dayFilter.value = items.some(i => String(i.day) === day) ? day : 'all'; render(); }
      });
      categoryFilter?.addEventListener('change', render);
      render();
      root.classList.add('data-ready');
    })
    .catch(error => {
      const host = document.getElementById('day-groups') || document.getElementById('data-table');
      if (host) host.innerHTML = `<div class="alert alert-warn"><strong>Unable to load itinerary data</strong><p>${esc(error.message)}. Please reload the page or inspect data/itinerary.json.</p></div>`;
    });
})();
