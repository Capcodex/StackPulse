// NAVIGATION LOGIC
function switchView(viewId) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    // Remove active class from nav
    document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active', 'bg-zinc-900', 'text-white'));
    document.querySelectorAll('.sidebar-item').forEach(i => i.classList.add('text-zinc-400'));

    // Show selected view
    document.getElementById('view-' + viewId).classList.add('active');

    // Update Nav item style
    const activeNav = document.getElementById('nav-' + viewId);
    activeNav.classList.add('active', 'text-white');
    activeNav.classList.remove('text-zinc-400');

    // Update Header Title
    const titles = { 'feed': 'Home / Feed', 'stack': 'Workspace / My Stack', 'skillgap': 'Intelligence / Skill-Gap' };
    document.getElementById('view-title').innerText = titles[viewId];
}

// SIDE SHEET LOGIC
function openSheet(title) {
    document.getElementById('sheet-title').innerText = title;
    document.getElementById('side-sheet').classList.remove('translate-x-full');
}

function closeSheet() {
    document.getElementById('side-sheet').classList.add('translate-x-full');
}
