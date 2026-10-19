# EV Share — PRD Summary

**Product Name:** EV Share  
**Tagline:** Your Charger. Someone Else’s Journey. Everyone Benefits.  
**Version:** 3.0 (Master Baseline Summary)  
**Target Market:** India (Initial launch: Delhi–Agra Yamuna Expressway travel corridor pilot)  
**Platform:** Responsive Web Application (PWA-ready), Server-rendered Django with MongoDB  
**Document Source:** `PRD.md`

---

## 1. Executive Summary & Value Proposition

EV Share is a peer-to-peer EV charging marketplace in India connecting EV drivers in need of charging with verified hosts (residential property owners, hotels, highway restaurants, offices, commercial parking) who have underutilized charging facilities.

### Value Delivery:
- **Drivers:** Discover verified, compatible, genuinely bookable chargers along highway travel corridors; inspect rated power, transparent INR pricing, and real-time availability; reserve instantly with no double-booking risk; receive verified access directions post-booking; record sessions and report issues.
- **Hosts:** Monetize idle private/commercial charging assets under strict access rules and customizable schedules; review bookings and manage slots; track completed charging visits and simulated earnings.
- **Administrators:** Verify host applications and listings; review safety/installation evidence; moderate listings; resolve disputes; monitor platform audit logs and operational health.

---

## 2. User Roles & Permissions

1. **Guest (Unauthenticated):**
   - Browse landing page, corridor search, and public charger details (with protected approximate location).
   - Register or log in as Driver or Host.
   - *Restrictions:* Cannot access private booking records, exact residential addresses, or host verification documents.

2. **EV Driver:**
   - Manage personal profile, vehicles, and preferred connectors.
   - Search chargers by location, connector type (Type 2, CCS2, Bharat AC001, 15A Socket), charging power, and time.
   - Instant-book available slots; review transparent pricing breakdown (energy cost + platform fee + GST snapshot).
   - View booking details and navigation directions upon confirmation.
   - Cancel eligible bookings (releasing reserved capacity).
   - Record session completion and submit ratings/reviews (1–5 scale) for completed visits.

3. **Charger Host:**
   - Onboard and submit verification applications (identity, property access proof, installation photos).
   - Create, edit, and pause charger listings.
   - Configure recurring weekly availability schedules and specific blackout exceptions.
   - Inspect upcoming and past reservations for hosted chargers.
   - Record manual visit start and end events.
   - View transparent transaction summaries and illustrative earnings.
   - *Restrictions:* Cannot approve own listing or alter payment records directly.

4. **Platform Administrator:**
   - Review host verification queue (Approve, Reject, Request Changes).
   - Moderate charger listings (Publish, Suspend, Deactivate).
   - Oversee bookings, simulated transactions, support disputes, and audit logs.
   - Strict server-side authorization enforcement (no reliance on hidden UI elements).

---

## 3. Scope Boundaries

### In Scope (P0 MVP):
- Full account registration, password hashing, session management, and RBAC (Driver, Host, Admin).
- Host verification onboarding with document/photo uploads and administrative review workflow.
- Charger listing management with geospatial GeoJSON coordinates (`2dsphere` index) and corridor search.
- Compatibility checking against connector standards (Type 2, CCS2, GB/T, 15A/16A Indian 3-pin).
- Availability management with weekly time-slots and blackouts.
- Concurrency-safe instant booking engine with atomic slot locking to strictly prevent double bookings.
- Transparent price calculation snapshot in INR.
- Manual charging session start/end tracking with distinct audit states.
- Simulated payment checkout demonstrating authorized, pending, paid, failed, and refund states.
- Review and rating system strictly restricted to completed visits.
- Support case / dispute ticket creation and resolution workflow.
- Protected custom Admin Dashboard for platform operations.
- Apple India-inspired quiet, premium visual aesthetic (`Design.md`) with responsive Bootstrap/vanilla JS.

### Explicitly Excluded (P1 / P2 Deferred):
- Direct hardware/OCPP integration or automatic meter telematics (manual records clearly labelled).
- Live financial payouts / credit card merchant holding (simulated payment engine clearly watermarked).
- Native iOS/Android apps (responsive web only).
- AI route recommendation or autonomous battery drain predictions.
- Physical roadside rescue operations.

---

## 4. Key Business Rules (BR-001 to BR-022)
- **BR-001:** Only approved, verified chargers appear in bookable search results.
- **BR-005:** Overlapping confirmed reservations on exclusive chargers are strictly blocked by atomic constraints.
- **BR-007:** Pricing snapshots are permanently fixed at time of booking confirmation.
- **BR-008:** Booking status, charging session status, and payment transaction status remain completely decoupled states.
- **BR-012:** Precise residential addresses and private gate access codes are disclosed *only* to drivers with confirmed bookings.
- **BR-013:** Reviews can only be submitted once per completed booking by the respective driver.
