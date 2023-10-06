from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

# from .views import SignUpForm


# Create list of URL paths to direct URL to functions
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.sign_up, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/email/", views.change_email, name="change_email" ),
    path("profile/password/", views.change_password, name="change_password"),
    # path("logout/", views.logout, name="logout"),
    path("journal/", views.journal, name="journal"),
    path("journallist/", views.JournalEntryList.as_view(), name="journallist"),
    path("<int:pk>/", views.JournalEntryDetailView.as_view(), name="journalentry"),
    path( "<int:pk>/journaldetailview",views.ExpandDetailView.as_view(), name="journaldetailview",),
    path("<int:pk>/delete/", views.JournalDeleteView.as_view(), name="delete"),
    path("sentiment/", views.sentiment, name="sentiment"),
]
