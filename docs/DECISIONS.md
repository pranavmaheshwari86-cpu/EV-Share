# EV Share — Architecture & Design Decisions

This document logs key architectural choices, conflict resolutions between PRD and TRD, and decisions made in accordance with founder requirements.

---

## Decision Record 1: Django Session & Authentication Strategy
- **Context:** Standard Django authentication relies on relational SQL models (`django.contrib.auth.models.User`) and relational database tables (`django_session`). However, both PRD and TRD specify MongoDB with MongoEngine as the primary database without relational database tables.
- **Decision:**
  1. Define a native MongoEngine `User` document in `accounts/documents.py`.
  2. Use Django's PBKDF2 algorithm (`django.contrib.auth.hashers.make_password`, `check_password`) for secure hashing.
  3. Configure Django's signed-cookie session engine:  
     `SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`.
  4. Implement lightweight, robust decorators (`@login_required_mongo`, `@role_required_mongo`) and custom context processors (`accounts.context_processors.current_user`) to seamlessly inject authenticated user objects into views and templates.
- **Status:** Approved & Implemented.

---

## Decision Record 2: Booking Concurrency & Double-Booking Prevention
- **Context:** MongoDB does not automatically provide table-level row lock semantics or declarative interval overlap prevention across documents without replica set transactions or custom locking.
- **Decision:**
  1. Create a dedicated `SlotLock` collection in MongoDB.
  2. Implement a compound unique index on `(charger, slot_start)`.
  3. During booking reservation, atomically acquire `SlotLock` documents before creating the `Booking` document.
  4. If a duplicate key error is encountered, abort gracefully and notify the user that the slot was reserved concurrently.
  5. Upon cancellation or booking expiration, release the associated `SlotLock` documents.
- **Status:** Approved & Implemented.

---

## Decision Record 3: Pilot Travel Corridor Selection
- **Context:** PRD §5.1 states EV Share will launch on "one compact section of a selected highway travel corridor in India" and that the specific corridor must be confirmed.
- **Decision:** We establish the **Yamuna Expressway Corridor (Delhi NCR to Agra)** as the pilot corridor baseline. Seed data covers 6 realistic charging hubs across Noida, Greater Noida, Jewar, Mathura, and Agra, with realistic AC (7.4kW Type 2) and DC (30kW/60kW CCS2) chargers.
- **Status:** Approved & Implemented.

---

## Decision Record 4: Address Disclosure & Host Privacy
- **Context:** PRD FR-037 & BR-012 mandate that private residential addresses must not be exposed publicly on search maps.
- **Decision:**
  1. Public search results and detail pages expose `address.city`, `address.state`, and a generalized `display_address` (e.g. "Near Jewar Toll Plaza, Yamuna Expressway") with jittered/approximate location.
  2. The precise private address, gate code, and host phone number are revealed *only* inside the authenticated driver's confirmed booking detail view.
- **Status:** Approved & Implemented.

---

## Decision Record 5: Visual Styling & Design Philosophy
- **Context:** `Design.md` establishes an Apple India-inspired photography-first storefront with quiet chrome, pill buttons, and action blue (`#0071E3`), while `taste-design` strictly bans generic AI clutter (no purple neon, no 3 equal cards, no fake uptime numbers, no placeholder buttons).
- **Decision:** Combine Bootstrap 5.3 grid utilities with custom CSS tokens (`static/css/ev_share.css`) matching the Apple India specification: neutral canvas surfaces (`#F5F5F7` / `#FFFFFF`), dark ink (`#1D1D1F`), action blue (`#0071E3`), pill action buttons, clean sans-serif typography, and subtle micro-interactions.
- **Status:** Approved & Implemented.
