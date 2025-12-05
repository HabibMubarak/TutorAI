# TutorAI - Systemarchitektur & Dokumentation

## 0. Ablauf (Der Lebenszyklus einer Nachricht)

Wie fließt eine Nachricht durch das System? Hier ist der Weg von der Tastatur des Schülers bis zur Antwort der KI – inklusive Monitoring und Sicherheitsnetzen.

### Phase 1: Der Request (Frontend → Backend)
* **User:** Tippt "Erkläre mir die Mitternachtsformel" und wählt Realschule, 10. Klasse.
* **Frontend:** `chatService.ts` generiert eine lokale `session_id` und sendet einen POST Request an `http://api/chat`.
* **Analytics:** Parallel sendet das Frontend ein Event an PostHog: *"User Message Sent"*.
* **Payload:** `{ "msg": "...", "context": { "school": "realschule", "grade": 10 } }`

### Phase 2: Die Analyse & Tracing (Backend Logic)
* **API Layer:** Der Endpoint `chat.py` empfängt die Daten.
* **Tracing Init:** Eine `trace_id` wird generiert (für LangSmith/LangFuse), um den Request über alle Agenten hinweg zu verfolgen.
* **Orchestrator:**
    * Lädt die History aus `memory.py` (damit die KI den Kontext kennt).
    * Ruft den **Router Agent** auf.
* **Router Agent:** Analysiert den Intent.
    * *Log:* `logger.info("intent_detected", extra={"intent": "explanation", "trace_id": "..."})`
* **Ergebnis:** Domain=Mathe, Intent=Erklärung.

### Phase 3: Die Vorbereitung (Resource Gathering)
* **Orchestrator:** Baut das "Paket" für den Tutor Agent zusammen:
    * Lädt Schul-Profil aus `school_config.yaml` (z.B. "Nutze einfache Sprache").
    * Lädt Mathe-Tools aus `domains/math/tools.py`.
    * Lädt Curriculum-Infos aus `domains/math/curriculum.json`.

### Phase 4: Die Generierung mit Safety Layer (Backend → LLM)
* **Tutor Agent:** Baut den finalen Prompt (System Prompt + Kontext + User Frage).
* **LLM Client (Safety Net):**
    * **Circuit Breaker Check:** Ist der Provider (Gemini) gerade down?
    * **Versuch 1:** Sendet Prompt an Gemini.
    * *Falls Fehler (5xx):* **Retry Logic** wartet kurz und versucht es erneut.
    * *Falls Totalausfall:* **Fallback** auf alternatives Modell (z.B. Claude/OpenAI) oder Cache.

### Phase 5: Das Streaming (LLM → Frontend)
* **Gemini:** Generiert Text Stück für Stück (Tokens).
* **Backend:** Reicht diese Stücke sofort per Server-Sent Events (SSE) an das Frontend weiter.
* **Guardrails:** (Optional) Prüft parallel, ob toxische Inhalte generiert werden und bricht ggf. ab.
* **Frontend:** `useChat.ts` empfängt die Stücke und aktualisiert den Text live.

### Phase 6: Abschluss & Feedback (Aftermath)
* **DB:** Die fertige Nachricht wird in der Datenbank (`db/`) gespeichert.
* **User:** Klickt auf "Daumen runter".
* **Frontend:** Sendet Feedback an `/api/feedback`. Das System verknüpft dies mit der `trace_id`, damit du später im Dashboard genau diesen fehlerhaften Chat-Verlauf analysieren kannst.

---

## 1. Zielarchitektur — Überblick

Die Architektur besteht nun aus **5 Schichten** (inklusive Operations/Monitoring):

backend/
├── main.py                      # Startpunkt (Inkl. Middleware für Sentry/Prometheus)
├── alembic/                     # Datenbank-Migrationen
└── app/
    ├── api/                     # SCHICHT 1: Die Tür nach außen
    │   ├── endpoints/           # URL-Routen
    │   │   ├── chat.py          # Haupt-Chatlogik
    │   │   ├── feedback.py      # User Feedback (Daumen hoch/runter)
    │   │   └── health.py        # Health Checks für Kubernetes/Docker
    │   └── deps.py              # Auth & DB-Session Injection
    │
    ├── core/                    # SCHICHT 2: Globale Settings
    │   ├── config.py            # Lädt Keys (API, DB, LangSmith, Sentry)
    │   ├── feature_flags.py     # Kill-Switches für Features
    │   └── school_config.yaml   # ZENTRAL: Definition der Schulformen
    │
    ├── logic/                   # SCHICHT 3: Die KI-Logik (Herzstück)
    │   ├── orchestrator.py      # Koordiniert Agenten & Tracing
    │   ├── memory.py            # Chat-Kontext (Redis/DB)
    │   ├── llm_client.py        # Wrapper für LLM (Inkl. Retries & Fallbacks)
    │   │
    │   ├── agents/              # Die spezialisierten Arbeiter
    │   │   ├── router.py        # Intent Classification
    │   │   ├── tutor.py         # Erklärer
    │   │   ├── examiner.py      # Prüfer
    │   │   └── guardrails.py    # Input/Output Sicherheitsfilter
    │   │
    │   └── domains/             # Fachwissen (Modular)
    │       ├── math/
    │       ├── german/
    │       └── english/
    │
    ├── db/                      # SCHICHT 4: Datenspeicherung
    │   ├── models.py            # Tabellen (User, Message, Feedback)
    │   └── crud.py              # DB-Operationen
    │
    └── ops/                     # SCHICHT 5: Operations & Monitoring (NEU)
        ├── telemetry.py         # LangSmith/LangFuse Tracing Setup
        ├── logging_conf.py      # Strukturiertes JSON-Logging
        ├── monitoring.py        # Prometheus Metriken (Latenz, Error Rates)
        └── sentry.py            # Error Reporting Setup

    └── schemas/                 # Daten-Validierung (Pydantic)
        ├── chat.py
        ├── feedback.py
        └── user.py

---

## 2. Projektstruktur (fertig für Python)

tutor-ai/
├── docker-compose.yml           # Startet Frontend, Backend, DB & Monitoring
├── .env                         # API-Keys, DB-URL, Sentry-DSN, LangSmith-Key
├── .gitignore
├── README.md
├── backend/
└── frontend/

### Backend Struktur
backend/
├── Dockerfile
├── requirements.txt             # Jetzt inkl. sentry-sdk, langsmith, prometheus-client, tenacity
├── alembic.ini
├── main.py                      # Initiiert App, Sentry & Middleware
│
└── app/
    ├── __init__.py
    │
    ├── api/
    │   ├── api_v1.py
    │   ├── deps.py
    │   └── endpoints/
    │       ├── chat.py          # POST /chat
    │       ├── tasks.py         # Übungsaufgaben
    │       ├── feedback.py      # POST /feedback (Monitoring)
    │       ├── health.py        # GET /healthz (Uptime Check)
    │       └── auth.py
    │
    ├── core/
    │   ├── config.py
    │   ├── security.py
    │   ├── feature_flags.py     # Einfaches Toggles-System
    │   ├── exceptions.py
    │   └── school_config.yaml
    │
    ├── logic/
    │   ├── llm_client.py        # Logik für Retry, Timeout & Fallback Models
    │   ├── orchestrator.py
    │   ├── memory.py
    │   │
    │   ├── agents/
    │   │   ├── router.py
    │   │   ├── tutor.py
    │   │   ├── examiner.py
    │   │   └── base.py
    │   │
    │   └── domains/
    │       └── math/
    │           ├── tools.py
    │           └── curriculum.json
    │
    ├── db/
    │   ├── session.py
    │   ├── models.py            # User, Message, Task, UserFeedback
    │   └── crud/
    │
    ├── ops/                     # NEU: Der Maschinenraum
    │   ├── telemetry.py         # Tracing Callbacks
    │   └── monitoring.py        # Metriken Definitionen
    │
    └── schemas/
        ├── chat.py
        ├── feedback.py
        └── user.py

### Frontend Struktur
frontend/
├── Dockerfile
├── package.json
├── src/
    ├── main.tsx
    ├── App.tsx
    ├── api/
    │   ├── client.ts
    │   ├── chatService.ts
    │   ├── feedbackService.ts   # NEU: API Call für Daumen hoch/runter
    │   └── analytics.ts         # NEU: Wrapper für PostHog/Mixpanel
    │
    ├── components/
    │   ├── common/
    │   │   ├── ErrorBoundary.tsx # NEU: Fängt UI-Crashes ab
    │   │   └── Button.tsx
    │   │
    │   ├── chat/
    │   │   ├── ChatWindow.tsx
    │   │   ├── ChatBubble.tsx
    │   │   ├── FeedbackButtons.tsx # NEU: UI für Bewertung
    │   │   └── InputArea.tsx
    │
    ├── hooks/
    │   ├── useChat.ts            # Handhabt auch Fehlerzustände (Toasts)
    │   └── useAuth.ts
    │
    └── utils/
        ├── logger.ts             # Remote Logging (Frontend Errors -> Sentry)
        └── streamParser.ts

---

## 3. Datenfluss-Beispiel mit Monitoring

Um zu verstehen, wie die "Guardrails" funktionieren, hier der Weg einer Nachricht im Fehlerfall:

1.  **Frontend:** `InputArea.tsx` fängt User-Eingabe ab → ruft `useChat.ts`.
2.  **Netzwerk:** POST Request an `http://api.tutorai.com/chat`.
3.  **Backend (API):** `main.py` Middleware startet Metrik-Messung (Latenz) und weist Trace-ID zu.
4.  **Backend (Logic):**
    * `orchestrator.py` initialisiert LangSmith Trace.
    * Router entscheidet: "Mathe".
    * `tutor.py` ruft `llm_client.py`.
5.  **Safety Check (LLM Client):**
    * `llm_client.py` versucht Google Gemini API zu erreichen.
    * **Szenario:** Gemini antwortet mit `503 Service Unavailable`.
    * **Reaktion:** `Tenacity` (Bibliothek) fängt den Fehler, wartet 0.5s und versucht es erneut.
    * **Erfolg:** Beim 2. Versuch klappt es.
    * **Log:** Warnung wird an Sentry gesendet ("LLM Flakiness detected"), aber der User merkt nichts.
6.  **Antwort:** Chunks fließen zurück zum Frontend.
7.  **Feedback:** User ist zufrieden und klickt "Daumen hoch".
    * Frontend sendet POST an `/feedback` mit `{score: 1, trace_id: ...}`.
    * Das System markiert diesen Trace in LangSmith als "Positive Example" (wichtig für zukünftiges Fine-Tuning).