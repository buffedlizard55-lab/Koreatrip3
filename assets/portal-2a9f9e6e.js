document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.querySelector("[data-table-search]");
  const statusSelect = document.querySelector("[data-status-filter]");
  const daySelect = document.querySelector("[data-day-filter]");
  const countEl = document.querySelector("[data-row-count]");
  const rows = Array.from(document.querySelectorAll("table.data-table tbody tr[data-filterable]"));

  if (!rows.length) return;

  function applyFilters() {
    const query = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const status = statusSelect ? statusSelect.value : "all";
    const day = daySelect ? daySelect.value : "all";
    let visible = 0;

    for (const row of rows) {
      const textMatch = !query || (row.textContent || "").toLowerCase().includes(query);
      const rowStatus = row.getAttribute("data-status") || "";
      const rowDay = row.getAttribute("data-day") || "";
      const statusMatch =
        status === "all" ||
        rowStatus === status ||
        (status === "flagged" && rowStatus !== "verified");
      const dayMatch = day === "all" || rowDay === day;

      const show = textMatch && statusMatch && dayMatch;
      row.hidden = !show;
      if (show) visible += 1;
    }

    if (countEl) {
      countEl.textContent = `Showing ${visible} of ${rows.length} rows`;
    }
  }

  if (searchInput) searchInput.addEventListener("input", applyFilters);
  if (statusSelect) statusSelect.addEventListener("change", applyFilters);
  if (daySelect) daySelect.addEventListener("change", applyFilters);
  applyFilters();
});
