# Generated by Django 4.2.6 on 2024-01-07 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapapp', '0004_alter_scraps_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wishlists',
            field=models.ManyToManyField(blank=True, related_name='wishlisted_by', to='scrapapp.scraps'),
        ),
    ]
