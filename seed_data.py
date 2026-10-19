"""
EV Share — Corridor Pilot Data Seeding Script (Yamuna Expressway)
Delhi NCR – Greater Noida – Mathura – Agra (~165 km)

Creates:
- System Administrator (admin@evshare.in / admin123)
- Corridor Hosts with KYC verifications
- Registered Driver (driver@evshare.in / driver123) with registered Tata Nexon EV
- 5 Verified & 1 Pending Charger Listings with realistic coordinates, connectors, and amenities
- 1 Completed Booking with visit telemetry, simulated payment, and 5-star review
- 1 Upcoming Confirmed Reservation
- 1 Resolved Support Ticket
"""

import os
import sys
from datetime import datetime, timezone, timedelta, date

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
from django.apps import apps
if not apps.ready:
    django.setup()

from django.contrib.auth.hashers import make_password
from accounts.documents import User, Vehicle, HostVerification
from chargers.documents import Charger, ChargerAddress, AvailabilityRule
from bookings.documents import Booking, SlotLock, PricingSnapshot
from sessions_app.documents import ChargingSession
from payments.documents import PaymentTransaction
from reviews.documents import Review
from support.documents import SupportCase
from core.documents import AuditEvent

def seed_database():
    print("[*] Initializing EV Share Yamuna Expressway Pilot Seeding...")

    # 1. Clear existing collections
    print("  -> Clearing existing collections...")
    Review.objects.delete()
    PaymentTransaction.objects.delete()
    ChargingSession.objects.delete()
    SlotLock.objects.delete()
    Booking.objects.delete()
    Charger.objects.delete()
    HostVerification.objects.delete()
    SupportCase.objects.delete()
    AuditEvent.objects.delete()
    User.objects.delete()

    now = datetime.now(timezone.utc)

    # 2. Create Platform Administrator
    print("  -> Creating Platform Administrator (admin@evshare.in)...")
    admin_user = User(
        full_name="Aditi Sharma (Admin)",
        email="admin@evshare.in",
        password_hash=make_password("admin123"),
        phone_number="+91 99000 11223",
        roles=["driver", "host", "admin"],
        is_active=True,
        is_superuser=True,
        is_verified_host=True,
        created_at=now - timedelta(days=30)
    )
    admin_user.save()

    # 3. Create Pilot Drivers
    print("  -> Creating Verified EV Driver (driver@evshare.in)...")
    nexon_ev = Vehicle(
        make="Tata",
        model="Nexon EV Max",
        registration_number="DL-01-EV-2024",
        connector_type="CCS2",
        battery_capacity_kwh=40.5
    )
    driver_user = User(
        full_name="Rahul Mehra",
        email="driver@evshare.in",
        password_hash=make_password("driver123"),
        phone_number="+91 98111 22334",
        roles=["driver"],
        vehicles=[nexon_ev],
        is_active=True,
        created_at=now - timedelta(days=20)
    )
    driver_user.save()

    # Driver 2: Priya Nair
    mg_ev = Vehicle(
        make="MG",
        model="ZS EV",
        registration_number="UP-16-EV-8899",
        connector_type="CCS2",
        battery_capacity_kwh=50.3
    )
    driver_priya = User(
        full_name="Priya Nair",
        email="priya.driver@evshare.in",
        password_hash=make_password("driver123"),
        phone_number="+91 98222 33445",
        roles=["driver"],
        vehicles=[mg_ev],
        is_active=True,
        created_at=now - timedelta(days=15)
    )
    driver_priya.save()

    # 4. Create Hosts along Yamuna Expressway Corridor
    print("  -> Creating Verified Corridor Hosts...")
    
    # Host 1: Greater Noida (KM 0)
    host_noida = User(
        full_name="Rohan Gupta",
        email="host.noida@evshare.in",
        password_hash=make_password("host123"),
        phone_number="+91 98333 44556",
        roles=["driver", "host"],
        is_active=True,
        is_verified_host=True,
        created_at=now - timedelta(days=25)
    )
    host_noida.save()
    HostVerification(
        user=host_noida,
        host_type="residential",
        contact_phone="+91 98333 44556",
        property_address="Plot 14, Pari Chowk Road, Greater Noida",
        id_proof_type="aadhaar",
        id_proof_number="XXXX-XXXX-4412",
        safety_declaration_agreed=True,
        status="approved",
        admin_notes="Commercial 25 kW 3-phase connection verified.",
        reviewed_by=admin_user.email,
        reviewed_at=now - timedelta(days=23),
        submitted_at=now - timedelta(days=24)
    ).save()

    # Host 2: Jewar (KM 38)
    host_jewar = User(
        full_name="Vikram Chaudhary",
        email="host.jewar@evshare.in",
        password_hash=make_password("host123"),
        phone_number="+91 98444 55667",
        roles=["driver", "host"],
        is_active=True,
        is_verified_host=True,
        created_at=now - timedelta(days=20)
    )
    host_jewar.save()
    HostVerification(
        user=host_jewar,
        host_type="commercial_restaurant",
        business_name="Jewar Highway Food Oasis",
        contact_phone="+91 98444 55667",
        property_address="Service Lane, Jewar Interchange KM 38",
        id_proof_type="electricity_bill",
        id_proof_number="UPPCL-COMM-70KW-991",
        safety_declaration_agreed=True,
        status="approved",
        admin_notes="Direct high-tension transformer on highway property.",
        reviewed_by=admin_user.email,
        reviewed_at=now - timedelta(days=18),
        submitted_at=now - timedelta(days=19)
    ).save()

    # Host 3: Mathura (KM 108)
    host_mathura = User(
        full_name="Pooja Agarwal",
        email="host.mathura@evshare.in",
        password_hash=make_password("host123"),
        phone_number="+91 98555 66778",
        roles=["driver", "host"],
        is_active=True,
        is_verified_host=True,
        created_at=now - timedelta(days=18)
    )
    host_mathura.save()
    HostVerification(
        user=host_mathura,
        host_type="commercial_hotel",
        business_name="Mathura Heritage Retreat",
        contact_phone="+91 98555 66778",
        property_address="Raysan Road, Mathura Toll Exit",
        id_proof_type="aadhaar",
        id_proof_number="XXXX-XXXX-9912",
        safety_declaration_agreed=True,
        status="approved",
        admin_notes="Resort driveway verified with 24/7 security cabin.",
        reviewed_by=admin_user.email,
        reviewed_at=now - timedelta(days=16),
        submitted_at=now - timedelta(days=17)
    ).save()

    # Host 4: Agra (KM 165)
    host_agra = User(
        full_name="Arjun Verma",
        email="host.agra@evshare.in",
        password_hash=make_password("host123"),
        phone_number="+91 98666 77889",
        roles=["driver", "host"],
        is_active=True,
        is_verified_host=True,
        created_at=now - timedelta(days=15)
    )
    host_agra.save()
    HostVerification(
        user=host_agra,
        host_type="commercial_parking",
        business_name="Agra Ring Road Gateway Hub",
        contact_phone="+91 98666 77889",
        property_address="Inner Ring Road Toll Compound, Agra",
        id_proof_type="gstin",
        id_proof_number="09AABCV9910Z1Z5",
        safety_declaration_agreed=True,
        status="approved",
        admin_notes="Terminus facility with shaded bay and cafeteria.",
        reviewed_by=admin_user.email,
        reviewed_at=now - timedelta(days=13),
        submitted_at=now - timedelta(days=14)
    ).save()

    # Host 5: Pending Host (for KYC queue testing)
    host_pending = User(
        full_name="Amit Patel",
        email="host.pending@evshare.in",
        password_hash=make_password("host123"),
        phone_number="+91 98777 88990",
        roles=["driver", "host"],
        is_active=True,
        is_verified_host=False,
        created_at=now - timedelta(days=2)
    )
    host_pending.save()
    HostVerification(
        user=host_pending,
        host_type="residential",
        contact_phone="+91 98777 88990",
        property_address="Bajna Interchange, KM 75",
        id_proof_type="aadhaar",
        id_proof_number="XXXX-XXXX-1102",
        safety_declaration_agreed=True,
        status="submitted",
        submitted_at=now - timedelta(days=2)
    ).save()

    # 5. Seed Charger Listings along Yamuna Expressway Corridor
    print("  -> Seeding Chargers along Yamuna Expressway Corridor...")

    chargers = []

    # Charger 1: Greater Noida (Zero Point, KM 0)
    c1 = Charger(
        host=host_noida,
        title="Greater Noida Expressway Fast Hub",
        description="Private destination charging station 1 km before Yamuna Expressway Zero Point toll. Shaded driveway with high-reliability power back-up and clean washroom.",
        charger_type="DC",
        connector_types=["CCS2", "Type 2"],
        power_output_kw=30.0,
        price_per_kwh=16.50,
        address=ChargerAddress(
            city="Greater Noida",
            state="Uttar Pradesh",
            postal_code="201310",
            display_address="Near Zero Point / Pari Chowk, Greater Noida",
            private_directions="Turn left into Greenfields Driveway behind Sector 14 Security Gate. Tell security guard code 'EV-2026' to enter Bay 2."
        ),
        location=[77.5040, 28.4744],  # [lng, lat]
        amenities=["Restroom", "Wi-Fi", "Café / Dining", "Covered Parking"],
        verification_status="approved",
        is_active=True,
        availability_rules=[
            AvailabilityRule(day_of_week=d, start_time="06:00", end_time="23:00") for d in range(7)
        ],
        reviews_count=18,
        average_rating=4.9,
        created_at=now - timedelta(days=22)
    )
    c1.save()
    chargers.append(c1)

    # Charger 2: Jewar Highway Pitstop (KM 38)
    c2 = Charger(
        host=host_jewar,
        title="Jewar Toll Expressway Dual Fast Charger",
        description="High-power 60 kW DC dual-gun charging bay adjacent to Jewar Toll Plaza. 24x7 highway access, well-lit paved bay with round-the-clock convenience store and coffee.",
        charger_type="DC",
        connector_types=["CCS2"],
        power_output_kw=60.0,
        price_per_kwh=18.00,
        address=ChargerAddress(
            city="Jewar",
            state="Uttar Pradesh",
            postal_code="203135",
            display_address="Adjacent to Jewar Toll Plaza (KM 38), Yamuna Expressway",
            private_directions="Take the service exit immediately 200m before the Jewar Toll Booth. Charger bay is on the right with yellow bollards and EV Share signage."
        ),
        location=[77.5562, 28.1287],
        amenities=["Restroom", "Café / Dining", "24/7 Security", "Wi-Fi"],
        verification_status="approved",
        is_active=True,
        availability_rules=[
            AvailabilityRule(day_of_week=d, start_time="00:00", end_time="23:59") for d in range(7)
        ],
        reviews_count=42,
        average_rating=4.8,
        created_at=now - timedelta(days=19)
    )
    c2.save()
    chargers.append(c2)

    # Charger 3: Jewar Organic Farmstead (KM 42)
    c3 = Charger(
        host=host_jewar,
        title="Jewar Heritage Farmstead AC Station",
        description="Quiet organic farmstay with 7.4 kW Type 2 AC charging. Perfect for relaxed lunch stop or overnight top-up. Farm café serves fresh local dishes.",
        charger_type="AC",
        connector_types=["Type 2", "15A 3-Pin"],
        power_output_kw=7.4,
        price_per_kwh=13.50,
        address=ChargerAddress(
            city="Jewar",
            state="Uttar Pradesh",
            postal_code="203135",
            display_address="Dayanatpur Village, 3 km from Jewar Interchange",
            private_directions="Enter main wooden estate gate; charger is mounted beside the organic farm shop porch."
        ),
        location=[77.5720, 28.1050],
        amenities=["Restroom", "Café / Dining", "Covered Parking"],
        verification_status="approved",
        is_active=True,
        availability_rules=[
            AvailabilityRule(day_of_week=d, start_time="07:00", end_time="21:00") for d in range(7)
        ],
        reviews_count=9,
        average_rating=5.0,
        created_at=now - timedelta(days=16)
    )
    c3.save()
    chargers.append(c3)

    # Charger 4: Mathura Interchange Oasis (KM 108)
    c4 = Charger(
        host=host_mathura,
        title="Mathura Highway Oasis 30 kW Station",
        description="Midway expressway hub located at the Mathura / Vrindavan exit. Dedicated 30 kW DC fast charger suitable for Tata, MG, Mahindra, BYD, and Hyundai vehicles.",
        charger_type="DC",
        connector_types=["CCS2", "Type 2"],
        power_output_kw=30.0,
        price_per_kwh=16.00,
        address=ChargerAddress(
            city="Mathura",
            state="Uttar Pradesh",
            postal_code="281001",
            display_address="Mathura Interchange (KM 108), Yamuna Expressway",
            private_directions="Exit right at KM 108 ramp. Turn into the Highway Oasis Courtyard. Charger is located under the solar canopy."
        ),
        location=[77.6250, 27.6042],
        amenities=["Restroom", "Wi-Fi", "Café / Dining", "Covered Parking"],
        verification_status="approved",
        is_active=True,
        availability_rules=[
            AvailabilityRule(day_of_week=d, start_time="06:00", end_time="23:00") for d in range(7)
        ],
        reviews_count=31,
        average_rating=4.7,
        created_at=now - timedelta(days=15)
    )
    c4.save()
    chargers.append(c4)

    # Charger 5: Agra Expressway Ring Road Gateway (KM 165)
    c5 = Charger(
        host=host_agra,
        title="Agra Gateway 50 kW Ultra-Fast Bay",
        description="Expressway terminus charging facility right at the Agra Inner Ring Road intersection. Rapid 50 kW CCS2 charging allows full highway turnaround in 45 minutes.",
        charger_type="DC",
        connector_types=["CCS2"],
        power_output_kw=50.0,
        price_per_kwh=17.50,
        address=ChargerAddress(
            city="Agra",
            state="Uttar Pradesh",
            postal_code="282001",
            display_address="Agra End Point / Inner Ring Road (KM 165)",
            private_directions="Follow Inner Ring Road signs towards Fatehabad Road. Drive into the Secure Gateway Complex; bay is clearly illuminated."
        ),
        location=[77.9940, 27.2185],
        amenities=["Restroom", "Wi-Fi", "Café / Dining", "Covered Parking"],
        verification_status="approved",
        is_active=True,
        availability_rules=[
            AvailabilityRule(day_of_week=d, start_time="00:00", end_time="23:59") for d in range(7)
        ],
        reviews_count=27,
        average_rating=4.9,
        created_at=now - timedelta(days=12)
    )
    c5.save()
    chargers.append(c5)

    # Charger 6: Pending Charger for Moderation Workflow
    c6_pending = Charger(
        host=host_pending,
        title="Bajna Interchange Solar Top-Up Station",
        description="Newly installed 11 kW AC charger powered by rooftop solar array near Bajna interchange (KM 75).",
        charger_type="AC",
        connector_types=["Type 2", "15A 3-Pin"],
        power_output_kw=11.0,
        price_per_kwh=14.00,
        address=ChargerAddress(
            city="Mathura Rural",
            state="Uttar Pradesh",
            postal_code="281201",
            display_address="Near Bajna Cut (KM 75), Yamuna Expressway",
            private_directions="Private orchard entrance."
        ),
        location=[77.5800, 27.8800],
        amenities=["Restroom"],
        verification_status="pending",
        is_active=False,
        created_at=now - timedelta(days=1)
    )
    c6_pending.save()

    # 6. Seed Realistic Bookings, Visit Session, Simulated Payment, and Review
    print("  -> Seeding Historical Completed Booking & Review...")
    
    past_start = now - timedelta(days=2, hours=4)
    past_end = past_start + timedelta(hours=1)
    
    b1_completed = Booking(
        booking_reference="BK-202610-JEW88",
        driver=driver_user,
        host=host_jewar,
        charger=c2,
        vehicle=nexon_ev,
        slot_start=past_start,
        slot_end=past_end,
        status="completed",
        payment_status="simulated_paid",
        pricing_snapshot=PricingSnapshot(
            rate_per_kwh=18.00,
            estimated_energy_kwh=25.0,
            subtotal_amount=450.0,
            platform_fee=15.0,
            gst_amount=2.70,
            total_amount=467.70
        ),
        created_at=past_start - timedelta(days=1)
    )
    b1_completed.save()

    # Associated Charging Session
    s1 = ChargingSession(
        booking=b1_completed,
        charger=c2,
        driver=driver_user,
        host=host_jewar,
        started_at=past_start + timedelta(minutes=5),
        completed_at=past_end - timedelta(minutes=10),
        meter_start_kwh=1420.0,
        meter_end_kwh=1446.4,
        actual_energy_kwh=26.4,
        session_status="completed",
        is_manual_entry=True,
        start_notes="Driver arrived promptly. Plugged into CCS2 bay.",
        end_notes="Charged Tata Nexon smoothly from 24% to 88% SOC.",
        created_at=past_start
    )
    s1.save()

    # Associated Simulated Payment Transaction
    t1 = PaymentTransaction(
        booking=b1_completed,
        driver=driver_user,
        host=host_jewar,
        amount=467.70,
        platform_commission=70.15,
        host_payout_amount=397.55,
        currency="INR",
        transaction_reference="TXN-SIM-202610-8819",
        status="successful",
        is_simulation=True,
        paid_at=past_start - timedelta(minutes=10),
        created_at=past_start - timedelta(minutes=10)
    )
    t1.save()

    # Associated Driver Review
    r1 = Review(
        charger=c2,
        booking=b1_completed,
        driver=driver_user,
        rating=5,
        comment="Lifesaver on the Yamuna Expressway! The 60 kW DC charger gave my Nexon Max 26 kWh in under 45 minutes while I grabbed a coffee. Host was very courteous and directions were crystal clear.",
        is_visible=True,
        created_at=past_end + timedelta(hours=2)
    )
    r1.save()

    # 7. Seed Upcoming Confirmed Booking with Atomic SlotLock
    print("  -> Seeding Upcoming Confirmed Booking...")
    tomorrow_start = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    tomorrow_end = tomorrow_start + timedelta(hours=1)

    b2_ref = "BK-202610-MTH22"

    lock1 = SlotLock(
        charger=c4,
        slot_start=tomorrow_start,
        slot_end=tomorrow_end,
        booking_ref=b2_ref,
        locked_at=now - timedelta(hours=3)
    )
    lock1.save()

    b2_upcoming = Booking(
        booking_reference=b2_ref,
        driver=driver_user,
        host=host_mathura,
        charger=c4,
        vehicle=nexon_ev,
        slot_start=tomorrow_start,
        slot_end=tomorrow_end,
        status="confirmed",
        payment_status="simulated_paid",
        pricing_snapshot=PricingSnapshot(
            rate_per_kwh=16.00,
            estimated_energy_kwh=20.0,
            subtotal_amount=320.0,
            platform_fee=15.0,
            gst_amount=2.70,
            total_amount=337.70
        ),
        created_at=now - timedelta(hours=3)
    )
    b2_upcoming.save()

    t2 = PaymentTransaction(
        booking=b2_upcoming,
        driver=driver_user,
        host=host_mathura,
        amount=337.70,
        platform_commission=50.65,
        host_payout_amount=287.05,
        currency="INR",
        transaction_reference="TXN-SIM-202610-9921",
        status="successful",
        is_simulation=True,
        paid_at=now - timedelta(hours=3),
        created_at=now - timedelta(hours=3)
    )
    t2.save()

    # 8. Seed Sample Resolved Support Case
    print("  -> Seeding Support Case...")
    case1 = SupportCase(
        ticket_id="SUP-202610-001",
        user=driver_priya,
        related_booking=None,
        category="general_query",
        subject="Inquiry regarding CCS2 compatibility at Jewar Toll stop",
        description="I am planning to drive my MG ZS EV down to Agra this weekend. Wanted to confirm if the 60 kW Jewar station supports 50 kWh battery charging curve without tripping.",
        status="resolved",
        resolution_notes="Contacted host Vikram Chaudhary; confirmed station has dedicated 70 kW commercial transformer with active cooling CCS2 connector fully tested on MG ZS EV.",
        resolved_at=now - timedelta(days=3),
        resolved_by=admin_user.email,
        created_at=now - timedelta(days=5)
    )
    case1.save()

    # 9. Audit trail seed
    AuditEvent(
        actor_id=str(admin_user.id),
        actor_email=admin_user.email,
        action="pilot_database_seeded",
        target_type="System",
        target_id=str(admin_user.id),
        details={"corridor": "Yamuna Expressway (Greater Noida - Agra)", "chargers_seeded": len(chargers)}
    ).save()

    print("\n[OK] Pilot Seeding Completed Successfully!")
    print(f"   * Users: Admin ({admin_user.email}), Driver ({driver_user.email}), Hosts ({len(chargers)})")
    print(f"   * Chargers: {len(chargers)} verified highway corridor listings + 1 pending listing")
    print(f"   * Bookings: 1 completed with telemetry/payment/review, 1 upcoming confirmed")
    print("   * Default credentials: admin@evshare.in / admin123 | driver@evshare.in / driver123")

if __name__ == '__main__':
    seed_database()
