# Generated by Django 5.1.6 on 2025-02-16 13:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'developers',
            },
        ),
    ]
