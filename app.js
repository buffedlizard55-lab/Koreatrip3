(() => {
  'use strict';
  // All itinerary data is built into HTML; networking and JavaScript are optional.
  document.querySelector('.print-button')?.addEventListener('click', () => window.print());
  const sections = [...document.querySelectorAll('[data-day-section]')];
  const picker = [...document.querySelectorAll('[data-day]')];
  const search = document.getElementById('search');
  const status = document.getElementById('status-filter');
  const count = document.getElementById('result-count');
  const empty = document.getElementById('empty-results');
  const allRows = [...document.querySelectorAll('tr[data-search]')];
  let selectedDay = null;
  function filter() {
    const query = (search?.value || '').trim().toLocaleLowerCase();
    const evidence = status?.value || 'all';
    let matches = 0;
    allRows.forEach(row => {
      const owner = row.closest('[data-day-section]');
      const inDay = !owner || selectedDay === null || Number(owner.dataset.daySection) === selectedDay;
      const matchesFilters = row.dataset.search.includes(query) && (evidence === 'all' || row.dataset.status === evidence);
      row.hidden = !matchesFilters;
      if (inDay && matchesFilters) matches++;
    });
    if (count) count.textContent = `${matches} ${matches === 1 ? 'entry' : 'entries'}`;
    if (empty) empty.hidden = matches !== 0;
  }
  function selectFromHash() {
    if (!sections.length) { filter(); return; }
    const hash = window.location.hash;
    const dayMatch = /^#day-(\d+)$/.exec(hash);
    const rowTarget = /^#R\d+$/.test(hash) ? document.getElementById(hash.slice(1)) : null;
    const rowDay = rowTarget?.closest('[data-day-section]')?.dataset.daySection;
    if (hash === '#all-days') selectedDay = null;
    else if (rowDay) selectedDay = Number(rowDay);
    else if (dayMatch && Number(dayMatch[1]) >= 1 && Number(dayMatch[1]) <= 16) selectedDay = Number(dayMatch[1]);
    else selectedDay = 1;
    sections.forEach(section => { section.hidden = selectedDay !== null && Number(section.dataset.daySection) !== selectedDay; });
    picker.forEach(link => {
      if (Number(link.dataset.day) === selectedDay) link.setAttribute('aria-current', 'date');
      else link.removeAttribute('aria-current');
    });
    const prev = document.getElementById('previous-day');
    const next = document.getElementById('next-day');
    if (prev && next) {
      const day = selectedDay || 1;
      prev.href = `#day-${Math.max(1, day - 1)}`;
      next.href = `#day-${Math.min(16, day + 1)}`;
      prev.setAttribute('aria-disabled', String(day === 1));
      next.setAttribute('aria-disabled', String(day === 16));
    }
    const all = document.getElementById('show-all');
    if (all) all.textContent = selectedDay === null ? 'Back to Day 1' : 'Show all days';
    filter();
  }
  document.getElementById('show-all')?.addEventListener('click', () => { window.location.hash = selectedDay === null ? 'day-1' : 'all-days'; });
  search?.addEventListener('input', filter);
  status?.addEventListener('change', filter);
  window.addEventListener('hashchange', selectFromHash);
  selectFromHash();
})();
