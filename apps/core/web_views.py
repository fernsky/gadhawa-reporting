"""
Web views (template-based) for core app.
"""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view for authenticated users.
    """
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'municipality_name': 'गढवा गाउँपालिका',
            'municipality_english': 'Gadhawa Rural Municipality',
            'page_title': 'मुख्य ड्यासबोर्ड',  # Main Dashboard
            'user': self.request.user,
        })
        return context


class LoginView(DjangoLoginView):
    """
    Custom login view with Nepali localization.
    """
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'municipality_name': 'गढवा गाउँपालिका',
            'municipality_english': 'Gadhawa Rural Municipality',
            'page_title': 'लगइन',  # Login
        })
        return context


class LogoutView(DjangoLogoutView):
    """
    Custom logout view.
    """
    next_page = reverse_lazy('core_web:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile view.
    """
    template_name = 'auth/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'municipality_name': 'गढवा गाउँपालिका',
            'municipality_english': 'Gadhawa Rural Municipality',
            'page_title': 'प्रोफाइल',  # Profile
            'user': self.request.user,
        })
        return context
