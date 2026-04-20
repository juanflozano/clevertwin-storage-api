const API_URL = "https://howehwhis6.execute-api.us-east-1.amazonaws.com"
let token = null

async function login() {
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })

    if (response.ok) {
        const data = await response.json()
        token = data.access_token
        const company = JSON.parse(atob(token.split(".")[1])).sub
        document.getElementById("company-name").textContent = company
        document.getElementById("login-section").style.display = "none"
        document.getElementById("events-section").style.display = "block"
        loadEvents()
    } else {
        document.getElementById("login-error").textContent = "Invalid credentials"
    }
}

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'))
    document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none')
    
    document.getElementById(`tab-${tab}`).style.display = 'block'
    event.target.classList.add('active')
}

async function loadEvents() {
    const response = await fetch(`${API_URL}/events`, {
        headers: { "Authorization": `Bearer ${token}` }
    })
    const events = await response.json()
    const tbody = document.getElementById("events-body")
    tbody.innerHTML = ""
    events.forEach(event => {
    tbody.innerHTML += `
        <tr>
            <td>${event.id}</td>
            <td>${event.company}</td>
            <td>${event.event_type}</td>
            <td>${event.file_size}</td>
            <td>${event.file_type}</td>
            <td>
                <button class="delete-btn" onclick="deleteEvent(${event.id})">Delete</button>
            </td>
        </tr>
    `
    })
}

function logout() {
    token = null
    document.getElementById("login-section").style.display = "block"
    document.getElementById("events-section").style.display = "none"
    document.getElementById("email").value = ""
    document.getElementById("password").value = ""
}

async function registerEvent() {
    const event_type = document.getElementById("new-event-type").value
    const file_size = parseInt(document.getElementById("new-file-size").value)
    const file_type = document.getElementById("new-file-type").value

    const company = JSON.parse(atob(token.split(".")[1])).sub

    const response = await fetch(`${API_URL}/events`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ company, event_type, file_size, file_type })
    })

    if (response.ok) {
        document.getElementById("new-file-size").value = ""
        loadEvents()
    } else {
        document.getElementById("create-error").textContent = "Error registering event"
    }
}

async function deleteEvent(id) {
    const response = await fetch(`${API_URL}/events/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })

    if (response.ok) {
        loadEvents()
    }
}

async function registerCompany() {
    const company = document.getElementById("reg-company").value
    const email = document.getElementById("reg-email").value
    const password = document.getElementById("reg-password").value

    const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, email, password })
    })

    const data = await response.json()

    if (response.ok) {
        document.getElementById("register-message").style.color = "#00d4ff"
        document.getElementById("register-message").textContent = "Company registered successfully. You can now login."
        document.getElementById("reg-company").value = ""
        document.getElementById("reg-email").value = ""
        document.getElementById("reg-password").value = ""
    } else {
        document.getElementById("register-message").style.color = "#ff4d4d"
        document.getElementById("register-message").textContent = data.detail
    }
}