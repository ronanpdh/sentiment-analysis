from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from .models import JournalEntry, CustomUser
from .forms import CreateJournalEntry
from .utils import analyse_journal_entry


# Home View
@login_required
def home(request):
    context = {
        "name": request.user.username,
        "email": request.user.email,
    }
    return render(request, "journal/home.html", context)


# Sign Up View
class SignUp(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("registration/login.html")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# Create new advanced sign up view for registration. Double check model and form to ensure functionality.


# Profile View
@login_required
def profile(request):
    context = {"name": request.user.username}
    return render(request, "journal/profile.html", context)


# Login view


# Log out View
def logout_view(request):
    logout(request)
    return redirect("login")


# Journal View - Add Journal Entry and Analyse
@login_required
def journal(request):
    if request.method == "POST":
        form = CreateJournalEntry(request.POST)
        if form.is_valid():
            text_entry = request.POST["text_entry"]
            analysed_text = analyse_journal_entry(text_entry)
            journal_entry = JournalEntry()
            journal_entry.title = request.POST["title"]
            journal_entry.text_entry = request.POST["text_entry"]
            journal_entry.sentiment = analysed_text["sentiment"]
            journal_entry.thought_distortions = analysed_text["thought-distortions"]
            journal_entry.thought_distortion_type = analysed_text["distortion-types"]
            journal_entry.count = analysed_text["count"]
            journal_entry.save()
            return redirect("journallist")
    else:
        form = CreateJournalEntry()
    return render(request, "journal/journal.html", {"form": form})


# Create ListView class for Archive
class JournalEntryList(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = "journal/journallist.html"
    context_object_name = "entries"
    fields = ("text_entry", "date", "sentiment", "user_name")
    ordering = ["-date"]


# Views to allow users to go into a journal entry and view or delete
class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = "journal/journalentry.html"
    context_object_name = "distortion_types"
    fields = "thought_distortion_type"


# View to allow user to expand thought distortion types and see analysed text
class ExpandDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = "journal/journalentrydetail.html"
    context_object_name = "detail_view"
    fields = ("distortion_type", "thought_distortions")


# Delete View
class JournalDeleteView(LoginRequiredMixin, DeleteView):
    model = JournalEntry
    success_url = reverse_lazy("journallist")
    template_name = "journal/confirm_delete.html"


# Sentiment View
sentiment_data = "Sentiment"


@login_required
def sentiment(request):
    context = {"sentiment_data": sentiment_data}
    return render(request, "journal/sentiment.html", context)
