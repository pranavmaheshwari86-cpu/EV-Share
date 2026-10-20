# EV Share — Complete Technical Requirements Document (TRD)

**Project:** EV Share  
**Document Type:** Technical Requirements Document  
**Version:** 1.0 — Final  
**Target Market:** India  
**Application Type:** Web-based peer-to-peer EV charging marketplace  
**Backend Language:** Python  
**Backend Framework:** Django  
**Database:** MongoDB  
**MongoDB Integration:** MongoEngine  
**Frontend:** Django Templates, HTML5, CSS3, Bootstrap, vanilla JavaScript  
**Deployment Database:** MongoDB Atlas  
**Development Approach:** Beginner-friendly, modular monolithic architecture

---

# 1. Project Overview

## 1.1 What is EV Share?

EV Share is a peer-to-peer electric vehicle charging marketplace that connects EV drivers who need charging with people and businesses that have compatible charging facilities available for others to use.

Potential hosts include:

- EV owners with compatible home charging facilities.
- Residential property owners.
- Shops, hotels, restaurants, and cafés.
- Offices, parking facilities, and commercial properties.
- Other eligible property owners with suitable charging infrastructure.

Instead of relying exclusively on dedicated public charging stations, EV drivers can discover available private charging locations, check compatibility and pricing, and reserve a charging time slot.

Hosts can list their chargers, define availability, set prices, and receive eligible payments for completed bookings.

EV Share acts as the digital platform connecting drivers and hosts.

## 1.2 Problem Statement

EV drivers may struggle to find convenient charging facilities, particularly in areas with limited charging infrastructure.

The key problems are:

1. Insufficient charging options in some locations.
2. Range anxiety during everyday travel and long journeys.
3. Difficulty discovering compatible chargers nearby.
4. Limited visibility into charger availability and pricing.
5. Underutilized private charging infrastructure.
6. Lack of a convenient system for booking private charging facilities.

## 1.3 Proposed Solution

EV Share will provide a web application where:

- Drivers can search for charging facilities near a location.
- Drivers can filter chargers by connector compatibility, charging power, price, and availability.
- Hosts can register and publish charger listings.
- Drivers can book available charging time slots.
- Hosts can manage reservations and listing availability.
- Users can view booking status and booking history.
- Eligible drivers can review chargers after completed bookings.
- Administrators can manage users, listings, bookings, reports, and disputes.

The first version will focus on a reliable charger discovery and booking experience. Advanced payment settlement, live charger telemetry, and automated hardware integrations will be added only when appropriate.

---

# 2. Technical Objectives

The system must:

1. Provide secure user registration and login.
2. Support driver and host roles.
3. Allow hosts to create, update, deactivate, and manage charger listings.
4. Support location-based charger discovery.
5. Display charger specifications, pricing, availability, and compatibility.
6. Prevent overlapping confirmed bookings for the same charger.
7. Maintain a reliable booking lifecycle.
8. Provide booking history and cancellation functionality.
9. Support payment integration through a third-party provider.
10. Store application data in MongoDB.
11. Protect personal information and payment-related metadata.
12. Work on desktop, tablet, and mobile browsers.
13. Be straightforward for a beginner to build, debug, and maintain.
14. Support future expansion without requiring a complete architectural rewrite.

---

# 3. Scope of the First Version

## 3.1 Features Included in the MVP

### Authentication and accounts
- User registration.
- Login and logout.
- Password hashing.
- Role-based permissions.
- Profile management.
- Password reset workflow.
- Account status management.

### Charger marketplace
- Create charger listings.
- Edit and deactivate listings.
- Upload charger images.
- Display charger specifications.
- Set prices and availability.
- Search and filter chargers.
- Search by geographic location.
- View charger details.

### Booking system
- Select a date and time slot.
- Check availability.
- Create bookings.
- Prevent conflicting reservations.
- View upcoming and previous bookings.
- Cancel eligible bookings.
- Update booking status.

### Payments
- Payment-provider integration when configured.
- Payment status tracking.
- Payment confirmation verification.
- Transaction history.
- Refund status tracking where supported.

### Reviews
- Rate chargers.
- Submit written reviews.
- Display ratings.
- Restrict reviews to eligible completed bookings.

### Administration
- View and manage users.
- Review charger listings.
- Suspend inappropriate listings or accounts.
- Review booking and payment statuses.
- Handle reported content and disputes.

## 3.2 Features Excluded from the Initial MVP

The following are not required for the first release:

- Native Android and iOS applications.
- Live vehicle battery-level integration.
- Direct communication with charger hardware.
- Automatic start/stop charging control.
- Automatic electricity meter integration.
- AI-based charging recommendations.
- Automatic host payouts without a supported payment-provider arrangement.
- Subscription plans.
- Loyalty programs.
- Multi-country support.
- Microservices architecture.
- Real-time charger telemetry.

These features may be considered in future versions.

---

# 4. Technology Stack

## 4.1 Backend

**Python**

Used for application logic, data processing, validation, and integrations.

**Django**

Used for:
- URL routing.
- Request handling.
- HTML page rendering.
- Form processing.
- Middleware.
- CSRF protection.
- Password hashing utilities.
- Input validation.
- Application configuration.

Use Django as a conventional server-rendered web application rather than introducing a separate frontend framework in the MVP.

## 4.2 Database

**MongoDB**

MongoDB is the primary application database. It stores application data as flexible BSON documents in collections.

**MongoEngine**

MongoEngine provides Python document models and validation for MongoDB.

**PyMongo**

MongoEngine uses PyMongo internally. Direct PyMongo usage should be limited to cases where it provides a clear benefit.

**MongoDB Atlas**

Use MongoDB Atlas for a hosted database environment. A local MongoDB Community Server instance can be used during development.

### Important integration constraint

This project will use MongoEngine documents rather than Django's standard relational ORM for application data.

Django's built-in authentication tables, database-backed sessions, migrations, and admin site must not be assumed to work with MongoEngine automatically.

For the MVP:

- Store users as MongoDB documents.
- Use Django's password-hashing utilities with MongoEngine user documents.
- Use Django's signed-cookie session backend, with appropriate expiry and logout handling.
- Implement application-specific permission checks.
- Build a protected custom administration dashboard.
- Use MongoEngine document validation and explicit index management.

If conventional Django authentication and admin integration becomes a priority, evaluate a compatible alternative architecture before implementation.

## 4.3 Frontend

- HTML5 for page structure.
- CSS3 for styling.
- Bootstrap for responsive layouts and common UI components.
- Vanilla JavaScript for interactions.
- Django Templates for server-rendered pages.

No React, Angular, Vue, or Next.js is required for the initial version.

## 4.4 Maps and Location

- Leaflet for interactive maps.
- OpenStreetMap-compatible map tiles, subject to provider terms.
- Browser geolocation only after user permission.
- GeoJSON Point coordinates in MongoDB.
- MongoDB `2dsphere` index for nearby searches.

## 4.5 Image Storage

During local development, images may be stored in a local media directory.

For production, use object storage or a managed image-storage service. Store image URLs and relevant metadata in MongoDB rather than saving image binaries directly inside ordinary charger documents.

## 4.6 Payments

Integrate a payment gateway that supports the required Indian payment methods and the intended marketplace business model.

Provider selection must account for:
- Merchant onboarding and business verification.
- Payment acceptance.
- Server-side payment verification.
- Refund capabilities.
- Marketplace or split-settlement support, if required.
- Applicable legal and regulatory requirements.

Do not assume that accepting payments automatically permits the platform to hold or distribute money between hosts and drivers.

## 4.7 Deployment

Recommended deployment arrangement:

- Django application on a Python-compatible hosting platform.
- MongoDB on MongoDB Atlas.
- Production static files served through the hosting platform or a suitable static-file service.
- Uploaded images stored in managed object storage.
- HTTPS enabled for all production traffic.

---

# 5. System Architecture

## 5.1 Architecture Pattern

Use a **modular monolithic architecture**.

The entire application runs as one Django project, organized into smaller functional modules.

This is simpler to develop and maintain than microservices.

## 5.2 Request Flow

1. The user opens a page in the browser.
2. Django receives the HTTP request.
3. Middleware handles applicable security and session requirements.
4. The URL router identifies the appropriate view.
5. The view checks authentication, permissions, and input validity.
6. The service layer performs business operations.
7. MongoEngine reads or updates MongoDB documents.
8. The view returns a rendered template or JSON response.
9. The browser displays the result.

For booking and payment operations, the service layer must enforce the relevant consistency and authorization rules.

## 5.3 Logical Architecture

Browser → Django URLs → Views → Services and Validation → MongoEngine → MongoDB Atlas

Supporting services:

- Image storage.
- Map tiles and geocoding, where configured.
- Payment gateway.
- Email provider.
- Application logging and monitoring.

## 5.4 Suggested Project Structure

```text
ev_share/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py
│   └── utils.py
│
├── accounts/
│   ├── __init__.py
│   ├── documents.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py
│   ├── forms.py
│   └── permissions.py
│
├── chargers/
│   ├── __init__.py
│   ├── documents.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py
│   ├── forms.py
│   └── search.py
│
├── bookings/
│   ├── __init__.py
│   ├── documents.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py
│   └── validators.py
│
├── payments/
│   ├── __init__.py
│   ├── documents.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py
│   └── providers.py
│
├── reviews/
│   ├── __init__.py
│   ├── documents.py
│   ├── urls.py
│   ├── views.py
│   └── services.py
│
├── administration/
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py
│   └── permissions.py
│
├── templates/
│   ├── base.html
│   ├── core/
│   ├── accounts/
│   ├── chargers/
│   ├── bookings/
│   ├── payments/
│   ├── reviews/
│   └── administration/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
└── tests/
    ├── test_accounts.py
    ├── test_chargers.py
    ├── test_bookings.py
    ├── test_payments.py
    └── test_permissions.py
```

The `media/` directory is for local development only and should not be treated as durable production storage.

---

# 6. User Roles and Permissions

## 6.1 Driver

A driver can:

- Register and log in.
- Manage their own profile.
- Browse and search chargers.
- View charger details.
- Check availability.
- Create eligible bookings.
- View their own bookings.
- Cancel eligible bookings.
- View their own payment history.
- Review eligible completed bookings.

A driver cannot modify another user's profile, change charger ownership, or access another driver's private booking information.

## 6.2 Host

A host can:

- Register and log in.
- Manage their own profile.
- Create charger listings.
- Edit their own listings.
- Upload charger photos.
- Configure supported connector types and pricing.
- Define available time slots.
- View bookings for their own chargers.
- Manage eligible reservation statuses.
- Review booking and payment summaries.

A host cannot modify another host's listings, mark payments successful without verified evidence, or access unrelated users' private information.

Hosts may also book chargers as drivers. Role-specific capabilities should be enforced by permissions rather than assuming a user can have only one role.

## 6.3 Administrator

A platform administrator can:

- View and manage users.
- Suspend or reactivate accounts.
- Review, deactivate, or remove inappropriate listings.
- Inspect booking and payment metadata.
- Handle user reports and disputes.
- Review platform activity.
- Manage configuration and supported connector types.

Administrative access must be protected by explicit authorization and should not be granted merely because a user has supplied an `admin` role string during registration.

---

# 7. Authentication and Session Management

## 7.1 Registration

Required fields:

- Full name.
- Email address.
- Password.
- Password confirmation.
- Accepted terms and privacy notice.

Phone number may be optional during initial registration and required before activities that need it.

Requirements:

- Normalize email addresses before uniqueness checks.
- Enforce unique email addresses with a MongoDB unique index.
- Validate password requirements on the server.
- Hash passwords using Django's password-hashing utilities.
- Never store plaintext passwords.
- Provide meaningful validation messages.
- Do not expose whether an account exists through password-reset responses.

## 7.2 Login

Users must be able to log in using their registered email and password.

The backend must:

1. Normalize the submitted email.
2. Locate the user document.
3. Verify the password hash.
4. Check whether the account is active.
5. Establish a secure session.
6. Redirect the user to an appropriate page.

Use generic error messages for invalid credentials.

Apply login throttling or rate limiting to reduce brute-force attempts.

## 7.3 Session Management

Because the project uses MongoEngine rather than Django's standard relational ORM, use a deliberately configured session strategy.

For the initial version, Django's signed-cookie session backend is an option. It stores signed session data in the browser rather than requiring the standard database-backed session table.

Requirements:

- Keep session contents minimal.
- Do not store passwords, payment credentials, or sensitive profile information in session data.
- Store only the user identifier and other minimal authentication state.
- Reload and validate the account's current status for protected operations.
- Configure secure cookie flags in production.
- Use HTTPS.
- Define appropriate session expiry.
- Clear the session on logout.
- Test session invalidation after account suspension and password changes.

A signed cookie provides integrity, not confidentiality. Sensitive information must not be placed in it.

## 7.4 Password Reset

Implement a secure password-reset workflow using expiring, single-use tokens.

Requirements:

- Generate tokens securely.
- Send reset links through a configured email provider.
- Expire tokens after a defined period.
- Invalidate used tokens.
- Apply rate limits.
- Avoid revealing whether the submitted email is registered.

## 7.5 Authorization

Every protected view and service must validate permissions on the server.

Hiding a button in HTML is not sufficient authorization.

For example, a host may update a charger only when the authenticated user owns that charger or has explicit administrative permission.

---

# 8. MongoDB Database Design

## 8.1 Database Name

Use a dedicated database named:

`ev_share`

Development and production environments must use separate database credentials and preferably separate databases or clusters.

## 8.2 Data Modeling Rules

- Use MongoEngine document models.
- Use MongoDB ObjectId values as primary identifiers.
- Store references between related documents.
- Validate all input before writing to the database.
- Add indexes for frequently queried fields.
- Use UTC timestamps internally.
- Display times in the appropriate local timezone.
- Never trust prices, ownership IDs, or status values supplied by the browser.
- Avoid duplicating mutable data unnecessarily.
- When snapshots are needed for historical records, document which values are intentionally preserved.

## 8.3 Collection: `users`

Purpose: Store user accounts and profile information.

Example structure:

```json
{
  "_id": "ObjectId",
  "full_name": "Example User",
  "email": "user@example.com",
  "password_hash": "secure-hash",
  "phone_number": null,
  "roles": ["driver"],
  "is_active": true,
  "email_verified": false,
  "created_at": "UTC datetime",
  "updated_at": "UTC datetime"
}
```

Requirements:

- Unique normalized email address.
- Securely hashed password.
- Valid roles.
- Account activation status.
- Created and updated timestamps.
- Optional phone number and verification state.

Do not permit public registration to create administrator accounts.

## 8.4 Collection: `chargers`

Purpose: Store charger listings.

Example structure:

```json
{
  "_id": "ObjectId",
  "host_id": "ObjectId",
  "title": "Home EV Charger",
  "description": "Private charging point",
  "charger_type": "AC",
  "connector_types": ["Type 2"],
  "power_output_kw": 7.4,
  "price_per_kwh": 12.0,
  "currency": "INR",
  "address": {
    "city": "Example City",
    "state": "Uttar Pradesh",
    "postal_code": "000000",
    "display_address": "Example address"
  },
  "location": {
    "type": "Point",
    "coordinates": [78.0, 29.0]
  },
  "amenities": [],
  "photos": [],
  "availability_rules": [],
  "is_active": true,
  "created_at": "UTC datetime",
  "updated_at": "UTC datetime"
}
```

The example coordinates and address are placeholders, not a real charging location.

Requirements:

- Valid host reference.
- Non-empty title and description.
- Positive charging power.
- Non-negative and valid pricing.
- Supported connector types.
- Valid geographic coordinates.
- Active/inactive status.
- Image metadata.
- Listing timestamps.

For GeoJSON, coordinates must be ordered as `[longitude, latitude]`.

## 8.5 Collection: `bookings`

Purpose: Store charger reservations.

Example structure:

```json
{
  "_id": "ObjectId",
  "driver_id": "ObjectId",
  "host_id": "ObjectId",
  "charger_id": "ObjectId",
  "start_time": "UTC datetime",
  "end_time": "UTC datetime",
  "estimated_energy_kwh": 10.0,
  "unit_price_snapshot": 12.0,
  "estimated_total": 120.0,
  "currency": "INR",
  "status": "pending",
  "payment_status": "unpaid",
  "cancellation_reason": null,
  "created_at": "UTC datetime",
  "updated_at": "UTC datetime"
}
```

Requirements:

- Valid driver, host, and charger references.
- Start time earlier than end time.
- Booking within allowed booking limits.
- Server-calculated price.
- Status validation.
- Ownership validation.
- Conflict detection.
- Booking history.
- Audit timestamps.

Store a price snapshot so historical bookings are not silently repriced when a host changes their current listing price.

## 8.6 Collection: `payments`

Purpose: Store payment transaction metadata.

Example structure:

```json
{
  "_id": "ObjectId",
  "booking_id": "ObjectId",
  "driver_id": "ObjectId",
  "host_id": "ObjectId",
  "provider": "configured-provider",
  "provider_order_id": "provider-order-reference",
  "provider_payment_id": null,
  "amount": 120.0,
  "currency": "INR",
  "status": "initiated",
  "refund_status": "not_applicable",
  "created_at": "UTC datetime",
  "updated_at": "UTC datetime"
}
```

Requirements:

- Store provider references and transaction metadata.
- Verify payment outcomes on the server.
- Track refunds separately.
- Prevent duplicate payment processing.
- Never store raw card numbers, CVVs, UPI PINs, or banking passwords.

Only verified payment events may update a payment to successful.

## 8.7 Collection: `reviews`

Purpose: Store charger ratings and written feedback.

Example structure:

```json
{
  "_id": "ObjectId",
  "booking_id": "ObjectId",
  "driver_id": "ObjectId",
  "charger_id": "ObjectId",
  "rating": 5,
  "comment": "Charging experience was good.",
  "created_at": "UTC datetime"
}
```

Requirements:

- Rating must be within the allowed range of 1–5.
- Only eligible completed bookings may be reviewed.
- Prevent duplicate reviews for the same booking.
- Allow moderation of inappropriate content.
- Do not allow users to review unrelated chargers.

## 8.8 Optional Collection: `notifications`

Purpose: Track in-app notifications.

Possible fields:

- `_id`
- `user_id`
- `type`
- `title`
- `message`
- `related_booking_id`
- `is_read`
- `created_at`

Email notifications can be implemented first. In-app notifications may be added after core workflows are stable.

## 8.9 Optional Collection: `audit_logs`

Purpose: Record important administrative and security events.

Possible fields:

- `_id`
- `actor_id`
- `action`
- `target_type`
- `target_id`
- `timestamp`
- `metadata`

Avoid storing passwords, access tokens, or unnecessary personal data in logs.

---

# 9. Database Indexes and Consistency

## 9.1 Required Indexes

Create and verify indexes for:

### Users
- Unique normalized email.

### Chargers
- `host_id`.
- `is_active`.
- Location using `2dsphere`.
- Relevant search and filtering fields.

### Bookings
- `charger_id`.
- `driver_id`.
- `host_id`.
- `status`.
- `start_time`.
- `end_time`.

### Payments
- `booking_id`.
- Provider transaction identifiers, with appropriate uniqueness rules.

### Reviews
- `charger_id`.
- Unique `booking_id`, if one review per booking is the chosen policy.

Index design must reflect actual query patterns and be tested with representative data.

## 9.2 Booking Consistency

MongoDB does not automatically enforce non-overlapping time intervals.

A query followed by an insert is not enough to prevent two simultaneous requests from booking the same charger.

Implement a deliberate concurrency-control strategy.

Recommended initial approach:

1. Represent each reservable charger time slot using a fixed booking interval or another clearly defined slot model.
2. Create a separate reservation-lock or slot-reservation collection where necessary.
3. Enforce uniqueness for the charger and slot combination using a compound unique index.
4. Acquire reservation slots atomically.
5. Release slots when a booking is cancelled or expires.
6. Ensure the booking document and slot reservations remain consistent.
7. Use MongoDB transactions where supported and correctly configured, or implement a recoverable reservation workflow.
8. Add tests for simultaneous booking requests.

If arbitrary-duration bookings are required, implement a robust overlap-checking and atomic reservation design rather than relying solely on unique start-time indexes.

MongoDB multi-document transactions require an appropriate deployment configuration. Do not assume they work in every local MongoDB setup.

## 9.3 Money and Pricing

- Use a consistent currency, initially INR.
- Use validated decimal values or integer minor units where appropriate.
- Do not rely on floating-point arithmetic for final financial calculations.
- Calculate prices on the server.
- Record the applicable price snapshot when creating a booking.
- Verify payment amounts against the expected server-side amount.
- Define rounding rules and cancellation/refund policies.

---

# 10. Charger Listing Management

## 10.1 Create Listing

Hosts must provide:

- Charger title.
- Description.
- Charger type.
- Connector type.
- Maximum power output.
- Pricing information.
- Address or location.
- Available days and time slots.
- Optional amenities.
- Charger photographs.

The backend validates all required information before saving a listing.

## 10.2 Edit Listing

Only the listing owner or an authorized administrator may edit a listing.

Requirements:

- Validate changed fields.
- Preserve booking history.
- Prevent inappropriate changes to an existing booking's agreed price.
- Handle changes to availability without invalidating confirmed reservations unexpectedly.
- Log significant administrative changes.

## 10.3 Deactivate Listing

A host may deactivate a listing.

Deactivation must:

- Prevent new bookings.
- Preserve existing booking records.
- Apply a defined process to affected future reservations.
- Notify affected users when necessary.

Deleting a listing must not erase financial or booking records that need to be retained.

## 10.4 Charger Compatibility

Display connector type and charging power clearly.

Compatibility filtering should use structured connector values rather than unvalidated free-text searches.

The system must not claim a charger is compatible with a vehicle unless sufficient vehicle and connector information is available.

---

# 11. Charger Search and Discovery

## 11.1 Search Methods

Users can discover chargers through:

- Current permitted location.
- Entered address or city.
- Map browsing.
- Search by charger name or description.
- Filters.

## 11.2 Filters

Initial filters:

- Distance or search radius.
- AC/DC charger type.
- Connector type.
- Power output.
- Price range.
- Available date and time.
- Minimum rating, when reviews exist.

## 11.3 Location Search

Use GeoJSON Point data and a MongoDB `2dsphere` index.

Search requirements:

1. Obtain location from the user or a configured geocoding service.
2. Validate latitude and longitude.
3. Query active chargers within the requested radius.
4. Apply connector, price, and availability filters.
5. Return paginated results.
6. Display results as cards and optionally as map markers.

Browser geolocation must be optional and permission-based.

Do not expose private host contact information or exact residential details beyond what is necessary and authorized for the product's workflow.

## 11.4 Search Performance

- Paginate results.
- Limit returned fields.
- Avoid loading every charger into the browser.
- Add indexes for common queries.
- Use server-side filtering.
- Cache only data that can safely become stale.

---

# 12. Booking System

## 12.1 Booking Workflow

1. Driver opens a charger listing.
2. Driver selects a date and time.
3. The backend validates the requested period.
4. The system checks charger availability.
5. The server calculates the expected cost.
6. The driver confirms the booking request.
7. The system atomically reserves the requested slot or interval.
8. The booking receives an appropriate status.
9. The driver sees a confirmation or pending-payment message.
10. The system sends a notification when configured.

## 12.2 Booking Statuses

Recommended booking states:

- `pending`
- `confirmed`
- `cancelled`
- `completed`
- `expired`

Use explicit, validated status transitions. A booking must not jump arbitrarily between states.

For example:

- `pending` → `confirmed`
- `pending` → `cancelled`
- `pending` → `expired`
- `confirmed` → `cancelled`, if policy permits
- `confirmed` → `completed`

## 12.3 Availability Rules

The backend must check:

- Charger is active.
- Requested time is valid.
- Start time is before end time.
- Requested time falls within host availability.
- Booking is not in the past, except for explicitly supported administrative corrections.
- No incompatible confirmed or temporarily held reservation exists.
- Required lead time and maximum booking duration are respected.

## 12.4 Double Booking Prevention

Two drivers must not receive confirmed reservations for conflicting time slots.

The backend must use atomic slot reservations, a robust interval-locking mechanism, or another tested concurrency-safe design.

The frontend availability display is informative only; the backend makes the final decision.

## 12.5 Booking Cancellation

Cancellation rules must be configurable and displayed before confirmation.

The backend must:

1. Authenticate the requester.
2. Verify booking ownership or administrative permission.
3. Check cancellation eligibility.
4. Update booking status.
5. Release reserved slots where appropriate.
6. Initiate the applicable refund workflow if payment has already been captured.
7. Record the cancellation reason and timestamp.
8. Notify affected parties when configured.

## 12.6 Booking History

Drivers can view their own bookings.

Hosts can view bookings for their own chargers.

Each booking should show:

- Charger name.
- Booking date.
- Start and end times.
- Estimated price.
- Booking status.
- Payment status.
- Cancellation or completion information where applicable.

---

# 13. Payment System

## 13.1 Payment Architecture

Payment integration should be introduced after registration, charger listings, and booking logic work reliably.

The platform must use a supported third-party payment provider.

## 13.2 Payment Flow

1. Driver selects a charger and time slot.
2. Backend calculates the expected amount.
3. Backend creates a pending booking or temporary reservation.
4. Backend creates a payment order with the provider.
5. Driver completes payment through the provider's approved interface.
6. Provider returns the payment result.
7. Backend verifies the payment signature or equivalent provider evidence.
8. Backend validates the payment amount, currency, and order reference.
9. Backend processes verified webhooks idempotently.
10. Booking is confirmed only when the required payment conditions are satisfied.

If payment fails or the reservation expires, release the slot according to the defined policy.

## 13.3 Payment Statuses

Recommended payment states:

- `initiated`
- `pending`
- `successful`
- `failed`
- `refund_pending`
- `partially_refunded`
- `refunded`

Keep payment status separate from booking status.

## 13.4 Security Requirements

- Never trust a client-side success screen.
- Verify payment on the server.
- Validate webhook signatures.
- Handle duplicate webhook delivery safely.
- Match provider order IDs and expected amounts.
- Never store raw payment credentials.
- Keep API keys in environment variables.
- Use provider-supported refund mechanisms.
- Log transaction references without exposing secrets.

## 13.5 Marketplace Settlement

Host payouts and commission handling depend on the chosen payment provider, merchant arrangement, and applicable requirements.

Do not represent a booking payment as a completed host payout unless the payout has actually been verified.

---

# 14. Reviews and Ratings

## 14.1 Review Eligibility

A user may submit a review only if:

- They are authenticated.
- They are the driver associated with the booking.
- The booking has been completed.
- No review already exists for that booking.

## 14.2 Review Features

- Rating from 1 to 5.
- Optional written comment.
- Review submission.
- Review display on charger pages.
- Administrative moderation.
- Average charger rating.

## 14.3 Rating Calculation

Calculate the average rating from eligible reviews.

For small datasets, the application can aggregate reviews through MongoDB queries. Add caching or denormalized rating summaries only when performance measurements justify it.

---

# 15. Frontend Requirements

## 15.1 Design Principles

- Responsive design.
- Mobile-first layouts.
- Clear navigation.
- Consistent buttons and forms.
- Readable typography.
- Accessible color contrast.
- Clear loading, success, empty, and error states.
- Simple booking and listing workflows.

## 15.2 Public Pages

### Home page
- EV Share introduction.
- Charger search field.
- Location search.
- Featured or nearby chargers where available.
- Explanation of how the platform works.
- Host registration call to action.

### Charger search page
- Search and filters.
- Charger cards.
- Map/list display.
- Price and connector information.
- Availability indicators.

### Charger detail page
- Photos.
- Charger specifications.
- Host information permitted by policy.
- Address and location information.
- Pricing.
- Availability calendar or time slots.
- Rating and reviews.
- Booking action.

## 15.3 Authentication Pages

- Registration.
- Login.
- Forgot password.
- Reset password.
- Account profile.

## 15.4 Driver Dashboard

- Upcoming bookings.
- Previous bookings.
- Booking details.
- Cancellation options.
- Payment status.
- Review submission.

## 15.5 Host Dashboard

- My chargers.
- Add charger.
- Edit charger.
- Availability management.
- Upcoming reservations.
- Booking history.
- Payment and settlement status, when supported.

## 15.6 Administration Dashboard

- User management.
- Charger listing moderation.
- Booking overview.
- Payment metadata and refund tracking.
- Reports and disputes.
- Audit events.

## 15.7 Accessibility

- Proper form labels.
- Keyboard-accessible controls.
- Visible focus indicators.
- Useful alternative text for images.
- Clear validation messages.
- Responsive pages on common screen sizes.

---

# 16. URL and Routing Plan

Example routes:

```text
/                           Home page
/chargers/                  Search chargers
/chargers/<charger_id>/     Charger details
/accounts/register/         Registration
/accounts/login/            Login
/accounts/logout/           Logout
/accounts/profile/          User profile
/driver/dashboard/          Driver dashboard
/host/dashboard/            Host dashboard
/host/chargers/new/         Create charger
/host/chargers/<id>/edit/   Edit charger
/bookings/create/           Create booking
/bookings/                  Booking history
/bookings/<id>/             Booking details
/bookings/<id>/cancel/      Cancel booking
/payments/<id>/             Payment status
/chargers/<id>/reviews/     Charger reviews
/admin-panel/               Custom administration dashboard
```

These are illustrative route names. The implementation may adjust them while preserving the documented functionality.

Every route must enforce the appropriate authentication and permission rules.

---

# 17. API and Request Handling

The MVP can use Django-rendered HTML pages for most functionality.

JSON endpoints may be added for interactive features such as availability checks, map searches, and asynchronous status updates.

Example endpoints:

```text
GET    /api/chargers/
GET    /api/chargers/<id>/
GET    /api/chargers/nearby/
GET    /api/chargers/<id>/availability/
POST   /api/bookings/
GET    /api/bookings/
GET    /api/bookings/<id>/
POST   /api/bookings/<id>/cancel/
POST   /api/payments/create-order/
POST   /api/payments/webhook/
POST   /api/reviews/
```

Requirements:

- Validate request bodies.
- Return consistent status codes.
- Enforce ownership and role permissions.
- Avoid exposing database internals.
- Paginate list endpoints.
- Validate ObjectId input.
- Never expose password hashes or secrets.
- Apply CSRF protection to cookie-authenticated state-changing requests.
- Use idempotency protections for booking and payment operations.

These endpoints describe the logical interface; they do not require a separate REST framework in the initial version.

---

# 18. Security Requirements

## 18.1 Application Security

- Use HTTPS in production.
- Enable CSRF protection.
- Apply output escaping in templates.
- Validate and normalize user inputs.
- Prevent unauthorized object access.
- Enforce ownership checks on every protected operation.
- Rate-limit sensitive endpoints.
- Use secure password-reset tokens.
- Protect administrative routes.
- Configure secure session cookies.
- Keep dependencies updated.

## 18.2 Database Security

- Keep MongoDB credentials in environment variables.
- Use a dedicated database user with least-privilege permissions.
- Enable TLS for hosted database connections.
- Restrict network access where possible.
- Never commit connection strings or secrets to Git.
- Configure backups and test restoration.
- Avoid logging sensitive database fields.

## 18.3 File Upload Security

- Restrict file types and sizes.
- Validate uploaded images.
- Generate safe filenames.
- Do not trust browser-provided MIME types alone.
- Store production uploads outside the application code directory.
- Avoid serving executable uploads.
- Apply authorization to private files if any are introduced.

## 18.4 Privacy

- Collect only necessary personal information.
- Explain location permissions.
- Avoid exposing a host's private residential address unnecessarily.
- Restrict access to booking and payment records.
- Define data retention and deletion procedures.
- Publish appropriate privacy terms before public launch.

---

# 19. Environment Configuration

## 19.1 Environment Variables

Create a local `.env` file containing settings such as:

```env
DJANGO_SECRET_KEY=replace-with-a-secure-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>/<database>
MONGODB_DATABASE=ev_share

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

PAYMENT_PROVIDER=
PAYMENT_PUBLIC_KEY=
PAYMENT_SECRET_KEY=
PAYMENT_WEBHOOK_SECRET=

MAP_TILE_PROVIDER=
GEOCODING_PROVIDER=
```

The connection string is a placeholder. Replace it with your own MongoDB connection details.

Never commit a real `.env` file to source control.

## 19.2 Development Dependencies

The core dependency list should include compatible, pinned versions of:

```text
Django
mongoengine
pymongo
python-dotenv
Pillow
```

Additional packages may be introduced when needed for:

- Email delivery.
- Rate limiting.
- Payment gateway integration.
- Image storage.
- Testing.
- Production serving.

Choose mutually compatible versions and record exact versions in the project's dependency lock or requirements file.

## 19.3 Initial Setup

Example Windows commands:

```bash
mkdir ev_share
cd ev_share

python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
pip install django mongoengine pymongo python-dotenv pillow

django-admin startproject config .
python manage.py check
```

Then:

1. Create the application modules.
2. Configure environment variables.
3. Connect MongoEngine to MongoDB.
4. Verify the database connection.
5. Implement the user document and authentication workflow.
6. Add the first page and test the complete request flow.

Do not run Django relational migrations as a substitute for creating MongoEngine collections and indexes. Configure and verify MongoDB indexes separately.

---

# 20. Testing Requirements

## 20.1 Authentication Tests

Test that:

- Valid registration creates a user.
- Duplicate normalized emails are rejected.
- Passwords are hashed.
- Valid login succeeds.
- Invalid login fails safely.
- Suspended users cannot perform protected actions.
- Logout invalidates the session.
- Password reset tokens expire and cannot be reused.

## 20.2 Charger Tests

Test that:

- Hosts can create valid listings.
- Invalid prices and power values are rejected.
- Users cannot edit another host's charger.
- Inactive chargers cannot be newly booked.
- Connector filters return correct results.
- Geographic searches return nearby eligible chargers.

## 20.3 Booking Tests

Test that:

- Valid bookings can be created.
- Invalid time ranges are rejected.
- Overlapping reservations are rejected.
- Simultaneous booking requests cannot both reserve the same slot.
- Cancelled or expired reservations release eligible slots.
- A driver cannot cancel another driver's booking.
- A host cannot modify unrelated bookings.
- Prices are calculated on the server.
- Status transitions follow the defined workflow.

## 20.4 Payment Tests

Use sandbox or mocked provider responses.

Test that:

- Invalid signatures are rejected.
- Failed payments are not marked successful.
- Duplicate webhooks do not duplicate financial effects.
- Payment amounts are verified.
- Refund states are tracked correctly.
- Booking status is updated only after the required payment verification.

## 20.5 Security Tests

Test for:

- Unauthorized access.
- Object ownership violations.
- CSRF failures.
- Invalid ObjectIds.
- Malicious form inputs.
- Oversized uploads.
- Login abuse.
- Secret leakage in logs and responses.

## 20.6 Browser Testing

Verify:

- Responsive layouts.
- Navigation.
- Forms and validation.
- Search filters.
- Booking selection.
- Error messages.
- Empty states.
- Map behavior when location permission is denied.

---

# 21. Non-Functional Requirements

## 21.1 Performance

Initial targets, to be validated in a realistic deployment:

- Typical server-rendered page responses should target approximately 2 seconds or less under normal pilot traffic.
- Common charger searches should target approximately 1 second or less under normal pilot traffic.
- Search endpoints should be paginated and indexed.
- The booking workflow must prioritize correctness over marginal speed improvements.

These are engineering targets, not guaranteed performance figures.

## 21.2 Reliability

- Handle database connection failures gracefully.
- Avoid reporting successful writes before the database confirms them.
- Make booking and payment operations recoverable.
- Log unexpected application errors.
- Configure database backups.
- Document database restoration steps.

## 21.3 Scalability

The modular monolith should be sufficient for the initial pilot.

Possible future improvements:

- Background jobs for emails and notifications.
- Caching for safe, frequently requested data.
- Managed image storage.
- More detailed database index tuning.
- Read replicas or additional infrastructure if required.
- Dedicated services only when measured needs justify them.

## 21.4 Maintainability

- Separate document models, views, services, and validation.
- Use descriptive function and variable names.
- Keep business rules out of templates.
- Add automated tests for critical workflows.
- Document environment setup.
- Keep dependencies and configuration manageable.
- Use Git for source control.

---

# 22. Deployment Plan

## 22.1 Pre-Deployment Checklist

- Set `DEBUG=False`.
- Configure production hosts.
- Use a strong secret key.
- Set secure cookie options.
- Enable HTTPS.
- Configure the production MongoDB URI.
- Verify MongoDB network access and database permissions.
- Configure email delivery.
- Configure production image storage.
- Configure payment-provider credentials only when payment integration is ready.
- Create and verify database indexes.
- Run tests.
- Back up the database.
- Verify logging and error handling.
- Review privacy and platform terms.

## 22.2 Deployment Steps

1. Push the project to a private or appropriately managed Git repository.
2. Create a production MongoDB Atlas database.
3. Configure database credentials and network access.
4. Deploy the Django application to a Python-compatible host.
5. Set environment variables in the hosting dashboard.
6. Install pinned dependencies.
7. Collect and serve static files according to the chosen hosting setup.
8. Initialize and verify MongoDB indexes.
9. Run smoke tests.
10. Verify authentication, charger discovery, and booking flows.
11. Configure monitoring and backups.
12. Enable public access only after critical workflows have passed testing.

---

# 23. Implementation Roadmap

## Phase 1 — Project Foundation

Tasks:

- Create the Django project.
- Set up the virtual environment.
- Configure environment variables.
- Connect MongoEngine to MongoDB.
- Verify connectivity and basic document operations.
- Establish templates and static files.
- Configure error handling and logging.

**Completion condition:** The application starts and successfully reads and writes a test MongoDB document.

## Phase 2 — Authentication

Tasks:

- Create the user document.
- Implement registration.
- Implement login and logout.
- Configure password hashing and sessions.
- Add authorization helpers.
- Build the profile page.
- Add basic authentication tests.

**Completion condition:** Users can securely register, log in, log out, and access only authorized pages.

## Phase 3 — Charger Marketplace

Tasks:

- Create charger documents.
- Build listing forms.
- Implement create, edit, and deactivate actions.
- Add image upload validation.
- Build charger cards and detail pages.
- Add connector and price filters.

**Completion condition:** Hosts can manage their listings and drivers can discover them.

## Phase 4 — Location Search

Tasks:

- Add GeoJSON coordinates.
- Create the geographic index.
- Implement nearby-charger queries.
- Add map display.
- Add optional browser geolocation.
- Handle denied location permission.

**Completion condition:** Users can search for chargers by location without requiring automatic access to their device location.

## Phase 5 — Booking System

Tasks:

- Define booking rules and statuses.
- Implement availability checks.
- Implement concurrency-safe reservations.
- Calculate booking prices on the server.
- Add cancellation and expiry workflows.
- Build driver and host booking dashboards.
- Add booking conflict tests.

**Completion condition:** Valid reservations work and conflicting simultaneous bookings are safely rejected.

## Phase 6 — Reviews and Notifications

Tasks:

- Implement reviews.
- Restrict reviews to eligible completed bookings.
- Display charger ratings.
- Configure email delivery.
- Add booking notifications.

**Completion condition:** Eligible users can review completed bookings and receive configured notifications.

## Phase 7 — Payments

Tasks:

- Select a suitable payment provider.
- Configure sandbox credentials.
- Create provider payment orders.
- Verify payment responses and webhooks.
- Implement idempotent payment processing.
- Add refund tracking.
- Test booking and payment consistency.

**Completion condition:** Payment states are based on verified provider events, and duplicate events do not duplicate financial actions.

## Phase 8 — Administration and Deployment

Tasks:

- Build the protected administration dashboard.
- Add listing moderation.
- Add account suspension.
- Add booking and payment oversight.
- Configure production hosting.
- Verify database security and backups.
- Run end-to-end tests.
- Perform a controlled pilot launch.

**Completion condition:** Administrators can manage the marketplace and the production application passes its release checklist.

---

# 24. MVP Acceptance Criteria

The first version is considered functionally ready when the following conditions are met:

1. A user can register and log in securely.
2. Users can access only the capabilities permitted by their roles.
3. A host can create, edit, and deactivate a charger listing.
4. A driver can search and view active charger listings.
5. Connector type, power, price, and availability are visible.
6. Nearby charger search works with valid coordinates.
7. A driver can request an eligible reservation.
8. The backend calculates booking prices.
9. Conflicting reservations cannot both be confirmed.
10. Booking cancellation follows the defined policy.
11. Drivers and hosts can view the appropriate booking records.
12. Payment status is not changed to successful without verification.
13. Eligible drivers can submit reviews.
14. Administrators can moderate users and charger listings.
15. Secrets are not committed to the repository.
16. Critical authentication, authorization, booking, and payment tests pass.
17. The application can be deployed with a secured MongoDB connection.
18. The system can recover from expected validation errors and common service failures.

---

# 25. Risks and Technical Decisions

## 25.1 MongoDB and Django Integration

**Risk:** Django's default relational features do not automatically integrate with MongoEngine documents.

**Mitigation:** Use a clearly defined MongoEngine document layer, explicit authentication and session configuration, custom administration screens, and automated tests.

## 25.2 Booking Concurrency

**Risk:** Multiple users may request the same charging time simultaneously.

**Mitigation:** Use atomic reservation slots or another rigorously tested concurrency-safe design. Do not rely on a simple availability query.

## 25.3 Payment Consistency

**Risk:** A payment may succeed while a booking update fails, or a webhook may arrive multiple times.

**Mitigation:** Verify provider events, make handlers idempotent, and implement recovery for incomplete operations.

## 25.4 Host Payouts and Legal Compliance

**Risk:** Marketplace settlement, refunds, electricity resale, and private charging arrangements may require provider approval or additional compliance measures.

**Mitigation:** Confirm the intended operating model, provider capabilities, applicable local requirements, and contractual responsibilities before public launch.

## 25.5 Charger Compatibility

**Risk:** A vehicle may not support the listed connector or charging characteristics.

**Mitigation:** Display accurate charger specifications and avoid unsupported compatibility claims.

## 25.6 Location Privacy

**Risk:** Publishing precise residential charger locations may reveal private information.

**Mitigation:** Define which location details are public, which are disclosed after booking, and how consent and access controls work.

---

# 26. Instructions for AI Coding Tools

When implementing EV Share using an AI coding assistant, follow these instructions.

## Core Instructions

1. Read this entire TRD before writing code.
2. Use Python and Django for the backend.
3. Use MongoDB as the primary database.
4. Use MongoEngine for document models.
5. Use Django Templates, Bootstrap, HTML, CSS, and vanilla JavaScript for the frontend.
6. Do not introduce React, Next.js, or microservices unless explicitly requested.
7. Do not assume Django's relational ORM, authentication tables, migrations, or admin automatically work with MongoEngine.
8. Keep authentication, permissions, booking, and payment rules in backend services.
9. Keep templates focused on presentation.
10. Use environment variables for secrets.
11. Never store plaintext passwords or raw payment credentials.
12. Validate all user input on the server.
13. Use MongoDB indexes and concurrency-safe reservation logic.
14. Write tests for every critical workflow.
15. Avoid fake payment success responses in production code.
16. Do not claim a feature is complete unless it has been implemented and tested.
17. Do not change existing visual design unnecessarily when working on a feature-specific task.
18. Keep the application beginner-friendly and explain complex implementation decisions.
19. Use compatible, pinned dependencies.
20. Update documentation when architecture or setup changes.

## Recommended Coding Workflow

Implement in small, verifiable stages:

1. Project setup and database connection.
2. User registration and authentication.
3. Charger document and listing management.
4. Charger search and filters.
5. Location-based discovery.
6. Booking and concurrency controls.
7. Cancellation and booking history.
8. Reviews and notifications.
9. Payment-provider integration.
10. Administration, security review, and deployment.

After each stage:

- Run the relevant tests.
- Fix errors before continuing.
- Verify database operations.
- Check permissions.
- Confirm the feature works in the browser.
- Update the README and implementation checklist.

---

# 27. Final Technical Decision Summary

| Component | Final decision |
|---|---|
| Application | EV Share |
| Backend language | Python |
| Web framework | Django |
| Architecture | Modular monolith |
| Primary database | MongoDB |
| Database integration | MongoEngine |
| Database hosting | MongoDB Atlas |
| Frontend | Django Templates |
| Styling | Bootstrap and CSS |
| Browser interactions | Vanilla JavaScript |
| Authentication | MongoEngine user documents with explicitly configured Django password hashing and session handling |
| Administration | Protected custom Django dashboard |
| Geographic search | GeoJSON and MongoDB `2dsphere` index |
| Maps | Leaflet with a suitable tile provider |
| Payments | Third-party provider with server-side verification |
| Image storage | Local in development; managed storage in production |
| Testing | Automated tests plus browser-based verification |
| Deployment | Python-compatible application hosting and MongoDB Atlas |

## Final Recommendation

Build EV Share as a single Django application backed by MongoDB, and implement it in phases.

Start with authentication, charger listings, location-based discovery, and safe booking reservations. Introduce payments only after the booking workflow is reliable.

**The most important technical requirement is booking correctness:** the application must never rely only on what the browser displays, and it must safely handle simultaneous reservation attempts. MongoDB can support this design, but the reservation strategy, session handling, and payment workflow must be implemented deliberately rather than assumed to work automatically.