# 🛕 Debi-Dorshon

Debi-Dorshon is a comprehensive Durga Puja guide application providing detailed pandal location, navigation, and transport information across Kolkata.

---

## 🚀 Quick Start with Docker (Recommended)

Run the entire application (FastAPI Backend + MongoDB) with **one single command**:

```bash
docker compose up --build
```

That's it! 
- **MongoDB**: Automatically starts on `localhost:27017`
- **FastAPI API**: Available at [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: Available at [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Routes Documentation**: See [API_ROUTES.md](file:///d:/Coding_local/Debi-Dorshon/API_ROUTES.md)

To stop all services:
```bash
docker compose down
```

---

## 🛠 Local Development Setup (Without Docker)

### 1. Backend Server Setup (`/server`)
```bash
cd server
uv sync
uv run uvicorn app.main:app --reload
```

### 2. (Optional) Database Seeding (`/scripts`)
To import or re-seed pandal data into MongoDB from `scripts/debi_dorshon.json`:
```bash
uv run --project server python scripts/seed_db.py
```

---

## 🗂 Project Architecture
```
Debi-Dorshon/
├── docker-compose.yml     # Docker Compose orchestration
├── README.md              # Project documentation
├── API_ROUTES.md          # Complete API Endpoint & Schema Reference
├── scripts/               # Developer tooling & data scripts
│   ├── convert.py         # Parses Excel -> JSON
│   ├── seed_db.py         # Database seeding script
│   └── debi_dorshon.json  # Master Puja Pandals dataset
├── server/                # FastAPI & Async MongoDB backend
│   ├── Dockerfile         # Docker build recipe
│   ├── pyproject.toml     # Backend dependencies
│   └── app/               # FastAPI core, schemas, services & endpoints
└── client/                # Reserved for Frontend client app
```
