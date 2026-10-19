"""
Test suite for Authentication, User Profile, and RBAC.
"""
import pytest
from django.test import Client
from accounts.documents import User, Vehicle
from accounts.services import register_user, authenticate_user

@pytest.fixture(autouse=True)
def clean_db():
    User.objects.delete()
    yield
    User.objects.delete()

def test_user_registration_success():
    """Verify clean user registration with password hashing."""
    user = register_user(
        email="testdriver@evshare.in",
        password="SecurePassword123!",
        full_name="Arun Kumar",
        phone_number="+91 98111 00001",
        role="driver"
    )
    assert user is not None
    assert user.email == "testdriver@evshare.in"
    assert user.full_name == "Arun Kumar"
    assert "driver" in user.roles
    assert user.password_hash != "SecurePassword123!"  # Must be hashed

def test_user_registration_duplicate_email():
    """Verify system blocks duplicate email registration."""
    register_user(
        email="unique@evshare.in",
        password="Password123!",
        full_name="Driver One"
    )
    with pytest.raises(ValueError, match="already exists"):
        register_user(
            email="unique@evshare.in",
            password="AnotherPassword!",
            full_name="Driver Two"
        )

def test_user_authentication_success_and_failure():
    """Verify credential verification with PBKDF2."""
    register_user(
        email="auth.test@evshare.in",
        password="CorrectPassword99",
        full_name="Auth Tester"
    )
    
    # Valid credentials
    user = authenticate_user("auth.test@evshare.in", "CorrectPassword99")
    assert user is not None
    assert user.email == "auth.test@evshare.in"
    
    # Invalid password
    bad_pass = authenticate_user("auth.test@evshare.in", "WrongPassword")
    assert bad_pass is None
    
    # Non-existent user
    non_user = authenticate_user("ghost@evshare.in", "AnyPassword")
    assert non_user is None

def test_rbac_role_checking():
    """Verify RBAC role checks."""
    user = register_user(
        email="host.user@evshare.in",
        password="Password123!",
        full_name="Host User",
        role="host"
    )
    assert user.has_role("host") is True
    assert user.has_role("driver") is True  # Hosts also have driver capabilities
    assert user.has_role("admin") is False

def test_login_http_flow():
    """Verify HTTP client login and signed cookie session resolution."""
    register_user(
        email="weblogin@evshare.in",
        password="TestWebPassword123",
        full_name="Web Login User"
    )
    
    client = Client()
    # Attempt login via POST
    response = client.post('/accounts/login/', {
        'email': 'weblogin@evshare.in',
        'password': 'TestWebPassword123'
    })
    # Should redirect to home or next
    assert response.status_code == 302
    assert client.session.get('_mongo_user_id') is not None
