from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, VerifyLoginCodeForm
from .models import OtpCode, User
import random
from utils import send_otp_code
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "account/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            phone = form.cleaned_data["phone"]
            send_otp_code(phone, random_code)
            OtpCode.objects.create(phone_number=phone, code=random_code)
            request.session["user_registration_info"] = {
                "phone_number": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "full_name": form.cleaned_data["full_name"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, "We have sent you a code.", "success")
            return redirect("account:verify_code")
        return render(request, self.template_name, {"form": form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "account/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_registration_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)

        if datetime.now() > code_instance.created.replace(tzinfo=None) + timedelta(minutes=2):
            code_instance.delete()
            messages.error(request, "Code is not valid.", "danger")
            return render(request, "account/verify.html", {"form": form})

        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == code_instance.code:
                User.objects.create_user(
                    user_session["phone_number"],
                    user_session["email"],
                    user_session["full_name"],
                    user_session["password"],
                )
                # we must delete the sent code
                code_instance.delete()
                messages.success(request, "You registered successfully", "success")
                return redirect("home:home")
            else:
                messages.error(request, "Code is wrong", "danger")
                return redirect("accounts:verify_code")
        messages.error(request, "Error", "danger")
        return render(request, "account/verify.html", {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = cd['phone_number']
            password = cd['password']
            user = authenticate(request, username=phone_number, password=password)
            
            random_code = random.randint(1000,9999)
            send_otp_code(phone_number, random_code)
            OtpCode.objects.create(phone_number=phone_number, code=random_code)
            request.session["user_login_info"] = {
                "phone_number": form.cleaned_data["phone_number"],
                "password": form.cleaned_data["password"],
            }
            if user is not None:
                user = None
                # login(request, user)
                # messages.success(request, 'You logged in successfully.', 'success')
                return redirect('account:verify_login_code')
            else:
                messages.error(request, 'Username or password is not correct.', 'warning')
                return redirect('account:user_login')

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')


class UserLoginVerifyCodeView(View):
    form_class = VerifyLoginCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "account/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_login_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)

        if datetime.now() > code_instance.created.replace(tzinfo=None) + timedelta(minutes=2):
            code_instance.delete()
            messages.error(request, "Code is not valid.", "danger")
            return render(request, "account/verify.html", {"form": form})
        
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = user_session['phone_number']
            password = user_session['password']
            user = authenticate(request, username=phone_number, password=password)
            if cd["code"] == code_instance.code and user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully.', 'success')
                code_instance.delete()
                return redirect("home:home")
            else:
                messages.error(request, "Code is wrong", "danger")
                return redirect("account:verify_login_code")
        messages.error(request, "Error", "danger")
        return render(request, "account/verify.html", {"form": form})
