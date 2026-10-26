(() => {
  const page = document.body.dataset.page || 'itinerary';
  const root = document.body;
  const sourceHref = (url) => {
    try {
      const u = new URL(url);
      return ['https:', 'http:'].includes(u.protocol) ? u.href : '#';
    } catch {
      return '#';
    }
  };
  const esc = (value = '') => String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
  const isFlagged = item => Boolean(item.flag);
  const categoryClass = category => `cat-${String(category).toLowerCase().replace(/[^a-z0-9]+/g, '-')}`;
  const dayKey = day => day === null || day === undefined || day === '' ? 'unassigned' : String(day);
  const dayLabel = key => key === 'unassigned' ? 'Unassigned references' : `Day ${key}`;
  const sourceLinksFor = item => {
    if (Array.isArray(item.sourceLinks) && item.sourceLinks.length) return item.sourceLinks;
    return [{ label: item.sourceLabel || 'Official source', url: item.source || '' }];
  };
  const sourceAnchors = item => sourceLinksFor(item).map(link =>
    `<a class="source-link" href="${esc(sourceHref(link.url))}" target="_blank" rel="noopener noreferrer">${esc(link.label || 'Official source')} <span aria-hidden="true">↗</span></a>`
  ).join('');

  document.querySelector('.menu-toggle')?.addEventListener('click', event => {
    const nav = document.querySelector('.main-nav');
    const open = nav.classList.toggle('nav-open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });

  const columns = `<thead><tr>
    <th scope="col">Plan item</th><th scope="col">Proposed plan</th>
    <th scope="col">Officially sourced detail</th><th scope="col">Status</th><th scope="col">Source</th>
  </tr></thead>`;

  const itemRow = item => `<tr>
    <td data-label="Plan item"><span class="category ${categoryClass(item.category)}">${esc(item.category)}</span><strong class="item-title">${esc(item.item)}</strong><span class="item-date">${esc(item.date)}</span></td>
    <td data-label="Proposed plan">${esc(item.plan)}</td>
    <td data-label="Officially sourced detail">${item.facts ? esc(item.facts) : '<span class="blank-value">Not confirmed</span>'}</td>
    <td data-label="Status"><span class="status ${item.verification === 'verified' ? 'status-source' : 'status-pending'}">${item.verification === 'verified' ? 'Source-linked' : 'Needs confirmation'}</span>${item.flag ? `<span class="row-flag">${esc(item.flag)}</span>` : ''}</td>
    <td data-label="Source"><div class="source-links">${sourceAnchors(item)}</div></td>
  </tr>`;

  const makeTable = (rows, label) => rows.length
    ? `<div class="table-scroll"><table class="data-table" aria-label="${esc(label)}">${columns}<tbody>${rows.map(itemRow).join('')}</tbody></table></div>`
    : '<div class="empty-state">No matching itinerary items.</div>';

  function renderAnalysis(items) {
    const metrics = document.getElementById('analysis-metrics');
    const dayHost = document.getElementById('analysis-days');
    if (!metrics && !dayHost) return;

    const numberedDays = [...new Set(items.filter(item => Number.isInteger(item.day)).map(item => item.day))].sort((a, b) => a - b);
    const verified = items.filter(item => item.verification === 'verified').length;
    const pending = items.filter(item => item.verification !== 'verified').length;
    const flagged = items.filter(isFlagged).length;
    const unassigned = items.filter(item => !Number.isInteger(item.day)).length;

    if (metrics) {
      metrics.innerHTML = [
        ['Day numbers', numberedDays.length, 'Present in data; missing-detail placeholders remain'],
        ['Plan rows', items.length, 'Including unresolved reference rows'],
        ['Source-linked', verified, 'At least one listed fact has an official source'],
        ['Flagged', flagged, `${pending} rows still need confirmation`]
      ].map(([label, value, note]) => `<article class="stat-card"><span class="stat-label">${esc(label)}</span><strong>${esc(value)}</strong><small>${esc(note)}</small></article>`).join('');
    }

    if (dayHost) {
      const rows = numberedDays.map(day => {
        const dayItems = items.filter(item => item.day === day);
        const source = sourceLinksFor(dayItems[0])[0] || { label: 'Official source', url: '' };
        const confirmed = dayItems.filter(item => item.verification === 'verified').length;
        const review = dayItems.filter(isFlagged).length;
        return `<tr>
          <td data-label="Day"><strong>Day ${day}</strong><span class="item-date">${esc(dayItems[0]?.date || 'Date/year unresolved')}</span></td>
          <td data-label="Plan rows">${dayItems.length}</td>
          <td data-label="Source-linked rows">${confirmed}</td>
          <td data-label="Flagged rows">${review}</td>
          <td data-label="Example row source"><a class="source-link" href="${esc(sourceHref(source.url))}" target="_blank" rel="noopener noreferrer">${esc(source.label)} <span aria-hidden="true">↗</span></a></td>
          <td data-label="Open day"><a href="itinerary.html?day=${day}">View Day ${day} →</a></td>
        </tr>`;
      }).join('');
      const unassignedNote = unassigned
        ? `<p class="analysis-note"><strong>${unassigned} unassigned research references</strong> are kept outside the day-by-day plan because their original day placement is not preserved. They are not treated as scheduled stops.</p>`
        : '';
      dayHost.innerHTML = `${unassignedNote}<div class="table-scroll"><table class="data-table analysis-table" aria-label="Day-by-day completeness and review status"><thead><tr><th scope="col">Day</th><th scope="col">Plan rows</th><th scope="col">Source-linked rows</th><th scope="col">Flagged rows</th><th scope="col">Example row source</th><th scope="col">Plan</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    }
  }

  fetch(new URL('data/itinerary.json', window.location.href))
    .then(response => {
      if (!response.ok) throw new Error(`Data request failed (${response.status})`);
      return response.json();
    })
    .then(items => {
      const flaggedCount = items.filter(isFlagged).length;
      const numberedDays = [...new Set(items.filter(item => Number.isInteger(item.day)).map(item => item.day))];
      document.getElementById('nav-flag-count')?.replaceChildren(document.createTextNode(String(flaggedCount)));
      document.getElementById('stat-days')?.replaceChildren(document.createTextNode(String(numberedDays.length)));
      document.getElementById('stat-items')?.replaceChildren(document.createTextNode(String(items.length)));
      document.getElementById('stat-flags')?.replaceChildren(document.createTextNode(String(flaggedCount)));
      renderAnalysis(items);

      const dayFilter = document.getElementById('day-filter');
      if (dayFilter) {
        const keys = [...new Set(items.map(item => dayKey(item.day)))].sort((a, b) => {
          if (a === 'unassigned') return 1;
          if (b === 'unassigned') return -1;
          return Number(a) - Number(b);
        });
        keys.forEach(key => {
          const option = document.createElement('option');
          option.value = key;
          option.textContent = dayLabel(key);
          dayFilter.append(option);
        });
        const requestedDay = new URLSearchParams(window.location.search).get('day');
        if (requestedDay && keys.includes(requestedDay)) dayFilter.value = requestedDay;
      }

      const baseFiltered = () => {
        if (page === 'transit') return items.filter(item => item.category === 'Transit');
        if (page === 'food') return items.filter(item => ['Food', 'Shopping', 'Nightlife'].includes(item.category));
        if (page === 'dining') return items.filter(item => ['Food', 'Nightlife'].includes(item.category));
        if (page === 'shopping') return items.filter(item => item.category === 'Shopping');
        if (page === 'attractions') return items.filter(item => item.category === 'Activities');
        if (page === 'stays') return items.filter(item => item.category === 'Stay');
        if (page === 'flags') return items.filter(isFlagged);
        return items;
      };

      const categoryFilter = document.getElementById('category-filter');
      if (categoryFilter) [...new Set(baseFiltered().map(item => item.category))].sort().forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.append(option);
      });

      const render = () => {
        const search = (document.getElementById('search')?.value || '').trim().toLowerCase();
        const dayValue = dayFilter?.value || 'all';
        const categoryValue = categoryFilter?.value || 'all';
        const visible = baseFiltered().filter(item => {
          const text = [item.date, item.category, item.item, item.plan, item.facts, item.flag, ...sourceLinksFor(item).map(source => source.label)].join(' ').toLowerCase();
          return (!search || text.includes(search))
            && (dayValue === 'all' || dayKey(item.day) === dayValue)
            && (categoryValue === 'all' || item.category === categoryValue);
        });

        const dayHost = document.getElementById('day-groups');
        if (dayHost) {
          if (!visible.length) {
            dayHost.innerHTML = '<div class="empty-state">No matching itinerary items.</div>';
            return;
          }
          const dayKeys = [...new Set(visible.map(item => dayKey(item.day)))].sort((a, b) => {
            if (a === 'unassigned') return 1;
            if (b === 'unassigned') return -1;
            return Number(a) - Number(b);
          });
          dayHost.innerHTML = dayKeys.map(key => {
            const groupItems = visible.filter(item => dayKey(item.day) === key);
            const title = key === 'unassigned' ? 'Day placement unresolved — research references only' : (groupItems[0].date || 'Date/year unresolved');
            const label = key === 'unassigned' ? 'REFERENCE' : `DAY ${key}`;
            return `<section class="day-card"><div class="day-head"><div><span class="day-number">${esc(label)}</span><h3>${esc(title)}</h3></div><span class="day-count">${groupItems.length} ${groupItems.length === 1 ? 'item' : 'items'}</span></div>${makeTable(groupItems, `${dayLabel(key)} itinerary`)}</section>`;
          }).join('');
        } else {
          const tableHost = document.getElementById('data-table');
          if (tableHost) tableHost.innerHTML = makeTable(visible, page === 'flags' ? 'Flagged itinerary entries' : `${page} itinerary items`);
        }
      };

      document.getElementById('search')?.addEventListener('input', render);
      dayFilter?.addEventListener('change', render);
      categoryFilter?.addEventListener('change', render);
      render();
      root.classList.add('data-ready');
    })
    .catch(error => {
      const host = document.getElementById('day-groups') || document.getElementById('data-table') || document.getElementById('analysis-days');
      if (host) host.innerHTML = `<div class="alert alert-warn"><strong>Unable to load itinerary data</strong><p>${esc(error.message)}. Please reload the page or inspect data/itinerary.json.</p></div>`;
    });
})();
