import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse



# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    # password = models.CharField(max_length=50, null=False, default=0)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # class Methods
    def __str__(self):
        return self.username


class JournalEntry(models.Model):
    text_entry = models.TextField()
    title = models.CharField(max_length=300, default="")
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    sentiment = models.CharField(max_length=30, null=True, blank=True, db_index=True)
    thought_distortions = models.CharField(max_length=30, null=True, blank=True)
    thought_distortion_type = models.CharField(max_length=30, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, db_index=True
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Journal Entry Methods
    def __str__(self):
        return self.title

    def __str__(self):
        return self.text_entry

    def returnDate(self):
        return self.date

    def returnSentiment(self):
        return self.sentiment

    def get_absolute_url(self):
        return reverse("journalentry", args=[str(self.id)])

    #  Journal entry metadata
    class Meta:
        ordering = ["date"]
        verbose_name = "Journal Entry"


#  Models for Sentiment Analysis
class SentimentAnalysis(models.Model):
    sentiment = models.CharField(max_length=30)
    confidence = models.FloatField()
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE)


# Model for Thought Distortions - better access for analysis page
class ThoughtDistortion(models.Model):
    distortion_type = models.CharField(max_length=30)
    description = models.TextField()
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
