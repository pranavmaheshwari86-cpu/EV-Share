# EV Share — Project Assumptions

This document records the foundational technical and business assumptions governing the implementation of the EV Share web application.

---

## 1. Pilot Geography & Travel Corridor
- **Corridor Selection:** The initial pilot corridor is modeled along the **Yamuna Expressway (Delhi NCR – Greater Noida – Mathura – Agra)**. This corridor is approximately 165 km, has high EV passenger traffic, and exhibits distinct charging demand during inter-city travel.
- **Seeded Locations:** Seed data includes realistic waypoints (e.g., Greater Noida Tech Zone, Jewar Interchange, Mathura Highway Rest Stop, Agra City Outskirts) with realistic latitude and longitude coordinates.

## 2. Currency, Financials & Timezone
- **Currency:** All financial figures are denominated in Indian Rupees (INR, ₹).
- **Timezone:** Datetime values are stored internally as UTC ISO datetimes in MongoDB and presented to users in **Indian Standard Time (IST, UTC+5:30)**.
- **Platform Commission:** The platform fee model is set at an illustrative 15% platform commission on gross booking value, with 85% allocated to the host's illustrative payout balance.

## 3. Database & Local Development Fallback
- **Database Architecture:** MongoDB with MongoEngine document models is the primary persistence layer.
- **Local / Mock Fallback:** When a remote MongoDB Atlas cluster is not configured or network access is restricted, the application test suite and local environment gracefully utilize an in-memory/mock connector (`mongomock`) or a local MongoDB connection string, ensuring that all functionality and automated tests can run autonomously without external infrastructure blockers.

## 4. Authentication & Session Strategy
- **Session Backend:** Because MongoEngine replaces the standard relational Django ORM, Django's signed-cookie session backend (`django.contrib.sessions.backends.signed_cookies`) is utilized. This avoids relational SQL dependency while maintaining cryptographic tamper-proof security.
- **Password Hasher:** Django's battle-tested PBKDF2 SHA256 password hasher (`make_password` / `check_password`) is used for credential storage in the MongoEngine `User` document.

## 5. Booking Concurrency & Hardware Telemetry
- **Booking Time Interval:** Reservable slots are discretized into 1-hour intervals or defined fixed slots. Atomic slot locks (`SlotLock`) with compound unique indexes on `(charger, slot_start)` strictly prevent double-booking.
- **Telemetry Reality:** Because third-party hardware integration (OCPP 1.6/2.0) is out of MVP scope, charging sessions are manually reported by hosts and drivers. All session screens explicitly state "Manual Host Entry — Unverified Telemetry" to preserve transparency.

## 6. Payment Processing
- **Simulated Payment Gateway:** A built-in sandbox payment simulator is provided to demonstrate the full checkout experience, order creation, transaction references, success states, and refund states without collecting real card numbers or executing real banking transfers.
