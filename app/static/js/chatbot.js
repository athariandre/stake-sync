// Chatbot Interface JavaScript

let currentUserId = null;
const API_BASE = '';

// Show status message
function showStatus(message, isError = false) {
    const statusEl = document.getElementById('status-message');
    statusEl.textContent = message;
    statusEl.classList.remove('error');
    if (isError) {
        statusEl.classList.add('error');
    }
    statusEl.classList.add('show');
    
    setTimeout(() => {
        statusEl.classList.remove('show');
    }, 3000);
}

// Handle user setup (login or register)
async function handleUserSetup() {
    const userId = document.getElementById('user-id').value;
    const userName = document.getElementById('user-name').value;
    const userEmail = document.getElementById('user-email').value;
    
    if (userId) {
        // Try to get existing user
        try {
            const response = await fetch(`${API_BASE}/auth/user/${userId}`);
            if (response.ok) {
                const user = await response.json();
                currentUserId = user.id;
                document.getElementById('user-selection').classList.add('hidden');
                document.getElementById('main-interface').classList.remove('hidden');
                showStatus(`Welcome back, ${user.name}!`);
                loadUpdates();
                loadAudiences();
                return;
            }
        } catch (error) {
            showStatus('User not found. Please create a new account.', true);
            return;
        }
    }
    
    // Register new user
    if (!userName || !userEmail) {
        showStatus('Please provide name and email to create an account.', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: userName, email: userEmail })
        });
        
        if (response.ok) {
            const user = await response.json();
            currentUserId = user.id;
            document.getElementById('user-selection').classList.add('hidden');
            document.getElementById('main-interface').classList.remove('hidden');
            showStatus(`Welcome, ${user.name}! Your user ID is ${user.id}`);
        } else {
            const error = await response.json();
            showStatus(error.detail || 'Registration failed', true);
        }
    } catch (error) {
        showStatus('Failed to register. Please try again.', true);
    }
}

// Show tab
function showTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Load data for specific tabs
    if (tabName === 'review') {
        loadUpdates();
    } else if (tabName === 'audience') {
        loadAudiences();
    }
}

// Submit weekly update
async function submitUpdate() {
    const content = document.getElementById('update-content').value;
    
    if (!content.trim()) {
        showStatus('Please enter your update content.', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/update/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUserId, content })
        });
        
        if (response.ok) {
            const update = await response.json();
            showStatus('Update submitted successfully!');
            document.getElementById('update-content').value = '';
            
            // Generate drafts
            generateDrafts(update.id);
        } else {
            showStatus('Failed to submit update.', true);
        }
    } catch (error) {
        showStatus('Error submitting update.', true);
    }
}

// Generate drafts for an update
async function generateDrafts(updateId) {
    showStatus('Generating drafts... This may take a moment.');
    
    try {
        const response = await fetch(`${API_BASE}/drafts/generate/${updateId}?user_id=${currentUserId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showStatus('Drafts generated successfully!');
            showTab('review');
            loadUpdates();
        } else {
            showStatus('Failed to generate drafts.', true);
        }
    } catch (error) {
        showStatus('Error generating drafts.', true);
    }
}

// Upload style sample
async function uploadStyleSample() {
    const content = document.getElementById('style-sample').value;
    
    if (!content.trim()) {
        showStatus('Please enter a writing sample.', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/style/upload`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUserId, content })
        });
        
        if (response.ok) {
            const data = await response.json();
            showStatus('Style sample uploaded successfully!');
            document.getElementById('style-sample').value = '';
            
            // Display style profile
            const profileEl = document.getElementById('style-profile');
            profileEl.innerHTML = `
                <h4>Your Style Profile</h4>
                <pre>${JSON.stringify(data.style_profile, null, 2)}</pre>
            `;
        } else {
            showStatus('Failed to upload sample.', true);
        }
    } catch (error) {
        showStatus('Error uploading sample.', true);
    }
}

// Load updates and their drafts
async function loadUpdates() {
    try {
        const response = await fetch(`${API_BASE}/update/list?user_id=${currentUserId}`);
        
        if (response.ok) {
            const updates = await response.json();
            displayUpdates(updates);
        }
    } catch (error) {
        console.error('Error loading updates:', error);
    }
}

// Display updates with drafts
async function displayUpdates(updates) {
    const container = document.getElementById('updates-list');
    
    if (updates.length === 0) {
        container.innerHTML = '<p>No updates yet. Submit your first update!</p>';
        return;
    }
    
    container.innerHTML = '';
    
    for (const update of updates) {
        const updateEl = document.createElement('div');
        updateEl.className = 'update-item';
        
        const date = new Date(update.timestamp).toLocaleDateString();
        updateEl.innerHTML = `
            <div class="update-meta">Submitted on ${date}</div>
            <div><strong>Content Preview:</strong> ${update.content.substring(0, 150)}...</div>
            <button onclick="showDrafts(${update.id})" class="btn btn-secondary" style="margin-top: 10px;">View Drafts</button>
            <div id="drafts-${update.id}" class="draft-container"></div>
        `;
        
        container.appendChild(updateEl);
    }
}

// Show drafts for an update
async function showDrafts(updateId) {
    const container = document.getElementById(`drafts-${updateId}`);
    
    // Check if already loaded
    if (container.innerHTML) {
        container.innerHTML = '';
        return;
    }
    
    showStatus('Loading drafts...');
    
    // In a real scenario, we'd fetch drafts by update_id
    // For now, let's generate them if they don't exist
    try {
        const response = await fetch(`${API_BASE}/drafts/generate/${updateId}?user_id=${currentUserId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const drafts = await response.json();
            displayDrafts(container, drafts);
            showStatus('Drafts loaded successfully!');
        }
    } catch (error) {
        showStatus('Error loading drafts.', true);
    }
}

// Display drafts
function displayDrafts(container, drafts) {
    container.innerHTML = '';
    
    for (const [audience, draft] of Object.entries(drafts)) {
        const draftEl = document.createElement('div');
        draftEl.className = 'draft-box';
        
        draftEl.innerHTML = `
            <div class="draft-header">
                <span class="draft-audience">${audience}</span>
                <span class="draft-status ${draft.status}">${draft.status}</span>
            </div>
            <div class="draft-content">${draft.content}</div>
            <div class="draft-actions">
                <button onclick="approveDraft(${draft.id})" class="btn btn-primary">Approve</button>
                <button onclick="regenerateDraft(${draft.id})" class="btn btn-secondary">Regenerate</button>
                <button onclick="editDraft(${draft.id})" class="btn btn-secondary">Request Edit</button>
            </div>
        `;
        
        container.appendChild(draftEl);
    }
}

// Approve draft
async function approveDraft(draftId) {
    try {
        const response = await fetch(`${API_BASE}/review/approve/${draftId}?user_id=${currentUserId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showStatus('Draft approved!');
            
            // Ask if user wants to send
            if (confirm('Draft approved! Would you like to send it now?')) {
                sendDraft(draftId);
            }
        } else {
            showStatus('Failed to approve draft.', true);
        }
    } catch (error) {
        showStatus('Error approving draft.', true);
    }
}

// Send draft
async function sendDraft(draftId) {
    try {
        const response = await fetch(`${API_BASE}/send/${draftId}?user_id=${currentUserId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const result = await response.json();
            showStatus(`Email sent to ${result.recipients_count} recipients!`);
            loadUpdates();
        } else {
            const error = await response.json();
            showStatus(error.detail || 'Failed to send email.', true);
        }
    } catch (error) {
        showStatus('Error sending email.', true);
    }
}

// Regenerate draft
async function regenerateDraft(draftId) {
    showStatus('Regenerating draft...');
    
    try {
        const response = await fetch(`${API_BASE}/review/regenerate/${draftId}?user_id=${currentUserId}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showStatus('Draft regenerated!');
            loadUpdates();
        } else {
            showStatus('Failed to regenerate draft.', true);
        }
    } catch (error) {
        showStatus('Error regenerating draft.', true);
    }
}

// Edit draft
async function editDraft(draftId) {
    const instructions = prompt('What changes would you like to make?');
    
    if (!instructions) return;
    
    showStatus('Applying edits...');
    
    try {
        const response = await fetch(`${API_BASE}/review/apply-edits/${draftId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUserId, edit_instructions: instructions })
        });
        
        if (response.ok) {
            showStatus('Edits applied!');
            loadUpdates();
        } else {
            showStatus('Failed to apply edits.', true);
        }
    } catch (error) {
        showStatus('Error applying edits.', true);
    }
}

// Save audience
async function saveAudience(audienceType) {
    const textarea = document.getElementById(`${audienceType}-emails`);
    const emailsText = textarea.value;
    
    // Parse emails (one per line)
    const emails = emailsText.split('\n')
        .map(e => e.trim())
        .filter(e => e && e.includes('@'));
    
    if (emails.length === 0) {
        showStatus('Please enter at least one valid email address.', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/audience/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUserId,
                group_type: audienceType,
                emails: emails
            })
        });
        
        if (response.ok) {
            showStatus(`${audienceType} audience saved successfully!`);
        } else {
            showStatus('Failed to save audience.', true);
        }
    } catch (error) {
        showStatus('Error saving audience.', true);
    }
}

// Load audiences
async function loadAudiences() {
    try {
        const response = await fetch(`${API_BASE}/audience/list?user_id=${currentUserId}`);
        
        if (response.ok) {
            const groups = await response.json();
            
            // Populate each audience textarea
            groups.forEach(group => {
                const textarea = document.getElementById(`${group.group_type}-emails`);
                if (textarea) {
                    textarea.value = group.emails.join('\n');
                }
            });
        }
    } catch (error) {
        console.error('Error loading audiences:', error);
    }
}
