# Debi-Dorshon Backend API (`server/`)

Welcome to the backend server repository for **Debi-Dorshon**, a Durga Puja guide application built with **FastAPI** & **MongoDB**.

---

## 🗂 Server Directory Structure

```
server/
├── .env                     # Local environment config (MongoDB URL, DB name)
├── .env.example             # Template for environment variables
├── requirements.txt         # Python dependencies
├── seed_db.py               # Database seeding script
├── README.md               # Backend documentation
│
├── data/
│   └── debi_dorshon.json    # Initial Durga Puja dataset for MongoDB seeding
│
└── app/                     # Core FastAPI Application
    ├── main.py              # Application entry point (FastAPI, CORS, MongoDB lifespan)
    │
    ├── core/                # System configuration & DB connection
    │   ├── config.py        # Settings loaded from `.env`
    │   └── database.py      # Async Motor MongoDB connection manager
    │
    ├── schemas/             # Pydantic schemas (Request / Response DTO validation)
    │   └── pandal.py        # Durga Puja pandal data schema
    │
    ├── services/            # Business logic & MongoDB query methods
    │   └── pandal_service.py # Pandal CRUD & search operations
    │
    └── api/v1/              # API Version 1 Routers & Endpoints
        ├── router.py        # Router aggregator
        └── endpoints/
            ├── health.py    # Health check endpoint (/api/v1/health)
            └── pandals.py   # Pandal endpoints (/api/v1/pandals)
```

---

## 🔄 For Node / Express (MVC) Developers: Concept Mapping

| Node.js / Express (MVC) | FastAPI Equivalent in Debi-Dorshon | Description |
| :--- | :--- | :--- |
| `dotenv` / `.env` | `app/core/config.py` | Environment variable parsing |
| `mongoose.connect()` | `app/core/database.py` | Async Motor MongoDB connection |
| `Mongoose Schema / Joi` | `app/schemas/pandal.py` | Pydantic validation schemas & types |
| `Controllers / Service` | `app/services/pandal_service.py` | Database operations & search logic |
| `express.Router()` | `app/api/v1/endpoints/pandals.py` | FastAPI `APIRouter()` routes |
| `server.js` | `app/main.py` | App entry point, CORS & middleware |

---

## 🚀 Quick Start Guide

Navigate into the `server/` directory:
```bash
cd server
```

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB Credentials (`.env`)
Edit `server/.env` with your MongoDB connection details:
```env
PROJECT_NAME="Debi-Dorshon API"
API_V1_STR="/api/v1"
HOST="0.0.0.0"
PORT=8000

# Local MongoDB:
MONGODB_URL="mongodb://localhost:27017"

# MongoDB Atlas (Cloud):
# MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.xxx.mongodb.net/?retryWrites=true&w=majority"

MONGODB_DB_NAME="debi_dorshon_db"
PANDAL_COLLECTION_NAME="pandals"
```

### 3. Seed MongoDB with Pandal Data
To import `data/debi_dorshon.json` into MongoDB, run:
```bash
python seed_db.py
```

### 4. Run FastAPI Server
```bash
uvicorn app.main:app --reload
```

---

## 📚 API Documentation
When the server is running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
