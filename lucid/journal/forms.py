from django import forms
from .models import JournalEntry, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username", "email", "password")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username", "email", "password")


# Create Class for Journal Entry Form
class CreateJournalEntry(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["title", "text_entry"]

    class Media:
        css = {
            "all": ("style.css",),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "pure-input-1", "required": " "}
        )
        self.fields["title"].widget.attrs["placeholder"] = "Title"
        self.fields["text_entry"].widget.attrs.update(
            {"class": "pure-input-5-5", "cols=": "100", "rows=": "3"}
        )
        self.fields["text_entry"].widget.attrs[
            "placeholder"
        ] = "Start Typing, thoughts, feelings, whatever you like"
