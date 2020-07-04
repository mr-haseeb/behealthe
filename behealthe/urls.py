"""behealthe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from allauth.account.views import LoginView, LogoutView, ConfirmEmailView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView


# from apis.github.views import GitHubLoginView, FacebookLogin
from apis.behealthe.v1.signout.views import SessionLogoutView
from behealthe.users.views import LoginViewCustom

react_home_template = 'react/home.html'
react_signup_template = 'react/signup.html'
react_dashboard_template = 'react/dashboard.html'

favicon_view = RedirectView.as_view(url='/static/images/logos/logojoy/favicon.png', permanent=True)

REACT_SIGNUP_TEMPLATE_VIEW = TemplateView.as_view(template_name=react_signup_template)
REACT_DASHBOARD_TEMPLATE_VIEW = TemplateView.as_view(template_name=react_dashboard_template)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^$', TemplateView.as_view(template_name=react_home_template), name='home'),
    url(r'^favicon\.ico$', favicon_view),

    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # url(settings.ADMIN_URL, include(admin.site.urls)),

    # User Management
    url(r'^users/', include('betterself.users.urls', namespace='users')),

    # SSO Logins such as when GitHub aka
    # /accounts/github/login/
    url(r'^accounts/', include('allauth.urls')),

    # Where most of the frontend interacts with
    url(r'^api/', include('apis.urls')),

    url(r'^dashboard/authenticate$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-authenticate'),
    url(r'^dashboard-signup/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-signup'),
    # Specific api-end point for fitbit to redirect for authorization
    # this allows for pulling in Fitbit data using an API Token without being SessionAuthentication
    url(r'^dashboard/fitbit/oauth2/callback/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='fitbit-complete'),
    url(r'^dashboard-login/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-login'),
    url(r'^dashboard-logout/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-logout'),
    url(r'^dashboard.*/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-dashboard'),

    url(r'^demo-signup/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-demo-signup'),
    url(r'^settings/$', REACT_DASHBOARD_TEMPLATE_VIEW, name='react-settings'),

    # you may want to take out api-auth and have all traffic through rest-auth instead
    # im not sure if you even use rest_framework/api-auth anymore
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # https://github.com/Tivix/django-rest-auth/issues/159#issuecomment-173909852
    url(r'^rest-auth/login/$', LoginViewCustom.as_view(), name='rest_login'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email'),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^rest-auth/github/$', GitHubLoginView.as_view(), name='github_login'),
    # url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^session-logout/$', SessionLogoutView.as_view()),
]

