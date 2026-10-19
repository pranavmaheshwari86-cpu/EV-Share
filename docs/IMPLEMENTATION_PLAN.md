# EV Share — Detailed Implementation Plan

**Objective:** Build a complete, production-grade, demonstrable web application for the EV Share peer-to-peer charging marketplace following the PRD, TRD, Design System, and Agents operational guidelines.

---

## Phase 1 — Requirements & Architectural Alignment
- [x] Read and analyze `PRD.md`, `TRD.md`, `Design.md`, and `Agents.md`.
- [x] Produce `docs/PRD_SUMMARY.md`.
- [x] Produce `docs/TRD_SUMMARY.md`.
- [x] Produce `docs/REQUIREMENTS_TRACEABILITY.md`.
- [x] Produce `docs/IMPLEMENTATION_PLAN.md` (this document).
- [x] Produce `docs/ASSUMPTIONS.md`.
- [x] Produce `docs/DECISIONS.md`.

---

## Phase 2 — Architecture, Foundation & Core Setup
1. **Django Project Initialization:**
   - Create project structure under `ev_share/` (or root with `config/`).
   - Configure `manage.py` and `config/settings.py`.
   - Setup `SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`.
   - Setup `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` via `python-dotenv`.
2. **MongoDB Connectivity & MongoEngine:**
   - Create `config/database.py` initializing MongoEngine connection with fallback for local test mock (`mongomock`) if no remote URI is active.
   - Verify document connection and index creation scripts.
3. **Design System & UI Assets:**
   - Base template `templates/base.html` incorporating Apple India-inspired quiet aesthetic:
     - Neutral background (`--color-canvas: #F5F5F7`, elevated: `#FFFFFF`, ink: `#1D1D1F`).
     - Action blue (`--color-action: #0071E3`, hover: `#0076DF`).
     - Clean typography using system sans-serif font stack.
     - Pill buttons (`border-radius: 999px`), restrained badges, and quiet 1px dividers.
     - Leaflet CSS/JS bundle integration for interactive corridor maps.
     - Clean responsive navigation with role-aware drawer menu.
     - Zero AI clichés (no glowing purple cards, no fake uptime numbers, no placeholder buttons).

---

## Phase 3 — Core Functional Modules & Persistence
1. **Accounts & Authentication (`accounts`):**
   - Documents: `User` (email unique, hashed password, roles `['driver', 'host', 'admin']`, active state).
   - `HostVerification` (KYC details, property proof, status lifecycle).
   - Views & URLs: Registration, Login, Logout, Profile update, Host Onboarding application.
   - Decorators: `@login_required_mongo`, `@role_required_mongo`.
2. **Charger Marketplace & Discovery (`chargers`):**
   - Documents: `Charger`, `AvailabilityRule`, `BlackoutPeriod`.
   - GeoJSON Point field with `2dsphere` index.
   - Views & URLs:
     - Search & Corridor Explorer (Map view + List view + Filters for connector, power, price, availability).
     - Charger Detail view (connector specs, verified badge, pricing breakdown, schedule).
     - Host listing management: Create, Edit, Toggle Pause/Active.
     - Low-Battery Assistance view (quick urgent nearest charger finder).
3. **Concurrency-Safe Booking Engine (`bookings`):**
   - Documents: `Booking`, `SlotLock`.
   - Concurrency barrier: `SlotLock` with compound unique index `[('charger', 1), ('slot_start', 1)]`.
   - Views & URLs:
     - Booking checkout & slot selection.
     - Instant booking confirmation & reference generator (`EVS-XXXXXX`).
     - Driver Booking History & detail views.
     - Cancellation workflow with automatic slot lock release.
4. **Charging Sessions Tracking (`sessions_app`):**
   - Documents: `ChargingSession`.
   - Views & URLs:
     - Host visit check-in (start session + initial meter reading).
     - Host visit checkout (end session + final meter reading + manual entry note).
     - Report charging problem / visit issue.
5. **Simulated Payments & Pricing (`payments`):**
   - Documents: `PaymentTransaction`.
   - Server-side quote calculator (energy charge + platform commission + GST snapshot).
   - Simulated payment gateway checkout modal/page (success/failure triggers, mock webhook handler).
   - Permanent pricing snapshot on confirmed booking.
6. **Reviews, Support & Administration (`reviews`, `support`, `administration`):**
   - Reviews restricted strictly to completed bookings with 1–5 star rating.
   - Support ticket creation for booking disputes and safety escalation.
   - Custom Protected Administration Dashboard:
     - Host verification approval/rejection queue.
     - Charger moderation (suspend/publish).
     - Booking & simulated payment monitoring.
     - Audit logs review.

---

## Phase 4 — Seed Data & Corridor Pilot Integration
1. **Corridor Demonstration Seed Data:**
   - Seed realistic pilot chargers along the Yamuna Expressway corridor (Greater Noida, Jewar, Mathura, Agra).
   - Pre-populate verified commercial hosts (hotels, restaurants, highway stops) and residential hosts.
   - Seed admin user account for turnkey evaluation.
2. **End-to-End User Journeys Verification:**
   - Guest → Register → Search on Map → Check Compatibility → Instant Book.
   - Host → Onboard → Admin Review → Approved → Create Listing → Configure Schedule.
   - Active Booking → Host Check-in → Session Record → Driver Review.

---

## Phase 5 — Testing, Validation & Bug Fixing
1. Automated unit and integration tests using `pytest` and Django test client.
2. Booking concurrency conflict tests (attempting double booking on same slot).
3. Security boundary tests (unauthorized access to private records, RBAC enforcement).
4. Address privacy verification (unbooked view vs. confirmed driver view).

---

## Phase 6 — Handoff & Documentation
1. `README.md` with turnkey startup instructions, environment variable guide, and test commands.
2. Update `docs/REQUIREMENTS_TRACEABILITY.md` to verified status.
3. Delivery report detailing all implemented features, architecture, and pilot recommendations.
