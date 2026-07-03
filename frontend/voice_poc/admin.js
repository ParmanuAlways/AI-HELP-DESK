// Admin console — login, then list faults raised through the help desk.

const loginCard = document.getElementById("loginCard");
const dash = document.getElementById("dash");
const loginBtn = document.getElementById("loginBtn");
const loginError = document.getElementById("loginError");
const userEl = document.getElementById("user");
const passEl = document.getElementById("pass");
const rowsEl = document.getElementById("rows");
const emptyEl = document.getElementById("empty");
const statTotal = document.getElementById("statTotal");
const statPending = document.getElementById("statPending");

let token = sessionStorage.getItem("hd_admin_token") || null;

async function api(path, opts = {}) {
  const res = await fetch(path, {
    ...opts,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: "Bearer " + token } : {}),
      ...(opts.headers || {}),
    },
  });
  if (res.status === 401) {
    showLogin("Session expired — please login again.");
    throw new Error("unauthorized");
  }
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function showLogin(message = "") {
  token = null;
  sessionStorage.removeItem("hd_admin_token");
  dash.style.display = "none";
  loginCard.style.display = "block";
  loginError.textContent = message;
}

function showDash() {
  loginCard.style.display = "none";
  dash.style.display = "block";
  refresh();
}

async function doLogin() {
  loginError.textContent = "";
  try {
    const data = await api("/api/admin/login", {
      method: "POST",
      body: JSON.stringify({ username: userEl.value.trim(), password: passEl.value }),
    });
    token = data.token;
    sessionStorage.setItem("hd_admin_token", token);
    showDash();
  } catch (e) {
    if (e.message !== "unauthorized") loginError.textContent = "Invalid username or password.";
  }
}

function fmtTime(iso) {
  if (!iso) return "—";
  const d = new Date(iso + (iso.endsWith("Z") ? "" : "Z")); // stored as UTC
  return d.toLocaleString([], { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });
}

async function refresh() {
  const [tickets, stats] = await Promise.all([
    api("/api/admin/tickets"),
    api("/api/admin/stats"),
  ]);
  statTotal.textContent = stats.total;
  statPending.textContent = stats.pending_review;

  rowsEl.innerHTML = "";
  emptyEl.style.display = tickets.length ? "none" : "block";
  for (const t of tickets) {
    const tr = document.createElement("tr");
    const cells = [
      { cls: "num", text: t.ticket_number },
      { cls: "muted", text: fmtTime(t.created_at) },
      { html: t.application ? `<span class="badge app">${esc(t.application)}</span>` : "—" },
      { text: t.fault_type || "—" },
      { text: t.severity || "—" },
      { cls: "muted", text: t.confidence != null ? t.confidence.toFixed(2) : "—" },
      { html: `<span class="badge pending">${esc(t.status)}</span>` },
      { cls: "text", text: t.raw_text || "" },
    ];
    for (const c of cells) {
      const td = document.createElement("td");
      if (c.cls) td.className = c.cls;
      if (c.html != null) td.innerHTML = c.html; else td.textContent = c.text;
      tr.appendChild(td);
    }
    rowsEl.appendChild(tr);
  }
}

function esc(s) {
  const d = document.createElement("div");
  d.textContent = String(s);
  return d.innerHTML;
}

loginBtn.addEventListener("click", doLogin);
passEl.addEventListener("keydown", (e) => { if (e.key === "Enter") doLogin(); });
document.getElementById("refreshBtn").addEventListener("click", refresh);
document.getElementById("logoutBtn").addEventListener("click", async () => {
  try { await api("/api/admin/logout", { method: "POST" }); } catch (_) {}
  showLogin("Logged out.");
});

if (token) showDash(); else showLogin();
