(() => {
  const view = document.body.dataset.view;
  const activeNav = document.body.dataset.active;
  const categoryView = document.body.dataset.category || "";

  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);

  const setText = (selector, value) => {
    document.querySelectorAll(selector).forEach((node) => { node.textContent = value; });
  };

  const initMenu = () => {
    const toggle = document.querySelector(".menu-toggle");
    const nav = document.getElementById("primary-nav");
    if (!toggle || !nav) return;
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      toggle.textContent = open ? "Close" : "Menu";
    });
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      nav.classList.remove("is-open");
      toggle.textContent = "Menu";
    }));
  };

  const setActiveNav = () => {
    document.querySelectorAll("[data-link]").forEach((link) => {
      if (link.dataset.link === activeNav) link.setAttribute("aria-current", "page");
    });
  };

  const sourceLinks = (ids, sourceMap) => {
    const list = (ids || []).map((id) => sourceMap.get(id)).filter(Boolean);
    if (!list.length) return '<span class="not-listed">—</span>';
    return `<div class="source-links">${list.map((source) => `<a class="source-link" href="${esc(source.url)}" target="_blank" rel="noopener noreferrer" title="${esc(source.title)} · ${esc(source.publisher)}">${esc(shortPublisher(source.publisher))}</a>`).join("")}</div>`;
  };

  const shortPublisher = (publisher) => {
    const aliases = [
      [/Korea Tourism Organization/, "VISITKOREA"],
      [/Visit Seoul/, "Visit Seoul"],
      [/Seoul Metro/, "Seoul Metro"],
      [/Busan Transportation Corporation/, "Busan Metro"],
      [/MARGESHERWOOD/, "MARGESHERWOOD"],
      [/LOTTE HOTELS/, "L7 Hotels"]
    ];
    for (const [pattern, label] of aliases) if (pattern.test(publisher)) return label;
    return publisher.length > 22 ? `${publisher.slice(0, 20)}…` : publisher;
  };

  const statusLabel = (status) => ({
    verified: ["Verified", "status-verified"],
    partial: ["Partial", "status-partial"],
    review: ["Review", "status-review"],
    conflict: ["Conflict", "status-conflict"]
  }[status] || ["Review", "status-review"]);

  const blankValue = (value) => value
    ? esc(value).replace(/\n/g, "<br>")
    : '<span class="not-listed" title="No confirmed value published">—</span>';

  const dayName = (dayId, dayMap) => {
    if (!dayId) return "Day not assigned";
    const day = dayMap.get(dayId);
    return day ? day.label : "Day not assigned";
  };

  const entryRow = (entry, sourceMap, dayMap) => {
    const [label, className] = statusLabel(entry.status);
    const search = [entry.name, entry.category, entry.planned, entry.officialFacts, entry.address, entry.hours, entry.price, entry.reviewNote].join(" ").toLowerCase();
    return `<tr id="entry-${esc(entry.id)}" class="entry-row" data-search="${esc(search)}">
      <td data-label="Stop">${esc(entry.name)}<small>${esc(capitalize(entry.category))} · ${esc(dayName(entry.dayId, dayMap))}</small></td>
      <td class="col-plan" data-label="As planned">${blankValue(entry.planned)}</td>
      <td class="col-facts" data-label="Officially checked">${blankValue(entry.officialFacts)}</td>
      <td class="col-address" data-label="Address">${blankValue(entry.address)}</td>
      <td class="col-hours" data-label="Hours / open days">${blankValue([entry.hours, entry.days].filter(Boolean).join(" · "))}</td>
      <td data-label="Price / fare">${blankValue(entry.price)}</td>
      <td class="col-status" data-label="Status"><span class="status-pill ${className}">${label}</span></td>
      <td class="col-audit" data-label="Audit note">${blankValue(entry.reviewNote)}</td>
      <td class="col-sources" data-label="Official sources">${sourceLinks(entry.sourceIds, sourceMap)}</td>
    </tr>`;
  };

  const entryTable = (entries, sourceMap, dayMap, caption) => {
    if (!entries.length) return '<div class="empty-state">No matching itinerary rows.</div>';
    return `<div class="table-card"><div class="table-scroll"><table class="data-table"><thead><tr>
      <th>Stop</th><th>As planned</th><th>Officially checked</th><th>Address</th><th>Hours / open days</th><th>Price / fare</th><th>Status</th><th>Audit note</th><th>Official sources</th>
    </tr></thead><tbody>${entries.map((entry) => entryRow(entry, sourceMap, dayMap)).join("")}</tbody></table></div>${caption ? `<div class="table-caption">${esc(caption)}</div>` : ""}</div>`;
  };

  const capitalize = (value) => value ? value.charAt(0).toUpperCase() + value.slice(1) : "Entry";
  const displaySourceUrl = (url) => url.replace(/^https?:\/\//, "").replace(/\/$/, "");

  const searchBox = (id, placeholder = "Search names, details, or neighborhoods…") => `<div class="content-toolbar"><label class="search-field"><span class="visually-hidden">Search this page</span><input id="${esc(id)}" class="js-search" type="search" placeholder="${esc(placeholder)}" autocomplete="off"></label><span class="toolbar-count" id="${esc(id)}-count" aria-live="polite"></span></div>`;

  const bindSearch = (inputId, itemSelector, countId) => {
    const input = document.getElementById(inputId);
    const items = Array.from(document.querySelectorAll(itemSelector));
    const count = document.getElementById(countId);
    if (!input) return;
    const update = () => {
      const query = input.value.trim().toLowerCase();
      let visible = 0;
      items.forEach((item) => {
        const text = (item.dataset.search || item.textContent || "").toLowerCase();
        const match = !query || text.includes(query);
        item.hidden = !match;
        if (match) visible += 1;
      });
      if (count) count.textContent = `${visible} ${visible === 1 ? "result" : "results"}`;
    };
    input.addEventListener("input", update);
    update();
  };

  const renderDashboard = (itinerary, sources, flags) => {
    const stats = document.getElementById("dashboard-stats");
    if (stats) {
      const openFlags = flags.filter((flag) => flag.severity !== "info").length;
      stats.innerHTML = `
        <div class="stat-card"><span class="stat-label">PLANNED DAYS</span><strong>${itinerary.days.length}</strong><span>Day 7 &amp; 8 stay blank</span></div>
        <div class="stat-card"><span class="stat-label">ITINERARY NOTES</span><strong>${itinerary.entries.length}</strong><span>Every row has official review links</span></div>
        <div class="stat-card stat-review"><span class="stat-label">OPEN CHECKS</span><strong>${openFlags}</strong><span>One informational schedule note excluded</span></div>
        <div class="stat-card"><span class="stat-label">OFFICIAL SOURCES</span><strong>${sources.length}</strong><span>Direct pages and indexed excerpts labeled</span></div>`;
    }
    setText("[data-checked-date]", itinerary.meta.sourceCheckedOn);
  };

  const renderItinerary = (itinerary, sources) => {
    const host = document.getElementById("itinerary-content");
    if (!host) return;
    const sourceMap = new Map(sources.map((source) => [source.id, source]));
    const dayMap = new Map(itinerary.days.map((day) => [day.id, day]));
    const daySections = itinerary.days.map((day) => {
      const entries = itinerary.entries.filter((entry) => entry.dayId === day.id);
      const rawDate = day.rawDate ? `<span class="day-date">${esc(day.rawDate)}</span>` : '<span class="day-date">DATE NOT PROVIDED</span>';
      const summary = `<div class="day-body"><p>${esc(day.summary)}</p></div>`;
      const content = entries.length
        ? entryTable(entries, sourceMap, dayMap, `${entries.length} source-linked ${entries.length === 1 ? "entry" : "entries"} · blanks indicate details not confirmed from the linked official source.`)
        : `<div class="day-empty">${esc(day.emptyNote || "No day-specific entry is assigned here. See unassigned itinerary notes below.")}</div>`;
      return `<section class="day-section" id="${esc(day.id)}"><div class="day-heading"><span class="day-badge">${esc(day.label)}</span><div><h2>${esc(day.city || "Unscheduled day")}</h2><p>${esc(day.summary)}</p></div>${rawDate}</div>${content}</section>`;
    }).join("");
    const unassigned = itinerary.entries.filter((entry) => !entry.dayId);
    host.innerHTML = `${searchBox("itinerary-search", "Search the itinerary…")}<div id="day-sections">${daySections}</div>
      <div id="unassigned-section"><div class="unassigned-heading"><div><p class="eyebrow eyebrow-muted">Retained, not re-sequenced</p><h2>Not assigned to a day</h2></div><p>These named places and leads remain in the plan/research record. Their exact day order is not established, so this site does not invent a schedule.</p></div>
      <div id="unassigned-table">${entryTable(unassigned, sourceMap, dayMap, `${unassigned.length} retained notes · assign only after checking the original sequence.`)}</div></div>`;
    bindSearch("itinerary-search", ".entry-row", "itinerary-search-count");
    const input = document.getElementById("itinerary-search");
    const updateSections = () => {
      const query = input.value.trim();
      document.querySelectorAll(".day-section").forEach((section) => {
        const rows = Array.from(section.querySelectorAll(".entry-row"));
        section.hidden = Boolean(query) && (rows.length === 0 || rows.every((row) => row.hidden));
      });
      const unassignedSection = document.getElementById("unassigned-section");
      const unassignedRows = Array.from(unassignedSection.querySelectorAll(".entry-row"));
      unassignedSection.hidden = Boolean(query) && (unassignedRows.length === 0 || unassignedRows.every((row) => row.hidden));
    };
    input.addEventListener("input", updateSections);
    updateSections();
  };

  const renderCategory = (itinerary, sources, categoryList) => {
    const host = document.getElementById("category-content");
    if (!host) return;
    const sourceMap = new Map(sources.map((source) => [source.id, source]));
    const dayMap = new Map(itinerary.days.map((day) => [day.id, day]));
    const allowed = categoryList.split(",").map((value) => value.trim()).filter(Boolean);
    const entries = itinerary.entries.filter((entry) => allowed.includes(entry.category));
    host.innerHTML = `${searchBox("category-search", "Search this category…")}<div id="category-table">${entryTable(entries, sourceMap, dayMap, `${entries.length} entries · Confirmed fields only; blank values are intentionally not supplied.`)}</div>`;
    bindSearch("category-search", ".entry-row", "category-search-count");
  };

  const renderTransit = (transit, sources) => {
    const host = document.getElementById("transit-content");
    if (!host) return;
    const sourceMap = new Map(sources.map((source) => [source.id, source]));
    host.innerHTML = `${searchBox("transit-search", "Search a route, station, or mode…")}<div class="route-grid">${transit.routes.map((route) => {
      const [label, className] = statusLabel(route.status);
      const search = [route.title, route.city, route.mode, route.route, route.confirmedDuration, route.confirmedFare, route.officialDetails, route.transferNote].join(" ").toLowerCase();
      return `<article class="route-card" data-search="${esc(search)}"><div class="route-top"><span class="route-city">${esc(route.city)}</span><span class="route-mode">${esc(route.mode)}</span></div><h3>${esc(route.title)}</h3><p class="route-detail">${esc(route.route)}</p><div class="route-facts"><div class="route-fact"><strong>Duration</strong>${route.confirmedDuration ? esc(route.confirmedDuration) : '<span class="not-listed">—</span>'}</div><div class="route-fact"><strong>Fare</strong>${route.confirmedFare ? esc(route.confirmedFare) : '<span class="not-listed">—</span>'}</div></div><div class="route-caveat"><strong>Review note · ${label}</strong><br>${esc(route.transferNote)}${route.officialDetails ? `<br><br>${esc(route.officialDetails)}` : ""}</div>${sourceLinks(route.sourceIds, sourceMap)}</article>`;
    }).join("")}</div>`;
    bindSearch("transit-search", ".route-card", "transit-search-count");
    const intro = document.getElementById("transit-intro");
    if (intro) intro.textContent = transit.intro;
  };

  const renderSources = (sources) => {
    const host = document.getElementById("sources-content");
    if (!host) return;
    const cards = sources.map((source) => {
      const search = [source.title, source.publisher, source.evidenceType, source.notes, source.url].join(" ").toLowerCase();
      return `<article class="source-card" id="source-${esc(source.id)}" data-search="${esc(search)}"><div class="source-card-head"><div><h3>${esc(source.title)}</h3><p class="source-publisher">${esc(source.publisher)}</p></div><span class="evidence-tag">${esc(source.evidenceType)}</span></div><p>${esc(source.notes)}</p><a class="source-link external-source" href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">Open official source</a><div class="source-meta"><span class="source-url">${esc(displaySourceUrl(source.url))}</span><span>Checked ${esc(source.checkedOn)}</span></div></article>`;
    }).join("");
    host.innerHTML = `${searchBox("sources-search", "Search an agency, business, or source…")}<div class="source-grid">${cards}</div>`;
    bindSearch("sources-search", ".source-card", "sources-search-count");
  };

  const renderFlags = (flags, itinerary, sources) => {
    const host = document.getElementById("flags-content");
    if (!host) return;
    const sourceMap = new Map(sources.map((source) => [source.id, source]));
    const entryMap = new Map(itinerary.entries.map((entry) => [entry.id, entry]));
    const openCount = flags.filter((flag) => flag.severity !== "info").length;
    const cards = flags.map((flag) => {
      const affected = (flag.affectedIds || []).map((id) => entryMap.get(id)?.name || id).filter(Boolean);
      const search = [flag.id, flag.category, flag.title, flag.summary, flag.detail, flag.nextStep, affected.join(" ")].join(" ").toLowerCase();
      return `<article class="flag-card flag-${esc(flag.severity)}" id="${esc(flag.id)}" data-search="${esc(search)}"><span class="flag-bar" aria-hidden="true"></span><div class="flag-content"><div class="flag-head"><div><div class="flag-title-wrap"><span class="flag-id">${esc(flag.id.toUpperCase())}</span><h3>${esc(flag.title)}</h3></div><p class="flag-category">${esc(flag.category)}</p></div><span class="severity-tag">${esc(flag.severity)}</span></div><p class="flag-summary-text">${esc(flag.summary)}</p><p class="flag-detail">${esc(flag.detail)}</p><p class="flag-next"><strong>Next step:</strong> ${esc(flag.nextStep)}</p><div class="flag-bottom"><span class="affected-items">Affects: ${esc(affected.join(" · ") || "Schedule note")}</span>${sourceLinks(flag.sourceIds, sourceMap)}</div></div></article>`;
    }).join("");
    host.innerHTML = `<div class="flag-summary"><div><strong>Flagged for Review</strong><p>Unverified values stay blank; unresolved flags do not block publication, but do need a travel-date check.</p></div><span class="flag-counter" aria-label="${openCount} open checks">${openCount}</span></div>${searchBox("flags-search", "Search flagged items…")}<div class="flag-list">${cards}</div>`;
    bindSearch("flags-search", ".flag-card", "flags-search-count");
  };

  const showError = (error) => {
    const host = document.querySelector("main");
    if (!host) return;
    const note = document.createElement("div");
    note.className = "error-note";
    note.setAttribute("role", "alert");
    note.textContent = `The trip data could not be loaded. Please refresh this static site. (${error.message})`;
    host.prepend(note);
  };

  initMenu();
  setActiveNav();

  Promise.all([
    fetch("data/itinerary.json").then((response) => { if (!response.ok) throw new Error("itinerary data unavailable"); return response.json(); }),
    fetch("data/transit.json").then((response) => { if (!response.ok) throw new Error("transit data unavailable"); return response.json(); }),
    fetch("data/sources.json").then((response) => { if (!response.ok) throw new Error("source register unavailable"); return response.json(); }),
    fetch("data/flags.json").then((response) => { if (!response.ok) throw new Error("review register unavailable"); return response.json(); })
  ]).then(([itinerary, transit, sources, flags]) => {
    if (view === "dashboard") renderDashboard(itinerary, sources, flags);
    if (view === "itinerary") renderItinerary(itinerary, sources);
    if (view === "category") renderCategory(itinerary, sources, categoryView);
    if (view === "transit") renderTransit(transit, sources);
    if (view === "sources") renderSources(sources);
    if (view === "flags") renderFlags(flags, itinerary, sources);
  }).catch(showError);
})();
