const API = '';  // mismo dominio, sin slash final
let token = localStorage.getItem('token');
let currentUser = JSON.parse(localStorage.getItem('user') || 'null');

// ── INIT ──
document.addEventListener('DOMContentLoaded', () => {
  if (token && currentUser) showApp();
});

// ── MODAL ──
function openModal(tab) {
  document.getElementById('authModal').classList.add('open');
  switchTab(tab);
}

function closeModal() {
  document.getElementById('authModal').classList.remove('open');
}

function switchTab(tab) {
  document.getElementById('formLogin').style.display = tab === 'login' ? 'block' : 'none';
  document.getElementById('formRegister').style.display = tab === 'register' ? 'block' : 'none';
  document.getElementById('tabLogin').className = 'tab-btn' + (tab === 'login' ? ' active' : '');
  document.getElementById('tabRegister').className = 'tab-btn' + (tab === 'register' ? ' active' : '');
}

// ── TOAST ──
function showToast(msg, type = 'success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = `toast ${type}`;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 3500);
}

// ── AUTH ──
async function register() {
  const nombre = document.getElementById('regName').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;
  if (!nombre || !email || !password) return showToast('Completa todos los campos', 'error');
  try {
    const r = await fetch(`${API}/auth/registro`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, email, password })
    });
    if (!r.ok) { const e = await r.json(); throw new Error(e.detail || 'Error'); }
    showToast('¡Cuenta creada! Inicia sesión 🎉');
    switchTab('login');
    document.getElementById('loginEmail').value = email;
  } catch (e) { showToast(e.message, 'error'); }
}

async function login() {
  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;
  if (!email || !password) return showToast('Completa todos los campos', 'error');
  try {
    const form = new FormData();
    form.append('username', email);
    form.append('password', password);
    const r = await fetch(`${API}/auth/login`, { method: 'POST', body: form });
    if (!r.ok) throw new Error('Credenciales inválidas');
    const data = await r.json();
    token = data.access_token;
    localStorage.setItem('token', token);
    currentUser = { email, nombre: email.split('@')[0] };
    localStorage.setItem('user', JSON.stringify(currentUser));
    closeModal();
    showApp();
    showToast('¡Bienvenido de vuelta! 👨‍🍳');
  } catch (e) { showToast(e.message, 'error'); }
}

function logout() {
  token = null; currentUser = null;
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  document.getElementById('app').style.display = 'none';
  document.getElementById('hero').style.display = 'flex';
  document.getElementById('navActions').innerHTML = `
    <button class="btn-nav btn-outline" onclick="openModal('login')">Iniciar sesión</button>
    <button class="btn-nav btn-solid" onclick="openModal('register')">Registrarse</button>
  `;
  showToast('Sesión cerrada');
}

function showApp() {
  document.getElementById('hero').style.display = 'none';
  document.getElementById('app').style.display = 'block';
  document.getElementById('navActions').innerHTML =
    `<span style="font-size:0.85rem;color:var(--text-muted)">${currentUser?.email || ''}</span>`;
  const name = currentUser?.nombre || 'Chef';
  document.getElementById('userAvatar').textContent = name.charAt(0).toUpperCase();
  document.getElementById('userName').textContent = name.charAt(0).toUpperCase() + name.slice(1);
  document.getElementById('userEmail').textContent = currentUser?.email || '';
  loadIngredients();
  loadRecipes();
}

// ── INGREDIENTS ──
async function loadIngredients() {
  const r = await fetch(`${API}/ingredientes/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!r.ok) return;
  renderIngredients(await r.json());
}

function renderIngredients(ings) {
  const list = document.getElementById('ingredientList');
  if (!ings.length) {
    list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-muted);font-size:0.85rem">Sin ingredientes aún</div>';
    return;
  }
  list.innerHTML = ings.map(i => `
    <div class="ingredient-item">
      <div>
        <div class="ing-name">${i.nombre}</div>
        ${i.cantidad ? `<div class="ing-detail">${i.cantidad}${i.unidad ? ' ' + i.unidad : ''}</div>` : ''}
      </div>
      <button class="btn-del" onclick="deleteIngredient(${i.id})">✕</button>
    </div>
  `).join('');
}

async function addIngredient() {
  const input = document.getElementById('ingName');
  const nombre = input.value.trim();
  if (!nombre) return;
  try {
    const r = await fetch(`${API}/ingredientes/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ nombre })
    });
    if (!r.ok) throw new Error('Error');
    input.value = '';
    loadIngredients();
  } catch (e) { showToast('No se pudo agregar', 'error'); }
}

async function deleteIngredient(id) {
  await fetch(`${API}/ingredientes/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
  loadIngredients();
}

// ── RECIPES ──
async function loadRecipes() {
  const r = await fetch(`${API}/recetas/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!r.ok) return;
  renderRecipes(await r.json());
}

function renderRecipes(recipes) {
  const grid = document.getElementById('recipesGrid');
  if (!recipes.length) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">👨‍🍳</div>
        <h3>¡Aún no hay recetas!</h3>
        <p>Agrega ingredientes y presiona "Generar receta"<br>para que la IA cree algo delicioso para ti.</p>
      </div>`;
    return;
  }
  grid.innerHTML = recipes.map(r => {
    const ings = JSON.parse(r.ingredientes_json || '[]');
    const pasos = JSON.parse(r.pasos_json || '[]');
    const date = new Date(r.created_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'long' });
    return `
    <div class="recipe-card" id="card-${r.id}">
      <div class="recipe-header">
        <div>
          <div class="recipe-meta">
            ${r.tiempo_estimado ? `<span class="badge badge-time">⏱ ${r.tiempo_estimado}</span>` : ''}
            ${r.nivel_dificultad ? `<span class="badge badge-diff">📊 ${r.nivel_dificultad}</span>` : ''}
          </div>
          <div class="recipe-name">${r.nombre_plato}</div>
          <div class="recipe-date">${date}</div>
        </div>
        <div class="recipe-actions">
          <button class="btn-icon" onclick="deleteRecipe(${r.id})" title="Eliminar">🗑</button>
        </div>
      </div>
      <div class="recipe-body">
        <button class="recipe-toggle" onclick="toggleRecipe(${r.id})">
          <span id="toggle-text-${r.id}">Ver receta completa</span> ↓
        </button>
        <div class="recipe-details" id="details-${r.id}">
          <div class="details-grid">
            <div class="details-section">
              <h4>Ingredientes</h4>
              <ul>${ings.map(i => `<li>${i.nombre}${i.cantidad ? ` — ${i.cantidad}${i.unidad ? ' ' + i.unidad : ''}` : ''}</li>`).join('')}</ul>
            </div>
            <div class="details-section">
              <h4>Preparación</h4>
              <ul class="steps-list">${pasos.map(p => `<li>${p}</li>`).join('')}</ul>
            </div>
          </div>
          <div class="stars-row">
            <span>Calificar:</span>
            ${[1, 2, 3, 4, 5].map(s => `<button class="star-btn" onclick="rateRecipe(${r.id},${s})" id="star-${r.id}-${s}">☆</button>`).join('')}
          </div>
        </div>
      </div>
    </div>`;
  }).join('');
}

function toggleRecipe(id) {
  const det = document.getElementById(`details-${id}`);
  const txt = document.getElementById(`toggle-text-${id}`);
  det.classList.toggle('open');
  txt.textContent = det.classList.contains('open') ? 'Ocultar receta' : 'Ver receta completa';
}

async function generateRecipe() {
  const btn = document.getElementById('btnGenerate');
  const card = document.getElementById('generatingCard');
  btn.disabled = true;
  document.getElementById('genText').textContent = 'Generando...';
  card.style.display = 'block';
  try {
    const r = await fetch(`${API}/recetas/generar`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!r.ok) { const e = await r.json(); throw new Error(e.detail || 'Error al generar'); }
    showToast('¡Receta generada! 🍽', 'success');
    loadRecipes();
  } catch (e) { showToast(e.message, 'error'); }
  finally {
    btn.disabled = false;
    document.getElementById('genText').textContent = 'Generar receta';
    card.style.display = 'none';
  }
}

async function deleteRecipe(id) {
  if (!confirm('¿Eliminar esta receta?')) return;
  await fetch(`${API}/recetas/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
  showToast('Receta eliminada');
  loadRecipes();
}

async function rateRecipe(recipeId, stars) {
  try {
    const r = await fetch(`${API}/recetas/${recipeId}/calificar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ estrellas: stars })
    });
    if (!r.ok) throw new Error();
    for (let i = 1; i <= 5; i++) {
      const s = document.getElementById(`star-${recipeId}-${i}`);
      if (s) s.textContent = i <= stars ? '★' : '☆';
    }
    showToast(`Calificado con ${stars} estrella${stars > 1 ? 's' : ''}! ⭐`);
  } catch (e) { showToast('Error al calificar', 'error'); }
}
