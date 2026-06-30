# Smart Matter Terminal (SMT) 🖥️🏡

> **⚠️ Alpha Software Notice:** This project is currently in **Alpha**. While it is fully functional and ready for daily use, you may encounter occasional bugs. Core base features are stable, and expansion is actively underway!

The Smart Matter Terminal (SMT) is a centralized, customizable smart home dashboard hub. Built with a Python Flask backend, it utilizes a multi-threaded architecture to handle background data syncing, database logging, and device monitoring completely separate from frontend client requests. The intended use case for this is to run on a rasberry pi or similar such device that can live on your desk or wall to manage your house and allow for 'data at a glance'

---

## 🏗️ Core Architecture & Thread Management

To keep the UI responsive, SMT splits runtime tasks across concurrent threads managed by `start.py`:
* **Main Thread:** Runs the Flask web application, serving backend API routes and processing client interactions.
* **`sqlThread`:** Operates asynchronously in the background to handle persistent data transactions via SQLite (`smt_database.db`).
* **`pluginsThread`:** Independent thread loop dedicated to polling active plugin streams, tracking device communication, and scheduling metric checks.

---

## 👥 Multi-Client Network Support

The SMT architecture natively supports concurrent multi-client connections. Multiple devices across your local network—including desktop web browsers, smartphones, and tablets—can actively stream the dashboard and interface with widgets simultaneously without interrupting background service cycles or blocking frontend UI loops. 

---

## 🧩 Working Plugins & Status

The terminal comes pre-packaged with a modular plugin system (`SMTplugins/`). Below is the current status of all built-in widgets:

| Plugin Name | Status | Description |
| :--- | :--- | :--- |
| **Clock** | ✅ Working | Real-time local digital clock widget. |
| **Date** | ✅ Working | Calendar date display widget. |
| **Time-Zones** | ✅ Working | Tracks multiple configureable international time zones concurrently. |
| **Calendar** | ⏳ Basic Calandar Working | **COMING SOON** Integrates your personal schedules and upcoming calendar events. |
| **Google Tasks** | ✅ Working | Synchronizes, displays, and updates personal to-do checklists. |
| **Spotify Integration** | ✅ Working | Streams current media states, tracking playback and track details. |
| **Blackjack** | ✅ Working | A fully playable classic Blackjack card game module built into your grid. |
| **Weather** | ✅ Working | Live local weather forecasting and ambient metric tracking. |
| **Temperature Sensor** | ⏳ Coming Soon | Infrastructure ready; local physical/dummy sensor read functionality is in progress. |
| **Smart Device Control** | ⏳ Coming Soon | Initial Home Assistant integration hooks are present; full cross-platform control coming soon. |
| **Arriving Today** | ✅ Working | Tracks inbound package deliveries. Currently expanding towards seamless automated Gmail scanning. |

---

## 🛠️ Installation & Local Development

### Project Structure Notes
* The `static/` folder contains structural CSS stylesheets and core element assets.
* The `templates/` folder stores the modular HTML component blocks that are rendered dynamically by the Flask engine.

### Prerequisites
Ensure you have **`uv`** installed as your rapid Python package manager:

* **macOS / Linux:**
  ```bash
  curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
  ```

* **Windows (PowerShell):**
    ```powershell
    powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
    ```



### Standard Setup

1. Clone the repository and navigate into the root directory.
2. Synchronize your virtual environment and dependencies using `uv`:
    ```bash
    uv sync
    ```


3. Run the application master entry point:
    ```bash
    uv run start.py
    ```



---

## 🐳 Running with Docker (Recommended)

To isolate the terminal instance and easily broadcast it across your entire local network, deploy it using Docker and Docker Compose. This ensures your layout states and databases persist between restarts.

### 1. Spin Up the Container

Open your terminal in the root directory and run:

```bash
docker compose up --build -d
```
---
### Network Navigation

Once the container / server (with normal setup) is running, the terminal broadcasts across your local network interface:

* **To View the Dashboard:** Open a browser on any machine, phone, or tablet on your local network and navigate to:
```text
http://<IP_OF_SERVER_MACHINE>:5000
```


* **To Adjust Settings & Layouts:** Navigate to the dedicated settings route to customize your drag-and-drop dashboard arrangement:
```text
http://<IP_OF_SERVER_MACHINE>:5000/settings
```



---

## 🛠️ Custom Widgets & Development

> **✨ Documentation Coming Soon!**
> Detailed architecture guides, structural boilerplates, and step-by-step instructions on how to engineer, style, and hook your own custom sub-widgets into the `SMTplugins/` ecosystem are on the way. Stay tuned for the next updates!
