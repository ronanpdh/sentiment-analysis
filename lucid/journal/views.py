from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.shortcuts import redirect

# from .forms import CustomUserCreationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib import messages
from .models import JournalEntry, ThoughtDistortion
from .forms import CreateJournalEntry, SignUpForm, EmailChangeForm, PasswordChangeForm
from .utils import analyse_journal_entry, format_content

# Imports for organising chart data 
from collections import OrderedDict
from django.db.models import Count
from django.db.models.functions import ExtractMonth, TruncMonth 
import json


# Home View
@login_required
def home(request):
    context = {
        "name": request.user.username,
        "email": request.user.email,
    }
    return render(request, "journal/home.html", context)


# Create new advanced sign up view for registration. Double check model and form to ensure functionality

def sign_up(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You've signed up successfully!")
            login(request, user)
            return redirect("home")
    else:
        # This block will not be reached under normal circumstances
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


# Profile View
@login_required
def profile(request):
    context = {"name": request.user.username}
    return render(request, "journal/profile.html", context)

# User Information Change Forms
@login_required
def change_email(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return redirect('profile')
    else: 
        form = EmailChangeForm
    return render(request, 'journal/emailchange.html', {'form': form})



# Password Change Form
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
        update_session_auth_hash(request, form.user)
        return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'journal/passwordchange.html', {'form': form})




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
            journal_entry = JournalEntry()
            journal_entry.user = request.user
            text_entry = request.POST["text_entry"]
            journal_entry.title = request.POST["title"]
            journal_entry.text_entry = request.POST["text_entry"]
            analysed_text = analyse_journal_entry(text_entry)
            formatted_text = format_content(analysed_text)
            journal_entry.sentiment = formatted_text["sentiment"]
            journal_entry.thought_distortions = formatted_text["thought-distortions"]
            journal_entry.thought_distortion_type = formatted_text["distortion-types"]
            journal_entry.count = formatted_text["count"]
            journal_entry.save()

            # Save Thought Distortions to Model 
            distortion_types_list = formatted_text["distortion-types"].split(", ")
            for distortion_type in distortion_types_list:
                ThoughtDistortion.objects.create(
                    distortion_type=distortion_type,    
                    journal_entry=journal_entry,
                )

            return redirect("journallist")
    else:
        form = CreateJournalEntry()
    return render(request, "journal/journal.html", {"form": form})


# Create ListView class for Archive
class JournalEntryList(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = "journal/journallist.html"
    context_object_name = "entries"
    # fields = ("text_entry", "date", "sentiment", "user_name")
    ordering = ["-date"]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user).order_by("-date")


# Views to allow users to go into a journal entry and view or delete
class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = "journal/journalentry.html"
    context_object_name = "distortion_types"
    # fields = "thought_distortion_type"

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)


# View to allow user to expand thought distortion types and see analysed text
class ExpandDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = "journal/journalentrydetail.html"
    context_object_name = "detail_view"
    # fields = ("distortion_type", "thought_distortions")

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        journal_entry = self.object
        thought_distortions_str = journal_entry.thought_distortions
        thought_distortions_list = thought_distortions_str.split(", ")
        context["thought_distortions_list"] = thought_distortions_list
        return context


# Delete View
class JournalDeleteView(LoginRequiredMixin, DeleteView):
    model = JournalEntry
    success_url = reverse_lazy("journallist")
    template_name = "journal/confirm_delete.html"

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)


# Analytics View
@login_required
def sentiment(request):
    # Gather Data from models and order
    entries_by_date = (
        JournalEntry.objects.filter(user=request.user)
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    distortion_data = (
        ThoughtDistortion.objects.filter(journal_entry__user=request.user)
        .values('distortion_type')
        .annotate(count=Count('journal_entry'))
        .order_by('-count')
    )

    # Organise data for ChartJs
    # Journal Entry Count Data
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    counts = [0] * 12 
    for entry in entries_by_date:
        counts[entry['month'] -1 ] = entry['count']
    data = {
        'labels': months,
        'datasets': [{
            'label': 'Journal Entries',
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.5, 
            'data': counts,
        }]
    }

    # Distortion Data format for ChartJS
    distortion_data_list = list(distortion_data)
    distortion_types = [item['distortion_type'] for item in distortion_data_list]
    counts = [item['count'] for item in distortion_data_list]

    distortion_data = {
    'labels': distortion_types,
    'datasets': [{
        'label': 'Count',
        'data': counts
        }]
    }

    # Convert data to JSON for chartJS
    data_json = json.dumps(data)
    distortions_json = json.dumps(distortion_data)
    # Data Context Dictionary 
    context = {
        'data': data_json,
        'distortion_data': distortions_json
    }
    print(distortion_data_list)
    return render(request, "journal/sentiment.html", context)
