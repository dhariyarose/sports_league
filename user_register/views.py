import pdb
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings


class SignUp(CreateView):
    """
    Sign Up View
    """
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class LoginView(View):
    """
    Login View
    """
    template_name = 'login.html'

    def get(self,request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('sports_league/dashboard')
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_url = '/sports_league/dashboard/'
                if 'next' in request.META['HTTP_REFERER']: # Redirect the user after login to the URL in the Next
                    prev_url = self.request.META['HTTP_REFERER']
                    next_list = prev_url.split("=")
                    if 'http' in next_list[1]:
                        redirect_url_split_list = next_list[1].split('/')
                        redirect_url = "/"
                        for index, elem in enumerate(redirect_url_split_list):
                            if index > 2:
                                if index < len(redirect_url_split_list)-1:
                                    redirect_url+=redirect_url_split_list[index]+'/'
                                else:
                                    redirect_url+=redirect_url_split_list[index]
                    else:
                        redirect_url_split_list = prev_url.split('/')
                        redirect_url = next_list[1]
                return HttpResponseRedirect(redirect_url)
            else:
                return HttpResponse("Inactive user.")
        else:
            return render(request, self.template_name, {'error':'Login failed. Try again.'})

class LogoutView(View):
    """
    Logout View
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/user/login/")