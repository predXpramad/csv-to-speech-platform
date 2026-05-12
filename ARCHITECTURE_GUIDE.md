# CSV-to-Speech Platform Architecture Guide

## 1. Scalable Folder Hierarchy

The project is structured into three main domains: **Frontend**, **Backend**, and **Infrastructure**, along with dedicated **Storage** for handling files.

```text
├── frontend/               # React + Vite Application
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── components/     # Reusable UI & Feature components
│   │   │   ├── ui/         # shadcn/ui generic components
│   │   │   └── features/   # Feature-specific components (e.g., tts)
│   │   ├── hooks/          # Custom React hooks (e.g., useWebSocket)
│   │   ├── lib/            # Utility libraries (e.g., tailwind merge)
│   │   ├── pages/          # Route-level components
│   │   ├── services/       # API and WebSocket client services
│   │   ├── store/          # Global state management (Zustand/Redux)
│   │   ├── styles/         # Global CSS and Tailwind directives
│   │   └── types/          # TypeScript interfaces and types
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── api/            # API Routers and Endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       └── api.py
│   │   ├── core/           # Configuration, Security, Events
│   │   ├── middleware/     # Custom HTTP middlewares (CORS, Logging)
│   │   ├── models/         # Database / Domain models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic (EdgeTTS, CSV parsing)
│   │   ├── storage/        # File management abstraction
│   │   ├── utils/          # Helper functions (ZIP creation, async tasks)
│   │   └── websocket/      # WebSocket connection managers
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── storage/                # Shared Volume for File Lifecycle
│   ├── uploads/            # Raw user uploaded CSVs
│   ├── temp_audio/         # Individual generated .wav/.mp3 files
│   ├── zip_exports/        # Final compressed archives for download
│   └── metadata/           # Job metadata and processing states (optional JSON)
│
├── nginx/                  # Reverse Proxy Configuration
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
│
├── docker-compose.yml      # Multi-container orchestration
├── .env.example            # Environment variables template
└── README.md
```

## 2. Naming Conventions

### Frontend (TypeScript / React)
*   **Components & Pages**: PascalCase (e.g., `FileUpload.tsx`, `Dashboard.tsx`).
*   **Hooks**: camelCase with `use` prefix (e.g., `useWebSocket.ts`, `useTTSJob.ts`).
*   **Services & Utils**: camelCase (e.g., `apiService.ts`, `formatDate.ts`).
*   **Types/Interfaces**: PascalCase, often with 'I' prefix or plain name (e.g., `JobStatus.ts`, `User.ts`).
*   **Store**: camelCase (e.g., `ttsStore.ts`).

### Backend (Python / FastAPI)
*   **Files & Modules**: snake_case (e.g., `edge_tts_service.py`, `zip_manager.py`).
*   **Classes**: PascalCase (e.g., `EdgeTTSService`, `JobCreateSchema`).
*   **Functions & Variables**: snake_case (e.g., `generate_audio`, `active_connections`).
*   **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE`, `TEMP_DIR_PATH`).

## 3. Recommended Architecture Notes

### A. Modular Service-Based Backend
Decouple routing from business logic. Endpoints (`api/v1/endpoints/tts.py`) should only handle HTTP/WS requests and validation. The actual CSV parsing, audio generation via `edge-tts`, and ZIP archiving should be delegated to specialized modules in the `services/` and `utils/` directories.

### B. WebSocket Strategy
Use WebSockets for real-time progress monitoring. When a user uploads a CSV, return a `job_id`. The frontend connects to `ws://.../ws/{job_id}`. As the backend processes each row asynchronously using `asyncio` and `edge-tts`, it publishes progress updates (e.g., `{"row": 5, "status": "processing", "progress": "50%"}`) to the WebSocket manager, which relays it to the client.

### C. ZIP Lifecycle Management & Storage
Files need a strict lifecycle to prevent disk overflow:
1.  **Upload**: Save CSV to `storage/uploads/`.
2.  **Process**: Generate audio files into `storage/temp_audio/{job_id}/`.
3.  **Archive**: Once complete, bundle audio into `storage/zip_exports/{job_id}.zip`.
4.  **Cleanup**: Implement a background task (e.g., using `asyncio.create_task` or a lightweight scheduler like `APScheduler`/`Celery`) to delete `temp_audio/{job_id}` after zipping, and delete `zip_exports/{job_id}.zip` after 24 hours.

### D. Docker & Cloud Deployment
*   **Reverse Proxy (NGINX)**: Acts as the entry point, serving the static React build (or proxying to Vite in dev), and proxying `/api` and `/ws` to the FastAPI backend. It also handles WebSocket protocol upgrades.
*   **Volumes**: Map the `storage/` directory as a Docker volume so it persists across container restarts and can be backed up or mounted to cloud storage (e.g., AWS EFS) if needed.
*   **Scalability**: For horizontal scaling, the WebSocket manager may need a Redis pub/sub backplane to broadcast messages across multiple FastAPI instances, and a shared task queue (like Celery + Redis/RabbitMQ) for the TTS workload.
