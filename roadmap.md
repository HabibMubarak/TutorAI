# TutorAI – Implementierungs-Roadmap

Diese Roadmap beschreibt die technische Umsetzung des TutorAI-Projekts ohne Code, fokussiert auf Architektur, Datenfluss und Infrastruktur.

---

## Phase 1: Environment & Docker (Das Fundament)
**Ziel:** Eine isolierte Umgebung, die auf jedem Rechner gleich läuft.

### Tech Stack Definition
* **Backend:** Python 3.11 (stabil, schnell genug).
* **Frontend:** Node.js 20 (LTS) mit Vite.
* **Datenbank:** PostgreSQL 16 (Alpine Image für kleine Größe).
* **Container:** Docker Compose V2.

### Container-Konfiguration (`docker-compose.yml` Specs)

#### Service: `db`
* **Image:** `pgvector/pgvector:pg16`
* **Volumes:** Mapping von `./pgdata` auf `/var/lib/postgresql/data` (Datenpersistenz).
* **Environment:** `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (aus `.env`).

#### Service: `backend`
* **Build Context:** `./backend`
* **Command:** `uvicorn main:app --host 0.0.0.0 --reload` (Hot-Reloading).
* **Ports:** `8000:8000`
* **Depends on:** `db`

#### Service: `frontend`
* **Build Context:** `./frontend`
* **Command:** `npm run dev -- --host`
* **Ports:** `5173:5173`

### Environment Variables (`.env` Template)
DATABASE_URL=postgresql://user:pass@db:5432/tutorai
GEMINI_API_KEY=AIzaSy...
SECRET_KEY=supersecretkey...  # Für JWT Token Generierung

---

## Phase 2: Data Layer (Das Gedächtnis)
**Ziel:** Ein sauberes Schema, das Chats, User und Lern-Kontext speichert.

### Library Auswahl
* **ORM:** `SQLAlchemy` (Async Version) – modern und mächtig.
* **Migration:** `Alembic` – für Schema-Updates. Wichtig: Die erste Alembic-Migration muss den Befehl CREATE EXTENSION IF NOT EXISTS vector; enthalten, damit Postgres Vektoren verstehen kann.
* **Validation:** `Pydantic V2` – für Datenaustausch API ↔ DB.

### Datenmodell-Spezifikation (`models.py`)

#### Tabelle: `users`
* `id`: UUID (Primary Key)
* `email`: String (Unique, Index)
* `hashed_password`: String
* `grade_level`: Integer (z.B. 10)
* `school_type`: Enum (Realschule, Gymnasium)

#### Tabelle: `tasks`
* `id`: UUID
* `title`: String ("Mathe Arbeitsblatt 1")
* `content`: Text (Der reine Text der Aufgabe)

#### Tabelle: `task_embeddings`
* `id`: Integer
* `task_id`: ForeignKey
* `chunk_content`: Text (Ein kleiner Schnipsel des Textes, z.B. eine einzelne Aufgabe)
* `embedding`: Vector(768) (Der mathematische Vektor. 768 ist die Dimension von Geminis Embedding-Modell)


#### Tabelle: `conversations` (Threads)
* `id`: UUID
* `user_id`: ForeignKey zu `users`
* `created_at`: DateTime
* `subject`: String (z.B. "Mathe")

#### Tabelle: `messages`
* `id`: Integer (Auto Increment)
* `conversation_id`: ForeignKey zu `conversations`
* `role`: Enum ("user", "assistant", "system")
* `content`: Text
* `metadata`: JSON (z.B. verwendete Tools, Token-Count)
* `timestamp`: DateTime

### API Schema (`schemas/chat.py`)
**Input Model:** `ChatRequest`
* `message`: String (min_length=1)
* `conversation_id`: Optional[UUID]
* `context_overrides`: Optional[Dict] (falls man temporär die Schulform ändern will)

---

## Phase 3: The Logic Core (Das Gehirn)
**Ziel:** Die intelligente Verarbeitung des Requests. Hier passiert die Magie.

### Konfiguration (`school_config.yaml`)
Definition der Schul-Profile und Restriktionen:

realschule:
  tone: "ermutigend, praxisnah"
  complexity: "mittel"
  forbidden_concepts: ["Komplexe Zahlen", "Vektorräume"]

gymnasium:
  tone: "akademisch, fordernd"
  complexity: "hoch"
  required_steps: ["Herleitung", "Beweisansatz"]

### Orchestrator Logik (`orchestrator.py`)
**Input:** `user_message`, `user_profile`

1.  **History Fetch:** Lade die letzten 10 Nachrichten aus der DB (Kurzzeitgedächtnis).
2.  **Intent Recognition (Router):**
    * Sende *History* + *Input* an kleines LLM (z.B. Gemini Flash).
    * Frage: "Ist das eine Mathe-Frage, eine Scherzfrage oder Off-Topic?"
3.  **Context Assembly:**
    * Wenn Mathe: Lade `math/curriculum.json` für die Klasse.
    * Lade `school_config.yaml` basierend auf dem User-Profil.
4.  **System Prompt Builder:**
    * Kombiniere: `Persona` + `Constraints` (Config) + `Knowledge` (Curriculum) + `History`.

### Agenten Spezifikation
* **Router Agent:** Output muss striktes JSON sein (z.B. `{"intent": "math_explanation", "topic": "algebra"}`).
* **Tutor Agent:** Muss Streaming unterstützen. Benötigt Zugriff auf "Tools" (siehe Phase 5).


## Phase RAG: Knowledge Base & Vektorsuche
**Ziel:** Der Tutor kennt die spezifischen Aufgabenblätter des Schülers.

### Tech Stack Update
* **DB Extension:** `pgvector` (via Docker Image `pgvector/pgvector:pg16`).
* **Embedding Model:** `models/embedding-001` (via Google Gemini API).

### Neuer Ablauf: "Document Ingestion"
1.  **Parsing:** Text aus PDF/Bild extrahieren.
2.  **Chunking:** Text in sinnvolle Abschnitte teilen (z.B. pro Aufgabe).
3.  **Embedding:** Vektoren generieren.
4.  **Storage:** In `task_embeddings` Tabelle speichern.

### Neuer Ablauf: "Context Retrieval"
Der **Orchestrator** erhält einen neuen Schritt vor dem LLM-Aufruf:
* Generiere Embedding für User-Frage.
* Führe SQL-Query aus: `SELECT chunk_content FROM task_embeddings ORDER BY embedding <-> query_embedding LIMIT 3;`
* Füge die gefundenen Inhalte in den System-Prompt ein ("Nutze folgende Informationen zur Beantwortung: ...").

---

## Phase 4: Streaming Pipeline (Die Nervenbahnen)
**Ziel:** Die Antwort soll fließen, nicht blockieren.

### Backend Implementation
* Nutze `FastAPI.StreamingResponse`.
* Der Generator (in `llm_client.py`) muss `AsyncIterator` zurückgeben.
* **Format:** Server-Sent Events (SSE).
    * Chunk-Struktur: `data: {"token": "x"}\n\n`

### Frontend Hook (`useChat.ts` Deep Dive)
* Benötigt `AbortController` (falls User "Stop" drückt).
* **State Management:**
    * `messages`: Array `{role, content}`
    * `isLoading`: Boolean
    * `streamingContent`: String (Buffer für eingehende Chunks)
* **Logic Flow:**
    1.  User sendet → User-Message in State.
    2.  Leere AI-Message in State.
    3.  `fetch` Connection öffnen.
    4.  Loop: `reader.read()`
    5.  Decode Chunk → Append an `streamingContent` → Update State.

---

## Phase 5: UI & UX (Das Gesicht)
**Ziel:** Ein Interface, das Lernen fördert, nicht ablenkt.

### Component Architecture
* **`ChatLayout`:** Sidebar (History) + Main Area (Chat).
* **`MessageList`:** Scrollbare Area mit "Auto-Scroll to Bottom" bei neuem Text.
* **`InputArea`:** Textarea, die mitwächst (`react-textarea-autosize`).

### Rendering Engine
* **Markdown:** `react-markdown` für Formatierung (Fett, Listen).
* **Mathematik:** `rehype-katex` Plugin für LaTeX.
* **Wichtig:** Der LLM-Prompt muss anweisen, LaTeX-Formeln mit `$` oder `$$` zu umschließen.

### Visual Feedback
* **Skeleton Loader:** Anzeige während der Router analysiert (Pre-Token Phase).
* **Blinkender Cursor:** Am Ende des Streaming-Textes zur Aktivitätsanzeige.