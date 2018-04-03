# Generated by Django 2.0.3 on 2018-04-03 21:01

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_name', models.CharField(max_length=200, null=True)),
                ('billing_addr', models.TextField(null=True)),
                ('status', models.CharField(max_length=10)),
                ('stripe_charge_id', models.CharField(max_length=80)),
                ('stripe_charge_created', models.DateTimeField(null=True)),
                ('stripe_charge_failure_reason', models.CharField(blank=True, max_length=400)),
                ('unconfirmed_details', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_excl_vat', models.IntegerField()),
                ('rate', models.CharField(max_length=40)),
                ('thu', models.BooleanField()),
                ('fri', models.BooleanField()),
                ('sat', models.BooleanField()),
                ('sun', models.BooleanField()),
                ('mon', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='tickets.Order')),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TicketInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_addr', models.EmailField(max_length=254, unique=True)),
                ('token', models.CharField(max_length=12, unique=True)),
                ('status', models.CharField(default='unclaimed', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='tickets.Ticket')),
            ],
        ),
    ]
