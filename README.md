# Dashboard

A lightweight Terminal User Interface (TUI) dashboard that provides real-time information directly in your console. It is designed to be a simple, elegant way to keep track of time and local weather without leaving the terminal.

## Technologies

| Category | Technology |
| :--- | :--- |
| Language | Python >= 3.11 |
| TUI Framework | Textual |
| Styling | Rich |
| Package Manager | uv |

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv)

## Installation

The project uses `uv` for fast and reliable dependency management.

```bash
# Clone the repository
git clone https://github.com/ByteOwn3r/Dashboard.git
cd Dashboard
uv sync
```

## Usage

To launch the dashboard, run:

```bash
uv run main.py
```

### Controls
- **Tabbed Navigation**: Use the tabs to switch between the **Home** (Clock) and **Weather** views.
- **Exit**: Press `q` to quit the application.

## Architecture

The application is built using a component-based architecture provided by the Textual framework.

```
├── main.py              # Application logic and UI components
├── pyproject.toml       # Project configuration and dependencies
└── uv.lock              # Locked dependency versions
```

### Component Breakdown
- **DashboardApp**: The main application class that manages the layout and global bindings.
- **Home**: A container that centers the real-time clock on the screen.
- **Clock**: A specialized widget that updates every 0.1 seconds to provide high-precision time.
- **Weather**: An asynchronous widget that fetches weather data via `curl` from `wttr.in` and parses the output for a clean terminal display.

## Project State

The project is currently in its initial version, providing core functionality for time and weather tracking.
