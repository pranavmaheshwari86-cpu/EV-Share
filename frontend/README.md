# EV Share — Frontend Presentation Layer

## Overview
This directory contains the presentation-layer assets for **EV Share**, structured according to the Apple India quiet design system specification in `docs/Design.md`.

## Structure
```text
frontend/
├── static/
│   ├── css/
│   │   └── ev_share.css       # Design tokens, Apple typography, grid system, pill components
│   ├── images/
│   │   └── favicon.svg        # Apple-blue SVG lightning emblem
│   └── js/                    # Client-side progressive enhancement scripts
└── templates/
    ├── base.html              # Global navigation, pilot ribbon, skip link & footer
    ├── core/                  # Landing hero, waypoints promo grid, terms, privacy, safety
    ├── accounts/              # Driver & host login, registration, KYC verification
    ├── chargers/              # Corridor search, Leaflet interactive map, charger detail
    ├── bookings/              # Atomic time-slot grid, booking confirmation, driver history
    ├── sessions/              # Live check-in, odometer/kWh meter reading, dispute reporting
    ├── payments/              # Itemized fee breakdown (15%/85%), sandbox transaction receipts
    ├── reviews/               # 5-star rating submission, verified driver reviews
    ├── support/               # Grievance case submission & resolution tracking
    └── administration/        # Host KYC moderation queue, listing approvals, platform audit
```

## Design System Tokens
- **Primary Color:** Action Blue (`#0071E3`)
- **Background Surfaces:** Pure White (`#FFFFFF`) and Subtle Gray (`#F5F5F7`)
- **Typography:** System Sans-Serif (`-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif`)
- **Tile Gutter:** Fixed `12px` between paired charger promo cards
- **Baseline Scale:** 4px spacing unit (`--space-1: 4px`, `--space-2: 8px`, `--space-3: 12px`, ...)
- **Buttons:** Pill radius `999px` (`.btn-ev-pill`, `.btn-ev-primary`)
