// Korea Trip 2026 — tiny helpers
(function () {
  // Countdown to departure (client-side arithmetic only)
  var el = document.getElementById('cd-text');
  if (el) {
    var start = new Date('2026-11-01T00:00:00+09:00');
    var end = new Date('2026-11-09T23:59:59+09:00');
    var now = new Date();
    if (now < start) {
      var days = Math.ceil((start - now) / 86400000);
      el.textContent = days + (days === 1 ? ' day' : ' days') + ' until takeoff — Sun Nov 1, 2026';
    } else if (now <= end) {
      var dayN = Math.floor((now - start) / 86400000) + 1;
      el.textContent = 'You are on Day ' + dayN + ' of the trip — have a great day!';
    } else {
      el.textContent = 'Trip dates: Nov 1–9, 2026 (completed)';
    }
  }
  // Flag filters
  var btns = document.querySelectorAll('.fbtn');
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var f = b.getAttribute('data-f');
      document.querySelectorAll('.flag').forEach(function (card) {
        card.style.display = (f === 'all' || card.classList.contains(f)) ? '' : 'none';
      });
    });
  });
})();
