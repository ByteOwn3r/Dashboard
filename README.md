# Dashboard

A lightweight Terminal User Interface (TUI) dashboard for your console. It provides a clean, unified view of your clock, local weather, a persistent todo list, and your system calendar.

## Requirements
- Python 3.11+
- uv (recommended)

## Quick Start

This project uses `uv` for fast dependency management.

```bash
# Clone the repository
git clone https://github.com/ByteOwn3r/Dashboard.git
cd Dashboard

# Install dependencies
uv sync

# Run the app
uv run main.py
```

## Features & Compatibility

The dashboard is designed to be cross-platform, though some integrations depend on the OS:

| Feature | macOS | Linux | Windows | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Real-time Clock | ✓ | ✓ | ✓ | High-precision digital display. |
| Weather & Rain | ✓ | ✓ | ✓ | Fetches live data from wttr.in. |
| Task Manager | ✓ | ✓ | ✓ | Persistent .md list in user config. |
| Monthly Calendar | ✓ | ✓ | ✓ | Visual grid of the current month. |
| Calendar Events | ✓ | ✗ | ✗ | Integrated with native macOS calendar. |

### Key Functionalities
- **Task Management**: A simple, interactive todo list. Tasks are stored in a Markdown file (tasks.md) in your config folder (~/.config/Dashboard or AppData/Roaming), making them easy to edit outside the app.
- **Calendar Integration**: On macOS, selecting a date in the calendar opens a modal with actual events fetched from the system calendar via a helper script.
- **Live Weather**: Uses curl and wttr.in to display real-time weather and precipitation data directly in the TUI.

## Architecture

The app is built with Textual, using a component-based approach:

```
├── bin/
│   └── calendar-helper    # macOS system calendar bridge
├── main.py                # UI layout, Widgets, and App logic
├── tasks_manager.py       # OS-agnostic file handler for tasks.md
├── pyproject.toml         # Project metadata & dependencies
└── uv.lock                # Dependency lockfile
```

### Technical Breakdown
- **Dashboard (App)**: Manages the TabbedContent layout and global bindings (like q to quit).
- **Clock**: A specialized widget updating every 0.1s.
- **Weather/Rain**: Asynchronous workers that parse ANSI output from external API calls.
- **Tasks**: A state-synced container that reads/writes to the local filesystem in real-time.
- **Calendar/DetailDay**: A data-table implementation that triggers OS-specific logic for event retrieval.