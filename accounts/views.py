from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.contrib import messages
from book.models import BorrowBook
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request, "After registration , autoLogin successfully done")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def get_success_url(self):
        messages.success(self.request, "Login successfully")
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    http_method_names = ['post']
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    balance = 0

    def get(self, request):
        user_purchases = BorrowBook.objects.filter(user=request.user)
        account_balance = request.user.account.balance

        form = UserUpdateForm(instance=request.user)
        print(request.user)
        return render(request, self.template_name, {
            'user_purchases': user_purchases,
            'account_balance': account_balance,
            'form': form,
        })

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})