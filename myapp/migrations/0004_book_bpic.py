# Generated by Django 4.2.16 on 2025-01-31 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_myuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='Bpic',
            field=models.ImageField(blank=True, null=True, upload_to='book_pics/'),
        ),
    ]
