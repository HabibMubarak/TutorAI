# 🏗️ Projekt-Architektur & Struktur

Dieses Dokument beschreibt den Aufbau des Tutor-AI Projekts, unterteilt in die logischen Architekturschichten und die physische Dateistruktur.

## 1. 🧠 Zielarchitektur — Logische Schichten

Die Architektur des Backends ist in 4 Schichten unterteilt, um Verantwortlichkeiten sauber zu trennen.

```text
📂 backend/
├── 📄 main.py                      # 🏁 Startpunkt des Servers
├── 📂 alembic/                     # 🔄 Datenbank-Migrationen
└── 📂 app/
    ├── 📂 api/                     # 🚪 SCHICHT 1: Die Tür nach außen
    │   ├── 📂 endpoints/           # 🛣️ URL-Routen (z.B. /chat, /history)
    │   └── 📄 deps.py              # 💉 Auth & DB-Session Injection
    │
    ├── 📂 core/                    # ⚙️ SCHICHT 2: Globale Settings
    │   ├── 📄 config.py            # 📥 Lädt Umgebungsvariablen
    │   └── 📄 school_config.yaml   # 🏫 ZENTRAL: Definition der Schulformen
    │
    ├── 📂 logic/                   # 🤖 SCHICHT 3: Die KI-Logik (Herzstück)
    │   ├── 📄 orchestrator.py      # 👔 Koordiniert die Agenten
    │   ├── 📄 memory.py            # 🧠 Verwaltet den Chat-Kontext
    │   ├── 📄 llm_client.py        # 🔌 Wrapper für Google Gemini API
    │   │
    │   ├── 📂 agents/              # 👷 Die spezialisierten Arbeiter
    │   │   ├── 📄 router.py        # 🚦 Entscheidet: Mathe? Deutsch?
    │   │   ├── 📄 tutor.py         # 👨‍🏫 Der Erklärer
    │   │   ├── 📄 examiner.py      # 📝 Erstellt Übungsaufgaben
    │   │   └── 📄 grader.py        # ✅ Korrigiert Antworten
    │   │
    │   └── 📂 domains/             # 📚 Fachwissen (Modular)
    │       ├── 📂 math/
    │       │   ├── 📄 tools.py     # 🧮 Python-Rechner, Plotter
    │       │   └── 📄 curriculum.json
    │       ├── 📂 german/
    │       └── 📂 english/
    │
    ├── 📂 db/                      # 💾 SCHICHT 4: Datenspeicherung
    │   ├── 📄 models.py            # 🗺️ Tabellen-Definitionen
    │   └── 📄 crud.py              # 🛠️ Datenbank-Operationen
    │
    └── 📂 schemas/                 # 🛡️ Daten-Validierung (Pydantic)
        ├── 📄 chat.py              # 📨 Request/Response Struktur
        └── 📄 user.py
```

## 2. Projektstruktur (File System)

So sieht das Dateisystem für die Entwicklung aus (Docker-Setup).

### Root Level
```text
📂 tutor-ai/
├── 🐳 docker-compose.yml       # Orchestrierung aller Container
├── 🔒 .env                     # Secrets (Keys, Passwörter)
├── 📄 .gitignore
├── 📄 README.md
├── 📂 backend/                 # Python Backend
└── 📂 frontend/                # React Frontend
```

### Backend (`/backend`)
```text
📂 backend/
├── 🐳 Dockerfile
├── 📄 requirements.txt
├── 📄 alembic.ini              # Config für DB-Migrationen
├── 📄 main.py                  # Entry Point
│
└── 📂 app/
    ├── 📄 __init__.py
    ├── 📂 api/                 # REST Interface
    │   ├── 📄 api_v1.py
    │   ├── 📄 deps.py
    │   └── 📂 endpoints/
    │       ├── 📄 chat.py
    │       ├── 📄 tasks.py
    │       └── 📄 auth.py
    │
    ├── 📂 core/                # Config & Security
    │   ├── 📄 config.py
    │   ├── 📄 security.py
    │   └── 📄 school_config.yaml
    │
    ├── 📂 logic/               # AI Business Logic
    │   ├── 📄 llm_client.py
    │   ├── 📄 orchestrator.py
    │   ├── 📄 memory.py
    │   ├── 📂 agents/
    │   └── 📂 domains/
    │
    ├── 📂 db/                  # Database Layer
    │   ├── 📄 session.py
    │   ├── 📄 models.py
    │   └── 📂 crud/
    │
    └── 📂 schemas/             # Pydantic Models
        ├── 📄 chat.py
        ├── 📄 task.py
        └── 📄 user.py
```

### Frontend (`/frontend`)
```text
📂 frontend/
├── 🐳 Dockerfile
├── 📄 package.json
├── 📄 tsconfig.json
├── 📄 vite.config.ts
├── 📄 index.html
│
└── 📂 src/
    ├── 📄 main.tsx             # Entry Point
    ├── 📄 App.tsx              # Router Setup
    ├── 📄 index.css            # Tailwind Imports
    │
    ├── 📂 api/                 # Backend-Kommunikation
    │   ├── 📄 client.ts
    │   ├── 📄 chatService.ts
    │   └── 📄 authService.ts
    │
    ├── 📂 assets/              # Static Files
    │
    ├── 📂 components/          # UI Bausteine
    │   ├── 📂 common/          # (Button, Input, Modal)
    │   ├── 📂 chat/            # (ChatWindow, Bubble, MathRenderer)
    │   └── 📂 layout/          # (Sidebar, Header)
    │
    ├── 📂 hooks/               # React Logic
    │   ├── 📄 useChat.ts
    │   └── 📄 useAuth.ts
    │
    ├── 📂 pages/               # Views
    │   ├── 📄 ChatPage.tsx
    │   ├── 📄 LoginPage.tsx
    │   └── 📄 DashboardPage.tsx
    │
    ├── 📂 types/               # TypeScript Interfaces
    │   ├── 📄 chat.ts
    │   └── 📄 user.ts
    │
    └── 📂 utils/               # Helpers
        ├── 📄 date.ts
        └── 📄 streamParser.ts
```