# EV Share — TRD Summary

**Project:** EV Share  
**Architecture:** Modular Monolithic Web Application  
**Backend:** Python 3.12 + Django 6.1  
**Database:** MongoDB via MongoEngine 0.29 + PyMongo 4.19  
**Frontend:** Django Templates + Bootstrap 5.3 + Custom CSS (Apple India Quiet Design) + Vanilla JavaScript + Leaflet.js  
**Document Source:** `TRD.md`

---

## 1. Architectural Strategy & Modular Monolith

EV Share is organized as a clean, single-repository Django project divided into distinct functional applications:

```text
ev_share/
├── config/             # Django settings, root URLs, WSGI, ASGI
├── core/               # Layouts, landing page, utility services, helpers
├── accounts/           # User documents, authentication, profile, RBAC, decorators
├── chargers/           # Charger listings, geospatial search, availability schedules
├── bookings/           # Concurrency-safe booking engine, slot locks, lifecycle state machine
├── sessions_app/       # Charging session tracking (start/stop records, energy logs)
├── payments/           # Simulated payment transactions, pricing snapshots, refund states
├── reviews/            # Reviews, ratings (1-5), moderation
├── support/            # Support tickets, disputes, resolutions
├── administration/     # Custom protected admin portal (verification queue, listings, audit)
├── templates/          # Organized by app, semantic HTML, responsive
├── static/             # CSS tokens, Leaflet assets, custom JS components
├── media/              # Local upload storage for development (charger photos, KYC)
└── tests/              # Pytest & Django test suite
```

---

## 2. Database Design & MongoEngine Collections

All application entities are modeled as MongoEngine `Document` objects with explicit schema validation, default UTC timestamps, and targeted indexes:

1. **`User` (`users` collection):**
   - Fields: `full_name`, `email` (unique, lowercase indexed), `password_hash` (PBKDF2 via Django hasher), `phone_number`, `roles` (`['driver']`, `['host']`, `['admin']`), `is_active`, `is_verified_host`, `created_at`, `updated_at`.
2. **`HostVerification` (`host_verifications` collection):**
   - Fields: `user` (ReferenceField), `host_type` (residential/commercial), `id_proof_type`, `id_proof_file`, `property_permission_file`, `status` (`draft`, `submitted`, `approved`, `rejected`), `reviewer_notes`, `reviewed_by`, `reviewed_at`.
3. **`Charger` (`chargers` collection):**
   - Fields: `host` (ReferenceField), `title`, `description`, `charger_type` (`AC`/`DC`), `connector_types` (`['Type 2', 'CCS2', ...]`), `power_output_kw`, `price_per_kwh`, `currency` (`INR`), `location` (`PointField` GeoJSON), `address` (city, state, postal_code, display_address, private_directions), `amenities`, `photos`, `verification_status` (`pending`, `approved`, `rejected`, `suspended`), `is_active`.
   - Index: `[('location', '2dsphere')]`, `[('host', 1)]`, `[('verification_status', 1), ('is_active', 1)]`.
4. **`AvailabilityRule` & `BlackoutPeriod`:**
   - Weekly schedules (day_of_week 0-6, start_time, end_time) and specific date overrides.
5. **`SlotLock` (`slot_locks` collection):**
   - Concurrency barrier collection.
   - Compound Unique Index: `[('charger', 1), ('slot_start', 1)]` (unique=True).
   - Guarantees atomic slot acquisition before booking creation.
6. **`Booking` (`bookings` collection):**
   - Fields: `driver`, `host`, `charger`, `start_time`, `end_time`, `status` (`pending`, `confirmed`, `cancelled`, `completed`, `expired`, `disputed`), `pricing_snapshot` (unit_price, energy_kwh, subtotal, platform_fee, total_amount), `payment_status` (`unpaid`, `simulated_paid`, `refunded`), `cancellation_reason`, `created_at`.
7. **`ChargingSession` (`charging_sessions` collection):**
   - Fields: `booking`, `charger`, `driver`, `host`, `session_status` (`started`, `completed`, `aborted`), `meter_start_kwh`, `meter_end_kwh`, `actual_energy_kwh`, `is_manual_entry` (True), `start_notes`, `end_notes`, `recorded_at`.
8. **`PaymentTransaction` (`payment_transactions` collection):**
   - Fields: `booking`, `driver`, `amount`, `currency`, `provider` (`simulated`), `transaction_ref`, `status` (`initiated`, `success`, `failed`, `refunded`), `is_simulation` (True), `commission_amount`, `host_payout_amount`.
9. **`Review` (`reviews` collection):**
   - Fields: `booking` (unique), `charger`, `driver`, `rating` (1 to 5), `comment`, `is_moderated`, `created_at`.
10. **`SupportCase` (`support_cases` collection):**
    - Fields: `ticket_id`, `user`, `related_booking`, `subject`, `category`, `description`, `status` (`open`, `in_progress`, `resolved`), `resolution_notes`.
11. **`AuditEvent` (`audit_logs` collection):**
    - Fields: `actor_id`, `action`, `target_type`, `target_id`, `details`, `timestamp`.

---

## 3. Authentication & Session Strategy

Since Django ORM is decoupled from MongoEngine documents:
- **Sessions:** Configured to use Django's cryptographically signed cookie backend:  
  `SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`
  No relational SQL session tables required.
- **Passwords:** Generated and validated using Django's standard `make_password` and `check_password` (PBKDF2 SHA256).
- **Authentication State:** Current authenticated user ID is stored in `request.session['user_id']`.
- **Custom Middleware & Decorators:**  
  `@login_required_mongo`: validates active user session and reloads the MongoEngine `User` instance.  
  `@role_required_mongo('host')` / `@role_required_mongo('admin')`: enforces server-side role authorization.

---

## 4. Concurrency & Booking Safety

To prevent race conditions and double bookings on exclusive chargers:
1. Every booking attempts to claim atomic slot interval(s) in `SlotLock` collection.
2. The compound unique index on `(charger, slot_start)` immediately rejects concurrent reservation attempts with a duplicate key exception.
3. The booking service intercepts MongoDB `DuplicateKeyError` and converts it into a clean, friendly validation response: "This slot was just reserved by another driver. Please choose an alternate slot."
4. Cancelled or expired bookings delete corresponding slot locks, safely freeing capacity.

---

## 5. Security & Privacy Defaults
- **Input Validation:** Every form validated on the server with clean error responses.
- **CSRF Protection:** Django CSRF middleware enabled on all state-changing POST requests.
- **Privacy Policy for Addresses:** Unbooked chargers show approximate city/highway sector coordinates. Exact directions and host contact info are only revealed inside an authenticated driver's confirmed booking view.
- **Secret Isolation:** Environment settings parsed via `python-dotenv` from `.env`. Zero hardcoded credentials.
