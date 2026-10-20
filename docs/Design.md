# EV Share — UI/UX Design System Specification
**Document:** `Design.md`  
**Reference Design System:** Apple India-Inspired Quiet Commerce & Utility Design  
**Application:** EV Share — Peer-to-Peer EV Charging Marketplace for Yamuna Expressway Corridor (Delhi NCR – Greater Noida – Mathura – Agra, ~165 km)  
**Version:** 2.0.0 (Project-Adapted Specification)  
**Date:** 20 October 2026  
**Status:** Approved Architectural Contract for UI/UX Designers, Frontend Engineers, Content Designers, and QA.  

---

## 1. Executive Summary

**EV Share** is a peer-to-peer EV charging marketplace engineered specifically for long-distance highway travel corridors in India, starting with the pilot **Yamuna Expressway Corridor (Delhi NCR to Agra, 165 km)**.

Following the design discipline of Apple India's quiet, photography-first digital gallery, EV Share treats charging infrastructure as an essential, high-trust travel utility rather than a noisy classifieds board. The interface remains calm and restrained: neutral chrome, generous whitespace, high-contrast typography, large location and facility imagery, a focused action-blue (`#0071E3`) interaction palette, and clear transactional paths for drivers and hosts.

The design system unifies two operating modes:
1. **Showcase Mode:** Low-density, cinematic, narrative-led corridor storytelling highlighting waypoint milestones (Noida KM 0, Dankaur KM 38, Jewar KM 42, Mathura KM 108, Agra KM 165), host properties, and EV driver convenience.
2. **Utility Mode:** Compact navigation, interactive Leaflet vector mapping, connector filtering (CCS2, Type 2, 15A), atomic time-slot selection grids, real-time meter telemetry check-in, transparent pricing breakdowns, and an executive administration console.

### Design Outcome
Deliver a premium, highly dependable highway charging experience where drivers can locate verified chargers along the expressway within seconds, confirm connector and vehicle compatibility, lock guaranteed slots without double-booking anxiety, and check in smoothly at host locations.

### Confidence Labels
- **Preserved Design Token:** Core visual values (colors, spacing, typography, radii, motion) carried directly from the Apple-inspired reference specification.
- **Project Domain Component:** Custom UI components engineered specifically for EV Share (e.g., Slot Grid, Leaflet Map, Session Telemetry Meter, Payout Split Table).
- **Implementation Constraint:** Technical and compliance boundaries (e.g., WCAG 2.2 AA contrast, 15%/85% fee separation, simulation notices).

---

## 2. Product and UX Principles

1. **One Idea Per Module.** Every hero, banner, or card communicates a single primary waypoint, charger listing, or driver action.
2. **The Charger & Premise Is the Layout.** Real location photography (driveways, parking bays, charging units, waiting amenities) carries visual weight. Avoid arbitrary floating drop-shadowed cards.
3. **Quiet Chrome.** Headers, filter bars, and controls stay legible but visually subordinate to corridor maps, charger photography, and slot availability.
4. **Short, Confident Copy.** Use concise headlines, one clear supporting line, and at most two actions per section.
5. **Blue Means Interaction.** The action-blue color (`#0071E3`) is strictly reserved for interactive links, primary CTA buttons, focus indicators, and selected slot states. It is never used as decorative tinting.
6. **Whitespace Creates Hierarchy.** Rely on the 4px baseline spacing scale rather than cluttered dividers, heavy borders, or decorative gradients.
7. **Predictable Behavior.** Standardize the interactive map controls, slot selection grid, session start/end meters, and moderation cards across all screens.
8. **Progressive Disclosure.** Surface critical highway details (kW output, connector type, distance from expressway, tariff/kWh) first; reveal host rules, parking instructions, and fee splits on interaction.
9. **Responsive Art Direction.** Provide art-directed mobile adaptations: full-width listing cards on desktop become touch-friendly swipeable cards with sticky bottom booking sheets on mobile.
10. **Accessibility and Performance by Default.** WCAG 2.2 AA compliance, keyboard navigation for time slots, zero layout shift (CLS ≤ 0.1), and rapid vector tile rendering.
11. **India Highway Localization.** Native display of Indian Rupee (`₹`), en-IN number formatting, local expressway milestones (KM 0 to KM 165), and Indian EV charging standards (CCS2 DC Fast, Type 2 AC, 15A Socket).
12. **Truth Over Persuasion.** Explicitly label simulated payment checkouts and driver-entered meter telemetry. Never fabricate false charger availability, fake ratings, or countdown urgency timers.

### What to Avoid
- Decorative neon gradients, artificial glassmorphism, or colored card borders.
- Cluttered charging cards showing more than two competing action buttons.
- Generic stock photos of foreign charging stations (e.g., US/Europe plug standards like CCS1 or CHAdeMO).
- Excessive card rounding (keep card radii at a restrained 16px, controls at 8–12px, pills at 999px).
- Autoplaying audio or unpausable carousel animations.
- Missing or hidden disclaimers regarding simulated payments or manual meter verification.

---

## 3. Audience, Goals, and Success Criteria

### Primary Audiences
- **Corridor EV Drivers:** Commuters and road-trippers traveling between Delhi NCR and Agra (via Noida, Jewar, Mathura) needing guaranteed charging slots without queue anxiety.
- **Low-Battery Emergency Drivers:** Motorists with critical state-of-charge (< 20%) requiring immediate, distraction-free routing to the nearest active charging point.
- **Highway & Gated Property Hosts:** Homeowners, farmhouses, hotels, and highway rest-stop operators monetizing idle EV charging equipment.
- **Platform Administrators:** Internal operations team reviewing host KYC documents, moderating new charger listings, and resolving session meter disputes.

### Core User Journeys

| User Goal | Entry Point | Desired Next Step |
| :--- | :--- | :--- |
| **Discover Corridor Chargers** | Home / Search bar | Interactive Leaflet Map with filtered waypoint pins |
| **Reserve Guaranteed Slot** | Charger Detail Page | Time slot grid selection -> Atomic Slot Lock -> Checkout |
| **Emergency Charge (Low Battery)** | Quick Nav / Banner | High-contrast nearest waypoint list with 1-tap booking |
| **Check-In & Start Session** | Active Booking View | Enter starting kWh odometer meter reading & photo |
| **Complete Session & Pay** | Running Session View | Enter ending meter reading -> Review ₹ total -> Complete |
| **List a Charger (Host)** | Host Onboarding Nav | Multi-step form: Location, Connector, Power kW, Pricing |
| **Moderate Listing (Admin)** | Admin Dashboard | Review KYC / listing proof -> Approve or Request Edits |

### Success Measures
- **Slot Lock Conversion:** > 80% checkout completion without double-booking conflicts.
- **Zero Double-Bookings:** 100% enforcement of atomic database slot reservation.
- **Core Web Vitals:** LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 across all pages.
- **Accessibility:** 0 critical axe-core / WCAG 2.2 AA accessibility violations.

---

## 4. Information Architecture & Navigation

### 4.1 Global Navigation Hierarchy
The top-level navigation follows Apple's quiet, horizontal layout:
1. **Brand Mark:** `EV Share` (monoline lightning icon + semibold wordmark)
2. **Find Charger:** Link to `/chargers/` (interactive map + listing directory)
3. **Corridor Map:** Direct anchor link to expressway waypoint route
4. **Emergency Low Battery:** Urgent shortcut to `/chargers/low-battery/`
5. **How It Works:** Educational corridor journey guide (`/how-it-works/`)
6. **Safety & Standards:** Host and driver safety commitments (`/safety/`)
7. **Host Portal:** Contextual link (`/accounts/host-onboarding/` or `/chargers/manage/`)
8. **User Account / Garage:** Role-aware menu (Driver Profile, Host Reservations, Admin Portal, Sign Out)
9. **Authentication CTAs:** "Sign In" and "Join EV Share" for unauthenticated visitors

### 4.2 Navigation Behavior
- **Desktop (≥ 834px):** Fixed 44px height bar, `rgba(255, 255, 255, 0.85)` background with `backdrop-filter: blur(20px)`, subtle bottom border `rgba(0, 0, 0, 0.08)`. Centered nav items with action blue hover highlight.
- **Mobile (≤ 833px):** Compact 48px header with Brand Mark, Low-Battery icon badge, and accessible hamburger drawer toggle. When opened, an animated full-screen drawer displays left-aligned 24px category links, preventing background scrolling.

### 4.3 Homepage Section Sequence
1. **Global Navigation:** Frosted quiet chrome header.
2. **Corridor Announcement Ribbon:** Subtle banner highlighting Yamuna Expressway pilot operational status.
3. **Hero Module:** Cinematic headline, expressway route subtitle, quick search input, and dual actions ("Explore Corridor Nodes" & "List Your Charger").
4. **Corridor Waypoint Gallery:** Paired promo tiles showcasing verified highway chargers at Noida (KM 0), Dankaur (KM 38), Jewar (KM 42), Mathura (KM 108), and Agra (KM 165).
5. **Interactive Expressway Preview:** Embedded Leaflet map segment displaying route waypoints and real-time charger status.
6. **Host Partnership Section:** Clean, high-impact module encouraging property owners along the expressway to list their chargers.
7. **Platform Safety & Disclaimers:** Transparent badges detailing peer-to-peer verification, transparent 15%/85% fee split, and simulation watermarks.
8. **Footer Directory:** Categorized navigation links and legal disclosures.

### 4.4 Footer Directory Structure
- **Corridor Waypoints:** Noida Sector 128 (KM 0), Dankaur Interchange (KM 38), Jewar Airport Node (KM 42), Mathura Milestone (KM 108), Agra Expressway Terminal (KM 165).
- **Driver Services:** Find Highway Chargers, Vehicle Garage Profile, Booking History, Low Battery Finder, Cancellation Policy.
- **Host Hub:** List Your Charger, Host KYC Verification, Payout Breakdown (85%), Host Safety Protocol.
- **Governance & Legal:** About EV Share, Terms of Service, Privacy Policy, Audit Logs, Administrator Portal.
- **Base Row:** Regional mark (`Yamuna Expressway, India`), copyright, and clean legal links.

---

## 5. Visual Design Foundations

### 5.1 Color Tokens (Exact Preservation)
The design system preserves the exact Apple-inspired palette:

| Token Name | Hex / RGBA Value | Purpose & EV Share Usage |
| :--- | :--- | :--- |
| `--color-canvas` | `#FFFFFF` | Main page background, primary clean surfaces |
| `--color-canvas-subtle` | `#F5F5F7` | Corridor announcement ribbon, page section backgrounds, footer |
| `--color-canvas-elevated`| `#FAFAFC` | Card surfaces, modal sheets, map control overlays |
| `--color-ink` | `#1D1D1F` | Primary headings, charger titles, price figures |
| `--color-ink-secondary` | `#333336` | Subheadings, body copy, slot time labels |
| `--color-ink-tertiary` | `#6E6E73` | Distance metrics, amenities text, footnote labels |
| `--color-ink-quaternary`| `#86868B` | Timestamp metadata, input placeholder text, fine print |
| `--color-white` | `#FFFFFF` | Text on dark buttons, map badge labels |
| `--color-black` | `#000000` | Pure dark contrast elements, camera/image backgrounds |
| `--color-link` | `#0066CC` | Inline textual links on light surfaces |
| `--color-link-dark` | `#2997FF` | Links on dark or inverted card overlays |
| `--color-action` | `#0071E3` | Primary action buttons, selected slot outline, focus ring |
| `--color-action-hover` | `#0076DF` | Primary button hover state |
| `--color-action-active`| `#006EDB` | Primary button pressed state |
| `--color-action-subtle`| `rgba(0, 113, 227, 0.08)` | Active nav item background, unselected slot hover |
| `--color-divider` | `rgba(0, 0, 0, 0.16)` | Card dividers, table borders, header bottom line |
| `--color-divider-dark` | `rgba(255, 255, 255, 0.24)`| Dividers across dark photo banners |
| `--color-success` | `#008009` | Verified host badge, active slot available, session finished |
| `--color-warning` | `#B64400` | Pending KYC verification, pending charger moderation |
| `--color-danger` | `#E30000` | Double-booking lock error, emergency battery alert, cancellation |

---

### 5.2 Typography Foundations

**Font Family Stacks:**
- Primary Display: `"SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif`
- System Fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- Monospace (Telemetry / PINs / IDs): `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`

**Typography Hierarchy Scale:**

| Role | Large Desktop (≥1069px) | Tablet (735–1068px) | Mobile (≤734px) | Weight | Line Height |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Corridor Hero Display** | `56px` | `44px` | `32px` | 600 (Semibold) | 1.08 |
| **Section Title (h2)** | `40px` | `32px` | `26px` | 600 (Semibold) | 1.15 |
| **Charger Card Title (h3)**| `24px` | `20px` | `18px` | 600 (Semibold) | 1.25 |
| **Subhead / Lead** | `20px` | `18px` | `16px` | 400 (Regular) | 1.35 |
| **Body Copy** | `17px` | `16px` | `15px` | 400 (Regular) | 1.47 |
| **Metadata / Badges** | `13px` | `13px` | `12px` | 500 (Medium) | 1.30 |
| **Legal / Footnotes** | `12px` | `12px` | `11px` | 400 (Regular) | 1.40 |

---

### 5.3 Layout, Grid & Spacing Scale

The layout adheres strictly to Apple's **4px baseline spacing scale**:

| Token | Pixel Value | Typical Application |
| :--- | :--- | :--- |
| `--space-1` | `4px` | Badge inner gap, tight inline margins |
| `--space-2` | `8px` | Gap between icon and text, slot grid gap (mobile) |
| `--space-3` | `12px` | Gutter between paired charger tiles, card inner gap |
| `--space-4` | `16px` | Standard form field padding, mobile container margin |
| `--space-5` | `20px` | Desktop grid column gap, card body padding |
| `--space-6` | `24px` | Distance between subheadings and action buttons |
| `--space-8` | `32px` | Spacing between major content sub-sections |
| `--space-10` | `40px` | Hero bottom margin, search filter bar padding |
| `--space-12` | `48px` | Top padding for section titles |
| `--space-16` | `64px` | Major section vertical rhythm on desktop |
| `--space-24` | `96px` | Hero section top/bottom padding |

**Grid Specifications:**
- **Max Container Width:** `1200px` (`--content-max`) with secondary constrained container `1140px` (`--container-max`).
- **Tile Gutter:** Exactly `12px` between paired campaign tiles.
- **Columns:** 12 columns on desktop, 8 columns on tablet, 4 columns on mobile.

---

### 5.4 Shape, Elevation & Borders

- **Buttons & Pills:** Pill radius `999px` (`--radius-pill`) for all primary, secondary, and badge elements.
- **Cards & Surfaces:** Rounded `16px` (`--radius-card`) with a 1px border `rgba(0, 0, 0, 0.08)`.
- **Form Controls:** Rounded `10px–12px` (`--radius-input`).
- **Elevations (Quiet Shadows):**
  - Subtle: `0 2px 8px rgba(0, 0, 0, 0.04)` (standard card default)
  - Elevated: `0 8px 24px rgba(0, 0, 0, 0.06)` (card hover & filter overlay)
  - Modal / Drawer: `0 20px 48px rgba(0, 0, 0, 0.12)` (booking checkout bottom sheet)

---

## 6. Component Specifications

### 6.1 Global Navigation (`.evs-navbar`)
- **Purpose:** Persistent top navigation bar across all screens.
- **Anatomy:** Brand logo + lightning mark, primary destination links, emergency low battery badge, auth state menu (Driver/Host profile avatar or Sign In button).
- **Height:** 44px (desktop), 48px (mobile).
- **Material:** `rgba(255, 255, 255, 0.85)` with `backdrop-filter: blur(20px)`.
- **Border:** 1px solid `rgba(0, 0, 0, 0.08)`.

### 6.2 Corridor Announcement Ribbon (`.evs-corridor-ribbon`)
- **Purpose:** Top-of-page announcement declaring pilot operational status.
- **Styling:** Full width, background `--color-canvas-subtle` (`#F5F5F7`), font size `13px`, text color `--color-ink-secondary`.
- **Content:** *"Yamuna Expressway Pilot Active: 5 verified charging waypoints between Noida (KM 0) and Agra (KM 165). Guaranteed slot locks enabled."*

### 6.3 Corridor Hero (`.evs-hero`)
- **Purpose:** Primary visual anchor on home and corridor overview pages.
- **Anatomy:** Eyebrow tag (`Delhi – Agra Pilot`), bold display headline, one-line supporting statement, inline search input with connector dropdown, and dual CTAs.
- **Typography:** Headline `56px` semibold, lead `20px` regular.
- **Layout:** Centered content with maximum reading width of `820px`.

### 6.4 Waypoint & Charger Promo Tiles (`.evs-card`)
- **Purpose:** Primary visual presentation of individual corridor charging stations.
- **Anatomy:** 
  - Photo banner (16:9 ratio, object-fit cover, subtle hover zoom).
  - Floating badges: `Verified Host` (green), `Power kW` (purple/blue), and `Expressway Milestone` (KM marker).
  - Body: Station title, host name, connector type icons (CCS2 / Type 2 / 15A), available amenities (WiFi, Restroom, Cafe).
  - Price display: Prominent tariff (`₹18.50 / kWh` or `₹120 / hr`) with zero hidden fee disclaimer.
  - Action: "Reserve Slot" primary pill button.
- **Grid Layout:** 2 columns desktop (12px gap), 1 column mobile.

### 6.5 Interactive Corridor Map (`#corridor-map`)
- **Purpose:** Visual geo-spatial exploration of the Yamuna Expressway corridor.
- **Implementation:** Leaflet.js with custom Apple-quiet map styling (subdued roads, high-contrast route polyline, custom waypoint markers with pulse animation for active chargers).
- **Dimensions:** Fixed height `480px` on desktop, `320px` on mobile.

### 6.6 Time Slot Booking Selector (`.slot-grid`, `.slot-item`)
- **Purpose:** Interactive time selection grid for booking a charging session.
- **Anatomy:** 1-hour slot buttons showing start-end time and real-time status.
- **States:**
  - *Available:* White surface, 1px border, hover blue border + subtle action background.
  - *Selected:* Filled action-blue (`#0071E3`), white text, bold label, `aria-selected="true"`.
  - *Locked / Booked:* Disabled state, opacity 0.4, cross-hatch or neutral gray fill, `cursor: not-allowed`, `aria-disabled="true"`.
- **Grid:** CSS Grid `repeat(auto-fill, minmax(130px, 1fr))`, gap `12px`.

### 6.7 Charging Session Meter Card (`.session-meter-card`)
- **Purpose:** Live check-in and check-out interface for recording vehicle odometer / charging meter kWh readings.
- **Anatomy:** Monospace digital meter display, starting kWh input, optional odometer photo upload, elapsed timer, and live estimated cost calculation.
- **Disclaimers:** Mandatory simulation notice: *"Manual unverified telemetry: Final billing calculated on host-confirmed meter delta."*

### 6.8 Checkout & Payment Fee Separation Table
- **Purpose:** Transparent breakdown of booking costs.
- **Anatomy:** 
  - Base Energy / Slot Tariff: `₹ [Amount]`
  - Platform Service Fee (15%): `₹ [Fee]` (clearly labeled)
  - Host Net Payout (85%): `₹ [Payout]`
  - Total Payable: Prominent bold figure.
  - Payment Action: Simulated payment button with clear test badge.

### 6.9 Status Badges (`.evs-badge`)
- **Pill Badges:** Capsule radius `999px`, padding `4px 10px`, font size `11px`, font-weight `600`, letter-spacing `0.02em`.
  - `.evs-badge-verified`: Green text (`#008009`), light green background (`rgba(0, 128, 9, 0.08)`).
  - `.evs-badge-dc`: Purple text (`#7B1FA2`), light purple background (`rgba(123, 31, 162, 0.1)`).
  - `.evs-badge-ac`: Cyan text (`#0288D1`), light cyan background (`rgba(2, 136, 209, 0.1)`).
  - `.evs-badge-simulation`: Amber text (`#E65100`), amber background (`#FFF3E0`).

---

## 7. Content Design & India Localization

- **Tone of Voice:** Confident, quiet, helpful, transparent. No artificial urgency or countdown timers.
- **Currency & Pricing:** Always prefix with `₹` symbol (e.g., `₹18.50 / kWh`). Format large numbers with Indian comma separation (`₹1,25,000`).
- **Highway Milestones:** Always reference exact expressway chainage:
  - *Noida Toll Plaza (KM 0)*
  - *Dankaur Interchange / Formula 1 Track (KM 38)*
  - *Jewar International Airport Interchange (KM 42)*
  - *Mathura Milestone (KM 108)*
  - *Agra Toll Plaza / Expressway Terminal (KM 165)*
- **EV Specifications:** Standardize Indian EV terminology:
  - Connector: CCS2 (DC Fast), Type 2 (AC), 15A 3-Pin Socket.
  - Vehicle Models: Tata Nexon EV Max, MG ZS EV, Mahindra XUV400, Hyundai Ioniq 5, BYD Atto 3.
- **Simulation Transparency:** Every simulated payment screen and test checkout must include the label:  
  *“DEMO ENVIRONMENT: This payment transaction is simulated for pilot validation. No real funds are deducted.”*

---

## 8. Motion & Micro-Interactions

Motion must explain state changes and provide immediate physical feedback without causing motion sickness:

- **Tokens:**
  ```css
  --motion-fast: 150ms;
  --motion-normal: 240ms;
  --motion-slow: 320ms;
  --ease-standard: cubic-bezier(0.28, 0.11, 0.32, 1);
  ```
- **Button Interactions:** Scale transition (`transform: translateY(-1px)`) on hover, active state returns to `translateY(0)` with instant color change.
- **Slot Selection:** 150ms border-color and background color transition with spring-like crispness.
- **Drawer / Modal Motion:** Slide up from bottom on mobile (`translateY(0)` from `translateY(100%)`) over 240ms with standard ease.
- **Accessibility:** Strict enforcement of `@media (prefers-reduced-motion: reduce)`: disable all transforms, scale effects, and animated transitions.

---

## 9. Responsive Breakpoints & Art Direction

| Viewport Range | Device Category | Layout & Navigation Behavior |
| :--- | :--- | :--- |
| **≤ 734px** | Mobile phones | Single-column listings, 100% width cards, bottom sticky action sheet for slot booking, map collapses to toggle button |
| **735px – 833px** | Compact Tablets | 2-column tiles where text allows, compact hamburger navigation |
| **834px – 1068px** | Landscape Tablets | Full horizontal navigation bar, 2-column grid with 12px tile gutter |
| **1069px – 1439px**| Standard Desktop | 12-column grid, max width 1140px, paired promo tiles, side-by-side map and listing view |
| **≥ 1440px** | Large Displays | Centered fluid canvas, max container 1200px, generous negative margins |

---

## 10. Accessibility Requirements (WCAG 2.2 AA)

- **Contrast Ratios:** Minimum 4.5:1 for normal body text against canvas (`#1D1D1F` on `#FFFFFF` yields 16.1:1). Minimum 3:1 for graphical controls and pill badges.
- **Focus Rings:** Distinct 3px solid action-blue focus ring (`rgba(0, 113, 227, 0.5)`) on all interactive buttons, inputs, and slot items.
- **ARIA Attributes:**
  - Map markers: `role="button"` with descriptive `aria-label="Charger at KM 42 Jewar, 22 kW Type 2, Available"`.
  - Slot selector: `role="grid"` with child `role="gridcell"`, `aria-selected="true/false"`, and `aria-disabled="true"`.
- **Keyboard Trapping:** Modal dialogs and mobile navigation drawers must trap focus and close via `Escape` key, restoring focus to the opening element.

---

## 11. Imagery & Media Performance

- **Asset Storage:** WebP format with JPEG fallbacks.
- **Aspect Ratios:** Explicit aspect-ratio definitions (`aspect-ratio: 16 / 9` for listing cards, `4 / 3` for thumbnails) to ensure Cumulative Layout Shift (CLS) = 0.
- **Lazy Loading:** Native `loading="lazy"` on all listing cards below the fold. Hero and map tiles prioritized with `fetchpriority="high"`.

---

## 12. Complete CSS Design Tokens (`:root`)

The following CSS variables represent the complete production design system contract in `static/css/ev_share.css`:

```css
:root {
  /* Color - Canvas & Surfaces */
  --color-canvas: #FFFFFF;
  --color-canvas-subtle: #F5F5F7;
  --color-canvas-elevated: #FAFAFC;

  /* Color - Typography Ink */
  --color-ink: #1D1D1F;
  --color-ink-secondary: #333336;
  --color-ink-tertiary: #6E6E73;
  --color-ink-quaternary: #86868B;
  --color-white: #FFFFFF;
  --color-black: #000000;

  /* Color - Interactive & Action */
  --color-link: #0066CC;
  --color-link-dark: #2997FF;
  --color-action: #0071E3;
  --color-action-hover: #0076DF;
  --color-action-active: #006EDB;
  --color-action-subtle: rgba(0, 113, 227, 0.08);

  /* Color - Dividers & Borders */
  --color-border: rgba(0, 0, 0, 0.08);
  --color-border-subtle: rgba(0, 0, 0, 0.04);
  --color-border-focus: rgba(0, 113, 227, 0.4);
  --color-divider: rgba(0, 0, 0, 0.16);
  --color-divider-dark: rgba(255, 255, 255, 0.24);

  /* Color - Semantic Feedback */
  --color-success: #008009;
  --color-success-bg: rgba(0, 128, 9, 0.08);
  --color-warning: #B64400;
  --color-warning-bg: rgba(182, 68, 0, 0.08);
  --color-danger: #E30000;
  --color-danger-bg: rgba(227, 0, 0, 0.08);

  /* Typography Stacks */
  --font-display: "SF Pro Display", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-text: "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* 4px Base Spacing Scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-14: 56px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-30: 120px;

  /* Layout & Dimensions */
  --content-max: 1200px;
  --container-max: 1140px;
  --tile-gutter: 12px;
  --nav-height: 44px;
  --nav-height-compact: 48px;
  --page-gutter: clamp(16px, 3vw, 48px);

  /* Shape & Radii */
  --radius-none: 0;
  --radius-sm: 8px;
  --radius-input: 12px;
  --radius-card: 16px;
  --radius-pill: 999px;

  /* Elevation Shadows */
  --shadow-subtle: 0 2px 8px rgba(0, 0, 0, 0.04);
  --shadow-elevated: 0 8px 24px rgba(0, 0, 0, 0.06);
  --shadow-modal: 0 20px 48px rgba(0, 0, 0, 0.12);

  /* Motion & Transitions */
  --motion-fast: 150ms;
  --motion-normal: 240ms;
  --motion-slow: 320ms;
  --ease-standard: cubic-bezier(0.28, 0.11, 0.32, 1);
}
```

---

## 13. Component Mapping to Project Templates

The following table connects the design specification directly to existing Django templates:

| Component Specification | Template File | Implementation Responsibility |
| :--- | :--- | :--- |
| **Global Navigation & Header** | `templates/base.html` | Sticky 44px bar, quiet chrome blur, role-based auth menu |
| **Announcement Ribbon** | `templates/core/home.html` | Corridor pilot status, en-IN milestone callout |
| **Corridor Hero & Waypoints**| `templates/core/home.html` | Expressway overview, paired promo tiles with 12px gutters |
| **Interactive Route Map** | `templates/chargers/search.html` | Leaflet map container `#corridor-map`, waypoint markers |
| **Charger Detail & Slot Grid**| `templates/chargers/detail.html` | Facility photos, kW specs, pricing breakdown, `.slot-grid` |
| **Slot Lock & Checkout** | `templates/bookings/checkout.html` | Transparent tariff, 15% platform fee, 85% host payout |
| **Session Meter & Telemetry** | `templates/sessions/start_session.html` | Starting kWh meter entry, photo verification, disclaimer |
| **Host Listing Hub** | `templates/chargers/host_list.html` | Host listings overview, status badges, earnings counter |
| **Executive Admin Console** | `templates/administration/dashboard.html` | Host KYC queue, charger moderation cards, audit explorer |
| **Footer & Disclosures** | `templates/base.html` | Multi-column directory, disclaimer strip, en-IN legal base |

---

## 14. Primary Workflow Specifications

### 14.1 Corridor Charger Discovery to Slot Booking
1. **Entry:** Driver visits `/chargers/` and filters by connector (`CCS2` or `Type 2`) or enters waypoint (`Jewar`).
2. **Evaluation:** Interactive Leaflet map centers on Yamuna Expressway. Driver clicks on Jewar Interchange (KM 42) pin.
3. **Detail Review:** Driver inspects photos, verified host badge, parking bay instructions, and ₹/kWh rate.
4. **Slot Locking:** Driver taps an available 1-hour time slot. System atomically creates a `SlotLock` (5-minute hold).
5. **Checkout:** Driver reviews transparent summary (Tariff + 15% fee) and clicks "Confirm & Pay (Simulated)".
6. **Confirmation:** System displays confirmed booking, access PIN, and host contact information.

### 14.2 Session Check-in and Meter Reading Telemetry
1. **Arrival:** Driver arrives at host property and navigates to active booking.
2. **Start Telemetry:** Driver taps "Start Charging Session", inputs current vehicle/charger meter kWh reading, and attaches photo.
3. **Active Session:** Live countdown timer displays elapsed time and estimated energy consumption.
4. **End Telemetry:** Driver taps "End Session", inputs final meter reading, and reviews total kWh consumed.
5. **Settlement & Review:** Final bill calculated; driver rates the charging experience with a 5-star verified review.

### 14.3 Host Onboarding & KYC Moderation
1. **Submission:** Host navigates to `/accounts/host-onboarding/`, enters property address along expressway, and uploads electricity bill & identity proof.
2. **Charger Setup:** Host specifies charger model, connector types, max kW output, and tariff rules.
3. **Admin Review:** Administrator reviews submitted documents in `/administration/verifications/` and approves or rejects with feedback.
4. **Activation:** Approved charger goes live immediately on the Yamuna Expressway map.

---

## 15. QA and Definition of Done Checklist

### Visual & Aesthetic Standards
- [ ] Visual hierarchy is dominated by real charger and facility photography.
- [ ] Exact color tokens (`#0071E3` action blue, `#F5F5F7` subtle canvas) applied consistently.
- [ ] Paired promo tiles maintain consistent 12px gutters.
- [ ] Zero arbitrary drop shadows or decorative gradients on full-bleed modules.
- [ ] Pill radius (`999px`) used for all primary action buttons.

### Responsive & Device Quality
- [ ] Verified across 320px, 375px, 768px, 834px, 1024px, 1200px, and 1440px viewports.
- [ ] Zero horizontal scrollbar or element overflow at 320px.
- [ ] Interactive Leaflet map touch controls behave predictably on mobile devices.
- [ ] Slot booking grid switches from multi-column desktop to comfortable 2-column mobile cards.

### Accessibility Standards
- [ ] Color contrast verified: all normal text ≥ 4.5:1, all UI boundaries and large text ≥ 3:1.
- [ ] All interactive buttons and links have visible 3px focus indicators.
- [ ] Slot buttons provide explicit `aria-selected` and `aria-disabled` states.
- [ ] Full keyboard navigation supported without focus traps.

### Functional & Integrity Checks
- [ ] All CTA buttons link to valid, working Django routes.
- [ ] Simulated payments and manual meter telemetry are explicitly watermarked.
- [ ] Real-time atomic slot locking prevents double bookings.
- [ ] Test suite maintains 100% pass rate (`pytest` 21/21 passed).

---

## 16. Reference Interpretation & Limitations

This specification adapts Apple India's quiet, photography-first design language to the peer-to-peer EV charging ecosystem:
- **Preserved:** All visual design tokens (colors, typography scales, spacing, pill radius, motion curves, and quiet chrome navigation).
- **Adapted:** Replaced retail storefront concepts (iPhone, Mac, shopping cart, trade-in, retail stores) with EV Share infrastructure (CCS2/Type 2 chargers, Yamuna Expressway corridor waypoints, host KYC, slot locking, meter telemetry, and driver garages).
- **Reconciliation:** All styling maps directly to the active Django application in `c:\Users\Pranav\Desktop\EV Share` without breaking existing routes or backend services.