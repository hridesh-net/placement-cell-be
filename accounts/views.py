from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, SignInForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from placement_cell_be import settings
import requests
from django.contrib.auth.models import User
from .models import ProfileLinkedin

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup_views.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = SignInForm()
    return render(request, 'accounts/signin.html', {'form': form})

def linkedin_auth(request):
    # Construct the LinkedIn authorization URL with the scopes defined in settings.py
    linkedin_auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}"
        f"&redirect_uri={settings.LINKEDIN_REDIRECT_URI}"
        f"&scope={'+'.join(settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE)}"  # Use the scopes defined in settings.py
    )

    # Redirect the user to the LinkedIn authorization page

    return redirect(linkedin_auth_url)


from django.contrib.auth.models import User


def linkedin_callback(request):
    code = request.GET.get('code')
    if not code:
        # Handle missing authorization code
        return HttpResponse("Authorization code is missing.", status=400)

    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    access_token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'client_id': settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET
    }
    
    # Exchange authorization code for access token
    access_token_response = requests.post(access_token_url, data=access_token_data)
    access_token_json = access_token_response.json()
    access_token = access_token_json.get('access_token')
    
    if not access_token:
        # Handle missing access token
        return HttpResponse("Failed to obtain access token from LinkedIn.", status=400)
    
    # Fetch user profile information from LinkedIn
    profile_url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive'
    }
    profile_response = requests.get(profile_url, headers=headers)
    print(profile_response)
    profile_data = profile_response.json()
    print(profile_data)
    
    # Extract necessary information from the profile data
    first_name = profile_data.get('given_name')
    last_name = profile_data.get('family_name')
    email = profile_data.get('email')
    
    if not email:
        # Handle missing email address
        return HttpResponse("Email address is missing from LinkedIn profile.", status=400)
    
    # Check if the user already exists in the LinkedInProfile table
    try:
        linkedin_profile = ProfileLinkedin.objects.get(user__email=email)
        # Update the existing LinkedInProfile object
        linkedin_profile.first_name = first_name
        linkedin_profile.last_name = last_name
        linkedin_profile.save()
    except ProfileLinkedin.DoesNotExist:
        # If the user profile does not exist, create a new LinkedInProfile
        user, _ = User.objects.get_or_create(username=email, email=email)
        linkedin_profile = ProfileLinkedin.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            # linkedin_profile_url=profile_url
        )

    print("LinkedIn Profile saved successfully:", linkedin_profile.user.username)

    # Redirect or respond as needed
    return redirect('home')


def home(request):
    return render(request,"accounts/home.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('signin')
