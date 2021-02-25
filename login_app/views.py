# Render is a function that combines a given template with a given context dictionary
# Returns an HTTPResponse object with that rendered text
# Context is an optional argument of render, which by default is an empty dictionary
# Reverse is a function that helps with DRY
from django.shortcuts import render, reverse
# from django.contrib.auth the class models.User provides ready made fields like
# username, first_name, last_name, email, password etc
from django.contrib.auth.models import User
# from django.contrib.auth use authenticate(request, username, password) method to verify credentials
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect
from . models import PasswordResetRequest
# decorator for views that checks that the user is logged in, redirecting to the log-in page if necessary.
# other decorators include permission_required, user_passes_test, check_perms
from django.contrib.auth.decorators import login_required

def login(request):
    context = {}

    if request.method == "POST":
        # authenticate() returns a User object if the credentials are valid or None
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            # login(http request object, User object) saving the user's ID in the session using Django's session framework
            dj_login(request, user)
            return HttpResponseRedirect(reverse('mini_project_app:index'))
        else:
            context = {
                    'error': 'Bad username or password'
            }
    # render(request, template, context dictionary) 
    return render(request, 'login_app/login.html', context)

def logout(request):
    # logout() no return value, the session data is cleaned out
    dj_logout(request)
    return render(request, 'login_app/login.html')

# View function to handle the form from password_request.html
def password_reset(request):
    if request.method == "POST":
        post_user = request.POST['username']
        post_password = request.POST['password']
        post_cpassword = request.POST['confirm_password']
        token = request.POST['token']

        if post_password == post_cpassword:
            try:
                # We get with the Model if the token is the same
                prr = PasswordResetRequest.objects.get(token=token)
                print(prr)
                # If it is we save
                prr.save()
            except:
                # render() sends back a typical web page, while HttpResponseRedirect sends back a URL
                # render() is basically a simple wrapper around a HttpResponse which renders a template
                # You can use HttpResponse to return others things as well in the response
                print("Invalid password reset attempt.")
                return render(request, 'login_app/password_reset.html')
            
            user = prr.user
            user.set_password(post_password)
            user.save()
            return HttpResponseRedirect(reverse('login_app:login'))

    return render(request, 'login_app/password_reset.html')

def request_password_reset(request):
    if request.method == "POST":
        post_user = request.POST['username']
        user = None

        if post_user:
            try:
                # Query to check for existing username                
                user = User.objects.get(username=post_user)
            except:
                print(f"Invalid password request: {post_user}")
        else:
            post_user = request.POST['email']
            try:
                # Query to check for existing email                
                user = User.objects.get(email=post_user)
            except:
                print(f'Invalid password request: {post_user}')

        if user:
            prr = PasswordResetRequest()
            prr.user = user
            prr.save()
            # Because of the __str__ in the model class we can print
            # This is for the user to receive
            print(prr)
            return HttpResponseRedirect(reverse('login_app:password_reset'))

    # For GET requests we just render the template
    return render(request, 'login_app/request_password_reset.html')


def sign_up(request):
    context = {}
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_name = request.POST['user']
        email = request.POST['email']
        if password == confirm_password:
            if User.objects.create_user(user_name, email, password):
                return HttpResponseRedirect(reverse('login_app:login'))
            else:
                context = {
                        'error': 'Could not create user account - please try again'
                }
        else:
            context = {
                    'error': 'Passwords did not match. Please try again'
            }
    return render(request, 'login_app/sign_up.html', context)

@login_required
def delete_account(request):
    if request.method == "POST":
        if request.POST['confirm_deletion'] == "DELETE":
            user = authenticate(
                request, username=request.user.username, password=request.POST['password'])
            if user:
               print(f"Deleting user {user}")
               user.delete()
               return HttpResponseRedirect(reverse('login_app:login'))
            else:
               print("fail delete")
            # The GET returns the form/template while the POST does its thing
    return render(request, 'login_app/delete_account.html')
