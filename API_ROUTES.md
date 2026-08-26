# 🗺️ Debi-Dorshon API Routes Reference

This document provides a comprehensive reference for all available API endpoints in the **Debi-Dorshon** backend service for future developers and frontend integration.

---

## 📌 Base Information

- **Base URL**: `http://localhost:8000`
- **API v1 Prefix**: `http://localhost:8000/api/v1`
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON Schema**: `http://localhost:8000/api/v1/openapi.json`

---

## 🚀 Quick Reference Table

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API Root / Welcome Message | ❌ No |
| `GET` | `/api/v1/health` | Health Check (Server & MongoDB) | ❌ No |
| `GET` | `/api/v1/pandals/` | List all pandals (Filter, Search & Paginate) | ❌ No |
| `GET` | `/api/v1/pandals/{pandal_id}` | Get pandal details by ObjectId | ❌ No |
| `POST` | `/api/v1/pandals/` | Add a new Durga Puja pandal | ❌ No |

---

## 🧱 Data Schemas

### 1. `LocationSchema`
```json
{
  "latitude": 22.5986,
  "longitude": 88.3712
}
```

### 2. `TransportInfoSchema`
```json
{
  "name": "Shyambazar",
  "line": "Blue Line"
}
```

### 3. `PandalResponse`
```json
{
  "id": "64d3f1a2b3c4d5e6f7a8b9c0",
  "name": "Shikdar Bagan Pushparaj",
  "region": "North",
  "cluster": "Shyambazar",
  "location": {
    "latitude": 22.598634,
    "longitude": 88.371205
  },
  "nearest_metro": {
    "name": "Shyambazar",
    "line": "Blue Line"
  },
  "nearest_station": {
    "name": "Kolkata Railway Station",
    "line": null
  },
  "nearest_ferry": {
    "name": "Bagbazar Ghat",
    "line": null
  }
}
```

---

## 🛰️ Detailed Endpoint Specifications

### 1. Welcome Root Endpoint
Returns a basic welcome message and navigation links.

- **Method**: `GET`
- **Path**: `/`
- **Response**: `200 OK`
```json
{
  "message": "Welcome to Debi-Dorshon API!",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

---

### 2. Health Check
Verifies server health and active connection to MongoDB.

- **Method**: `GET`
- **Path**: `/api/v1/health`
- **Response**: `200 OK`
```json
{
  "status": "online",
  "database": "healthy",
  "service": "Debi-Dorshon Backend API"
}
```

---

### 3. List Pandals (With Search, Filters & Pagination)
Retrieves a list of Durga Puja pandals with optional query parameters.

- **Method**: `GET`
- **Path**: `/api/v1/pandals/`
- **Query Parameters**:

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `region` | `string` | ❌ No | `null` | Case-insensitive filter by region (e.g. `North`, `South`) |
| `cluster` | `string` | ❌ No | `null` | Case-insensitive filter by cluster (e.g. `Shyambazar`, `Ahiritola`) |
| `search` | `string` | ❌ No | `null` | Case-insensitive search on pandal `name` |
| `skip` | `integer` | ❌ No | `0` | Offset for pagination (`ge=0`) |
| `limit` | `integer` | ❌ No | `100` | Max items returned (`ge=1`, `le=500`) |

- **Example Request**:
  `GET /api/v1/pandals/?region=North&search=Shikdar&skip=0&limit=10`

- **Response**: `200 OK`
```json
[
  {
    "id": "66ce3f890123456789abcdef",
    "name": "Shikdar Bagan Pushparaj",
    "region": "North",
    "cluster": "Shyambazar",
    "location": {
      "latitude": 22.5986,
      "longitude": 88.3712
    },
    "nearest_metro": {
      "name": "Shyambazar",
      "line": "Blue Line"
    },
    "nearest_station": {
      "name": "Kolkata Station"
    },
    "nearest_ferry": null
  }
]
```

---

### 4. Get Pandal by ID
Retrieve details of a single pandal using its 24-character hexadecimal MongoDB `ObjectId`.

- **Method**: `GET`
- **Path**: `/api/v1/pandals/{pandal_id}`
- **Path Parameters**:
  - `pandal_id` (`string`, required): MongoDB ObjectId (e.g. `66ce3f890123456789abcdef`)

- **Responses**:
  - `200 OK`: Returns single `PandalResponse` object.
  - `404 Not Found`:
    ```json
    {
      "detail": "Pandal with ID 'invalid_id' not found."
    }
    ```

---

### 5. Create Pandal
Add a new pandal entry into the MongoDB collection.

- **Method**: `POST`
- **Path**: `/api/v1/pandals/`
- **Header**: `Content-Type: application/json`
- **Request Body** (`PandalCreate`):
```json
{
  "name": "Bagbazar Sarbojanin",
  "region": "North",
  "cluster": "Bagbazar",
  "location": {
    "latitude": 22.6025,
    "longitude": 88.3670
  },
  "nearest_metro": {
    "name": "Shyambazar",
    "line": "Blue Line"
  },
  "nearest_station": {
    "name": "Kolkata Station"
  },
  "nearest_ferry": {
    "name": "Bagbazar Ghat"
  }
}
```

- **Responses**:
  - `201 Created`: Returns newly created `PandalResponse` object with generated `id`.
  - `422 Unprocessable Entity`: Triggered if payload violates field validation.

---

## 💻 Code Snippets / Example Usage

### JavaScript (`fetch`)
```javascript
// Fetch pandals in South region
async function getSouthPandals() {
  const res = await fetch('http://localhost:8000/api/v1/pandals/?region=South');
  const pandals = await res.json();
  console.log(pandals);
}
```

### cURL
```bash
# List all pandals (first 10)
curl -X GET "http://localhost:8000/api/v1/pandals/?skip=0&limit=10"

# Search pandal by name
curl -X GET "http://localhost:8000/api/v1/pandals/?search=Hatibagan"

# Add a new pandal
curl -X POST "http://localhost:8000/api/v1/pandals/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Chetla Agrani",
       "region": "South",
       "cluster": "Kalighat",
       "location": { "latitude": 22.5186, "longitude": 88.3432 }
     }'
```
