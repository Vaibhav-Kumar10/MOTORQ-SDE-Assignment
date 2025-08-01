Video link
- https://drive.google.com/drive/folders/11zOHMIzi4Ck3WJcsLsQlmYKZI-U1ut-F?usp=sharing


## 🚗 Connected Car Fleet Management System

A Django-based microservice system for managing a fleet of connected vehicles with telemetry ingestion, real-time analytics, alerts, and optimizations like caching, rate limiting, and batch processing.

---

### 📦 Features

- Vehicle registration and management (CRUD)
- Real-time telemetry data ingestion
- Alerts for unusual driving behavior (e.g., speeding)
- Aggregated fleet analytics (average speed, fuel usage)
- Redis caching for fast API responses
- Rate limiting to prevent abuse
- Batch insertion for efficient data handling
- Dockerized setup for production-ready deployment

---

### 🏗️ System Architecture

```text
+---------------------------+
|        VehicleFleet       |
|   - Vehicle CRUD APIs     |
+-------------+-------------+
              |
              v
+-------------+-------------+
|        Telemetry          |
| - Accept telemetry data   |
| - Validate & store        |
+-------------+-------------+
              |
              v
+-------------+-------------+
|        Analytics           |
| - Compute stats & reports  |
| - Detect alerts            |
| - Cache with Redis         |
+-------------+-------------+

        [ PostgreSQL / SQLite ]   [ Redis ]
```

---

### 🐳 Docker Setup

> Requires: Docker + Docker Compose installed

#### 📁 Folder structure (as per your screenshot)

```
carFleetMngmntSys/
├── fleetMngmntSys/
│   ├── fleetAnalytics/
│   ├── telemetry/
│   ├── vehicleFleet/
│   ├── fleetMngmntSys/
│   ├── db.sqlite3
│   ├── manage.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
```

---

### ⚙️ Getting Started

#### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/carFleetMngmntSys.git
cd carFleetMngmntSys/fleetMngmntSys
```

#### 2. Build and Start Containers

```bash
docker-compose up --build
```

This will:

- Build the Django app
- Start Redis
- Launch app on `http://localhost:8000/`

#### 3. Apply Migrations

```bash
docker-compose exec web python manage.py migrate
```

#### 4. Create Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

---

### 🧪 API Usage

Use [Postman](https://www.postman.com/) or `curl` to test APIs.

#### 🚘 Vehicle APIs

```bash
# Add vehicle
curl -X POST http://localhost:8000/api/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{"vin": "AB1234", "vManufacturer": "Tata", "vModel": "Nexon"}'

# List vehicles
curl http://localhost:8000/api/vehicles/
```

#### 📡 Telemetry Ingestion

```bash
curl -X POST http://localhost:8000/api/telemetry/ \
  -H "Content-Type: application/json" \
  -d '{
        "vin": "AB1234",
        "speed": 85,
        "fuel_level": 60,
        "location": "28.644800, 77.216721",
        "timestamp": "2025-08-01T10:00:00Z"
      }'
```

#### 📊 Analytics

```bash
curl http://localhost:8000/api/analytics/summary/
```

---

### 🔐 Optional Features

- **Rate Limiting**: Prevents abuse using IP-based throttling
- **Redis Caching**: Speeds up frequently queried analytics
- **JWT Authentication**: Can be added for securing endpoints

---

### 📄 Technologies Used

- Django 4.x
- SQLite (or PostgreSQL)
- Redis
- Docker / Docker Compose
- Python 3.11
- `ratelimit`, `django-redis`, `uvicorn`

---

### 🧠 Design Decisions

- Split functionality into apps for modularity
- `Telemetry` writes frequently, so optimized with batch insert
- `Analytics` uses Redis cache to avoid recomputing expensive queries
- `Alerts` triggered when abnormal telemetry (e.g., high speed) is ingested

---

### 🧪 Testing Locally

```bash
python manage.py runserver
```

Or use Docker:

```bash
docker-compose up
```

---

### ✅ Submission Checklist

- [x] All APIs working (tested via curl/Postman)
- [x] Version-controlled with Git and clear commit history
- [x] Dockerfile and docker-compose configured
- [x] `README.md` and `architecture.md` added
- [x] Demonstrated telemetry and alert flow

---

### 📬 Contact

Vaibhav Kumar
📧 [vaibhav@example.com](mailto:vaibhav@example.com)
🔗 [GitHub Profile](https://github.com/yourusername)



## Project Structure

fleet_project/  
│  
├── vehicleFleet/ # Vehicle CRUD & fleet management  
├── telemetry/ # Telemetry endpoints & alert handling  
├── fleetAnalytics/ # Analytics endpoints  
├── manage.py  
└── ...
