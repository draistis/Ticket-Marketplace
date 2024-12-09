# Generated by Django 5.1.4 on 2024-12-09 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expiration_date', models.DateTimeField()),
                ('activation_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('description', models.TextField()),
                ('is_company', models.BooleanField(default=False)),
                ('company_registration_number', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password_hash', models.CharField(max_length=300)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('MUSIC', 'Music'), ('SPORTS', 'Sports'), ('ARTS', 'Arts'), ('FOOD', 'Food'), ('CHARITY', 'Charity'), ('EDUCATION', 'Education'), ('BUSINESS', 'Business'), ('TECH', 'Tech')], max_length=50)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.location')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('valid_for', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sector', models.CharField(max_length=50)),
                ('row', models.CharField(max_length=10)),
                ('seat', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('purchased_at', models.DateTimeField(default=None, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event')),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.reservation')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tickets')),
            ],
        ),
        migrations.AddField(
            model_name='organizer',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]