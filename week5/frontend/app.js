async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// ---------- Notes (with optimistic UI) ----------

let notesState = [];

async function loadNotes() {
  notesState = await fetchJSON('/notes/');
  renderNotes();
}

function renderNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  for (const n of notesState) {
    list.appendChild(makeNoteItem(n));
  }
}

function makeNoteItem(n) {
  const li = document.createElement('li');
  li.dataset.id = String(n.id);

  const span = document.createElement('span');
  span.textContent = `${n.title}: ${n.content}`;

  const editBtn = document.createElement('button');
  editBtn.textContent = 'Edit';
  editBtn.onclick = () => startEdit(li, n);

  const delBtn = document.createElement('button');
  delBtn.textContent = 'Delete';
  delBtn.onclick = () => deleteNote(n.id, li);

  li.append(span, ' ', editBtn, ' ', delBtn);
  return li;
}

function startEdit(li, n) {
  li.innerHTML = '';

  const titleInput = document.createElement('input');
  titleInput.value = n.title;

  const contentInput = document.createElement('input');
  contentInput.value = n.content;

  const saveBtn = document.createElement('button');
  saveBtn.textContent = 'Save';
  saveBtn.onclick = () =>
    saveEdit(n.id, titleInput.value.trim(), contentInput.value.trim(), li, n);

  const cancelBtn = document.createElement('button');
  cancelBtn.textContent = 'Cancel';
  cancelBtn.onclick = () => li.replaceWith(makeNoteItem(n));

  li.append(titleInput, ' ', contentInput, ' ', saveBtn, ' ', cancelBtn);
}

async function saveEdit(id, title, content, li, original) {
  // Optimistic: apply new values to DOM and state immediately
  const idx = notesState.findIndex((n) => n.id === id);
  const optimistic = { id, title, content };
  notesState[idx] = optimistic;
  const newLi = makeNoteItem(optimistic);
  li.replaceWith(newLi);

  try {
    const result = await fetchJSON(`/notes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    const newIdx = notesState.findIndex((n) => n.id === id);
    notesState[newIdx] = result;
    newLi.replaceWith(makeNoteItem(result));
  } catch (err) {
    // Rollback
    const newIdx = notesState.findIndex((n) => n.id === id);
    notesState[newIdx] = original;
    newLi.replaceWith(makeNoteItem(original));
    alert('Update failed: ' + err.message);
  }
}

async function deleteNote(id, li) {
  const idx = notesState.findIndex((n) => n.id === id);
  const [removed] = notesState.splice(idx, 1);
  // Optimistic: remove from DOM immediately
  li.remove();

  try {
    const res = await fetch(`/notes/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error(await res.text());
  } catch (err) {
    // Rollback: re-insert note and re-render
    notesState.splice(idx, 0, removed);
    renderNotes();
    alert('Delete failed: ' + err.message);
  }
}

// ---------- Action Items ----------

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  loadNotes();
  loadActions();
});
