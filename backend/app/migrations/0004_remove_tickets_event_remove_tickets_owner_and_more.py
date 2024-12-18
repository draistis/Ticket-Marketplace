# Generated by Django 5.1.4 on 2024-12-15 20:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_location_description_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickets',
            name='event',
        ),
        migrations.RemoveField(
            model_name='tickets',
            name='owner',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='created_at',
            new_name='reserved_at',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='event',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='valid_for',
        ),
        migrations.AddField(
            model_name='reservation',
            name='expires_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sector', models.CharField(max_length=50)),
                ('row', models.CharField(max_length=10)),
                ('seat', models.IntegerField()),
                ('is_reserved', models.BooleanField(default=False)),
                ('reserved_until', models.DateTimeField(blank=True, default=None, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.event')),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='tickets',
            field=models.ManyToManyField(to='app.ticket'),
        ),
        migrations.DeleteModel(
            name='ReservationTicket',
        ),
        migrations.DeleteModel(
            name='Tickets',
        ),
    ]
