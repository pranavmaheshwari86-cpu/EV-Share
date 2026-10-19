"""
Accounts views - Registration, login, logout, profile management, and host KYC onboarding.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from accounts.services import (
    create_user,
    authenticate_user,
    add_vehicle,
    submit_host_verification
)
from accounts.documents import HostVerification
from accounts.decorators import login_required_mongo

def register_view(request):
    """
    User registration view supporting role choice (driver, host, or both).
    """
    if getattr(request, 'current_user', None):
        return redirect('home')
        
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        phone = request.POST.get('phone_number', '').strip()
        role = request.POST.get('initial_role', 'driver')
        
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html', request.POST)
            
        roles = ['driver']
        if role == 'host':
            roles.append('host')
            
        try:
            user = create_user(
                full_name=full_name,
                email=email,
                password=password,
                roles=roles,
                phone_number=phone
            )
            request.session['user_id'] = str(user.id)
            messages.success(request, f"Welcome to EV Share, {user.full_name}!")
            
            if 'host' in roles:
                return redirect('accounts:host_onboarding')
            return redirect('accounts:profile')
        except ValueError as err:
            messages.error(request, str(err))
            return render(request, 'accounts/register.html', request.POST)
            
    return render(request, 'accounts/register.html', {'page_title': 'Join EV Share'})

def login_view(request):
    """
    User login view with email normalization and signed session creation.
    """
    if getattr(request, 'current_user', None):
        return redirect('home')
        
    next_url = request.GET.get('next', 'home')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate_user(email, password)
        if user:
            request.session['user_id'] = str(user.id)
            request.session['_mongo_user_id'] = str(user.id)
            messages.success(request, f"Welcome back, {user.full_name}!")
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'accounts/login.html', {'email': email, 'next': next_url})
            
    return render(request, 'accounts/login.html', {'next': next_url, 'page_title': 'Sign In — EV Share'})

def logout_view(request):
    """
    Clears the signed session and redirects to home.
    """
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required_mongo
def profile_view(request):
    """
    Driver/Host profile view: manage vehicles, toggle roles, view verification status.
    """
    user = request.current_user
    host_verification = HostVerification.objects(user=user).first()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            user.full_name = request.POST.get('full_name', user.full_name).strip()
            user.phone_number = request.POST.get('phone_number', user.phone_number).strip()
            user.save()
            messages.success(request, "Profile updated successfully.")
            
        elif action == 'add_vehicle':
            make = request.POST.get('make', '').strip()
            model = request.POST.get('model', '').strip()
            reg_num = request.POST.get('registration_number', '').strip()
            connector = request.POST.get('connector_type', 'CCS2')
            battery = request.POST.get('battery_capacity_kwh', 30.0)
            
            if make and model and reg_num:
                add_vehicle(user, make, model, reg_num, connector, battery)
                messages.success(request, f"Added {make} {model} to your garage.")
            else:
                messages.error(request, "Please fill in all vehicle details.")
                
        elif action == 'toggle_host_role':
            if 'host' in user.roles:
                user.roles.remove('host')
                messages.info(request, "Host mode deactivated for your profile.")
            else:
                user.roles.append('host')
                messages.success(request, "Host mode activated! Complete verification to list chargers.")
            user.save()
            
        return redirect('accounts:profile')
        
    context = {
        'user': user,
        'host_verification': host_verification,
        'page_title': 'Account Profile — EV Share',
    }
    return render(request, 'accounts/profile.html', context)

@login_required_mongo
def host_onboarding_view(request):
    """
    Host onboarding and KYC verification submission view.
    """
    user = request.current_user
    verification = HostVerification.objects(user=user).first()
    
    if request.method == 'POST':
        host_type = request.POST.get('host_type', 'residential')
        business_name = request.POST.get('business_name', '')
        contact_phone = request.POST.get('contact_phone', user.phone_number)
        property_address = request.POST.get('property_address', '')
        id_proof_type = request.POST.get('id_proof_type', 'aadhaar')
        id_proof_number = request.POST.get('id_proof_number', '')
        safety_agreed = request.POST.get('safety_declaration_agreed') == 'on'
        
        # Handle simple file names for MVP demonstration
        id_file = request.FILES.get('id_proof_file')
        perm_file = request.FILES.get('property_permission_file')
        
        id_file_path = id_file.name if id_file else (verification.id_proof_file if verification else "id_doc_sample.pdf")
        perm_file_path = perm_file.name if perm_file else (verification.property_permission_file if verification else "permission_sample.pdf")
        
        if not property_address or not id_proof_number:
            messages.error(request, "Please provide property address and ID proof number.")
        elif not safety_agreed:
            messages.error(request, "You must agree to the Electrical Safety & Operational Declaration.")
        else:
            submit_host_verification(
                user=user,
                host_type=host_type,
                contact_phone=contact_phone,
                property_address=property_address,
                id_proof_type=id_proof_type,
                id_proof_number=id_proof_number,
                business_name=business_name,
                id_proof_file=id_file_path,
                property_permission_file=perm_file_path,
                safety_agreed=safety_agreed
            )
            messages.success(request, "Verification application submitted! Our team will review your application shortly.")
            return redirect('accounts:host_onboarding')
            
    context = {
        'user': user,
        'verification': verification,
        'page_title': 'Host Verification & Onboarding — EV Share',
    }
    return render(request, 'accounts/host_onboarding.html', context)

def password_reset_request_view(request):
    """
    Simulated password reset request view.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        messages.info(request, f"If an account exists for {email}, password reset instructions have been sent.")
        return render(request, 'accounts/password_reset_sent.html', {'email': email})
    return render(request, 'accounts/password_reset_request.html', {'page_title': 'Reset Password'})
