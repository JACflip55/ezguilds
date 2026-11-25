# ezguilds 🌱

AI-powered permaculture design web application. Upload a photo of your land, describe your goals, and get a companion-planting layout optimized for your climate and soil.

## Stack

- **API**: Python (FastAPI/Uvicorn), Gemini AI
- **Worker**: Python, async task processing
- **Frontend**: TypeScript, Vite
- **Infra**: Firebase (Auth + Firestore), GCS, Docker Compose
- **Deploy**: Google Cloud Run

## Quick start

```bash
cp .env.example .env     # add your GEMINI_API_KEY
make dev                 # starts API, worker, and frontend concurrently
```

Or with Docker:

```bash
docker compose up
```

The Firebase emulator runs locally — no cloud account needed for development.

## Project structure

```
api/          Python API server (FastAPI)
worker/       Async task worker for AI generation
frontend/     TypeScript/Vite frontend
infra/        Cloud setup and teardown scripts
```

## License

MIT
