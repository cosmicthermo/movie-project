# Generated by Django 3.2.13 on 2022-05-15 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0004_auto_20220515_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='watchlist_app.watchlist'),
            preserve_default=False,
        ),
    ]
