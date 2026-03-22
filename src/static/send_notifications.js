/* send_notifications.js
   Prompts the user to enable browser notifications (if supported),
   and watches the #fillLevel value on the page to send notifications
   when it crosses configured thresholds (50, 75, 95).

   Behavior:
   - On page load, requests Notification permission if not already decided.
   - Initializes the previous value from the DOM (so we only notify on crossings).
   - Polls the displayed #fillLevel every few seconds and notifies when
     the value crosses a threshold upward.
*/
(function () {
  'use strict';

  const CHECK_INTERVAL_MS = 5000; // how often to check the displayed fill level

  const THRESHOLDS = [
    { level: 50, title: 'WARNING', body: 'WARNING: Sump Pit water level passed 50%! Pump may be struggling to keep up, consider calling for help!' },
    { level: 75, title: 'CAUTION', body: 'CAUTION: Sump pit water level passed 75%! Pump has likely failed, call for help! ' },
    { level: 95, title: 'ALERT', body: 'ALERT: SUMP PIT WATER LEVEL PASSED 95%, OVERFLOW IMMINENT!!! CALL FOR HELP NOW!!!' }
  ];

  let prevLevel = null;

  function isNumeric(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
  }

  function requestPermissionIfNeeded() {
    if (!('Notification' in window)) return;
    if (Notification.permission === 'default') {
      Notification.requestPermission().then(function (permission) {
        // nothing to do here; future checks will respect the permission
      });
    }
  }

  function sendNotification(title, body) {
    if (!('Notification' in window)) return;
    if (Notification.permission !== 'granted') return;
    try {
      new Notification(title, { body: body });
    } catch (e) {
      // Some browsers may throw if notifications are blocked at OS level
      console.warn('Failed to show notification', e);
    }
  }

  function readCurrentFillLevel() {
    const el = document.getElementById('fillLevel');
    if (!el) return null;
    const text = (el.textContent || el.innerText || '').trim();
    if (!isNumeric(text)) return null;
    return parseFloat(text);
  }

  function checkThresholds() {
    const current = readCurrentFillLevel();
    if (current === null) return;

    THRESHOLDS.forEach(function (t) {
      if ((prevLevel === null || prevLevel < t.level) && current >= t.level) {
        sendNotification(t.title, t.body);
      }
    });

    prevLevel = current;
  }

  window.addEventListener('load', function () {
    requestPermissionIfNeeded();

    // Initialize prevLevel from the page so we only notify on upward crossings
    const initial = readCurrentFillLevel();
    if (initial !== null) prevLevel = initial;

    // Periodically check the DOM value (update_temp_data.js updates it every 10s)
    setInterval(checkThresholds, CHECK_INTERVAL_MS);
  });

})();
