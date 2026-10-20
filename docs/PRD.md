# EV SHARE — MASTER PRODUCT REQUIREMENTS DOCUMENT (PRD)

**Product Name:** EV Share  
**Tagline:** Your Charger. Someone Else’s Journey. Everyone Benefits.  
**Document Version:** 3.0 — Consolidated Master PRD  
**Status:** Final Product Baseline for MVP Planning and Development  
**Last Updated:** October 2026  
**Initial Market:** India  
**Initial Launch Model:** Controlled pilot on one compact section of a selected highway travel corridor  
**Platform:** Responsive Web Application, PWA-ready  
**Backend:** Python + Django  
**Database:** MongoDB + MongoEngine  
**Frontend:** Django Templates, Bootstrap, HTML, CSS, and vanilla JavaScript  
**Primary Users:** EV Drivers, Verified Charger Hosts, Platform Administrators  
**Primary Revenue Model:** Commission on eligible completed charging sessions, subject to commercial and regulatory validation  
**Development Context:** Solo-founder, college project, and hackathon-friendly MVP  
**Budget:** Not yet finalised

---

# 1. EXECUTIVE SUMMARY

## 1.1 Product Overview

EV Share is a peer-to-peer electric vehicle charging marketplace that connects EV drivers who need charging with eligible individuals and businesses that have suitable charging facilities available for sharing.

EV drivers may experience difficulty finding compatible and accessible charging facilities while travelling, visiting unfamiliar locations, or driving through areas with limited charging options. At the same time, some hotels, restaurants, offices, parking facilities, and residential properties may have suitable charging equipment that is unused during certain periods.

EV Share aims to connect this existing charging capacity with genuine charging demand through a trusted digital marketplace.

Hosts can submit charging facilities for verification, publish approved listings, configure availability, set permitted pricing, and manage reservations. Drivers can discover compatible chargers, check available time slots, view pricing, reserve a charger, access authorised instructions, and manage their bookings.

EV Share will initially operate as a technology marketplace rather than owning or installing every charging station.

The MVP will focus on one core outcome: helping a driver find and reserve a suitable, genuinely available charging facility with minimal uncertainty.

## 1.2 Vision

Make suitable existing EV charging infrastructure more accessible by connecting verified hosts with drivers who need charging.

## 1.3 Mission

Build a dependable, easy-to-use charging marketplace that helps eligible charger hosts share available charging capacity and enables EV drivers to discover and reserve additional charging options.

## 1.4 Value Proposition

**For drivers**
- Discover additional charging options.
- Check connector compatibility and rated power.
- See availability and pricing before booking.
- Reserve an available charger.
- Receive clear directions and access instructions.

**For hosts**
- Make eligible charging infrastructure discoverable.
- Control availability and access.
- Manage reservations.
- Track completed visits and potential earnings.
- Maintain control over their equipment and property.

**For commercial businesses**
- Improve utilisation of suitable charging facilities.
- Manage charging access more systematically.
- Potentially attract additional EV-driving customers.

**For the EV ecosystem**
- Improve access to existing charging capacity.
- Complement public charging networks.
- Create a foundation for future charging integrations.

## 1.5 Product Positioning

EV Share is a **charging-access marketplace**, not simply a map of charging stations.

The platform's core value is connecting drivers to verified, compatible, bookable charging facilities through reliable availability, clear pricing, secure booking, and accountable support.

A charger appearing on a map does not automatically mean that it is verified, operational, compatible, or available for use. The interface must distinguish these conditions clearly.

---

# 2. PROBLEM STATEMENT

## 2.1 Problems Faced by EV Drivers

EV drivers may experience:

1. Limited charging options in certain areas and travel corridors.
2. Occupied or unavailable public chargers.
3. Incompatible connectors or charging modes.
4. Unclear charging power and expected cost.
5. Difficulty discovering privately owned or commercial chargers that permit external access.
6. Uncertainty about availability at a particular time.
7. Additional range anxiety when travelling through unfamiliar areas.

## 2.2 Problems Faced by Charger Hosts

Potential hosts may have suitable charging infrastructure but lack a simple way to:

- Make their charging facilities discoverable.
- Define available time slots.
- Control access to their property.
- Manage reservations.
- Share access instructions.
- Track completed visits.
- Maintain transparent transaction records.

Not every privately owned charger is suitable for paid sharing. Technical suitability, permission to offer access, electrical safety, property access, and applicable legal requirements must be evaluated before a listing becomes bookable.

## 2.3 Core Problem

Charging demand and potentially available charging capacity are not always connected efficiently.

EV Share aims to bridge this gap by making eligible charging facilities discoverable and bookable through a structured marketplace.

## 2.4 Jobs to Be Done

**Driver:** When I need charging away from my usual location, help me find a compatible charger that is available and accessible at the time I need it, so I can continue my journey with less uncertainty.

**Host:** When my suitable charger is unused, help me make it available under my own conditions, so I can manage access and potentially earn from eligible completed sessions.

**Administrator:** Help me verify hosts and chargers, monitor bookings, resolve problems, and maintain a trustworthy marketplace.

---

# 3. PRODUCT GOALS AND NON-GOALS

## 3.1 Primary Goals

1. Validate demand for peer-to-peer charging access.
2. Recruit and verify suitable hosts within a concentrated pilot area.
3. Enable drivers to find compatible and genuinely bookable chargers.
4. Make instant booking available for verified chargers with available slots.
5. Prevent conflicting confirmed reservations.
6. Display transparent booking prices and terms.
7. Record charging visits and their completion evidence.
8. Establish a manageable verification, support, and dispute process.
9. Validate whether hosts are willing and eligible to share charging facilities.
10. Measure booking reliability, repeat usage, and potential unit economics.
11. Build a technical foundation for future expansion.

## 3.2 MVP Success Hypothesis

Can EV drivers discover and reserve suitable third-party charging facilities within a compact highway-corridor pilot, while eligible hosts are willing to make charging capacity available under acceptable safety, access, and operational conditions?

The MVP must test this hypothesis with real users and controlled charging visits.

## 3.3 MVP Non-Goals

The initial release will not:

- Own or install all charging infrastructure.
- Guarantee nationwide charger coverage.
- Guarantee that every listed charger is operational.
- Guarantee that a low-battery driver can reach a charger.
- Automatically control third-party charging hardware.
- Read vehicle battery levels without authorised integrations.
- Claim automatic energy measurement without suitable hardware.
- Require AI-based recommendations.
- Require native Android or iOS applications.
- Implement fleet management.
- Operate a physical rescue service without an actual assistance partner.
- Enable live commercial payments before required commercial, legal, safety, and payment arrangements are approved.
- Build a complex microservices architecture.

---

# 4. TARGET USERS AND PERSONAS

## 4.1 EV Driver

**Description:** An electric vehicle owner who needs a convenient charging option near their current location, destination, or travel route.

**Goals**
- Find suitable charging options.
- Confirm connector compatibility.
- Compare availability and prices.
- Reserve a charging slot.
- Obtain directions and access instructions.
- Track bookings and report problems.

**Pain points**
- Limited information about privately accessible chargers.
- Uncertain availability.
- Range anxiety.
- Incompatible equipment.
- Unclear access and pricing.

**Success outcome:** The driver finds a suitable charger and completes the intended visit with minimal uncertainty.

## 4.2 Residential Charger Host

**Description:** A property owner or eligible resident with suitable charging infrastructure.

**Goals**
- Control when charging is offered.
- Restrict property access.
- Protect privacy.
- Manage bookings.
- Track eligible earnings.

Residential hosting is subject to applicable property permissions, safety requirements, and commercial eligibility.

## 4.3 Commercial Charger Host

**Description:** An eligible hotel, restaurant, office, parking facility, resort, or other commercial property.

**Goals**
- Make suitable charging capacity discoverable.
- Manage available time slots.
- Reduce manual reservation work.
- Improve utilisation.
- Track bookings and potential earnings.

## 4.4 Platform Administrator

**Description:** An authorised person responsible for platform operations.

**Goals**
- Review host and charger submissions.
- Manage users and listings.
- Monitor bookings and payment records.
- Resolve disputes.
- Investigate safety incidents.
- Maintain auditability and platform quality.

---

# 5. PILOT MARKET AND GO-TO-MARKET STRATEGY

## 5.1 Initial Geography

EV Share will begin with **one compact section of a selected highway travel corridor in India**.

The specific corridor and its endpoints must be confirmed during pilot discovery.

The product should not launch across multiple cities or an entire national highway network before sufficient local charging supply exists.

## 5.2 Why a Compact Corridor?

A broad map with scattered chargers may not provide meaningful value to drivers. A concentrated corridor allows the founder to recruit hosts, validate charger information, test bookings, and provide operational support within a manageable area.

## 5.3 Supply-First Strategy

The initial focus is to recruit suitable hosts and verify their charging facilities before broad driver acquisition.

Prioritise:

- Eligible commercial locations.
- Hosts willing to participate in controlled pilot testing.
- Reliable operating hours.
- Accurate connector and power information.
- Clear property access arrangements.
- Locations that provide useful coverage within the selected corridor.

Residential hosts may participate if they meet the applicable technical, safety, access, and legal requirements.

## 5.4 Pilot Validation Activities

Before public launch:

1. Interview EV drivers who use the selected route.
2. Identify current charging gaps and user pain points.
3. Contact prospective hosts.
4. Validate charger details and access permissions.
5. Assess the operational and regulatory model.
6. Recruit pilot participants.
7. Test the complete booking and charging-visit workflow.
8. Record failed visits, cancellations, and user feedback.

## 5.5 Pilot Launch Gate

The pilot can begin only when the participating chargers, access arrangements, verification process, support process, and applicable operating model have been reviewed.

Live paid charging transactions require a separate launch approval.

---

# 6. MVP SCOPE AND PRIORITISATION

## 6.1 P0 — Required for the Controlled MVP

### Account management
- Registration and login.
- Logout and account recovery.
- Driver and host capabilities.
- Profile management.
- Role-based access control.

### Host and charger verification
- Host verification submission.
- Charger listing submission.
- Administrator review.
- Listing approval, rejection, and suspension.
- Private storage of verification evidence.

### Charger marketplace
- Charger listing creation and management.
- Charger detail pages.
- Map and list views.
- Search by location.
- Connector and charging-power filters.
- Price and availability filters.
- Clear verification indicators.

### Booking
- Instant booking for eligible verified chargers with available slots.
- Server-side availability checks.
- Prevention of conflicting confirmed reservations.
- Booking confirmation and unique reference.
- Booking history.
- Cancellation and expiry workflows.
- Driver and host dashboards.

### Charging-session records
- Manual session start and end records.
- Session completion confirmation.
- Reported issue workflow.
- Clear distinction between a completed visit and verified energy delivery.

### Transaction records
- Server-calculated booking prices.
- Pricing snapshots.
- Simulated or sandbox payment flow.
- Payment status tracking.
- Refund and settlement status fields where applicable.
- No live commercial transactions until the required approvals are obtained.

### Trust and operations
- Reviews linked to eligible completed bookings.
- Basic notifications.
- Support cases and dispute reporting.
- Protected administrator dashboard.
- Audit logs.
- Basic analytics.
- Automated tests for critical workflows.

## 6.2 P1 — After Initial Validation

- Saved chargers.
- Better host analytics.
- Host reliability indicators.
- Improved search ranking.
- Route-aware discovery.
- Additional notification channels.
- Improved repeat-booking experience.
- More advanced commercial host tools.

## 6.3 P2 — Future Expansion

- Smart charger integrations.
- Automatic session detection.
- Verified energy metering.
- Live charger status.
- Advanced route planning.
- Vehicle-range-aware recommendations.
- Fleet management.
- Corporate accounts.
- Native mobile applications.
- Validated roadside-assistance partnerships.
- Demand forecasting and advanced analytics.

---

# 7. USER ROLES AND PERMISSIONS

## 7.1 Guest

Can:
- View public pages.
- Explore public charger information where enabled.
- Register or log in.

Cannot:
- Access private bookings.
- View protected residential addresses.
- Access verification documents.
- View another user's account information.

## 7.2 Driver

Can:
- Manage their profile.
- Search for chargers.
- View charger details and availability.
- Create eligible bookings.
- View their booking history.
- Cancel eligible bookings.
- Access authorised instructions.
- View transaction records.
- Submit eligible reviews.
- Contact support.

## 7.3 Host

Can:
- Submit host verification information.
- Create and manage their own charger listings.
- Configure availability and permitted pricing.
- View reservations for their chargers.
- Record authorised session events.
- View transaction and payout status.
- Pause eligible listings.
- Report problems.

Hosts cannot approve their own listings, modify payment-provider evidence, or access unrelated users' private information.

A user may have both driver and host capabilities.

## 7.4 Administrator

Can:
- Review host applications.
- Approve, reject, or suspend listings.
- Manage users.
- Inspect bookings and sessions.
- Review transaction and refund records.
- Manage support cases.
- Moderate reviews.
- Investigate safety reports.
- View platform analytics and audit logs.

Administrative permissions must be explicit and enforced by the backend.

---

# 8. FUNCTIONAL REQUIREMENTS

## 8.1 Authentication and Accounts

**FR-001:** Users can register using supported account credentials.

**FR-002:** Users can securely log in and log out.

**FR-003:** Account recovery uses secure, expiring tokens or an equivalent secure workflow.

**FR-004:** Users can update permitted profile information.

**FR-005:** Users can act as drivers and hosts when eligible.

**FR-006:** The backend validates all permissions.

**FR-007:** Suspended accounts cannot perform restricted operations.

**FR-008:** Users can request account deletion subject to legal and financial record-retention requirements.

**Acceptance criteria**
- Duplicate normalized email addresses are rejected.
- Passwords are never stored in plaintext.
- Users cannot elevate privileges by modifying browser data.
- Users cannot access another user's private records.
- Protected routes enforce authorization on the server.

## 8.2 Host Verification

**FR-010:** Hosts can submit a verification application.

**FR-011:** Verification may require:
- Name or business name.
- Contact details.
- Host category.
- Charger location.
- Charger manufacturer and model where known.
- Connector type and charging mode.
- Rated power where known.
- Charger photographs.
- Proof of ownership or permission to offer access.
- Relevant installation or safety evidence.
- Applicable business or identity information.

**FR-012:** Administrators can approve, reject, or request changes.

**FR-013:** Verification evidence must be stored privately.

**FR-014:** Host identity verification must not be treated as proof of charger safety.

**FR-015:** Material verification changes must be auditable.

Verification statuses:
- Draft.
- Submitted.
- Under Review.
- Changes Requested.
- Approved.
- Rejected.
- Suspended.

Only eligible approved hosts can publish bookable listings.

## 8.3 Charger Listing Management

**FR-020:** Eligible hosts can submit charger listings.

Required listing information:
- Title and description.
- Charger type.
- Connector type.
- Rated power where known.
- Location.
- Approved pricing configuration.
- Availability schedule.
- Access restrictions.
- Relevant images.
- Verification status.

**FR-021:** Hosts can edit their own listings.

**FR-022:** Hosts can pause a listing.

**FR-023:** Administrators can suspend or reject a listing.

**FR-024:** Inactive or suspended listings cannot accept new bookings.

**FR-025:** Material changes to location, technical specifications, access, or pricing may require re-review.

Listing statuses:
- Draft.
- Pending Review.
- Changes Requested.
- Approved and Published.
- Paused.
- Suspended.
- Rejected.
- Archived.

## 8.4 Charger Discovery

**FR-030:** Drivers can search by current location, manually entered location, or selected map location.

**FR-031:** Results can be viewed in map and list layouts.

**FR-032:** Search filters include:
- Connector compatibility.
- AC/DC charging type.
- Rated charging power.
- Price range.
- Available date and time.
- Distance.
- Rating when sufficient reviews exist.

**FR-033:** Only verified and eligible EV Share listings may be presented as bookable EV Share chargers.

**FR-034:** Calendar availability must not be represented as proof of live operational status.

**FR-035:** Search results must be paginated or otherwise bounded.

**FR-036:** If no suitable charger is found, users can broaden the search.

**FR-037:** The application must not fabricate charger locations, availability, prices, ratings, or coverage.

## 8.5 Charger Detail Page

Each listing must display, where available:
- Charger title and images.
- Location and distance.
- Connector type.
- Charging mode.
- Rated power.
- Compatibility information.
- Verification status.
- Available time slots.
- Pricing basis and applicable fees.
- Host or business information permitted by policy.
- Access restrictions.
- Reviews.
- Cancellation rules.
- Safety information.
- Support and reporting options.

Exact residential addresses and private access instructions must be protected and disclosed only when necessary and authorised.

## 8.6 Vehicle and Charger Compatibility

**FR-040:** Drivers can provide vehicle details where supported.

**FR-041:** The platform compares known vehicle capabilities with charger specifications.

**FR-042:** Compatibility checks must consider connector type, charging mode, relevant standards, and supported power.

**FR-043:** Unknown compatibility must be disclosed.

**FR-044:** The platform must not assume that an adapter makes every configuration safe.

**FR-045:** Charger rated power must be distinguished from the power a particular vehicle can accept.

## 8.7 Availability Management

**FR-050:** Hosts can configure recurring weekly availability.

**FR-051:** Hosts can create date-specific exceptions and block unavailable periods.

**FR-052:** Hosts can define permitted booking durations, advance notice, and booking horizons.

**FR-053:** The backend rechecks availability immediately before confirming a reservation.

**FR-054:** Exclusive charging slots cannot have overlapping confirmed bookings.

**FR-055:** Simultaneous booking requests cannot reserve the same exclusive slot twice.

**FR-056:** Booking timestamps must use a consistent timezone strategy.

**FR-057:** Changes affecting existing reservations must follow documented policies.

## 8.8 Instant Booking

Instant booking is the default for approved chargers that have available slots and satisfy all eligibility conditions.

**FR-060:** Drivers can select an available slot and request a booking.

**FR-061:** The server validates charger eligibility, availability, pricing, and booking rules.

**FR-062:** The server creates the reservation using concurrency-safe logic.

**FR-063:** The driver receives a booking reference and the resulting booking status.

**FR-064:** If the slot is no longer available, the request fails safely and the driver is asked to select another slot.

**FR-065:** Repeated requests must not create duplicate bookings.

**FR-066:** Payment or simulated payment status must be tracked separately from booking status.

**FR-067:** The application must never display a confirmed booking before the required confirmation conditions are met.

The MVP does not require manual host approval for every booking. A listing can use instant booking only when its host, charger, schedule, access arrangements, and applicable operating rules permit it.

## 8.9 Booking Lifecycle

The booking flow is:

1. Driver searches for a charger.
2. Driver checks compatibility and access requirements.
3. Driver selects an available slot.
4. The server validates availability.
5. The server calculates the booking amount.
6. The driver reviews pricing and cancellation terms.
7. The server reserves the slot.
8. The configured payment or simulated-payment step is completed.
9. The booking is confirmed according to the selected pilot policy.
10. The driver receives authorised instructions.
11. The charging visit is recorded.
12. The booking is completed, cancelled, expired, or disputed as appropriate.
13. Eligible reviews can be submitted.

Booking statuses may include:
- Pending.
- Pending Payment.
- Confirmed.
- Cancelled.
- Expired.
- In Progress.
- Completed.
- Failed.
- No-Show.
- Disputed.

Only documented state transitions are permitted.

## 8.10 Booking Cancellation

**FR-070:** Drivers can cancel eligible bookings.

**FR-071:** Hosts and administrators can cancel only when permitted by policy and their permissions.

**FR-072:** Cancellation rules must be visible before booking.

**FR-073:** The backend checks cancellation eligibility.

**FR-074:** Cancelled reservations release eligible reserved capacity.

**FR-075:** Refund status is tracked separately from booking status.

**FR-076:** Cancellation reasons and timestamps are recorded.

**FR-077:** Affected users are notified when the notification service is configured.

## 8.11 Charging-Session Records

**FR-080:** An authorised host can record the start of a charging visit.

**FR-081:** An authorised host can record the end of a charging visit.

**FR-082:** Session records reference the relevant booking.

**FR-083:** The system distinguishes:
- Booking confirmed.
- Visit started.
- Visit completed.
- Energy delivery verified.

**FR-084:** Manually entered session data must be labelled as manual.

**FR-085:** The MVP must not claim automatically metered energy without a reliable authorised source.

**FR-086:** Users can report failed or incomplete visits.

**FR-087:** A booking must not be marked as a successful charging session solely because the scheduled end time passed.

## 8.12 Pricing and Transaction Records

**FR-090:** Pricing is calculated on the server.

**FR-091:** Drivers see the known price breakdown before committing.

**FR-092:** Confirmed bookings preserve the agreed pricing snapshot.

**FR-093:** The system records transaction amount, currency, status, and applicable provider reference.

**FR-094:** Payment status is independent of booking status.

**FR-095:** Refunds and payout statuses are separately tracked where applicable.

**FR-096:** Raw card numbers, CVVs, UPI PINs, and banking passwords must never be stored by EV Share.

**FR-097:** Duplicate payment events must not create duplicate financial effects.

## 8.13 Simulated Payment MVP

The initial MVP will use a simulated or sandbox payment workflow.

The purpose is to demonstrate:
- Server-calculated amounts.
- Booking checkout.
- Payment-pending and payment-success states.
- Payment-failure handling.
- Transaction records.
- Booking/payment state consistency.
- Refund-state demonstrations where needed.

Simulated payment success must be visibly identified as simulated and must not be represented as real money received.

A simulated payment does not create a real financial transaction, host payout, or platform revenue.

Live commercial payments remain disabled until the required payment-provider, business, regulatory, tax, and operating arrangements have been approved.

## 8.14 Revenue and Host Settlement

The intended long-term revenue model is a commission on eligible completed charging sessions.

The MVP may demonstrate commission calculations against simulated transactions.

**FR-100:** The system can calculate illustrative platform commission and host share.

**FR-101:** Commission rules must be configurable.

**FR-102:** Financial calculations must use appropriate decimal or integer-minor-unit arithmetic.

**FR-103:** Transaction records must preserve the amounts used in calculations.

**FR-104:** Actual payouts must not be represented as completed without verified settlement evidence.

**FR-105:** Any live marketplace settlement must use a provider and operating model approved for the intended arrangement.

## 8.15 Reviews and Ratings

**FR-110:** Only eligible completed bookings can generate reviews.

**FR-111:** A booking can receive no more than the permitted number of reviews.

**FR-112:** Ratings use a 1–5 scale.

**FR-113:** Users can report inappropriate reviews.

**FR-114:** Administrators can moderate reviews.

**FR-115:** Ratings are not proof of energy delivery.

## 8.16 Notifications

The MVP should support basic in-app status messages and email notifications where configured.

Relevant events:
- Account verification.
- Host verification updates.
- Listing approval or rejection.
- Booking confirmation.
- Booking cancellation or expiry.
- Simulated or sandbox payment status.
- Upcoming booking reminders.
- Session completion.
- Support case updates.

SMS, WhatsApp, and push notifications can be considered later.

## 8.17 Low-Battery Assistance Mode

### MVP

- Let the driver enter or permit access to their location.
- Show nearby eligible, compatible chargers.
- Prioritise available bookable listings.
- Display route distance or estimated travel time when supported by a reliable routing provider.
- Provide alternative search options.

### Future

- Vehicle-range-aware routing.
- Live charger status.
- Supported smart-charger integrations.
- Validated roadside assistance partnerships.

The MVP must not guarantee that a driver can reach a charger before battery depletion. EV Share must not claim to provide physical rescue without a real operational assistance service.

## 8.18 Support and Administration

**FR-120:** Users can create support cases.

**FR-121:** Support cases have unique identifiers and statuses.

**FR-122:** Administrators can review booking-related disputes.

**FR-123:** Administrators can suspend unsafe or misleading listings.

**FR-124:** Material administrative actions are logged.

**FR-125:** Safety incidents follow a documented escalation process.

---

# 9. USER EXPERIENCE AND DESIGN REQUIREMENTS

## 9.1 Design Principles

- Clean, modern, trustworthy design.
- Mobile-first responsive layouts.
- Clear primary actions.
- Consistent typography and spacing.
- Accessible forms and navigation.
- Transparent pricing.
- Clear verification labels.
- Clear loading, success, empty, and error states.
- Minimal friction during discovery and booking.

## 9.2 Required Screens

1. Landing page.
2. Registration.
3. Login.
4. Account recovery.
5. Profile settings.
6. Charger discovery map.
7. Charger discovery list.
8. Search filters.
9. Charger detail page.
10. Availability calendar.
11. Booking checkout.
12. Booking confirmation.
13. Booking details.
14. Driver dashboard.
15. Host onboarding.
16. Verification status.
17. Charger creation and editing.
18. Host dashboard.
19. Booking management.
20. Session records.
21. Transaction history.
22. Notifications.
23. Support and dispute reporting.
24. Admin dashboard.
25. Verification review queue.
26. Listing moderation.
27. Simulated payment status page.
28. Privacy, terms, safety, and cancellation pages.
29. Error and not-found pages.

## 9.3 Landing Page Structure

- Navigation: Explore Chargers, Become a Host, Login, Sign Up.
- Hero section explaining the value proposition.
- Primary action: Find a Charger.
- Secondary action: Become a Host.
- How It Works for drivers and hosts.
- Trust and verification explanation.
- Genuine featured listings when available.
- FAQs.
- Support and contact.
- Privacy, terms, and cancellation links.

Do not fabricate charger counts, user counts, reviews, availability, testimonials, or nationwide coverage claims.

## 9.4 Accessibility

Aim for WCAG 2.2 AA where practical.

Include:
- Keyboard navigation.
- Visible focus indicators.
- Accessible form labels.
- Readable contrast.
- Useful image alternative text.
- Clear validation messages.
- Responsive layouts.

---

# 10. BUSINESS RULES

**BR-001:** Only eligible approved chargers can accept bookings.

**BR-002:** Paused or suspended listings cannot accept new bookings.

**BR-003:** Instant booking is permitted only when the listing and requested slot satisfy all booking rules.

**BR-004:** Availability is validated by the server.

**BR-005:** Conflicting confirmed reservations for an exclusive charger are prohibited.

**BR-006:** Pricing is calculated by the server and disclosed before commitment.

**BR-007:** Confirmed bookings preserve the applicable pricing snapshot.

**BR-008:** Booking, session, payment, refund, and payout states remain separate.

**BR-009:** Manual session evidence must be distinguished from automatically measured data.

**BR-010:** Only authorised users can access private records or perform session actions.

**BR-011:** Refunds follow the documented policy and applicable requirements.

**BR-012:** Exact residential addresses and private instructions are protected.

**BR-013:** Reviews must be associated with eligible bookings.

**BR-014:** Administrators can suspend unsafe, fraudulent, or non-compliant listings.

**BR-015:** External public charging information is distinguished from bookable EV Share listings.

**BR-016:** The platform does not guarantee a driver can reach a charger before battery depletion.

**BR-017:** Live paid transactions remain disabled until required launch conditions are satisfied.

**BR-018:** Frontend validation never replaces backend validation.

**BR-019:** Repeated payment events must not duplicate financial actions.

**BR-020:** Failed, rejected, and expired bookings release eligible temporary reservations.

**BR-021:** The platform must not claim a successful charging session without the defined completion evidence.

**BR-022:** Host payouts are not marked complete without settlement evidence.

---

# 11. BUSINESS MODEL AND UNIT ECONOMICS

## 11.1 Primary Revenue Model

EV Share intends to earn a commission on eligible completed charging sessions.

Illustrative example:

- Transaction value: ₹240.
- Hypothetical platform commission: 15%.
- Gross platform commission: ₹36.
- Host share before other applicable deductions: ₹204.

These figures are illustrative, not approved prices, forecasts, or proof of legal eligibility.

## 11.2 Future Revenue Streams

- Commercial host subscriptions.
- Multi-location charger management.
- Fleet and corporate partnerships.
- Charging management tools.
- Suitable EV ecosystem partnerships.
- Advanced operational analytics.

These are future opportunities, not MVP commitments.

## 11.3 Financial Metrics

Track:
- Gross transaction value.
- Platform commission revenue.
- Host earnings.
- Payment processing costs.
- Refunds and chargebacks.
- Support cost per transaction.
- Host acquisition cost.
- Driver acquisition cost.
- Contribution margin.
- Repeat transaction rate.

Simulated transactions must be excluded from actual revenue and real transaction-value reporting. They may be measured separately as test events.

---

# 12. TECHNICAL PRODUCT REQUIREMENTS

## 12.1 Agreed MVP Technology Stack

**Backend:** Python + Django.

**Database:** MongoDB.

**MongoDB Integration:** MongoEngine.

**Frontend:** Django Templates, HTML, CSS, Bootstrap, vanilla JavaScript.

**Maps:** Leaflet with a suitable map-tile provider.

**Location Search:** MongoDB geospatial queries using GeoJSON and a `2dsphere` index.

**Images:** Local storage during development; managed object storage for production.

**Payments:** Simulated or sandbox integration during the MVP.

**Deployment:** Python-compatible application hosting with MongoDB Atlas or an appropriately secured MongoDB deployment.

## 12.2 Architecture

Use a modular monolithic Django application.

Core modules:
1. Accounts and Authentication.
2. Host Verification.
3. Charger Listings.
4. Charger Discovery.
5. Availability.
6. Booking Management.
7. Charging Sessions.
8. Pricing and Transactions.
9. Reviews.
10. Notifications.
11. Support and Disputes.
12. Administration.
13. Analytics and Audit Logs.

Business rules must be enforced by backend services rather than being implemented only in frontend JavaScript.

## 12.3 Database Requirements

Use MongoDB collections for:
- Users.
- Host profiles and verification records.
- Charger listings.
- Availability rules and exceptions.
- Bookings.
- Reservation slots or locks where needed.
- Charging sessions.
- Payment records.
- Refund and settlement records where applicable.
- Reviews.
- Notifications.
- Support cases.
- Audit logs.

Use MongoDB ObjectIds, document validation, appropriate indexes, and explicit authorization checks.

The design must account for MongoEngine's differences from Django's relational ORM. Django's standard authentication tables, database-backed sessions, migrations, and admin must not be assumed to work automatically with MongoEngine.

## 12.4 Booking Consistency

A simple availability query followed by a database insert is not sufficient to prevent concurrent bookings.

The implementation must use a tested concurrency-safe reservation strategy, such as atomic reservation of defined time slots with suitable uniqueness constraints or another robust interval-reservation mechanism.

Where multiple documents must change together, use supported transaction mechanisms or a recoverable reservation workflow.

## 12.5 Security Requirements

- HTTPS in production.
- Secure password hashing.
- Server-side authentication and authorisation.
- CSRF protection.
- Rate limiting for sensitive operations.
- Secure session configuration.
- Private storage for verification documents.
- Restricted residential address disclosure.
- Environment variables for secrets.
- Verified payment webhooks if a provider is integrated.
- Audit logs for sensitive actions.
- Database backups and restoration testing.

## 12.6 Performance Targets

Proposed initial targets:
- Common page loads should remain responsive under pilot traffic.
- Typical search requests should target approximately one second or less under expected pilot conditions, excluding external provider latency.
- Search results must be paginated.
- Images should be optimised.
- Booking correctness takes priority over marginal performance improvements.

Targets must be measured and adjusted using realistic tests.

---

# 13. ANALYTICS AND SUCCESS METRICS

## 13.1 North-Star Metric

**Successful charging visits per active, eligible charger per week.**

A booking confirmation alone does not count as a successful charging visit.

Track verified energy-delivery sessions separately where reliable evidence exists.

## 13.2 Supply Metrics

- Approved hosts.
- Eligible active chargers.
- Percentage of bookable listings with required verification.
- Geographic coverage within the pilot corridor.
- Connector and power distribution.
- Host retention.

## 13.3 Demand Metrics

- Active drivers.
- Search volume.
- Searches with no suitable result.
- Search-to-listing-view conversion.
- Listing-view-to-booking conversion.
- Confirmed bookings.
- Repeat booking rate.

## 13.4 Reliability Metrics

- Booking confirmation rate.
- Visit completion rate.
- Verified charging-session completion rate.
- Host cancellation rate.
- Driver cancellation rate.
- No-show rate.
- Access failure rate.
- Compatibility failure rate.
- Payment simulation failure rate.
- Support cases per 100 bookings.
- Average dispute resolution time.

## 13.5 Business Metrics

- Actual gross transaction value after live payments are approved.
- Actual platform commission revenue.
- Host earnings.
- Refund rate.
- Payment processing costs.
- Support cost per transaction.
- Host and driver acquisition costs.
- Contribution margin.

Until live transactions are approved, report simulated financial results separately.

## 13.6 Proposed Pilot Targets

Initial hypotheses:
- 100% of bookable listings have the required verification records.
- Zero conflicting confirmed exclusive reservations.
- At least 85% booking-to-visit completion rate after a meaningful sample is collected.
- At least 90% successful confirmation for eligible instant-booking attempts, excluding user cancellations and defined external failures.
- Zero serious unresolved safety incidents.
- Establish baseline metrics for repeat usage, failed visits, and support costs.

These are proposed targets, not guarantees. Define denominators, measurement windows, and minimum sample sizes before judging results.

---

# 14. TESTING REQUIREMENTS

## 14.1 Authentication Tests

- Valid registration succeeds.
- Duplicate normalized email is rejected.
- Passwords are hashed.
- Valid login succeeds.
- Invalid login fails safely.
- Suspended users cannot perform restricted actions.
- Logout invalidates the session.
- Recovery tokens expire and cannot be reused.

## 14.2 Charger Tests

- Hosts can submit valid listings.
- Invalid prices and power values are rejected.
- Hosts cannot edit another host's listing.
- Inactive listings cannot be booked.
- Compatibility filters work.
- Geographic search returns eligible nearby results.
- Unapproved listings are not bookable.

## 14.3 Booking Tests

- Valid reservations succeed.
- Invalid time ranges are rejected.
- Overlapping bookings are rejected.
- Simultaneous requests cannot both reserve the same exclusive slot.
- Cancelled and expired reservations release eligible slots.
- Drivers cannot modify unrelated bookings.
- Hosts cannot modify unrelated chargers.
- Prices are calculated on the server.
- Booking state transitions follow defined rules.
- Repeated requests do not create duplicate bookings.

## 14.4 Session Tests

- Only authorised users can record session events.
- Session records reference valid bookings.
- Manual records are labelled as manual.
- A scheduled end time alone does not prove a successful visit.
- Disputed sessions can be investigated.

## 14.5 Payment Simulation Tests

- Simulated success is clearly identified.
- Simulated success does not claim real money was received.
- Failed payment states do not silently confirm bookings when payment is required.
- Duplicate events do not duplicate transaction records.
- Refund-state demonstrations do not claim a real refund was processed.

## 14.6 Security Tests

- Unauthorized access is rejected.
- Object ownership is enforced.
- Client-supplied prices are not trusted.
- Invalid identifiers are handled safely.
- Uploads are validated.
- Sensitive residential information is protected.
- Administrative routes require permission.
- Secrets do not appear in logs or source control.

## 14.7 End-to-End Test Scenarios

1. Driver registration and login.
2. Host registration and verification.
3. Administrator approval.
4. Charger listing creation and approval.
5. Location-based discovery.
6. Connector filtering.
7. Instant booking.
8. Simultaneous booking attempts.
9. Simulated payment success.
10. Simulated payment failure.
11. Booking cancellation and slot release.
12. Manual session start and end.
13. Disputed charging visit.
14. Eligible review submission.
15. Listing suspension.
16. Support case creation and resolution.
17. Unauthorized access attempt.
18. Database failure and recovery behavior.

---

# 15. LEGAL, SAFETY, AND OPERATIONAL REQUIREMENTS

Before enabling paid commercial charging, review the applicable Indian framework with qualified advisers.

Areas include:
- Current Ministry of Power EV charging guidelines and amendments.
- State and electricity distribution-company requirements.
- Permitted charging-access and commercial arrangements.
- Electricity metering and billing.
- Electrical installation and equipment standards.
- Property access and landlord permissions.
- Housing-society and building rules where relevant.
- Consumer protection and grievance handling.
- Payment-provider and settlement requirements.
- Tax and invoicing obligations.
- Applicable privacy and data-protection obligations.
- Insurance, liability, and safety incident handling.

The applicable requirements may differ by host type, charger type, state, property, and operating model.

This PRD is not legal advice. Software functionality does not establish that a paid charging arrangement is legally permitted.

---

# 16. RISKS AND MITIGATIONS

## 16.1 Insufficient Charger Supply

**Risk:** Drivers cannot find useful options within the pilot corridor.

**Mitigation:** Recruit and verify hosts first. Concentrate on a manageable section rather than launching across an entire highway.

## 16.2 Host Reluctance

**Risk:** Hosts may worry about privacy, property access, or operational burden.

**Mitigation:** Use controlled onboarding, host-managed availability, clear access rules, and restricted residential address disclosure.

## 16.3 Inaccurate Availability

**Risk:** Drivers reserve chargers that are not actually accessible.

**Mitigation:** Use explicit host schedules, server-side availability checks, booking conflict prevention, and a clear reporting workflow.

## 16.4 Technical Incompatibility

**Risk:** Drivers arrive at chargers that cannot charge their vehicles.

**Mitigation:** Collect structured connector and power information, display uncertainty, and avoid unsupported compatibility claims.

## 16.5 Electrical Safety

**Risk:** An unsuitable charging installation causes harm or damage.

**Mitigation:** Establish eligibility criteria, review required evidence, define safety escalation procedures, and obtain appropriate professional guidance.

## 16.6 Regulatory Uncertainty

**Risk:** The proposed commercial model is not permitted under a particular arrangement.

**Mitigation:** Validate the operating model before enabling live transactions and restrict pilot participation as needed.

## 16.7 Payment Complexity

**Risk:** Marketplace settlement and refunds introduce financial and compliance complexity.

**Mitigation:** Start with simulated payments and add live payments only after the provider and operating model are approved.

## 16.8 Booking Concurrency

**Risk:** Multiple users reserve the same time slot.

**Mitigation:** Implement atomic reservations or another tested concurrency-safe design and verify it with simultaneous-request tests.

## 16.9 Privacy

**Risk:** Public listings reveal private residential information.

**Mitigation:** Limit public address precision and disclose authorised access instructions only when necessary.

## 16.10 Overengineering

**Risk:** The MVP becomes too large for a solo founder to finish.

**Mitigation:** Keep the initial architecture simple, defer advanced integrations, and implement the core journey in small testable phases.

---

# 17. IMPLEMENTATION ROADMAP

## Phase 1 — Discovery and Product Validation

- Interview drivers and prospective hosts.
- Select a compact corridor section.
- Validate charging gaps.
- Recruit prospective hosts.
- Review technical eligibility and operating constraints.
- Define cancellation, access, and session policies.
- Create user flows and design specifications.

**Deliverables:** Pilot definition, initial host pipeline, product flows, and operating assumptions.

## Phase 2 — Project Foundation

- Set up Python and Django.
- Configure MongoDB and MongoEngine.
- Create shared templates and static assets.
- Implement error handling and logging.
- Establish basic testing.

**Deliverable:** A working application connected to MongoDB.

## Phase 3 — Accounts and Verification

- Implement registration and login.
- Configure sessions and permissions.
- Create host onboarding.
- Build verification review.
- Build a protected admin dashboard.

**Deliverable:** Secure accounts and controlled host onboarding.

## Phase 4 — Charger Marketplace

- Implement charger documents and forms.
- Add listing management.
- Build search and detail pages.
- Add compatibility filters.
- Implement geospatial search.
- Protect sensitive address information.

**Deliverable:** Approved chargers can be discovered through the web application.

## Phase 5 — Booking and Session Records

- Implement availability rules.
- Build concurrency-safe reservation logic.
- Add instant booking.
- Add cancellation and expiry.
- Add manual session records.
- Build driver and host dashboards.

**Deliverable:** A tested end-to-end booking and visit-recording workflow.

## Phase 6 — Simulated Transactions and Support

- Add simulated payment flow.
- Record transaction statuses.
- Add commission calculations for demonstration.
- Implement reviews.
- Add notifications.
- Build support and dispute workflows.

**Deliverable:** The full marketplace journey can be demonstrated without claiming real financial transactions.

## Phase 7 — Controlled Pilot

- Onboard eligible hosts.
- Run controlled visits.
- Test the application with real drivers.
- Collect feedback.
- Measure reliability and completion.
- Review safety, privacy, and operating issues.

**Deliverable:** Pilot results and a prioritised improvement plan.

## Phase 8 — Commercial Readiness

Only after the pilot and required approvals:
- Select a suitable payment provider.
- Validate the live transaction model.
- Implement verified payment processing.
- Add refund and settlement reconciliation.
- Review operational readiness.
- Decide whether to expand to another corridor.

**Deliverable:** A separate commercial launch decision.

The roadmap is a planning framework, not a guarantee of completion by a fixed date.

---

# 18. OPEN DECISIONS AND ASSUMPTIONS

The following decisions remain to be finalised.

1. Exact pilot corridor and endpoints.
2. Initial vehicle categories: electric cars, two-wheelers, or both.
3. Initial connector types and supported charging configurations.
4. Required host and charger verification evidence.
5. Allowed booking duration and booking horizon.
6. Cancellation rules and applicable fees.
7. Initial pricing model.
8. Future payment provider and settlement arrangement.
9. Definition of a completed charging visit.
10. Evidence required to confirm energy delivery.
11. Applicable operating permissions and insurance.
12. Support ownership and safety escalation responsibilities.
13. Production hosting and storage providers.
14. Pilot budget and timeline.
15. Conditions for enabling live commercial transactions.

The agreed MVP decisions remain:

- Responsive web application.
- Python + Django.
- MongoDB + MongoEngine.
- One compact section of a selected highway travel corridor.
- Instant booking for eligible verified chargers.
- Manual session records.
- Simulated or sandbox payments.
- Commission-based revenue model to be validated.
- No native mobile applications, live hardware control, or AI predictions in the MVP.

---

# 19. MVP ACCEPTANCE CRITERIA

The controlled MVP is ready for pilot testing when all of the following are satisfied.

## Accounts and Permissions
- Users can register, log in, log out, and recover access.
- Roles and resource ownership are enforced.
- Suspended users cannot perform restricted operations.

## Host and Charger Verification
- Hosts can submit verification information.
- Administrators can review applications.
- Only eligible approved chargers are bookable.
- Sensitive verification documents are protected.

## Discovery
- Drivers can search by location.
- Charger details display connector, power, price, and availability information.
- Compatibility filters work.
- Private residential information is protected.
- Unavailable or unapproved chargers are not presented as bookable.

## Booking
- Eligible drivers can book available chargers instantly.
- Availability is checked on the server.
- Conflicting confirmed reservations are prevented.
- Repeated requests do not create duplicate bookings.
- Cancellation and expiry release eligible reserved capacity.
- Booking status and payment status remain distinct.

## Sessions and Transactions
- Session records reference bookings.
- Manual session evidence is identified.
- Simulated payments are clearly labelled.
- Transaction amounts are calculated on the server.
- The application does not claim that simulated transactions are real revenue.
- Refund and settlement statuses are not falsely represented as completed.

## Operations and Security
- Administrators can manage users and listings.
- Support cases can be created and reviewed.
- Critical actions are logged.
- Authentication, authorisation, booking, and session tests pass.
- Backup and recovery procedures are documented.
- The application can be deployed with a secured MongoDB connection.

## Pilot Readiness
- Required host and charger checks are complete.
- Participating locations have appropriate access arrangements.
- Customer support and incident procedures are ready.
- The operating model has been reviewed for the selected pilot.
- Live payment functionality remains disabled unless the necessary approvals are complete.

---

# 20. FINAL PRODUCT STRATEGY

EV Share should be built around one dependable marketplace journey:

**Verified Host → Eligible Charger → Accurate Availability → Compatible Driver → Instant Booking → Charging Visit → Session Record → Transparent Transaction Record → Feedback and Support**

The initial product should prioritise reliability, safety, compatibility, privacy, and successful visits rather than the number of features.

The MVP should establish whether:
- Drivers can find useful charging options in the pilot area.
- Hosts are willing and eligible to share their charging infrastructure.
- Instant booking is reliable.
- Charging visits can be completed with acceptable failure rates.
- Users trust the platform.
- The intended commercial model is operationally and legally feasible.

Only after these conditions are validated should EV Share expand into additional corridors, live payment processing, smart charger integrations, advanced routing, and commercial management tools.

**EV Share is not just an app for finding charging stations. It is a marketplace designed to connect existing eligible charging capacity with the people who need it.**

**Your Charger. Someone Else’s Journey. Everyone Benefits.**

---

# 21. IMPLEMENTATION INSTRUCTIONS FOR AI CODING TOOLS

Treat this PRD as the master product baseline.

Before writing code:

1. Read the complete PRD.
2. Follow the agreed Python, Django, MongoDB, and MongoEngine stack.
3. Create a clear implementation plan.
4. Implement one phase at a time.
5. Keep the frontend simple and responsive.
6. Put business logic and permissions in backend services.
7. Do not assume Django's relational ORM and admin automatically support MongoEngine documents.
8. Use environment variables for secrets.
9. Validate inputs and permissions on the server.
10. Implement concurrency-safe booking reservations.
11. Keep simulated payments separate from real financial processing.
12. Write tests for every critical workflow.
13. Verify changes in the browser.
14. Update documentation as the project evolves.
15. Do not claim that a feature is complete unless it has been implemented and tested.

Do not fabricate chargers, hosts, reviews, booking activity, live availability, payment success, verification status, or energy-delivery evidence.

Do not implement deferred features merely because they appear in the future roadmap.

**END OF EV SHARE MASTER PRD — VERSION 3.0**