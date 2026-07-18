// =============================================
// CONFIGURATION
// =============================================
var API_BASE_URL = localStorage.getItem('apiBaseUrl') || 'http://127.0.0.1:8000';

// =============================================
// FALLBACK DATA (used when backend is offline)
// =============================================
var fallbackClassData = {
    'cse': {
        name: 'B.Tech CSE',
        description: 'Branch: Computer Science & Engineering',
        students: [
            { roll: '26CU0310001', name: 'Naveen', contact: '9104332181', attendance: 55 },
            { roll: '26CU0310002', name: 'Payal', contact: '9600133890', attendance: 62 },
            { roll: '26CU0310003', name: 'Preeti', contact: '9386379402', attendance: 48 },
            { roll: '26CU0310004', name: 'Lakshya', contact: '9654235116', attendance: 58 },
            { roll: '26CU0310005', name: 'Dhruv', contact: '9559407816', attendance: 65 },
            { roll: '26CU0310006', name: 'Kabir', contact: '9849593103', attendance: 52 },
            { roll: '26CU0310007', name: 'Vanshika', contact: '9413164752', attendance: 60 },
            { roll: '26CU0310008', name: 'Tanish', contact: '9534192832', attendance: 45 },
            { roll: '26CU0310009', name: 'Suman', contact: '9648350305', attendance: 92 },
            { roll: '26CU0310010', name: 'Pallavi', contact: '9413953767', attendance: 88 },
            { roll: '26CU0310011', name: 'Devansh', contact: '9423884969', attendance: 95 },
            { roll: '26CU0310012', name: 'Raghav', contact: '9328710122', attendance: 90 },
            { roll: '26CU0310013', name: 'Girish', contact: '9691669784', attendance: 87 },
            { roll: '26CU0310014', name: 'Sneha', contact: '9018451462', attendance: 93 },
            { roll: '26CU0310015', name: 'Vidya', contact: '9048281489', attendance: 78 },
            { roll: '26CU0310016', name: 'Saanvi', contact: '9252880957', attendance: 82 },
            { roll: '26CU0310017', name: 'Aditya', contact: '9154303911', attendance: 80 },
            { roll: '26CU0310018', name: 'Palak', contact: '9718227824', attendance: 76 },
            { roll: '26CU0310019', name: 'Ravi', contact: '9963834657', attendance: 79 },
            { roll: '26CU0310020', name: 'Sanjay', contact: '9713315098', attendance: 83 },
            { roll: '26CU0310021', name: 'Anika', contact: '9930103105', attendance: 75 },
            { roll: '26CU0310022', name: 'Rohan', contact: '9834738299', attendance: 75 },
            { roll: '26CU0310023', name: 'Kunal', contact: '9376311656', attendance: 75 },
            { roll: '26CU0310024', name: 'Snehal', contact: '9701065133', attendance: 75 },
            { roll: '26CU0310025', name: 'Myra', contact: '9872624731', attendance: 75 },
            { roll: '26CU0310026', name: 'Radhika', contact: '9810801326', attendance: 75 },
            { roll: '26CU0310027', name: 'Vikram', contact: '9736026064', attendance: 75 }
        ]
    },
    'aero': {
        name: 'B.Tech AERO',
        description: 'Branch: Aerospace Engineering',
        students: [
            { roll: '26AU0310001', name: 'Shreya', contact: '9687234309', attendance: 63 },
            { roll: '26AU0310002', name: 'Ritika', contact: '9805009788', attendance: 50 },
            { roll: '26AU0310003', name: 'Ananya', contact: '9081219136', attendance: 57 },
            { roll: '26AU0310004', name: 'Sarthak', contact: '9939909169', attendance: 42 },
            { roll: '26AU0310005', name: 'Komal', contact: '9854353462', attendance: 68 },
            { roll: '26AU0310006', name: 'Tarun', contact: '9475107991', attendance: 55 },
            { roll: '26AU0310007', name: 'Ajay', contact: '9384251354', attendance: 47 },
            { roll: '26AU0310008', name: 'Vishal', contact: '9498084124', attendance: 61 },
            { roll: '26AU0310009', name: 'Yash', contact: '9182449353', attendance: 89 },
            { roll: '26AU0310010', name: 'Sanya', contact: '9874016400', attendance: 91 },
            { roll: '26AU0310011', name: 'Varun', contact: '9242786801', attendance: 96 },
            { roll: '26AU0310012', name: 'Mohit', contact: '9280598262', attendance: 88 },
            { roll: '26AU0310013', name: 'Sai', contact: '9450533158', attendance: 94 },
            { roll: '26AU0310014', name: 'Nandini', contact: '9356159514', attendance: 87 },
            { roll: '26AU0310015', name: 'Isha', contact: '9232260256', attendance: 77 },
            { roll: '26AU0310016', name: 'Aman', contact: '9433036541', attendance: 81 },
            { roll: '26AU0310017', name: 'Nisha', contact: '9586850142', attendance: 84 },
            { roll: '26AU0310018', name: 'Anjali', contact: '9401965569', attendance: 76 },
            { roll: '26AU0310019', name: 'Manish', contact: '9169340608', attendance: 82 },
            { roll: '26AU0310020', name: 'Neha', contact: '9421607337', attendance: 79 },
            { roll: '26AU0310021', name: 'Deepak', contact: '9465648236', attendance: 75 },
            { roll: '26AU0310022', name: 'Ayush', contact: '9299468044', attendance: 75 },
            { roll: '26AU0310023', name: 'Aadhya', contact: '9699577738', attendance: 75 },
            { roll: '26AU0310024', name: 'Diya', contact: '9148951343', attendance: 75 },
            { roll: '26AU0310025', name: 'Vihaan', contact: '9037917693', attendance: 75 },
            { roll: '26AU0310026', name: 'Juhi', contact: '9676320163', attendance: 75 },
            { roll: '26AU0310027', name: 'Ishita', contact: '9870831727', attendance: 75 }
        ]
    },
    'it': {
        name: 'B.Tech IT',
        description: 'Branch: Information Technology',
        students: [
            { roll: '26IT0310001', name: 'Rashi', contact: '9579868727', attendance: 59 },
            { roll: '26IT0310002', name: 'Namrata', contact: '9434873471', attendance: 53 },
            { roll: '26IT0310003', name: 'Pooja', contact: '9455812236', attendance: 66 },
            { roll: '26IT0310004', name: 'Harsh', contact: '9316658760', attendance: 44 },
            { roll: '26IT0310005', name: 'Ritu', contact: '9690967054', attendance: 87 },
            { roll: '26IT0310006', name: 'Tanya', contact: '9668893734', attendance: 90 },
            { roll: '26IT0310007', name: 'Bhavna', contact: '9706562729', attendance: 88 },
            { roll: '26IT0310008', name: 'Divya', contact: '9990162720', attendance: 92 },
            { roll: '26IT0310009', name: 'Nikhil', contact: '9375564641', attendance: 86 },
            { roll: '26IT0310010', name: 'Sakshi', contact: '9805310033', attendance: 95 },
            { roll: '26IT0310011', name: 'Rudra', contact: '9719374529', attendance: 89 },
            { roll: '26IT0310012', name: 'Vaishnavi', contact: '9124190496', attendance: 91 },
            { roll: '26IT0310013', name: 'Rajat', contact: '9314919058', attendance: 78 },
            { roll: '26IT0310014', name: 'Swati', contact: '9518506716', attendance: 83 },
            { roll: '26IT0310015', name: 'Bhavya', contact: '9262849877', attendance: 80 },
            { roll: '26IT0310016', name: 'Tanvi', contact: '9531473799', attendance: 77 },
            { roll: '26IT0310017', name: 'Siddharth', contact: '9075273545', attendance: 81 },
            { roll: '26IT0310018', name: 'Vivaan', contact: '9831367837', attendance: 79 },
            { roll: '26IT0310019', name: 'Suraj', contact: '9770143634', attendance: 76 },
            { roll: '26IT0310020', name: 'Pranav', contact: '9957885685', attendance: 82 },
            { roll: '26IT0310021', name: 'Gaurav', contact: '9744431351', attendance: 75 },
            { roll: '26IT0310022', name: 'Urvashi', contact: '9233749894', attendance: 75 },
            { roll: '26IT0310023', name: 'Kritika', contact: '9352408240', attendance: 75 },
            { roll: '26IT0310024', name: 'Reyansh', contact: '9842710947', attendance: 75 },
            { roll: '26IT0310025', name: 'Rahul', contact: '9752047116', attendance: 75 },
            { roll: '26IT0310026', name: 'Shalini', contact: '9022941318', attendance: 75 }
        ]
    }
};

// =============================================
// APPLICATION STATE
// =============================================
var classData = {};
var usingFallback = false;

// =============================================
// AUTHENTICATION HANDLER
// =============================================
document.getElementById('login-btn').addEventListener('click', function() {
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('dashboard-container').classList.remove('hidden');
    document.body.classList.remove('items-center', 'justify-center');
    if (typeof window._auroraResize === 'function') {
        setTimeout(window._auroraResize, 50);
    }
});

window.triggerLogout = function() {
    document.getElementById('dashboard-container').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
    document.body.classList.add('items-center', 'justify-center');
};

var logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', window.triggerLogout);
}

// =============================================
// TAB CONTROLLER
// =============================================
window.switchTab = function(tabId) {
    var tabs = document.querySelectorAll('.tab-link');
    tabs.forEach(function(t) { 
        if (t.dataset.tab === tabId) {
            t.classList.add('bg-orange-500');
        } else {
            t.classList.remove('bg-orange-500');
        }
    });

    document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.add('hidden'); });
    var targetTab = document.getElementById('tab-' + tabId);
    if (targetTab) {
        targetTab.classList.remove('hidden');
    }
};

var tabs = document.querySelectorAll('.tab-link');
tabs.forEach(function(link) {
    link.addEventListener('click', function() {
        window.switchTab(link.dataset.tab);
    });
});

// =============================================
// API DATA FETCHING (with silent fallback)
// =============================================
window.fetchData = async function() {
    try {
        var sectionsRes = await fetch(API_BASE_URL + '/api/sections/');
        var studentsRes = await fetch(API_BASE_URL + '/api/students/');
        if (!sectionsRes.ok || !studentsRes.ok) throw new Error();
        var apiSections = await sectionsRes.json();
        var apiStudents = await studentsRes.json();
        if (apiSections.length === 0 && apiStudents.length === 0) throw new Error();
        document.getElementById('backend-status').textContent = 'Online';
        document.getElementById('backend-status').className = 'text-orange-700 bg-orange-100 px-3 py-1 rounded-full text-xs font-bold mr-24';
        usingFallback = false;
        classData = {};
        apiSections.forEach(function(sec) {
            var key = sec.name.toLowerCase().replace(/[^a-z]/g, '').replace('btch', '').replace('tech', '');
            if (key.indexOf('cse') !== -1) key = 'cse';
            else if (key.indexOf('aero') !== -1) key = 'aero';
            else if (key.indexOf('it') !== -1) key = 'it';
            else key = sec.name;
            classData[key] = { name: sec.name, description: sec.description || '', students: [] };
        });
        apiStudents.forEach(function(stu) {
            var prefix = stu.roll.substring(0, 5);
            var matched = false;
            Object.keys(classData).forEach(function(k) {
                if (classData[k].name.indexOf('CSE') !== -1 && prefix.indexOf('CU') !== -1) { classData[k].students.push(stu); matched = true; }
                else if (classData[k].name.indexOf('AERO') !== -1 && prefix.indexOf('AU') !== -1) { classData[k].students.push(stu); matched = true; }
                else if (classData[k].name.indexOf('IT') !== -1 && prefix.indexOf('IT') !== -1) { classData[k].students.push(stu); matched = true; }
            });
            if (!matched) {
                var firstKey = Object.keys(classData)[0];
                if (firstKey) classData[firstKey].students.push(stu);
            }
        });
    } catch (err) {
        classData = fallbackClassData;
        usingFallback = true;
        document.getElementById('backend-status').textContent = 'Offline';
        document.getElementById('backend-status').className = 'text-gray-500 bg-gray-100 px-3 py-1 rounded-full text-xs font-bold mr-24';
    }
    renderClassCards();
};

// =============================================
// CLASS CARDS RENDERER
// =============================================
function renderClassCards() {
    var grid = document.getElementById('classes-grid');
    var keys = Object.keys(classData);
    if (keys.length === 0) {
        grid.innerHTML = '';
        return;
    }
    var html =
        '<h2 class="text-xl font-bold text-gray-800 mb-4">Your Classes Overview</h2>' +
        '<p class="text-sm text-gray-500 mb-6">Select a section profile card below to view specific student records.</p>' +
        '<div class="grid grid-cols-1 md:grid-cols-3 gap-6">';
    keys.forEach(function(key) {
        var data = classData[key];
        var count = data.students.length;
        html +=
            '<div class="bg-white rounded-xl shadow p-6 border-l-4 border-orange-500">' +
                '<span class="inline-block bg-orange-100 text-orange-800 text-xs font-bold px-3 py-1 rounded-full mb-3">' + count + ' Students</span>' +
                '<h3 class="text-lg font-bold text-gray-800">' + data.name + '</h3>' +
                '<p class="text-sm text-gray-500 mt-1">' + (data.description || '') + '</p>' +
                '<button class="view-roster-btn mt-4 w-full bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-md text-sm transition" data-class="' + key + '">View Student Roster</button>' +
            '</div>';
    });
    html += '</div>';
    grid.innerHTML = html;
}

// =============================================
// ROSTER VIEW CONTROLLER
// =============================================
document.getElementById('classes-grid').addEventListener('click', function(e) {
    if (e.target.classList.contains('view-roster-btn')) {
        var classKey = e.target.dataset.class;
        var data = classData[classKey];
        if (!data) return;
        renderRoster(data);
        document.getElementById('classes-grid').classList.add('hidden');
        document.getElementById('student-roster').classList.remove('hidden');
    }
});

document.getElementById('back-to-classes').addEventListener('click', function() {
    document.getElementById('student-roster').classList.add('hidden');
    document.getElementById('classes-grid').classList.remove('hidden');
});

function renderRoster(data) {
    document.getElementById('roster-title').textContent = data.name + ' - Student Roster';
    var tbody = document.getElementById('roster-body');
    if (!data.students || data.students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="px-4 py-8 text-center text-gray-400">No students in this section.</td></tr>';
        return;
    }
    var html = '';
    data.students.forEach(function(s) {
        var isSafe = s.attendance >= 75;
        var statusBadge = isSafe
            ? '<span class="inline-block bg-green-100 text-green-700 text-xs font-semibold px-2 py-0.5 rounded-full">Safe</span>'
            : '<span class="inline-block bg-red-100 text-red-700 text-xs font-semibold px-2 py-0.5 rounded-full">At Risk</span>';
        var actionBtn = isSafe
            ? '<span class="text-gray-400 text-xs">--</span>'
            : '<button class="bg-orange-500 hover:bg-orange-600 text-white text-xs px-3 py-1 rounded">Send SMS Alert</button>';
        html += '<tr>' +
            '<td class="px-4 py-3">' + s.roll + '</td>' +
            '<td class="px-4 py-3 font-medium text-gray-800">' + s.name + '</td>' +
            '<td class="px-4 py-3 text-gray-600">' + s.contact + '</td>' +
            '<td class="px-4 py-3">' + s.attendance + '%</td>' +
            '<td class="px-4 py-3">' + statusBadge + '</td>' +
            '<td class="px-4 py-3">' + actionBtn + '</td>' +
            '</tr>';
    });
    tbody.innerHTML = html;
}

// =============================================
// API STORAGE MANAGER
// =============================================
document.getElementById('save-settings-btn').addEventListener('click', function() {
    var baseUrl = document.getElementById('api-base-url').value;
    var token = document.getElementById('api-token').value;
    var templateId = document.getElementById('api-template-id').value;

    localStorage.setItem('apiBaseUrl', baseUrl);
    localStorage.setItem('apiToken', token);
    localStorage.setItem('apiTemplateId', templateId);

    API_BASE_URL = baseUrl || 'http://127.0.0.1:8000';
    alert('API Gateway Configuration saved successfully!');
});

function loadApiSettings() {
    var baseUrl = localStorage.getItem('apiBaseUrl');
    var token = localStorage.getItem('apiToken');
    var templateId = localStorage.getItem('apiTemplateId');

    if (baseUrl) { document.getElementById('api-base-url').value = baseUrl; API_BASE_URL = baseUrl; }
    if (token) { document.getElementById('api-token').value = token; }
    if (templateId) { document.getElementById('api-template-id').value = templateId; }
}

// =============================================
// INIT
// =============================================
loadApiSettings();
window.fetchData();

// =============================================
// CHARTS — Alert Statistics (Chart.js v4)
// =============================================
(function initCharts() {
    if (typeof Chart === 'undefined') return;

    // ---- Color Palette (matches #F38B1C theme) ----
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
        green:      '#22c55e',
        greenLt:    'rgba(34,197,94,0.18)',
        red:        '#ef4444',
        redLt:      'rgba(239,68,68,0.18)',
    };

    // ---- Global Chart.js defaults ----
    Chart.defaults.font.family = "'Inter', 'Segoe UI', system-ui, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = C.text;
    Chart.defaults.plugins.legend.display = false;
    Chart.defaults.responsive = true;
    Chart.defaults.maintainAspectRatio = false;

    // ---- Mock Data (swap with API fetch later) ----
    // Line chart: daily alert volume derived from alert history
    var lineLabels  = ['Jul 06', 'Jul 07', 'Jul 08', 'Jul 09', 'Jul 10'];
    var lineSent    = [3, 5, 4, 4, 4];
    var lineFailed  = [0, 0, 1, 0, 0];

    // Bar chart: class-wise at-risk student count
    var barLabels = ['B.Tech CSE', 'B.Tech AERO', 'B.Tech IT'];
    var barCounts = [7, 8, 4];

    // ---- LINE CHART ----
    var lineCtx = document.getElementById('chart-alert-line');
    if (lineCtx) {
        new Chart(lineCtx, {
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
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle',
                            padding: 16,
                            font: { size: 11, weight: '600' }
                        }
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
                            title: function(items) { return 'Date: ' + items[0].label; },
                            label: function(ctx) {
                                return ' ' + ctx.dataset.label + ': ' + ctx.parsed.y + ' alerts';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 11, weight: '600' } },
                        border: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: C.grid },
                        border: { display: false },
                        ticks: {
                            stepSize: 1,
                            font: { size: 11 },
                            padding: 8
                        }
                    }
                }
            }
        });
    }

    // ---- BAR CHART ----
    var barCtx = document.getElementById('chart-subject-bar');
    if (barCtx) {
        var barGradient = barCtx.getContext('2d').createLinearGradient(0, 0, 0, 260);
        barGradient.addColorStop(0, C.primary);
        barGradient.addColorStop(1, C.accent);

        var barHoverGradient = barCtx.getContext('2d').createLinearGradient(0, 0, 0, 260);
        barHoverGradient.addColorStop(0, '#FB923C');
        barHoverGradient.addColorStop(1, C.primary);

        new Chart(barCtx, {
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
                            title: function(items) { return items[0].label; },
                            label: function(ctx) {
                                return ctx.parsed.y + ' student' + (ctx.parsed.y !== 1 ? 's' : '') + ' below 75% threshold';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            font: { size: 10, weight: '600' },
                            maxRotation: 0,
                            autoSkip: false
                        },
                        border: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: C.grid },
                        border: { display: false },
                        ticks: {
                            stepSize: 1,
                            font: { size: 11 },
                            padding: 8
                        }
                    }
                }
            }
        });
    }
})();
