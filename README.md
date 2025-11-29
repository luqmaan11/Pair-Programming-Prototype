# Pair Programming Prototype

## Requirements
- Python 3.11+
- Node.js 20+
- Postgres 14+ (Docker Desktop is the fastest way to get it running locally)

## Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Install/Postgres via Docker (recommended):
	- Install Docker Desktop, then run `docker run --name pair-programming-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16`.
	- Keep the container running; restart later with `docker start pair-programming-db`.
4. Copy `.env.example` to `.env` (or edit the existing one) and set `DATABASE_URL`. The default already points at the Docker container on `localhost:5432`.
5. With Postgres up, create the application database once: `py scripts/create_database.py`. The script loads `.env` and will create whatever database name `DATABASE_URL` references.
6. Launch the API server: `py -m uvicorn main:app --reload`.
7. Log behavior:
	- Connected successfully → `Connected to Postgres and initialized schema` (no warnings).
	- Postgres missing/unreachable → `Postgres unavailable ... falling back to in-memory store`; the app still works but data resets on restart.

## Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Using The App
- Create a room from the lobby page; the UI shows a generated room code and a shareable URL.
- Join either by pasting the code into the lobby textbox and clicking "Join" or by opening the shared `/room/<code>` URL directly.
- Room state persists in Postgres when `DATABASE_URL` is reachable. If the backend falls back to the in-memory store, the editor resets on every backend restart.
- While the backend is running with `uvicorn --reload`, any code edits cause an automatic server restart; the frontend reconnects once the server is back.

### Autocomplete Rules
- Autocomplete currently focuses on quick print helpers. Typing any of these prefixes and pausing (600 ms debounce in the frontend) issues a suggestion:
	- `pri`, `print` → `print('value')`
	- `con`, `console` → `console.log('value');`
	- `sys`, `system.out` → `System.out.println("value");`
- Other generic rules remain: `def foo` → returns a stub line, statements ending with `:` → adds `pass`, otherwise `# try adding more detail`.

### Collaboration Behavior
- Every room uses a shared WebSocket channel; multiple tabs/browsers can edit the same code simultaneously and see live cursor/code updates.
- Autocomplete suggestions appear beneath the editor—accepting them replaces the current line.
- If Postgres is online, room history survives browser refreshes; otherwise edits exist only in the current memory store session.

## Architecture Notes
- FastAPI serves REST + WebSocket endpoints. `RoomStore` persists code snapshots in Postgres via SQLAlchemy and the collaboration hub broadcasts updates over WebSockets.
- React + TypeScript + Redux Toolkit manage lobby state, room editor state, and debounce autocomplete calls.

## Improvements With More Time
- Add authentication and per-user cursors.
- Replace the mocked autocomplete with a real model/service.
- Add tests plus production build scripts/docker.
- Support room history and conflict resolution beyond last-write-wins.
- Try to replicate a more IDE type feel on the frontend.
- Run code with shared output and download data feature.
