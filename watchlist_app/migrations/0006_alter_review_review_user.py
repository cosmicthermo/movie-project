# Generated by Django 3.2.13 on 2022-05-15 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watchlist_app', '0005_review_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
