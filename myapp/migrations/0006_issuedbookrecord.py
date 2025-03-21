# Generated by Django 4.2.16 on 2025-02-11 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_cat_category_catid'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuedBookRecord',
            fields=[
                ('brid', models.BigAutoField(primary_key=True, serialize=False)),
                ('Issueded_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('returned_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.myuser')),
            ],
        ),
    ]
