// ============================================================
// Todo List Application - Local Storage Version
// ============================================================

class TodoApp {
    constructor() {
        // DOM Elements
        this.todoInput = document.getElementById('todoInput');
        this.addBtn = document.getElementById('addBtn');
        this.todoList = document.getElementById('todoList');
        this.emptyState = document.getElementById('emptyState');
        this.clearCompletedBtn = document.getElementById('clearCompletedBtn');
        this.clearAllBtn = document.getElementById('clearAllBtn');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.modal = document.getElementById('confirmModal');
        this.confirmBtn = document.getElementById('confirmBtn');
        this.cancelBtn = document.getElementById('cancelBtn');
        this.confirmMessage = document.getElementById('confirmMessage');
        this.toast = document.getElementById('successToast');
        
        // Stats
        this.totalCount = document.getElementById('totalCount');
        this.activeCount = document.getElementById('activeCount');
        this.completedCount = document.getElementById('completedCount');

        // Data
        this.todos = this.loadFromStorage();
        this.currentFilter = 'all';
        this.pendingAction = null;

        // Initialize
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.attachEventListeners();
        this.render();
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Add todo
        this.addBtn.addEventListener('click', () => this.addTodo());
        this.todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });

        // Filter buttons
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.setFilter(e.target.dataset.filter));
        });

        // Clear buttons
        this.clearCompletedBtn.addEventListener('click', () => this.confirmClearCompleted());
        this.clearAllBtn.addEventListener('click', () => this.confirmClearAll());

        // Modal buttons
        this.confirmBtn.addEventListener('click', () => this.executePendingAction());
        this.cancelBtn.addEventListener('click', () => this.closeModal());
    }

    /**
     * Add a new todo
     */
    addTodo() {
        const text = this.todoInput.value.trim();

        if (!text) {
            this.showToast('Please enter a task', 'error');
            return;
        }

        if (text.length > 500) {
            this.showToast('Task is too long (max 500 characters)', 'error');
            return;
        }

        const todo = {
            id: Date.now(),
            text: text,
            completed: false,
            createdAt: new Date().toLocaleDateString()
        };

        this.todos.unshift(todo);
        this.saveToStorage();
        this.render();
        this.todoInput.value = '';
        this.todoInput.focus();
        this.showToast('✅ Task added successfully!');
    }

    /**
     * Toggle todo completion status
     */
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveToStorage();
            this.render();
        }
    }

    /**
     * Delete a todo
     */
    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.saveToStorage();
        this.render();
        this.showToast('✅ Task deleted');
    }

    /**
     * Edit a todo
     */
    editTodo(id) {
        const todoItem = document.querySelector(`[data-id="${id}"]`);
        const todo = this.todos.find(t => t.id === id);

        if (!todo) return;

        // Create edit UI
        todoItem.classList.add('edit-mode');
        const content = todoItem.querySelector('.todo-content');
        const originalHTML = content.innerHTML;

        content.innerHTML = `
            <input type="text" class="edit-input" value="${this.escapeHtml(todo.text)}" autofocus>
        `;

        const input = content.querySelector('.edit-input');
        const actions = document.createElement('div');
        actions.className = 'edit-actions';
        actions.innerHTML = `
            <button class="save-btn">💾 Save</button>
            <button class="cancel-edit-btn">❌ Cancel</button>
        `;

        todoItem.appendChild(actions);

        const saveBtn = actions.querySelector('.save-btn');
        const cancelBtn = actions.querySelector('.cancel-edit-btn');

        const save = () => {
            const newText = input.value.trim();
            if (!newText) {
                this.showToast('Task cannot be empty', 'error');
                return;
            }
            if (newText.length > 500) {
                this.showToast('Task is too long', 'error');
                return;
            }
            todo.text = newText;
            this.saveToStorage();
            this.render();
            this.showToast('✅ Task updated');
        };

        const cancel = () => {
            todoItem.classList.remove('edit-mode');
            content.innerHTML = originalHTML;
            actions.remove();
        };

        saveBtn.addEventListener('click', save);
        cancelBtn.addEventListener('click', cancel);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') save();
            if (e.key === 'Escape') cancel();
        });
    }

    /**
     * Set filter
     */
    setFilter(filter) {
        this.currentFilter = filter;
        this.filterButtons.forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        this.render();
    }

    /**
     * Get filtered todos
     */
    getFilteredTodos() {
        switch (this.currentFilter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return this.todos;
        }
    }

    /**
     * Confirm clear completed
     */
    confirmClearCompleted() {
        const completed = this.todos.filter(t => t.completed);
        if (completed.length === 0) {
            this.showToast('No completed tasks to clear', 'error');
            return;
        }
        this.openModal('Clear all completed tasks?', 'clearCompleted');
    }

    /**
     * Confirm clear all
     */
    confirmClearAll() {
        if (this.todos.length === 0) {
            this.showToast('No tasks to clear', 'error');
            return;
        }
        this.openModal('Clear all tasks? This cannot be undone.', 'clearAll');
    }

    /**
     * Open confirmation modal
     */
    openModal(message, action) {
        this.confirmMessage.textContent = message;
        this.pendingAction = action;
        this.modal.classList.add('show');
    }

    /**
     * Close modal
     */
    closeModal() {
        this.modal.classList.remove('show');
        this.pendingAction = null;
    }

    /**
     * Execute pending action
     */
    executePendingAction() {
        if (this.pendingAction === 'clearCompleted') {
            this.clearCompleted();
        } else if (this.pendingAction === 'clearAll') {
            this.clearAll();
        }
        this.closeModal();
    }

    /**
     * Clear completed todos
     */
    clearCompleted() {
        const count = this.todos.filter(t => t.completed).length;
        this.todos = this.todos.filter(t => !t.completed);
        this.saveToStorage();
        this.render();
        this.showToast(`✅ Cleared ${count} completed task(s)`);
    }

    /**
     * Clear all todos
     */
    clearAll() {
        const count = this.todos.length;
        this.todos = [];
        this.saveToStorage();
        this.render();
        this.showToast(`✅ Cleared ${count} task(s)`);
    }

    /**
     * Update stats
     */
    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(t => t.completed).length;
        const active = total - completed;

        this.totalCount.textContent = total;
        this.activeCount.textContent = active;
        this.completedCount.textContent = completed;
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'success') {
        this.toast.textContent = message;
        this.toast.className = `toast show ${type}`;

        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }

    /**
     * Escape HTML special characters
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Render the todo list
     */
    render() {
        const filteredTodos = this.getFilteredTodos();
        this.todoList.innerHTML = '';

        if (filteredTodos.length === 0) {
            this.emptyState.classList.add('show');
        } else {
            this.emptyState.classList.remove('show');
            filteredTodos.forEach(todo => {
                const todoEl = this.createTodoElement(todo);
                this.todoList.appendChild(todoEl);
            });
        }

        this.updateStats();
        this.updateButtonStates();
    }

    /**
     * Create todo element
     */
    createTodoElement(todo) {
        const div = document.createElement('div');
        div.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        div.dataset.id = todo.id;

        div.innerHTML = `
            <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
            <div class="todo-content">
                <span class="todo-text">${this.escapeHtml(todo.text)}</span>
                <span class="todo-date">Added: ${todo.createdAt}</span>
            </div>
            <div class="todo-actions">
                <button class="todo-btn edit-btn" title="Edit">✏️</button>
                <button class="todo-btn delete-btn" title="Delete">🗑️</button>
            </div>
        `;

        // Checkbox event
        const checkbox = div.querySelector('.todo-checkbox');
        checkbox.addEventListener('change', () => this.toggleTodo(todo.id));

        // Edit button
        const editBtn = div.querySelector('.edit-btn');
        editBtn.addEventListener('click', () => this.editTodo(todo.id));

        // Delete button
        const deleteBtn = div.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', () => this.deleteTodo(todo.id));

        return div;
    }

    /**
     * Update button states
     */
    updateButtonStates() {
        const hasCompleted = this.todos.some(t => t.completed);
        const hasAny = this.todos.length > 0;

        this.clearCompletedBtn.disabled = !hasCompleted;
        this.clearAllBtn.disabled = !hasAny;
    }

    /**
     * Save todos to localStorage
     */
    saveToStorage() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }

    /**
     * Load todos from localStorage
     */
    loadFromStorage() {
        const stored = localStorage.getItem('todos');
        return stored ? JSON.parse(stored) : [];
    }
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new TodoApp();
    });
} else {
    new TodoApp();
}
