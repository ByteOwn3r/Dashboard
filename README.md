# Dashboard

A lightweight Terminal User Interface (TUI) dashboard for your console. It provides a clean, unified view of your clock, local weather, a persistent todo list, and your system calendar.

## Table of Contents
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Features & Compatibility](#features--compatibility)
- [Google Calendar Setup](#google-calendar-setup-optional)
- [Architecture](#architecture)

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

| Feature | macOS | Linux | Windows | Notes                                             |
| :--- | :---: | :---: | :---: |:--------------------------------------------------|
| Real-time Clock | ✓ | ✓ | ✓ | High-precision digital display.                   |
| Weather & Rain | ✓ | ✓ | ✓ | Fetches live data from wttr.in.                   |
| Task Manager | ✓ | ✓ | ✓ | Persistent .md list in user config.               |
| Monthly Calendar | ✓ | ✓ | ✓ | Visual grid of the current month.                 |
| Calendar Events | ✓ | ✓ | ✓ | Integrated with native macOS calendar and CalDAV. |

### Key Functionalities
- **Task Management**: A simple, interactive todo list. Tasks are stored in a Markdown file (tasks.md) in your config folder (~/.config/Dashboard or AppData/Roaming), making them easy to edit outside the app.
- **Calendar Integration**: On macOS, selecting a date in the calendar opens a modal with actual events fetched from the system calendar via a helper script.
- **Live Weather**: Uses curl and wttr.in to display real-time weather and precipitation data directly in the TUI.

## Google Calendar Setup

> [!WARNING]
> By default, Dashboard reads your calendar via Apple's Calendar app **on macOS only**. If you're on Linux/Windows, you'll need to set up CalDAV. If you want to use Google Calendar instead, follow the steps below to set up your own credentials — this is required due to Google's restrictions on third-party CalDAV access.

### 1. Create a Google Cloud project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (top-left project selector → "New Project")

### 2. Enable the CalDAV API

1. Go to **APIs & Services → Library**
2. Search for **"CalDAV API"**
3. Click **Enable**

### 3. Configure the OAuth consent screen

1. Go to **APIs & Services → OAuth consent screen** (or **Google Auth Platform → Audience**, depending on your console version)
2. Choose **External** as the user type
3. Fill in the required fields (app name, support email, developer contact)
4. Add the scope: `https://www.googleapis.com/auth/calendar`
5. Under **Test users**, add your own Gmail address (required while the app isn't published — otherwise you'll get an `access_denied` error)

### 4. Create OAuth credentials

1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Give it a name and click **Create**
5. Download the JSON file, rename it to `credentials.json`, and place it in the project root

### 5. First run

1. Enable Google Calendar in the **Config** tab of Dashboard
2. On first use, a browser window will open asking you to log in and grant access
3. You'll see a warning that says *"Google hasn't verified this app"* — click **Advanced → Go to Dashboard (unsafe)** to proceed. This is expected, since Dashboard isn't a published Google app
4. After granting access, a `token.json` file will be created automatically — you won't need to log in again unless you revoke access

> **Note:** `credentials.json` and `token.json` are unique to your Google account and should never be committed to a repository or shared publicly.

## Architecture

The app is built with Textual, using a component-based approach:

```
├── bin/
│   └── calendar-helper    # macOS system calendar bridge
├── main.py                # UI layout, Widgets, and App logic
├── tasks_manager.py       # Handler for tasks.md
├── calendar_manager.py    # Handler for both Apple and CalDAV calendars
├── config_manager.py      # Handler for configuration of the dashboard
├── pyproject.toml         # Project metadata & dependencies
└── uv.lock                # Dependency lockfile
```

### Technical Breakdown
- **Dashboard (App)**: Manages the TabbedContent layout and global bindings (like q to quit).
- **Clock**: A specialized widget updating every 0.1s.
- **Weather/Rain**: Asynchronous workers that parse ANSI output from external API calls.
- **Tasks**: A state-synced container that reads/writes to the local filesystem in real-time.
- **Calendar/DetailDay**: A data-table implementation that triggers OS-specific logic for event retrieval.
- **Config**: Configuration of dashboard things as city for weather, or url/user/password for CalDAV