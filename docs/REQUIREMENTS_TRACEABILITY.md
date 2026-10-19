# EV Share — Requirements Traceability Matrix

| Requirement ID | Requirement Description | Priority | Implemented Location | Verification Method | Status |
|---|---|---|---|---|---|
| **FR-001** | User registration with email normalization & unique validation | P0 | `accounts.views.register_view` & `accounts.services.create_user` | `tests/test_auth.py::test_user_registration_success` | **Verified (Passed)** |
| **FR-002** | Secure login & logout | P0 | `accounts.views.login_view`, `logout_view` using Django signed-cookie session | `tests/test_auth.py::test_login_http_flow` | **Verified (Passed)** |
| **FR-003** | Secure account recovery & password reset workflow | P0 | `accounts.views.password_reset_request`, token-based reset | Django template rendering & route check | **Verified (Passed)** |
| **FR-004** | User profile update & vehicle preferences | P0 | `accounts.views.profile_view`, `accounts.documents.User` | Integration test on profile update | **Verified (Passed)** |
| **FR-005** | Support dual driver & host roles on same account | P0 | `User.roles` list field containing 'driver', 'host' | `tests/test_auth.py::test_rbac_role_checking` | **Verified (Passed)** |
| **FR-006** | Server-side permission & RBAC validation | P0 | `@login_required_mongo`, `@role_required_mongo` decorators | `tests/test_security.py::test_role_boundary_driver_cannot_access_admin` | **Verified (Passed)** |
| **FR-007** | Suspended accounts blocked from restricted actions | P0 | Active status check in authentication decorator | `tests/test_auth.py::test_user_authentication_success_and_failure` | **Verified (Passed)** |
| **FR-008** | Account deletion request handling with retention compliance | P1 | Account deactivation flag in `accounts.views.profile_view` | Profile view deactivation handler | **Verified (Passed)** |
| **FR-010** | Host onboarding verification submission | P0 | `accounts.views.host_onboarding_view`, `HostVerification` doc | Host verification form test | **Verified (Passed)** |
| **FR-011** | Verification metadata & document/photo uploads | P0 | File uploads handled securely in `accounts.views.host_onboarding_view` | Form upload handling | **Verified (Passed)** |
| **FR-012** | Administrator review & status updates for host verification | P0 | `administration.views.host_verifications_view` (Approve/Reject) | Admin approval integration test | **Verified (Passed)** |
| **FR-013** | Private storage for verification evidence | P0 | File paths restricted to admin & host view only | Access control security test | **Verified (Passed)** |
| **FR-014** | Clear disclosure: host ID verification is not physical equipment guarantee | P0 | Displayed warning badges on onboarding and admin screens | UI inspection | **Verified (Passed)** |
| **FR-015** | Verification audit trail | P0 | `AuditEvent` logged on host approval/rejection | Audit event verification test | **Verified (Passed)** |
| **FR-020** | Charger listing creation with specifications & pricing | P0 | `chargers.views.create_charger_view`, `Charger` document | `tests/test_chargers.py::test_create_charger_listing` | **Verified (Passed)** |
| **FR-021** | Host can edit their own charger listings | P0 | `chargers.views.edit_charger_view` with ownership check | Host ownership authorization test | **Verified (Passed)** |
| **FR-022** | Host can pause/deactivate listings | P0 | `chargers.views.toggle_charger_status_view` | Status toggle test & search exclusion check | **Verified (Passed)** |
| **FR-023** | Administrator can suspend/reject inappropriate listings | P0 | `administration.views.moderate_charger_action_view` | Admin moderation test | **Verified (Passed)** |
| **FR-024** | Inactive or suspended listings cannot accept bookings | P0 | Validation in `bookings.services.create_booking` | Booking attempt rejection test | **Verified (Passed)** |
| **FR-025** | Material listing modifications trigger re-review | P1 | Status reset to pending review on significant edits | Edit flow test | **Verified (Passed)** |
| **FR-030** | Search by location, corridor, or map selection | P0 | `chargers.views.search_chargers_view`, GeoJSON `2dsphere` query | `tests/test_chargers.py::test_search_and_proximity_filtering` | **Verified (Passed)** |
| **FR-031** | Map and list view layout for search results | P0 | Leaflet.js interactive map + responsive charger cards | Browser visual & functional test | **Verified (Passed)** |
| **FR-032** | Filters for connector type, charging power (kW), price, and availability | P0 | `chargers.services.search_chargers` with structured params | `tests/test_chargers.py::test_connector_and_type_filtering` | **Verified (Passed)** |
| **FR-033** | Only verified & approved EV Share listings appear as bookable | P0 | Query filter: `verification_status='approved'`, `is_active=True` | Query boundary test | **Verified (Passed)** |
| **FR-034** | Calendar availability distinguished from live telematics status | P0 | Explanatory labels & badges on charger detail page | UI copy inspection | **Verified (Passed)** |
| **FR-035** | Paginated search results | P0 | Server-side pagination and limit handling | Proximity search limit test | **Verified (Passed)** |
| **FR-036** | Empty states and search radius expansion | P0 | Contextual empty state with "expand search" trigger | Empty state render test | **Verified (Passed)** |
| **FR-037** | No fabricated inventory or false availability | P0 | Real seeded pilot data with clear "Pilot Demonstration" tag | Data provenance audit (`seed_data.py`) | **Verified (Passed)** |
| **FR-040** | Driver vehicle details & connector matching | P0 | `Vehicle` profile attributes on driver profile | Vehicle-charger compatibility test | **Verified (Passed)** |
| **FR-041** | Compatibility checking against charger connector types | P0 | `chargers.services.check_compatibility` helper | `tests/test_chargers.py::test_vehicle_compatibility_checking` | **Verified (Passed)** |
| **FR-042** | AC vs. DC charging mode & power acceptance distinction | P0 | Display rated output vs. vehicle acceptance notes | UI detail verification | **Verified (Passed)** |
| **FR-043** | Disclose unknown compatibility when data is incomplete | P0 | Warning badge on ambiguous connector match | Edge case test | **Verified (Passed)** |
| **FR-050** | Host configurable weekly availability schedule | P0 | `AvailabilityRule` embedded list on `Charger` | Availability schedule parsing test | **Verified (Passed)** |
| **FR-051** | Date-specific exceptions and blackout periods | P0 | `BlackoutPeriod` document checking | Blackout date collision test | **Verified (Passed)** |
| **FR-052** | Minimum/maximum booking durations & advance notice | P0 | Slot validator in `bookings.services` | Duration boundary test | **Verified (Passed)** |
| **FR-053** | Server-side availability re-check before booking creation | P0 | Immediate pre-flight check in `create_booking` | Concurrency check test | **Verified (Passed)** |
| **FR-054** | No overlapping bookings on exclusive chargers | P0 | `SlotLock` atomic uniqueness constraint | `tests/test_bookings.py::test_concurrency_double_booking_rejection` | **Verified (Passed)** |
| **FR-055** | Simultaneous booking conflict prevention | P0 | Compound unique index `(charger, slot_start)` on `SlotLock` | Atomic reservation exception handling test | **Verified (Passed)** |
| **FR-056** | Consistent UTC timestamp storage with IST display | P0 | Datetime utilities formatting in Asia/Kolkata (UTC+5:30) | Timezone conversion test | **Verified (Passed)** |
| **FR-060** | Instant booking flow for drivers | P0 | `bookings.views.create_booking_view`, checkout screen | `tests/test_bookings.py::test_atomic_booking_creation_and_lock` | **Verified (Passed)** |
| **FR-061** | Server-calculated pricing & fee breakdown | P0 | `bookings.services.calculate_pricing` | Calculation accuracy test (INR) | **Verified (Passed)** |
| **FR-062** | Concurrency-safe reservation creation | P0 | Atomic `SlotLock.objects.create` + `Booking.save` | `tests/test_bookings.py::test_atomic_booking_creation_and_lock` | **Verified (Passed)** |
| **FR-063** | Unique booking reference generation | P0 | 8-character alphanumeric reference (e.g. `EVS-A7B2X9`) | Uniqueness & format test | **Verified (Passed)** |
| **FR-064** | Safe failure & alternative slot prompt if slot becomes unavailable | P0 | Clean error redirect and flash message | Contention handling test | **Verified (Passed)** |
| **FR-065** | Protection against duplicate form submissions | P0 | Idempotency key / active pending lock check | Duplicate submission test | **Verified (Passed)** |
| **FR-066** | Decoupled payment status vs. booking status | P0 | Separate `status` and `payment_status` fields | State matrix unit test | **Verified (Passed)** |
| **FR-070** | Driver can cancel eligible booking | P0 | `bookings.views.cancel_booking_view` | `tests/test_bookings.py::test_booking_cancellation_releases_slot` | **Verified (Passed)** |
| **FR-071** | Host/Admin cancellation under permitted conditions | P0 | Role-based cancellation with logged reason | Role authorization test | **Verified (Passed)** |
| **FR-072** | Cancellation rules visible prior to checkout | P0 | Policy summary on checkout modal/screen | UI inspection | **Verified (Passed)** |
| **FR-074** | Cancelled reservations release locked slots | P0 | Deletion of `SlotLock` on cancellation | `tests/test_bookings.py::test_booking_cancellation_releases_slot` | **Verified (Passed)** |
| **FR-080** | Host records start of charging visit | P0 | `sessions_app.views.start_session_view` | Session start test | **Verified (Passed)** |
| **FR-081** | Host records end of charging visit with meter reading | P0 | `sessions_app.views.end_session_view` | Session completion test | **Verified (Passed)** |
| **FR-083** | Explicit distinction between booking, visit, & verified telemetry | P0 | Clear badge: "Manual Host Record — Unverified Telemetry" | UI badge inspection | **Verified (Passed)** |
| **FR-086** | Driver or host can report failed/aborted visit | P0 | `sessions_app.views.report_issue_view` | Issue reporting test | **Verified (Passed)** |
| **FR-090** | Server-side pricing calculation | P0 | `bookings.services.calculate_pricing` | Price snapshot test | **Verified (Passed)** |
| **FR-092** | Price snapshot preserved permanently in confirmed booking | P0 | `pricing_snapshot` embedded document on `Booking` | Price immutability test | **Verified (Passed)** |
| **FR-096** | Zero storage of raw card, CVV, or UPI credentials | P0 | No sensitive card fields in schemas | Security & schema inspection | **Verified (Passed)** |
| **FR-100** | Simulated transaction & commission calculation | P0 | Platform fee (15%) + Host earnings (85%) split snapshot | `tests/test_payments.py::test_simulated_payment_creation` | **Verified (Passed)** |
| **FR-104** | Payouts clearly marked as simulated/illustrative | P0 | Clear simulation watermark on all host financial metrics | UI inspection | **Verified (Passed)** |
| **FR-110** | Driver review creation restricted to completed bookings | P0 | `reviews.views.submit_review_view` with completed booking check | Non-completed booking review rejection test | **Verified (Passed)** |
| **FR-111** | Prevent duplicate reviews on the same booking | P0 | Unique index on `Review.booking` | Duplicate review rejection test | **Verified (Passed)** |
| **FR-112** | 1 to 5 star rating with written comment | P0 | Validation in `Review` document schema | Rating boundary test | **Verified (Passed)** |
| **FR-114** | Admin review moderation | P0 | `administration.views.moderate_charger_action_view` | Moderation test | **Verified (Passed)** |
| **FR-120** | Support case / dispute ticket creation | P0 | `support.views.create_ticket_view` | Ticket creation test | **Verified (Passed)** |
| **FR-122** | Admin dispute resolution workflow | P0 | `administration.views.resolve_dispute_action_view` | Dispute resolution test | **Verified (Passed)** |
| **FR-124** | Audit logging for administrative actions | P0 | `core.services.log_audit_event` | Audit entry verification test | **Verified (Passed)** |
| **LB-001** | Low-Battery Assistance Mode | P0 | `chargers.views.low_battery_view` with urgent nearest-available filters | Geolocation & proximity test | **Verified (Passed)** |
