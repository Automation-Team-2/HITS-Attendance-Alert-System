// =============================================
// HITS Attendance Tracker — SPA Client
// Fetches data from FastAPI dynamically.
// No page reloads for filtering, searching,
// alert history, or chart rendering.
// =============================================

(function () {
  'use strict';

  // ─── CONFIGURATION ──────────────────────────────────────────────
  var FASTAPI_URL = localStorage.getItem('fastapiUrl') || 'http://127.0.0.1:8001';

  // ─── APPLICATION STATE ──────────────────────────────────────────
  var State = {
    sections: [],
    students: [],
    rawSections: [],
    rawStudents: [],
    activeTab: 'attendance',
    selectedClass: null,
    searchQuery: '',
    attendanceThreshold: 75,
    source: 'loading', // 'api' | 'fallback' | 'loading'
  };

  // ─── FALLBACK DATA ──────────────────────────────────────────────
  var fallbackSections = [
    { id: '1', name: 'B.Tech CSE', description: 'Branch: Computer Science & Engineering' },
    { id: '2', name: 'B.Tech AERO', description: 'Branch: Aerospace Engineering' },
    { id: '3', name: 'B.Tech IT', description: 'Branch: Information Technology' },
  ];

  var fallbackStudents = [
    { id: '1',  roll: '26CU0310001', name: 'Naveen',   contact: '9104332181', attendance: 55 },
    { id: '2',  roll: '26CU0310002', name: 'Payal',    contact: '9600133890', attendance: 62 },
    { id: '3',  roll: '26CU0310003', name: 'Preeti',   contact: '9386379402', attendance: 48 },
    { id: '4',  roll: '26CU0310004', name: 'Lakshya',  contact: '9654235116', attendance: 58 },
    { id: '5',  roll: '26CU0310005', name: 'Dhruv',    contact: '9559407816', attendance: 65 },
    { id: '6',  roll: '26CU0310006', name: 'Kabir',    contact: '9849593103', attendance: 52 },
    { id: '7',  roll: '26CU0310007', name: 'Vanshika', contact: '9413164752', attendance: 60 },
    { id: '8',  roll: '26CU0310008', name: 'Tanish',   contact: '9534192832', attendance: 45 },
    { id: '9',  roll: '26CU0310009', name: 'Suman',    contact: '9648350305', attendance: 92 },
    { id: '10', roll: '26CU0310010', name: 'Pallavi',  contact: '9413953767', attendance: 88 },
    { id: '11', roll: '26CU0310011', name: 'Devansh',  contact: '9423884969', attendance: 95 },
    { id: '12', roll: '26CU0310012', name: 'Raghav',   contact: '9328710122', attendance: 90 },
    { id: '13', roll: '26CU0310013', name: 'Girish',   contact: '9691669784', attendance: 87 },
    { id: '14', roll: '26CU0310014', name: 'Sneha',    contact: '9018451462', attendance: 93 },
    { id: '15', roll: '26CU0310015', name: 'Vidya',    contact: '9048281489', attendance: 78 },
    { id: '16', roll: '26CU0310016', name: 'Saanvi',   contact: '9252880957', attendance: 82 },
    { id: '17', roll: '26CU0310017', name: 'Aditya',   contact: '9154303911', attendance: 80 },
    { id: '18', roll: '26CU0310018', name: 'Palak',    contact: '9718227824', attendance: 76 },
    { id: '19', roll: '26CU0310019', name: 'Ravi',     contact: '9963834657', attendance: 79 },
    { id: '20', roll: '26CU0310020', name: 'Sanjay',   contact: '9713315098', attendance: 83 },
    { id: '21', roll: '26CU0310021', name: 'Anika',    contact: '9930103105', attendance: 75 },
    { id: '22', roll: '26CU0310022', name: 'Rohan',    contact: '9834738299', attendance: 75 },
    { id: '23', roll: '26CU0310023', name: 'Kunal',    contact: '9376311656', attendance: 75 },
    { id: '24', roll: '26CU0310024', name: 'Snehal',   contact: '9701065133', attendance: 75 },
    { id: '25', roll: '26CU0310025', name: 'Myra',     contact: '9872624731', attendance: 75 },
    { id: '26', roll: '26CU0310026', name: 'Radhika',  contact: '9810801326', attendance: 75 },
    { id: '27', roll: '26CU0310027', name: 'Vikram',   contact: '9736026064', attendance: 75 },
    { id: '28', roll: '26AU0310001', name: 'Shreya',   contact: '9687234309', attendance: 63 },
    { id: '29', roll: '26AU0310002', name: 'Ritika',   contact: '9805009788', attendance: 50 },
    { id: '30', roll: '26AU0310003', name: 'Ananya',   contact: '9081219136', attendance: 57 },
    { id: '31', roll: '26AU0310004', name: 'Sarthak',  contact: '9939909169', attendance: 42 },
    { id: '32', roll: '26AU0310005', name: 'Komal',    contact: '9854353462', attendance: 68 },
    { id: '33', roll: '26AU0310006', name: 'Tarun',    contact: '9475107991', attendance: 55 },
    { id: '34', roll: '26AU0310007', name: 'Ajay',     contact: '9384251354', attendance: 47 },
    { id: '35', roll: '26AU0310008', name: 'Vishal',   contact: '9498084124', attendance: 61 },
    { id: '36', roll: '26AU0310009', name: 'Yash',     contact: '9182449353', attendance: 89 },
    { id: '37', roll: '26AU0310010', name: 'Sanya',    contact: '9874016400', attendance: 91 },
    { id: '38', roll: '26AU0310011', name: 'Varun',    contact: '9242786801', attendance: 96 },
    { id: '39', roll: '26AU0310012', name: 'Mohit',    contact: '9280598262', attendance: 88 },
    { id: '40', roll: '26AU0310013', name: 'Sai',      contact: '9450533158', attendance: 94 },
    { id: '41', roll: '26AU0310014', name: 'Nandini',  contact: '9356159514', attendance: 87 },
    { id: '42', roll: '26AU0310015', name: 'Isha',     contact: '9232260256', attendance: 77 },
    { id: '43', roll: '26AU0310016', name: 'Aman',     contact: '9433036541', attendance: 81 },
    { id: '44', roll: '26AU0310017', name: 'Nisha',    contact: '9586850142', attendance: 84 },
    { id: '45', roll: '26AU0310018', name: 'Anjali',   contact: '9401965569', attendance: 76 },
    { id: '46', roll: '26AU0310019', name: 'Manish',   contact: '9169340608', attendance: 82 },
    { id: '47', roll: '26AU0310020', name: 'Neha',     contact: '9421607337', attendance: 79 },
    { id: '48', roll: '26AU0310021', name: 'Deepak',   contact: '9465648236', attendance: 75 },
    { id: '49', roll: '26AU0310022', name: 'Ayush',    contact: '9299468044', attendance: 75 },
    { id: '50', roll: '26AU0310023', name: 'Aadhya',   contact: '9699577738', attendance: 75 },
    { id: '51', roll: '26AU0310024', name: 'Diya',     contact: '9148951343', attendance: 75 },
    { id: '52', roll: '26AU0310025', name: 'Vihaan',   contact: '9037917693', attendance: 75 },
    { id: '53', roll: '26AU0310026', name: 'Juhi',     contact: '9676320163', attendance: 75 },
    { id: '54', roll: '26AU0310027', name: 'Ishita',   contact: '9870831727', attendance: 75 },
    { id: '55', roll: '26IT0310001', name: 'Rashi',      contact: '9579868727', attendance: 59 },
    { id: '56', roll: '26IT0310002', name: 'Namrata',    contact: '9434873471', attendance: 53 },
    { id: '57', roll: '26IT0310003', name: 'Pooja',      contact: '9455812236', attendance: 66 },
    { id: '58', roll: '26IT0310004', name: 'Harsh',      contact: '9316658760', attendance: 44 },
    { id: '59', roll: '26IT0310005', name: 'Ritu',       contact: '9690967054', attendance: 87 },
    { id: '60', roll: '26IT0310006', name: 'Tanya',      contact: '9668893734', attendance: 90 },
    { id: '61', roll: '26IT0310007', name: 'Bhavna',     contact: '9706562729', attendance: 88 },
    { id: '62', roll: '26IT0310008', name: 'Divya',      contact: '9990162720', attendance: 92 },
    { id: '63', roll: '26IT0310009', name: 'Nikhil',     contact: '9375564641', attendance: 86 },
    { id: '64', roll: '26IT0310010', name: 'Sakshi',     contact: '9805310033', attendance: 95 },
    { id: '65', roll: '26IT0310011', name: 'Rudra',      contact: '9719374529', attendance: 89 },
    { id: '66', roll: '26IT0310012', name: 'Vaishnavi',  contact: '9124190496', attendance: 91 },
    { id: '67', roll: '26IT0310013', name: 'Rajat',      contact: '9314919058', attendance: 78 },
    { id: '68', roll: '26IT0310014', name: 'Swati',      contact: '9518506716', attendance: 83 },
    { id: '69', roll: '26IT0310015', name: 'Bhavya',     contact: '9262849877', attendance: 80 },
    { id: '70', roll: '26IT0310016', name: 'Tanvi',      contact: '9531473799', attendance: 77 },
    { id: '71', roll: '26IT0310017', name: 'Siddharth',  contact: '9075273545', attendance: 81 },
    { id: '72', roll: '26IT0310018', name: 'Vivaan',     contact: '9831367837', attendance: 79 },
    { id: '73', roll: '26IT0310019', name: 'Suraj',      contact: '9770143634', attendance: 76 },
    { id: '74', roll: '26IT0310020', name: 'Pranav',     contact: '9957885685', attendance: 82 },
    { id: '75', roll: '26IT0310021', name: 'Gaurav',     contact: '9744431351', attendance: 75 },
    { id: '76', roll: '26IT0310022', name: 'Urvashi',    contact: '9233749894', attendance: 75 },
    { id: '77', roll: '26IT0310023', name: 'Kritika',    contact: '9352408240', attendance: 75 },
    { id: '78', roll: '26IT0310024', name: 'Reyansh',    contact: '9842710947', attendance: 75 },
    { id: '79', roll: '26IT0310025', name: 'Rahul',      contact: '9752047116', attendance: 75 },
    { id: '80', roll: '26IT0310026', name: 'Shalini',    contact: '9022941318', attendance: 75 },
  ];

  // ─── CHART INSTANCES (so we can destroy/recreate) ──────────────
  var lineChart = null;
  var barChart = null;

  // ─── HELPERS ────────────────────────────────────────────────────

  function branchKey(roll) {
    if (!roll) return 'other';
    var p = roll.substring(0, 5);
    if (p.indexOf('CU') !== -1) return 'cse';
    if (p.indexOf('AU') !== -1) return 'aero';
    if (p.indexOf('IT') !== -1) return 'it';
    return 'other';
  }

  function branchLabel(key) {
    var map = { cse: 'B.Tech CSE', aero: 'B.Tech AERO', it: 'B.Tech IT' };
    return map[key] || 'Other';
  }

  function groupStudentsByBranch(students) {
    var groups = { cse: [], aero: [], it: [], other: [] };
    students.forEach(function (s) { groups[branchKey(s.roll)].push(s); });
    return groups;
  }

  function getFilteredStudents() {
    var q = State.searchQuery.toLowerCase().trim();
    var thresh = State.attendanceThreshold;
    var cls = State.selectedClass;
    return State.students.filter(function (s) {
      if (cls && branchKey(s.roll) !== cls) return false;
      if (s.attendance >= thresh) return false;
      if (q) {
        var nameMatch = s.name.toLowerCase().indexOf(q) !== -1;
        var rollMatch = s.roll.toLowerCase().indexOf(q) !== -1;
        if (!nameMatch && !rollMatch) return false;
      }
      return true;
    });
  }

  function getAllVisibleStudents() {
    var q = State.searchQuery.toLowerCase().trim();
    var cls = State.selectedClass;
    return State.students.filter(function (s) {
      if (cls && branchKey(s.roll) !== cls) return false;
      if (q) {
        var nameMatch = s.name.toLowerCase().indexOf(q) !== -1;
        var rollMatch = s.roll.toLowerCase().indexOf(q) !== -1;
        if (!nameMatch && !rollMatch) return false;
      }
      return true;
    });
  }

  function esc(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ─── DATA FETCHING ──────────────────────────────────────────────

  async function fetchFromFastAPI() {
    try {
      var secRes = await fetch(FASTAPI_URL + '/api/sections/');
      var stuRes = await fetch(FASTAPI_URL + '/api/students/');
      if (!secRes.ok || !stuRes.ok) throw new Error('API error');
      var sections = await secRes.json();
      var students = await stuRes.json();
      if (!sections.length && !students.length) throw new Error('Empty');
      State.rawSections = sections;
      State.rawStudents = students;
      State.source = 'api';
    } catch (e) {
      State.rawSections = fallbackSections;
      State.rawStudents = fallbackStudents;
      State.source = 'fallback';
    }
    processData();
  }

  function processData() {
    // Group students into section objects
    var groups = groupStudentsByBranch(State.rawStudents);
    State.sections = [];
    ['cse', 'aero', 'it'].forEach(function (key) {
      var secMeta = State.rawSections.find(function (s) {
        return branchKey(s.name || s.id) === key || (s.name || '').toLowerCase().indexOf(key) !== -1;
      }) || {};
      State.sections.push({
        key: key,
        name: secMeta.name || branchLabel(key),
        description: secMeta.description || '',
        students: groups[key],
      });
    });
    State.students = State.rawStudents;
  }

  // ─── RENDER: STATUS BADGE ──────────────────────────────────────

  function renderStatus() {
    var el = document.getElementById('backend-status');
    if (!el) return;
    if (State.source === 'api') {
      el.textContent = 'Online';
      el.className = 'text-orange-700 bg-orange-100 px-3 py-1 rounded-full text-xs font-bold';
    } else if (State.source === 'fallback') {
      el.textContent = 'Offline';
      el.className = 'text-gray-500 bg-gray-100 px-3 py-1 rounded-full text-xs font-bold';
    } else {
      el.textContent = 'Loading...';
      el.className = 'text-blue-600 bg-blue-50 px-3 py-1 rounded-full text-xs font-bold';
    }
  }

  // ─── RENDER: CLASS CARDS ────────────────────────────────────────

  function renderClassCards() {
    var grid = document.getElementById('classes-grid');
    if (!grid) return;
    var groups = groupStudentsByBranch(State.students);
    var keys = ['cse', 'aero', 'it'];

    var html = '<h2 class="text-xl font-bold text-gray-800 mb-4">Your Classes Overview</h2>';
    html += '<p class="text-sm text-gray-500 mb-6">Select a section profile card below to view specific student records.</p>';
    html += '<div class="grid grid-cols-1 md:grid-cols-3 gap-6">';

    keys.forEach(function (key) {
      var students = groups[key];
      var atRisk = students.filter(function (s) { return s.attendance < State.attendanceThreshold; }).length;
      html +=
        '<div class="bg-white rounded-xl shadow p-6 border-l-4 border-orange-500 hover:shadow-lg transition">' +
          '<span class="inline-block bg-orange-100 text-orange-800 text-xs font-bold px-3 py-1 rounded-full mb-3">' + students.length + ' Students</span>' +
          '<h3 class="text-lg font-bold text-gray-800">' + esc(branchLabel(key)) + '</h3>' +
          '<p class="text-sm text-gray-500 mt-1">' + esc(
            (State.sections.find(function (s) { return s.key === key; }) || {}).description || ''
          ) + '</p>' +
          (atRisk > 0
            ? '<p class="text-xs text-red-500 font-semibold mt-2">' + atRisk + ' at risk (&lt;' + State.attendanceThreshold + '%)</p>'
            : '<p class="text-xs text-green-600 font-semibold mt-2">All students safe</p>'
          ) +
          '<button class="view-roster-btn mt-4 w-full bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-md text-sm transition" data-class="' + key + '">View Student Roster</button>' +
        '</div>';
    });

    html += '</div>';
    grid.innerHTML = html;
  }

  // ─── RENDER: STUDENT ROSTER ─────────────────────────────────────

  function renderRoster(classKey) {
    var students = State.students.filter(function (s) { return branchKey(s.roll) === classKey; });
    var q = State.searchQuery.toLowerCase().trim();

    if (q) {
      students = students.filter(function (s) {
        return s.name.toLowerCase().indexOf(q) !== -1 || s.roll.toLowerCase().indexOf(q) !== -1;
      });
    }

    var title = document.getElementById('roster-title');
    if (title) title.textContent = branchLabel(classKey) + ' — Student Roster (' + students.length + ' shown)';

    var tbody = document.getElementById('roster-body');
    if (!tbody) return;

    if (students.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="px-4 py-8 text-center text-gray-400">No students match your search.</td></tr>';
      return;
    }

    var html = '';
    students.forEach(function (s) {
      var isSafe = s.attendance >= State.attendanceThreshold;
      var statusBadge = isSafe
        ? '<span class="inline-block bg-green-100 text-green-700 text-xs font-semibold px-2 py-0.5 rounded-full">Safe</span>'
        : '<span class="inline-block bg-red-100 text-red-700 text-xs font-semibold px-2 py-0.5 rounded-full">At Risk</span>';
      var actionBtn = isSafe
        ? '<span class="text-gray-400 text-xs">--</span>'
        : '<button class="send-sms-btn bg-orange-500 hover:bg-orange-600 text-white text-xs px-3 py-1 rounded transition" data-roll="' + esc(s.roll) + '" data-name="' + esc(s.name) + '">Send SMS Alert</button>';
      html += '<tr class="hover:bg-orange-50 transition">' +
        '<td class="px-4 py-3 font-mono text-xs">' + esc(s.roll) + '</td>' +
        '<td class="px-4 py-3 font-medium text-gray-800">' + esc(s.name) + '</td>' +
        '<td class="px-4 py-3 text-gray-600">' + esc(s.contact) + '</td>' +
        '<td class="px-4 py-3 font-bold ' + (isSafe ? 'text-green-600' : 'text-red-600') + '">' + s.attendance + '%</td>' +
        '<td class="px-4 py-3">' + statusBadge + '</td>' +
        '<td class="px-4 py-3">' + actionBtn + '</td>' +
        '</tr>';
    });
    tbody.innerHTML = html;
  }

  // ─── RENDER: ALERT HISTORY (dynamic from student data) ──────────

  function renderAlertHistory() {
    var container = document.getElementById('tab-history');
    if (!container) return;

    var atRisk = State.students
      .filter(function (s) { return s.attendance < State.attendanceThreshold; })
      .sort(function (a, b) { return a.attendance - b.attendance; });

    var subjects = ['Data Structures', 'Algorithms', 'Operating Systems', 'Computer Networks', 'Database Systems', 'Software Engineering'];
    var statuses = [
      { text: 'Delivered via SMS', cls: 'bg-green-100 text-green-700' },
      { text: 'Delivered via SMS', cls: 'bg-green-100 text-green-700' },
      { text: 'Delivered via SMS', cls: 'bg-green-100 text-green-700' },
      { text: 'Delivered via SMS', cls: 'bg-green-100 text-green-700' },
      { text: 'Failed / Retrying', cls: 'bg-orange-100 text-orange-700' },
    ];

    var dates = ['2026-07-10', '2026-07-09', '2026-07-08', '2026-07-07', '2026-07-06'];
    var times = ['10:32 AM', '09:15 AM', '08:45 AM', '08:10 AM', '04:20 PM', '03:50 PM', '02:10 PM', '11:45 AM'];

    // Build the log table rows dynamically
    var tableBody = container.querySelector('.divide-y');
    if (!tableBody) return;

    var html = '';
    var showCount = Math.min(atRisk.length, 20);
    for (var i = 0; i < showCount; i++) {
      var s = atRisk[i];
      var dateStr = dates[i % dates.length];
      var timeStr = times[i % times.length];
      var subj = subjects[i % subjects.length];
      var status = statuses[i % statuses.length];
      html += '<tr class="hover:bg-orange-50 transition">' +
        '<td class="px-4 py-3 text-gray-600">' + dateStr + ' ' + timeStr + '</td>' +
        '<td class="px-4 py-3 font-medium text-gray-800">' + esc(s.name) + '</td>' +
        '<td class="px-4 py-3 text-gray-600">' + esc(s.contact) + '</td>' +
        '<td class="px-4 py-3 text-gray-700">' + esc(subj) + '</td>' +
        '<td class="px-4 py-3 font-bold text-red-600">' + s.attendance + '%</td>' +
        '<td class="px-4 py-3"><span class="inline-block ' + status.cls + ' text-xs font-semibold px-2 py-0.5 rounded-full">' + status.text + '</span></td>' +
        '</tr>';
    }
    if (atRisk.length > 20) {
      html += '<tr><td colspan="6" class="px-4 py-3 text-center text-gray-400 text-xs">… and ' + (atRisk.length - 20) + ' more alerts</td></tr>';
    }
    tableBody.innerHTML = html;
  }

  // ─── RENDER: METRIC CARDS ──────────────────────────────────────

  function renderMetricCards() {
    var total = State.students.length;
    var atRisk = State.students.filter(function (s) { return s.attendance < State.attendanceThreshold; });
    var atRiskCount = atRisk.length;
    var avgAtRisk = atRisk.length
      ? Math.round(atRisk.reduce(function (acc, s) { return acc + s.attendance; }, 0) / atRisk.length)
      : 0;
    var groups = groupStudentsByBranch(State.students);
    var classBreakdown = 'CSE: ' + groups.cse.length + ' | AERO: ' + groups.aero.length + ' | IT: ' + groups.it.length;

    // Update the metric cards in stats tab
    var metricCards = document.querySelectorAll('#tab-stats .grid > div');
    if (metricCards.length >= 3) {
      metricCards[0].querySelector('.text-3xl').textContent = atRiskCount;
      metricCards[0].querySelector('.text-xs:last-child').textContent = 'Students below ' + State.attendanceThreshold + '% threshold';
      metricCards[1].querySelector('.text-3xl').textContent = total;
      metricCards[1].querySelector('.text-xs:last-child').textContent = classBreakdown;
      metricCards[2].querySelector('.text-3xl').textContent = atRiskCount;
      metricCards[2].querySelector('.text-xs:last-child').textContent = 'Avg attendance: ' + avgAtRisk + '%';
    }
  }

  // ─── RENDER: CHARTS (from live data) ────────────────────────────

  function renderCharts() {
    if (typeof Chart === 'undefined') return;

    var C = {
      primary:    '#F38B1C',
      primaryLt:  'rgba(243,139,28,0.18)',
      primaryDk:  '#D67415',
      accent:     '#B45F11',
      accentLt:   'rgba(180,95,17,0.14)',
      grid:       'rgba(0,0,0,0.06)',
      gridBorder: 'rgba(0,0,0,0.08)',
      text:       '#64748b',
      textBold:   '#1e293b',
      white:      '#ffffff',
      red:        '#ef4444',
      redLt:      'rgba(239,68,68,0.18)',
    };

    Chart.defaults.font.family = "'Inter', 'Segoe UI', system-ui, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = C.text;
    Chart.defaults.plugins.legend.display = false;
    Chart.defaults.responsive = true;
    Chart.defaults.maintainAspectRatio = false;

    // ── Line chart: daily alert volume (simulated from at-risk students) ──
    var groups = groupStudentsByBranch(State.students);
    var lineLabels = ['Jul 06', 'Jul 07', 'Jul 08', 'Jul 09', 'Jul 10'];
    var atRiskTotal = State.students.filter(function (s) { return s.attendance < State.attendanceThreshold; }).length;
    // Simulate daily distribution of alerts
    var perDay = Math.ceil(atRiskTotal / 5);
    var lineSent = [perDay, perDay + 2, perDay + 1, perDay, perDay - 1];
    var lineFailed = [0, 0, 1, 0, 0];

    // Destroy existing charts
    if (lineChart) { lineChart.destroy(); lineChart = null; }
    if (barChart) { barChart.destroy(); barChart = null; }

    var lineCtx = document.getElementById('chart-alert-line');
    if (lineCtx) {
      lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
          labels: lineLabels,
          datasets: [
            {
              label: 'Delivered',
              data: lineSent,
              borderColor: C.primary,
              backgroundColor: C.primaryLt,
              borderWidth: 2.5,
              pointBackgroundColor: C.white,
              pointBorderColor: C.primary,
              pointBorderWidth: 2,
              pointRadius: 5,
              pointHoverRadius: 7,
              fill: true,
              tension: 0.35,
            },
            {
              label: 'Failed',
              data: lineFailed,
              borderColor: C.red,
              backgroundColor: C.redLt,
              borderWidth: 2,
              borderDash: [5, 4],
              pointBackgroundColor: C.white,
              pointBorderColor: C.red,
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6,
              fill: true,
              tension: 0.35,
            }
          ]
        },
        options: {
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              display: true,
              position: 'bottom',
              labels: { usePointStyle: true, pointStyle: 'circle', padding: 16, font: { size: 11, weight: '600' } }
            },
            tooltip: {
              backgroundColor: C.textBold,
              titleFont: { size: 12, weight: '700' },
              bodyFont: { size: 11 },
              padding: { top: 10, bottom: 10, left: 14, right: 14 },
              cornerRadius: 8,
              displayColors: true,
              boxPadding: 4,
              callbacks: {
                title: function (items) { return 'Date: ' + items[0].label; },
                label: function (ctx) { return ' ' + ctx.dataset.label + ': ' + ctx.parsed.y + ' alerts'; }
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { font: { size: 11, weight: '600' } }, border: { display: false } },
            y: { beginAtZero: true, grid: { color: C.grid }, border: { display: false }, ticks: { stepSize: 1, font: { size: 11 }, padding: 8 } }
          }
        }
      });
    }

    // ── Bar chart: class-wise at-risk count ──
    var barLabels = ['B.Tech CSE', 'B.Tech AERO', 'B.Tech IT'];
    var barCounts = [
      groups.cse.filter(function (s) { return s.attendance < State.attendanceThreshold; }).length,
      groups.aero.filter(function (s) { return s.attendance < State.attendanceThreshold; }).length,
      groups.it.filter(function (s) { return s.attendance < State.attendanceThreshold; }).length,
    ];

    var barCtx = document.getElementById('chart-subject-bar');
    if (barCtx) {
      var barGradient = barCtx.getContext('2d').createLinearGradient(0, 0, 0, 260);
      barGradient.addColorStop(0, C.primary);
      barGradient.addColorStop(1, C.accent);

      var barHoverGradient = barCtx.getContext('2d').createLinearGradient(0, 0, 0, 260);
      barHoverGradient.addColorStop(0, '#FB923C');
      barHoverGradient.addColorStop(1, C.primary);

      barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
          labels: barLabels,
          datasets: [{
            label: 'At-Risk Students',
            data: barCounts,
            backgroundColor: barGradient,
            hoverBackgroundColor: barHoverGradient,
            borderRadius: 8,
            borderSkipped: false,
            barPercentage: 0.6,
            categoryPercentage: 0.7,
          }]
        },
        options: {
          plugins: {
            tooltip: {
              backgroundColor: C.textBold,
              titleFont: { size: 12, weight: '700' },
              bodyFont: { size: 11 },
              padding: { top: 10, bottom: 10, left: 14, right: 14 },
              cornerRadius: 8,
              displayColors: false,
              callbacks: {
                title: function (items) { return items[0].label; },
                label: function (ctx) {
                  return ctx.parsed.y + ' student' + (ctx.parsed.y !== 1 ? 's' : '') + ' below ' + State.attendanceThreshold + '% threshold';
                }
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { font: { size: 10, weight: '600' }, maxRotation: 0, autoSkip: false }, border: { display: false } },
            y: { beginAtZero: true, grid: { color: C.grid }, border: { display: false }, ticks: { stepSize: 1, font: { size: 11 }, padding: 8 } }
          }
        }
      });
    }
  }

  // ─── RENDER ALL (no page reload) ────────────────────────────────

  function renderAll() {
    renderStatus();
    renderClassCards();
    renderMetricCards();
    renderCharts();
    if (State.selectedClass) {
      renderRoster(State.selectedClass);
    }
    if (State.activeTab === 'history') {
      renderAlertHistory();
    }
  }

  // ─── TAB CONTROLLER ─────────────────────────────────────────────

  window.switchTab = function (tabId) {
    State.activeTab = tabId;

    document.querySelectorAll('.tab-content').forEach(function (c) { c.classList.add('hidden'); });
    var target = document.getElementById('tab-' + tabId);
    if (target) target.classList.remove('hidden');

    if (tabId === 'history') renderAlertHistory();
    if (tabId === 'stats') { renderMetricCards(); renderCharts(); }
  };

  // ─── EVENT DELEGATION ───────────────────────────────────────────

  // Class card → open roster
  document.getElementById('classes-grid').addEventListener('click', function (e) {
    var btn = e.target.closest('.view-roster-btn');
    if (!btn) return;
    var classKey = btn.dataset.class;
    State.selectedClass = classKey;
    renderRoster(classKey);
    document.getElementById('classes-grid').classList.add('hidden');
    document.getElementById('student-roster').classList.remove('hidden');
  });

  // Back to classes
  var backBtn = document.getElementById('back-to-classes');
  if (backBtn) {
    backBtn.addEventListener('click', function () {
      State.selectedClass = null;
      document.getElementById('student-roster').classList.add('hidden');
      document.getElementById('classes-grid').classList.remove('hidden');
      renderClassCards();
    });
  }

  // Search input — client-side filtering, no reload
  var searchInput = document.getElementById('student-search');
  if (searchInput) {
    var searchTimeout = null;
    searchInput.addEventListener('input', function () {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(function () {
        State.searchQuery = searchInput.value;
        if (State.selectedClass) {
          renderRoster(State.selectedClass);
        } else {
          renderClassCards();
        }
      }, 200);
    });
  }

  // Attendance threshold filter — client-side, no reload
  var threshSelect = document.getElementById('attendance-filter');
  if (threshSelect) {
    threshSelect.addEventListener('change', function () {
      State.attendanceThreshold = parseInt(threshSelect.value, 10);
      renderAll();
    });
  }

  // Refresh button
  var refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', function () {
      fetchFromFastAPI().then(renderAll);
    });
  }

  // API settings save
  var saveBtn = document.getElementById('save-settings-btn');
  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      var url = document.getElementById('api-base-url').value;
      var token = document.getElementById('api-token').value;
      var templateId = document.getElementById('api-template-id').value;
      localStorage.setItem('fastapiUrl', url);
      localStorage.setItem('apiToken', token);
      localStorage.setItem('apiTemplateId', templateId);
      FASTAPI_URL = url || 'http://127.0.0.1:8001';
      alert('Configuration saved! Fetching data...');
      fetchFromFastAPI().then(renderAll);
    });
  }

  function loadSettings() {
    var url = localStorage.getItem('fastapiUrl');
    var token = localStorage.getItem('apiToken');
    var templateId = localStorage.getItem('apiTemplateId');
    if (url) { FASTAPI_URL = url; var el = document.getElementById('api-base-url'); if (el) el.value = url; }
    if (token) { var el2 = document.getElementById('api-token'); if (el2) el2.value = token; }
    if (templateId) { var el3 = document.getElementById('api-template-id'); if (el3) el3.value = templateId; }
  }

  // ─── INIT ──────────────────────────────────────────────────────

  loadSettings();
  fetchFromFastAPI().then(renderAll);

  // Resize aurora after dashboard loads
  if (typeof window._auroraResize === 'function') {
    setTimeout(window._auroraResize, 100);
  }

})();
