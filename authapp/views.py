from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.query import Q
from django.template.loader import render_to_string
from django.http import HttpResponse, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.contrib.auth.models import User

def signupview(request):
    form = SignUpForm() #blank
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}!')
            send_mail(
                'You Have Successfully Signed In',
                'Your Account has created succesfully',
                'swapnilpophale300@gamil.com',
                [user_email],
                fail_silently=False
            )
            return redirect('login')
    else:
        return render(request, 'signup.html', {'form':form})

def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('success')
        else:
            messages.error(request,'Invalid Credentials')
    return render(request, 'login.html')

def loginsuccess(request):
    return render(request, 'loginsuccess.html')

def logoutview(request):
    logout(request)
    return redirect('login')

def password_reset_view(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Request For Password Reset "
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'swapnilpophale300@gamil.com', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("home")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})