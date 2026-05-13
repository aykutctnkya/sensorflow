const API_BASE = 'http://localhost:8000/api';
const WS_URL = 'ws://127.0.0.1:8000/ws/sensor-data/';

let accessToken = null;
let ws = null;

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE}/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            alert('Login failed');
            return;
        }

        const data = await response.json();
        accessToken = data.access;

        document.getElementById('login-section').style.display = 'none';
        document.getElementById('dashboard').style.display = 'grid';

        loadDevices();
        loadAlerts();
        connectWebSocket();
    } catch (error) {
        alert('Connection error: ' + error.message);
    }
}

async function apiGet(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
    });
    return response.json();
}

async function loadDevices() {
    const devices = await apiGet('/devices/');
    const list = document.getElementById('devices-list');
    list.innerHTML = devices.map(d => `
        <div class="device-item">
            <strong>${d.name}</strong><br>
            <small>${d.location || 'No location'}</small><br>
            <small>${d.is_active ? '🟢 Active' : '🔴 Inactive'}</small>
        </div>
    `).join('');
}

async function loadAlerts() {
    const response = await apiGet('/alerts/?is_resolved=false');
    const alerts = response.results || response;
    const list = document.getElementById('alerts-list');
    list.innerHTML = alerts.map(a => `
        <div class="alert-item ${a.severity}">
            <strong>${a.severity.toUpperCase()}</strong>
            <div>${a.message}</div>
            <div class="timestamp">${new Date(a.created_at).toLocaleString()}</div>
        </div>
    `).join('') || '<p>No active alerts</p>';
}

function connectWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        document.getElementById('connection-status').textContent = 'Connected';
        document.getElementById('connection-status').className = 'status connected';
    };

    ws.onclose = () => {
        document.getElementById('connection-status').textContent = 'Disconnected';
        document.getElementById('connection-status').className = 'status disconnected';
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const liveData = document.getElementById('live-data');

        const item = document.createElement('div');
        item.className = 'data-item';
        item.innerHTML = `
            <strong>${data.value} ${data.unit}</strong>
            <div class="timestamp">${new Date(data.timestamp).toLocaleString()}</div>
        `;

        liveData.insertBefore(item, liveData.firstChild);

        if (liveData.children.length > 10) {
            liveData.removeChild(liveData.lastChild);
        }

        loadAlerts();
    };
}