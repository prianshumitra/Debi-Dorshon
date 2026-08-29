# 🛕 Debi-Dorshon

Debi-Dorshon is a comprehensive Durga Puja guide backend application providing detailed pandal location, search, navigation, transport guidance (Ride by Metro & Ride by Train), and itinerary trip planning (Puja Parikrama) across Kolkata.

---

## 🚀 Quick Start with Docker (Recommended)

Run the entire backend stack (FastAPI API + Async MongoDB) with **one single command**:

```bash
docker compose up --build -d
```

That's it!
- **MongoDB Database**: Automatically running on `localhost:27017`
- **FastAPI API**: Available at [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: Available at [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Routes Reference**: See [API_ROUTES.md](file:///e:/Debi-Dorshon/API_ROUTES.md)

To stop all services:
```bash
docker compose down
```

---

## 🛠 Local Development Setup (Without Docker)

### 1. Install Dependencies with UV
```bash
uv sync --project backend
```

### 2. Database Seeding (`/scripts`)
Import or re-seed pandal data from `data/processed/debi_dorshon.json` into MongoDB:
```bash
uv run --project backend python scripts/seed_db.py
```

### 3. Start FastAPI Server (`/backend`)
```bash
uv run --project backend uvicorn app.main:app --reload
```

---

## 🗂 Project Architecture

```
Debi-Dorshon/
├── backend/                           # FastAPI Backend Application
│   ├── app/                           # Source code
│   │   ├── main.py                    # App entry point & CORS
│   │   ├── api/v1/                    # API v1 routers and endpoints
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py          # Health check endpoint
│   │   │   │   ├── pandals.py         # Read-only pandals search & details
│   │   │   │   ├── transit.py         # Ride by Metro & Ride by Train APIs
│   │   │   │   └── trip.py            # Puja Parikrama trip planner API
│   │   │   └── router.py              # Central v1 router aggregator
│   │   ├── core/                      # Settings & Mongo database manager
│   │   ├── schemas/                   # Pydantic DTO models
│   │   ├── services/                  # Business logic & Mongo queries
│   │   └── utils/                     # Geo-spatial Haversine helpers
│   ├── tests/                         # Pytest unit tests
│   ├── Dockerfile                     # Production Docker build recipe
│   ├── pyproject.toml                 # Authoritative Python dependencies
│   └── uv.lock                        # Astral UV lockfile
│
├── data/                              # Data Repository
│   ├── raw/                           # Source dataset (Debi-Dorshon.xlsx)
│   └── processed/                     # Parsed JSON & coordinates cache
│
├── scripts/                           # ETL & Database Seeding Tools
│   ├── convert_excel.py               # Excel to JSON parser & link expander
│   └── seed_db.py                     # MongoDB database seeder
│
├── docker-compose.yml                 # Multi-container orchestration
├── API_ROUTES.md                      # Comprehensive API endpoints reference
├── README.md                          # Master documentation
└── .gitignore                         # Project-wide gitignore rules
```
