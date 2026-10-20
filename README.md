# EV Share — Peer-to-Peer EV Charging Marketplace

> **Pilot Travel Corridor:** Yamuna Expressway (Delhi NCR – Greater Noida – Mathura – Agra, ~165 km)  
> **Architecture:** Django 6.1 Modular Monolith · MongoDB via MongoEngine 0.29 / Mongomock Fallback · Leaflet.js · Bootstrap 5.3 Custom CSS

---

## 1. Project Overview

**EV Share** is a peer-to-peer electric vehicle charging marketplace engineered for highway corridors in India. It connects:
- **EV Drivers** requiring reliable, scheduled charging access along intercity highway routes.
- **Charger Hosts** with eligible private, farmstead, hotel, or commercial charging stations.
- **Platform Administrators** who moderate KYC identity verifications, inspect listing safety, manage bookings, and handle dispute resolutions.

The application features:
- **Atomic Concurrency Barriers (`SlotLock`):** Guaranteed double-booking prevention using unique compound indexes on `(charger, slot_start)`.
- **Interactive Leaflet Corridor Map:** Real-time GeoJSON marker placement with dynamic filter sync (connector type, charging mode, kW rating, price).
- **Vehicle Compatibility Matrix:** Instant port and battery compatibility checking (CCS2, Type 2, 15A Indian 3-Pin).
- **Address Privacy Protection:** Confidential private driveway directions and gate access codes are encrypted and displayed *only* to authorized drivers after slot confirmation.
- **Simulated Payment Sandbox:** Itemized billing with transparent platform fees (15%) and host earnings (85%) with prominent pilot simulation watermarks.
- **Visit Telemetry & Reviews:** Transparent tracking of manual meter readings with clear disclaimer labels, paired with verified driver reviews.
- **Urgent Low-Battery Assistance Mode:** Rapid one-touch discovery prioritizing the nearest bookable high-power fast chargers within 60 km.

---

## 2. Technology Stack

- **Backend:** Python 3.12 · Django 6.1.2 (Modular Monolith)
- **Database:** MongoDB via MongoEngine 0.29.3 + PyMongo 4.19
  - *Dynamic In-Memory Fallback:* Includes seamless `mongomock` in-memory fallback in `config/database.py`, enabling immediate zero-configuration local execution and test suite runs even when a local MongoDB daemon is not started.
- **Sessions & Auth:** Django signed-cookie session engine (`django.contrib.sessions.backends.signed_cookies`), completely decoupling the application from relational SQL tables. Passwords hashed using PBKDF2 (`make_password`, `check_password`).
- **Frontend:** Django Templates · Bootstrap 5.3 · Leaflet.js 1.9.4 · Custom Apple India quiet design CSS (`static/css/ev_share.css`).
- **Testing:** Pytest 9.1 with automated coverage for auth, chargers, bookings, payments, and security.

---

## 3. Project Structure

```text
EV Share/
├── config/                  # Project configuration, URLs, database connector, and WSGI/ASGI
├── core/                    # Base layout, corridor home, static content, and AuditEvent models
├── accounts/                # User identity, vehicle profiles, KYC onboarding, and decorators
├── chargers/                # Listings, availability rules, geospatial Haversine search, and compatibility
├── bookings/                # Reservation lifecycle, atomic SlotLock engine, and pricing snapshots
├── sessions_app/            # Charging visit check-in/out, meter telemetry, and dispute escalation
├── payments/                # Simulated payment checkout, transaction receipts, and fee splits
├── reviews/                 # Verified driver reviews and rating aggregation
├── support/                 # Support cases, grievance tracking, and inquiry tickets
├── administration/          # Admin dashboard, host KYC moderation, listing queue, and audit inspector
├── docs/                    # PRD, TRD, Traceability Matrix, Architecture Decisions, and Assumptions
├── static/css/              # Custom design system stylesheet (ev_share.css)
├── templates/               # Responsive Django templates organized by domain
├── tests/                   # Automated pytest suite covering all P0 workflows
├── seed_data.py             # Turnkey corridor pilot data seeding script
└── manage.py                # Django management CLI
```

---

## 4. Quick Start & Local Execution

### Option A: Local Python Environment
```bash
# 1. Create and activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env

# 4. Seed corridor pilot data
python seed_data.py

# 5. Start development server
python manage.py runserver 8000
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.

### Option B: Docker Compose (Full Stack with MongoDB)
```bash
docker-compose up --build
```
This boots both the EV Share Django web application (Gunicorn + WhiteNoise) and a dedicated MongoDB 7.0 database container with health checks.

---

## 5. Pre-Seeded Pilot Credentials

| Role | Email | Password | Details |
|---|---|---|---|
| **Administrator** | `admin@evshare.in` | `admin123` | Full administrative access to KYC queue, moderation, audit logs, and metrics |
| **Driver (Primary)** | `driver@evshare.in` | `driver123` | Rahul Mehra — Registered Tata Nexon EV Max (40.5 kWh, CCS2) with confirmed reservation |
| **Driver (Secondary)** | `priya.driver@evshare.in` | `driver123` | Priya Nair — Registered MG ZS EV (50.3 kWh, CCS2) |
| **Host (KM 0)** | `host.noida@evshare.in` | `host123` | Rohan Gupta — Greater Noida Expressway Fast Hub (30 kW DC) |
| **Host (KM 38)** | `host.jewar@evshare.in` | `host123` | Vikram Chaudhary — Jewar Toll Expressway Dual Fast Charger (60 kW DC) |
| **Host (KM 108)** | `host.mathura@evshare.in` | `host123` | Pooja Agarwal — Mathura Highway Oasis Station (30 kW DC) |
| **Host (KM 165)** | `host.agra@evshare.in` | `host123` | Arjun Verma — Agra Gateway Ultra-Fast Bay (50 kW DC) |
| **Host (Pending KYC)** | `host.pending@evshare.in` | `host123` | Amit Patel — Pending listing for admin moderation testing |

---

## 6. Running Automated Tests

Run the complete 25-test automated suite using `pytest`:

```bash
venv\Scripts\pytest -v
```

### Test Coverage Highlights:
- `tests/test_auth.py` (5 tests): Registration, PBKDF2 authentication, duplicate email rejection, RBAC roles, signed session cookie resolution.
- `tests/test_chargers.py` (4 tests): Geospatial proximity sorting (Haversine formula), corridor milestone queries, connector filtering, vehicle compatibility matching.
- `tests/test_bookings.py` (4 tests): Atomic `SlotLock` creation, race condition double-booking rejection, host self-booking block, booking cancellation slot release.
- `tests/test_payments.py` (4 tests): Simulated transaction generation, platform commission (15%) & host payout (85%) split, authorization success/fail paths, simulated refunds.
- `tests/test_security.py` (4 tests): Unauthenticated route protection, address privacy enforcement, driver data isolation.
- `tests/test_sessions_and_reviews.py` (4 tests): Charging visit check-in/out, meter kWh delta calculation, driver reviews & rating recalculation, support ticket resolution, and JSON health check endpoint.

**Result:** `25 passed in ~39s (100% pass rate)`.

---

## 7. Production & Cloud Deployment Readiness

- **Containerization:** Ready for Docker/Kubernetes with multi-stage [Dockerfile](file:///c:/Users/Pranav/Desktop/EV%20Share/Dockerfile) and [docker-compose.yml](file:///c:/Users/Pranav/Desktop/EV%20Share/docker-compose.yml).
- **PaaS Deployment:** Ready for Railway / Render / Fly.io with [Procfile](file:///c:/Users/Pranav/Desktop/EV%20Share/Procfile).
- **Static Assets:** Serves compressed and hashed static files via WhiteNoise (`whitenoise.middleware.WhiteNoiseMiddleware`).
- **Health Check Endpoint:** `GET /health/` returns JSON platform and database readiness status for container orchestrators and load balancers.


---

## 7. Pilot Corridor Milestones (Yamuna Expressway)

1. **KM 0 — Greater Noida (Zero Point):**
   - Coordinates: `28.4744, 77.5040`
   - *Greater Noida Expressway Fast Hub:* 30 kW DC Fast (CCS2) + Type 2 AC, ₹16.50/kWh.
2. **KM 38 — Jewar Toll Plaza:**
   - Coordinates: `28.1287, 77.5562`
   - *Jewar Toll Dual Fast Bay:* 60 kW DC (CCS2), ₹18.00/kWh, 24/7 food court.
3. **KM 42 — Jewar Farmstead:**
   - Coordinates: `28.1050, 77.5720`
   - *Jewar Heritage Farmstead AC:* 7.4 kW Type 2 AC, ₹13.50/kWh, organic dining.
4. **KM 108 — Mathura Interchange:**
   - Coordinates: `27.6042, 77.6250`
   - *Mathura Highway Oasis:* 30 kW DC Fast (CCS2) + Type 2 AC, ₹16.00/kWh.
5. **KM 165 — Agra Inner Ring Road (Expressway Terminus):**
   - Coordinates: `27.2185, 77.9940`
   - *Agra Gateway Ultra-Fast Bay:* 50 kW DC (CCS2), ₹17.50/kWh.

---

## 8. Pilot Compliance & Disclaimers

1. **Payment Simulation:** Real payment processing and merchant banking integrations are disabled pending regulatory pilot clearance. Transactions are simulated for demonstration and recorded in a sandbox ledger.
2. **Manual Telemetry:** Energy meter readings are manually logged by drivers and hosts upon visit arrival and departure. Values are clearly designated as self-reported and unverified.
3. **Address Privacy:** Exact driveway directions and gate codes are revealed exclusively to drivers holding confirmed reservations.
