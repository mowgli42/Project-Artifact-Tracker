// API base URL
const API_BASE = '/api/projects';

// DOM elements
const kanbanBoard = document.getElementById('kanbanBoard');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const addProjectBtn = document.getElementById('addProjectBtn');
const projectModal = document.getElementById('projectModal');
const projectForm = document.getElementById('projectForm');
const modalTitle = document.getElementById('modalTitle');
const closeModal = document.querySelector('.close');
const cancelBtn = document.getElementById('cancelBtn');

// Kanban column elements
const columnPlanning = document.getElementById('column-planning');
const columnActive = document.getElementById('column-active');
const columnOnHold = document.getElementById('column-onhold');
const columnCompleted = document.getElementById('column-completed');
const countPlanning = document.getElementById('count-planning');
const countActive = document.getElementById('count-active');
const countOnHold = document.getElementById('count-onhold');
const countCompleted = document.getElementById('count-completed');

// State
let currentProjects = [];
let editingProjectId = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    addProjectBtn.addEventListener('click', () => openModal());
    closeModal.addEventListener('click', () => closeModalWindow());
    cancelBtn.addEventListener('click', () => closeModalWindow());
    projectForm.addEventListener('submit', handleFormSubmit);
    searchInput.addEventListener('input', debounce(handleSearch, 300));
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === projectModal) {
            closeModalWindow();
        }
    });
}

// API Functions
async function fetchProjects(search = '') {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    
    const url = `${API_BASE}${params.toString() ? '?' + params.toString() : ''}`;
    const response = await fetch(url);
    return await response.json();
}

async function fetchProject(id) {
    const response = await fetch(`${API_BASE}/${id}`);
    return await response.json();
}

async function createProject(data) {
    const response = await fetch(API_BASE, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return await response.json();
}

async function updateProject(id, data) {
    const response = await fetch(`${API_BASE}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return await response.json();
}

async function deleteProject(id) {
    const response = await fetch(`${API_BASE}/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(`Delete failed: ${response.status} ${response.statusText}`);
    }
    return await response.json();
}

// Load and Display Projects
async function loadProjects() {
    try {
        const search = searchInput.value.trim();
        currentProjects = await fetchProjects(search);
        renderProjects(currentProjects);
    } catch (error) {
        console.error('Error loading projects:', error);
        showError('Failed to load projects');
    }
}

function renderProjects(projects) {
    if (projects.length === 0) {
        kanbanBoard.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    kanbanBoard.style.display = 'flex';
    emptyState.style.display = 'none';
    
    // Group projects by status
    const projectsByStatus = {
        'Planning': [],
        'Active': [],
        'On Hold': [],
        'Completed': []
    };
    
    projects.forEach(project => {
        const status = project.status || 'Active';
        if (projectsByStatus[status]) {
            projectsByStatus[status].push(project);
        } else {
            projectsByStatus['Active'].push(project);
        }
    });
    
    // Render each column
    columnPlanning.innerHTML = projectsByStatus['Planning'].map(project => createProjectCard(project)).join('');
    columnActive.innerHTML = projectsByStatus['Active'].map(project => createProjectCard(project)).join('');
    columnOnHold.innerHTML = projectsByStatus['On Hold'].map(project => createProjectCard(project)).join('');
    columnCompleted.innerHTML = projectsByStatus['Completed'].map(project => createProjectCard(project)).join('');
    
    // Update column counts
    countPlanning.textContent = projectsByStatus['Planning'].length;
    countActive.textContent = projectsByStatus['Active'].length;
    countOnHold.textContent = projectsByStatus['On Hold'].length;
    countCompleted.textContent = projectsByStatus['Completed'].length;
    
    // Attach event listeners to action buttons
    attachCardEventListeners();
}

function createProjectCard(project) {
    const createdDate = formatDate(project.created_date);
    const updatedDate = formatDate(project.updated_date);
    
    return `
        <div class="project-card" data-id="${project.id}">
            <div class="card-header">
                <h3 class="project-name">${escapeHtml(project.name)}</h3>
            </div>
            
            ${project.description ? `<p class="project-description">${escapeHtml(project.description)}</p>` : ''}
            
            <div class="card-links">
                ${project.map_link ? `<a href="${escapeHtml(project.map_link)}" target="_blank" class="link-btn link-map"><svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg> Map</a>` : '<span class="link-btn link-disabled"><svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg> Map</span>'}
                ${project.resources_link ? `<a href="${escapeHtml(project.resources_link)}" target="_blank" class="link-btn link-resources"><svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg> Resources</a>` : '<span class="link-btn link-disabled"><svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/></svg> Resources</span>'}
                ${project.proposal_briefing_link ? `<a href="${escapeHtml(project.proposal_briefing_link)}" target="_blank" class="link-btn link-proposal"><svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg> Proposal</a>` : '<span class="link-btn link-disabled"><svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg> Proposal</span>'}
            </div>
            
            <div class="card-footer">
                <div class="card-dates">
                    <small>Created: ${createdDate}</small>
                    <small>Updated: ${updatedDate}</small>
                </div>
                <div class="card-actions">
                    <button class="btn-icon btn-edit" data-id="${project.id}" title="Edit"><svg viewBox="0 0 24 24"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg></button>
                    <button class="btn-icon btn-delete" data-id="${project.id}" title="Delete"><svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg></button>
                </div>
            </div>
        </div>
    `;
}

function attachCardEventListeners() {
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(e.target.dataset.id || e.currentTarget?.dataset.id || btn.dataset.id);
            editProject(id);
        });
    });
    
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(e.target.dataset.id || e.currentTarget?.dataset.id || btn.dataset.id);
            confirmDelete(id);
        });
    });
}

// Modal Functions
function openModal(project = null) {
    editingProjectId = project ? project.id : null;
    modalTitle.textContent = project ? 'Edit Project' : 'Add Project';
    
    if (project) {
        document.getElementById('projectId').value = project.id;
        document.getElementById('projectName').value = project.name || '';
        document.getElementById('projectDescription').value = project.description || '';
        document.getElementById('projectStatus').value = project.status || 'Active';
        document.getElementById('mapLink').value = project.map_link || '';
        document.getElementById('resourcesLink').value = project.resources_link || '';
        document.getElementById('proposalBriefingLink').value = project.proposal_briefing_link || '';
    } else {
        projectForm.reset();
        document.getElementById('projectId').value = '';
    }
    
    projectModal.style.display = 'block';
}

function closeModalWindow() {
    projectModal.style.display = 'none';
    projectForm.reset();
    editingProjectId = null;
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const projectData = {
        name: document.getElementById('projectName').value.trim(),
        description: document.getElementById('projectDescription').value.trim(),
        status: document.getElementById('projectStatus').value,
        map_link: document.getElementById('mapLink').value.trim(),
        resources_link: document.getElementById('resourcesLink').value.trim(),
        proposal_briefing_link: document.getElementById('proposalBriefingLink').value.trim(),
    };
    
    if (!projectData.name) {
        showError('Project name is required');
        return;
    }
    
    try {
        if (editingProjectId) {
            await updateProject(editingProjectId, projectData);
        } else {
            await createProject(projectData);
        }
        
        closeModalWindow();
        loadProjects();
    } catch (error) {
        console.error('Error saving project:', error);
        showError('Failed to save project');
    }
}

async function editProject(id) {
    try {
        const project = await fetchProject(id);
        openModal(project);
    } catch (error) {
        console.error('Error loading project:', error);
        showError('Failed to load project');
    }
}

async function confirmDelete(id) {
    if (!confirm('Are you sure you want to delete this project?')) {
        return;
    }
    
    try {
        await deleteProject(id);
        loadProjects();
    } catch (error) {
        console.error('Error deleting project:', error);
        showError('Failed to delete project');
    }
}

// Search
function handleSearch() {
    loadProjects();
}

// Utility Functions
function getStatusClass(status) {
    const statusMap = {
        'Active': 'status-active',
        'Completed': 'status-completed',
        'On Hold': 'status-onhold',
        'Planning': 'status-planning',
    };
    return statusMap[status] || 'status-active';
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    } catch (e) {
        return dateString;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showError(message) {
    alert(message); // Simple error display - can be enhanced with a toast notification
}


