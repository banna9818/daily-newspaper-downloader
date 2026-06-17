# 📋 Todo List Application with Local Storage

A modern, fully-featured todo list application built with vanilla JavaScript, HTML, and CSS. All data is stored locally in the browser using localStorage.

## ✨ Features

### Core Features
✅ **Add Tasks** - Create new todos with a simple input
✅ **Mark Complete** - Check off completed tasks
✅ **Edit Tasks** - Modify existing tasks inline
✅ **Delete Tasks** - Remove individual tasks
✅ **Filter Tasks** - View All, Active, or Completed tasks
✅ **Local Storage** - All data persists in browser localStorage
✅ **Real-time Stats** - Track total, active, and completed tasks

### Advanced Features
✅ **Keyboard Support** - Press Enter to add tasks
✅ **Confirmation Dialogs** - Confirm before clearing tasks
✅ **Toast Notifications** - User feedback for actions
✅ **Responsive Design** - Works on desktop and mobile
✅ **Date Tracking** - See when each task was created
✅ **Input Validation** - Prevent empty or oversized tasks
✅ **Smooth Animations** - Professional UI transitions
✅ **Dark/Light Background** - Gradient purple theme

## 🚀 Getting Started

### Installation

1. Clone or download the files:
```bash
git clone <repository-url>
cd todo-app
```

2. Open `index.html` in your web browser:
   - Double-click `index.html`, OR
   - Use a local server (recommended):
     ```bash
     python -m http.server 8000
     # Then visit http://localhost:8000
     ```

### File Structure

```
todo-app/
├── index.html      # HTML structure
├── styles.css      # CSS styling
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## 📖 Usage Guide

### Adding a Task
1. Type your task in the input field
2. Click the "➕ Add" button or press Enter
3. Task appears at the top of the list

### Completing a Task
1. Click the checkbox next to the task
2. Task gets a strikethrough
3. Moves to "Completed" counter

### Editing a Task
1. Click the "✏️" edit button on a task
2. Edit the text in the input field
3. Click "💾 Save" or press Enter to confirm
4. Click "❌ Cancel" or press Escape to cancel

### Deleting a Task
1. Click the "🗑️" delete button on a task
2. Task is removed immediately

### Filtering Tasks
- **All**: Shows all tasks
- **Active**: Shows incomplete tasks only
- **Completed**: Shows completed tasks only

### Clearing Tasks
- **Clear Completed**: Removes all completed tasks
  - Confirmation required
  - Shows count of deleted tasks
- **Clear All**: Removes all tasks
  - Warning confirmation required
  - Cannot be undone

## 💾 Local Storage

All todos are automatically saved to your browser's localStorage under the key `'todos'`.

### Data Structure
```javascript
[
  {
    id: 1623456789,
    text: "Buy groceries",
    completed: false,
    createdAt: "6/11/2026"
  },
  // ... more todos
]
```

### Clear Local Storage

To manually clear all data (browser console):
```javascript
localStorage.removeItem('todos');
location.reload();
```

To export your data:
```javascript
JSON.stringify(JSON.parse(localStorage.getItem('todos')), null, 2)
```

## 🎨 Customization

### Change Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --primary-color: #6366f1;        /* Main color */
    --success-color: #10b981;        /* Success color */
    --danger-color: #ef4444;         /* Delete/danger color */
    --background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* ... more colors */
}
```

### Change Title
Edit in `index.html`:
```html
<h1>📋 My Todo List</h1>
<p class="subtitle">Stay organized and productive</p>
```

### Modify Validation Rules
Edit in `script.js`:
```javascript
if (text.length > 500) {  // Change max length
    // ...
}
```

## 📱 Responsive Design

- **Desktop**: Full layout with side-by-side elements
- **Tablet**: Optimized spacing and button sizes
- **Mobile**: Stacked layout with full-width inputs

Breakpoint: 600px width

## 🔍 Browser Support

✅ Chrome/Edge (latest)
✅ Firefox (latest)
✅ Safari (latest)
✅ Mobile browsers

Requirements:
- ES6 JavaScript support
- localStorage support
- CSS Grid/Flexbox support

## 🛠️ Technical Details

### Class Structure
The app uses a single `TodoApp` class with methods for:
- `addTodo()` - Create new task
- `toggleTodo()` - Mark complete/incomplete
- `deleteTodo()` - Remove task
- `editTodo()` - Modify task
- `setFilter()` - Change view filter
- `clearCompleted()` - Remove finished tasks
- `clearAll()` - Remove all tasks
- `saveToStorage()` - Persist data
- `loadFromStorage()` - Load data
- `render()` - Update UI

### Event Handling
- Keyboard events (Enter, Escape)
- Click events (buttons, checkboxes)
- Change events (filter selection)

### Data Persistence
- Automatic saving on every action
- Loads on page refresh
- Survives browser restarts
- Per-domain storage

## 📊 Statistics

Real-time tracking of:
- **Total**: All tasks count
- **Active**: Incomplete tasks count
- **Completed**: Finished tasks count

Updates automatically on every action.

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Add new task / Save edit |
| Escape | Cancel edit |
| Tab | Navigate between elements |

## 🎯 Validation Rules

✅ Task cannot be empty
✅ Task max length: 500 characters
✅ No duplicate checking (allows same text)
✅ Trim whitespace automatically

## 🚀 Performance

- ⚡ Instant UI updates
- 💾 Minimal storage usage
- 🎯 Efficient DOM manipulation
- 📦 Single JS file (no dependencies)
- 🔄 Fast localStorage operations

## 🐛 Known Limitations

- localStorage cleared if browser cache is cleared
- Different browsers have separate storage
- ~5-10MB storage limit per domain
- No cloud sync capability
- No multi-device sync

## 🔒 Privacy & Security

✅ All data stored locally (no server upload)
✅ No external dependencies
✅ HTML escaping prevents XSS
✅ No tracking or analytics
✅ No cookies used

## 📈 Future Enhancements

Possible additions:
- [ ] Dark mode toggle
- [ ] Task categories/tags
- [ ] Priority levels
- [ ] Due dates
- [ ] Recurring tasks
- [ ] Task search
- [ ] Export to CSV/JSON
- [ ] Drag and drop reordering
- [ ] Cloud sync (Firebase/Supabase)
- [ ] Mobile app version

## 📝 License

Free to use and modify for personal or commercial projects.

## 🤝 Contributing

Feel free to fork and submit improvements!

## 📧 Support

For issues or questions, please check:
1. Browser console for errors
2. localStorage is enabled
3. JavaScript is enabled

---

**Made with ❤️ - A simple, powerful todo list app**

**Version**: 1.0.0
**Last Updated**: 2026-06-17
