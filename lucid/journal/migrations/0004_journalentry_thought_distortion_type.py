# Generated by Django 4.2 on 2023-09-27 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_alter_journalentry_thought_distortions'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='thought_distortion_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]