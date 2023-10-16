from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
from .models import OtpCode, User
import random
from utils import send_otp_code
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm
    tmplate_name = "account/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.tmplate_name, {"form": form})

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
        return render(request, self.tmplate_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "account/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'], 
                                         user_session['full_name'], user_session['password'])
                # we must delete the sent code
                code_instance.delete()
                messages.success(request, 'You registered successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Code is wrong', 'danger')
                return redirect('accounts:verify_code')
        messages.error(request, 'Error', 'danger')
        return render(request, 'account/verify_code.html', {'form': form})
