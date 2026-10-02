<div align="center">

# 🚆 RailPlus AI
### *Real-Time Train Corridor Intelligence, Clash Prediction & Passenger Decision Support*

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=Leaflet&logoColor=white)](https://leafletjs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  A dual-perspective railway operations and intelligence suite featuring a real-time corridor map, predictive platform clash detection, what-if operational dispatch simulation, and passenger connection risk evaluations.
</p>

[Key Modules](#-key-modules) • [Architecture](#-project-architecture) • [Getting Started](#-getting-started) • [API & Sockets](#-real-time-infrastructure)

</div>

---

## 📌 Executive Summary

Modern rail networks face severe cascading delays due to platform conflicts, junction bottlenecks, and unmodeled weather impacts. 

**RailPlus AI** provides a unified platform serving two critical user personas:
1. **Train Controllers / Dispatchers:** Automated conflict forecasting, platform allocation clash detection, weather impact analysis, and scenario simulation.
2. **Passengers:** High-precision dynamic ETA tracking, interactive route timelines, and automated transfer/connection risk evaluations.

---

## ✨ Key Modules

### 🎛️ Controller & Operations Hub
- **Live Corridor GIS Map:** Real-time geospatial tracking of trains across track corridors powered by Leaflet.
- **Platform Clash Predictor:** Heuristic and schedule-based conflict detection preventing simultaneous platform occupancy.
- **Weather Impact Panel:** Meteorological anomaly monitoring to estimate speed restrictions and weather-induced headway adjustments.
- **"What-If" Dispatch Simulator:** Sandbox environment allowing dispatchers to model hold times, reroutes, and priority overtakes before execution.

### 👤 Passenger Experience Suite
- **Dynamic ETA Tracker:** Real-time arrival forecasts factoring in section delays and live corridor velocity.
- **Visual Route Timeline:** Step-by-step station progression bar displaying scheduled vs. actual arrival times.
- **Connection Risk Evaluator:** Intelligent transfer monitoring calculating missed connection probabilities based on upstream delays.

---

## 🛠️ Technology Stack

| Domain | Stack |
| :--- | :--- |
| **Frontend UI** | React, TypeScript, HTML5, Modern CSS |
| **Mapping & Geospatial** | Leaflet, React-Leaflet |
| **Real-Time Data** | WebSockets (`websocket.ts`), REST API Client (`api.ts`) |
| **Backend & Modeling** | Python, FastAPI / Flask, Pandas, Scikit-Learn |
| **Tooling & Orchestration** | Vite / Webpack, PowerShell (`.ps1`), Windows Batch (`.bat`) |

---

## 📂 Project Architecture

```text
railplus-ai/
├── 🌐 frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Controller/      # Clash predictor, weather panel, what-if simulator
│   │   │   ├── Map/             # Live corridor Leaflet map components
│   │   │   ├── Passenger/       # ETA card, timeline bar, connection risk evaluator
│   │   │   └── Navbar.tsx       # Primary navigation
│   │   ├── services/
│   │   │   ├── api.ts           # REST endpoints client
│   │   │   └── websocket.ts     # Real-time train telemetry stream
│   │   └── types/               # TypeScript interfaces and telemetry contracts
│   └── tsconfig.json
├── ⚙️ backend/                  # Analytical engine and API endpoints
├── 🚀 start_all.bat             # Single-click CMD launch orchestration
├── 💻 start_all.ps1             # PowerShell launch orchestration
└── 📄 README.md                 # System documentation
