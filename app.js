// =============================================
// AUTHENTICATION HANDLER
// =============================================
document.getElementById('login-btn').addEventListener('click', function() {
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('dashboard-container').classList.remove('hidden');
    document.body.classList.remove('items-center', 'justify-center');
});

document.getElementById('logout-btn').addEventListener('click', function() {
    document.getElementById('dashboard-container').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
    document.body.classList.add('items-center', 'justify-center');
});

// =============================================
// TAB CONTROLLER
// =============================================
var tabs = document.querySelectorAll('.tab-link');
tabs.forEach(function(link) {
    link.addEventListener('click', function() {
        tabs.forEach(function(t) { t.classList.remove('bg-amber-500'); });
        link.classList.add('bg-amber-500');

        document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.add('hidden'); });
        document.getElementById('tab-' + link.dataset.tab).classList.remove('hidden');
    });
});

// =============================================
// ROSTER DATA
// =============================================
var classData = {
    'cse-a': {
        name: 'B.Tech CSE - Section A',
        students: [
            { roll: 'CS101', name: 'Aarav Kumar', contact: '+91-9876543210', attendance: 82 },
            { roll: 'CS102', name: 'Priya Singh', contact: '+91-9876543211', attendance: 65 },
            { roll: 'CS103', name: 'Rohit Verma', contact: '+91-9876543212', attendance: 91 },
            { roll: 'CS104', name: 'Sneha Reddy', contact: '+91-9876543213', attendance: 48 },
            { roll: 'CS105', name: 'Ankit Joshi', contact: '+91-9876543214', attendance: 76 }
        ]
    },
    'cse-b': {
        name: 'B.Tech CSE - Section B',
        students: [
            { roll: 'CS201', name: 'Neha Kapoor', contact: '+91-9876543220', attendance: 73 },
            { roll: 'CS202', name: 'Vikram Patel', contact: '+91-9876543221', attendance: 88 },
            { roll: 'CS203', name: 'Ishita Gupta', contact: '+91-9876543222', attendance: 54 },
            { roll: 'CS204', name: 'Rahul Sharma', contact: '+91-9876543223', attendance: 79 },
            { roll: 'CS205', name: 'Divya Nair', contact: '+91-9876543224', attendance: 60 }
        ]
    },
    'it-a': {
        name: 'B.Tech IT - Section A',
        students: [
            { roll: 'IT301', name: 'Arjun Mehta', contact: '+91-9876543230', attendance: 95 },
            { roll: 'IT302', name: 'Kriti Bhatia', contact: '+91-9876543231', attendance: 80 },
            { roll: 'IT303', name: 'Manish Yadav', contact: '+91-9876543232', attendance: 72 },
            { roll: 'IT304', name: 'Pooja Desai', contact: '+91-9876543233', attendance: 89 },
            { roll: 'IT305', name: 'Saurabh Jain', contact: '+91-9876543234', attendance: 66 }
        ]
    }
};

// =============================================
// ROSTER VIEW CONTROLLER
// =============================================
document.querySelectorAll('.view-roster-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var classKey = btn.dataset.class;
        var data = classData[classKey];

        document.getElementById('roster-title').textContent = data.name + ' - Student Roster';

        var tbody = document.getElementById('roster-body');
        tbody.innerHTML = '';

        data.students.forEach(function(s) {
            var isSafe = s.attendance >= 75;
            var statusBadge = isSafe
                ? '<span class="inline-block bg-green-100 text-green-700 text-xs font-semibold px-2 py-0.5 rounded-full">Safe</span>'
                : '<span class="inline-block bg-red-100 text-red-700 text-xs font-semibold px-2 py-0.5 rounded-full">At Risk</span>';
            var actionBtn = isSafe
                ? '<span class="text-gray-400 text-xs">--</span>'
                : '<button class="bg-amber-500 hover:bg-amber-600 text-white text-xs px-3 py-1 rounded">Send WhatsApp Alert</button>';

            tbody.innerHTML += '<tr>' +
                '<td class="px-4 py-3">' + s.roll + '</td>' +
                '<td class="px-4 py-3 font-medium text-gray-800">' + s.name + '</td>' +
                '<td class="px-4 py-3 text-gray-600">' + s.contact + '</td>' +
                '<td class="px-4 py-3">' + s.attendance + '%</td>' +
                '<td class="px-4 py-3">' + statusBadge + '</td>' +
                '<td class="px-4 py-3">' + actionBtn + '</td>' +
                '</tr>';
        });

        document.getElementById('classes-grid').classList.add('hidden');
        document.getElementById('student-roster').classList.remove('hidden');
    });
});

document.getElementById('back-to-classes').addEventListener('click', function() {
    document.getElementById('student-roster').classList.add('hidden');
    document.getElementById('classes-grid').classList.remove('hidden');
});

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

    alert('API Gateway Configuration saved successfully!');
});

function loadApiSettings() {
    var baseUrl = localStorage.getItem('apiBaseUrl');
    var token = localStorage.getItem('apiToken');
    var templateId = localStorage.getItem('apiTemplateId');

    if (baseUrl) { document.getElementById('api-base-url').value = baseUrl; }
    if (token) { document.getElementById('api-token').value = token; }
    if (templateId) { document.getElementById('api-template-id').value = templateId; }
}

loadApiSettings();
