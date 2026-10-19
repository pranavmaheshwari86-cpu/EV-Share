"""
Test suite for Charger listings, search filtering, geolocation, and vehicle compatibility.
"""
import pytest
from datetime import date
from accounts.documents import User, Vehicle
from accounts.services import register_user
from chargers.documents import Charger, ChargerAddress, AvailabilityRule
from chargers.services import (
    create_charger,
    search_chargers,
    check_compatibility,
    get_available_slots_for_date
)

@pytest.fixture(autouse=True)
def clean_db():
    Charger.objects.delete()
    User.objects.delete()
    yield
    Charger.objects.delete()
    User.objects.delete()

@pytest.fixture
def test_host():
    return register_user(
        email="host.test@evshare.in",
        password="Password123!",
        full_name="Test Host",
        role="host"
    )

def test_create_charger_listing(test_host):
    """Verify charger creation with valid coordinates and attributes."""
    charger = create_charger(
        host=test_host,
        title="Greater Noida Fast Hub",
        description="Fast charger near Pari Chowk",
        charger_type="DC",
        connector_types=["CCS2", "Type 2"],
        power_kw=30.0,
        price_per_kwh=16.0,
        city="Greater Noida",
        display_address="Near Pari Chowk",
        private_directions="Gate 4, House 12",
        lat=28.4744,
        lng=77.5040,
        amenities=["Restroom", "Wi-Fi"]
    )
    assert charger is not None
    assert charger.title == "Greater Noida Fast Hub"
    assert charger.power_output_kw == 30.0
    assert charger.price_per_kwh == 16.0
    assert charger.latitude == 28.4744
    assert charger.longitude == 77.5040
    assert charger.address.private_directions == "Gate 4, House 12"

def test_search_and_proximity_filtering(test_host):
    """Verify geospatial proximity search along the corridor."""
    # Noida Charger (KM 0)
    c_noida = create_charger(
        host=test_host,
        title="Noida Hub",
        description="Near Expressway start",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=30.0,
        price_per_kwh=15.0,
        city="Greater Noida",
        display_address="Pari Chowk",
        lat=28.4744,
        lng=77.5040
    )
    c_noida.verification_status = "approved"
    c_noida.is_active = True
    c_noida.save()

    # Jewar Charger (KM 38)
    c_jewar = create_charger(
        host=test_host,
        title="Jewar Pitstop",
        description="Near Jewar toll",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=60.0,
        price_per_kwh=18.0,
        city="Jewar",
        display_address="Jewar Toll KM 38",
        lat=28.1287,
        lng=77.5562
    )
    c_jewar.verification_status = "approved"
    c_jewar.is_active = True
    c_jewar.save()

    # Search from near Greater Noida (28.47, 77.50)
    results = search_chargers(lat=28.4700, lng=77.5000)
    assert len(results) >= 2
    # Noida should be closest (< 5 km), Jewar further (~40 km)
    assert results[0]['charger'].title == "Noida Hub"
    assert results[0]['distance_km'] < 5.0
    assert results[1]['charger'].title == "Jewar Pitstop"
    assert results[1]['distance_km'] > 30.0

def test_connector_and_type_filtering(test_host):
    """Verify filtering by connector and AC/DC type."""
    c_dc = create_charger(
        host=test_host,
        title="DC CCS2 Only",
        description="Fast DC",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=50.0,
        price_per_kwh=18.0,
        city="Mathura",
        display_address="Mathura Interchange",
        lat=27.6042,
        lng=77.6250
    )
    c_dc.verification_status = "approved"
    c_dc.save()

    c_ac = create_charger(
        host=test_host,
        title="AC Slow Only",
        description="Slow AC destination",
        charger_type="AC",
        connector_types=["15A 3-Pin"],
        power_kw=3.3,
        price_per_kwh=12.0,
        city="Mathura",
        display_address="Mathura City",
        lat=27.5000,
        lng=77.6500
    )
    c_ac.verification_status = "approved"
    c_ac.save()

    # Filter for CCS2
    ccs2_results = search_chargers(connector="CCS2")
    titles = [r['charger'].title for r in ccs2_results]
    assert "DC CCS2 Only" in titles
    assert "AC Slow Only" not in titles

def test_vehicle_compatibility_checking(test_host):
    """Verify compatibility check logic between vehicle and charger."""
    charger = create_charger(
        host=test_host,
        title="Fast CCS2 Bay",
        description="CCS2 and Type 2",
        charger_type="DC",
        connector_types=["CCS2", "Type 2"],
        power_kw=50.0,
        price_per_kwh=16.0,
        city="Agra",
        display_address="Ring Road",
        lat=27.2185,
        lng=77.9940
    )

    # Compatible Vehicle (CCS2)
    nexon = Vehicle(
        make="Tata",
        model="Nexon EV",
        registration_number="DL-01-EV-1111",
        connector_type="CCS2"
    )
    is_compat, msg = check_compatibility(charger, nexon)
    assert is_compat is True

    # Incompatible Vehicle (GB/T)
    gbt_car = Vehicle(
        make="Mahindra",
        model="e2o Plus",
        registration_number="DL-01-EV-2222",
        connector_type="GB/T"
    )
    is_compat, msg = check_compatibility(charger, gbt_car)
    assert is_compat is False
    assert "GB/T" in msg
